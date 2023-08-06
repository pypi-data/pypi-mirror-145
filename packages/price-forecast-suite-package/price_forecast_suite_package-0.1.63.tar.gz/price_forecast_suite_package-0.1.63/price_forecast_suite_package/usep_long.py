

from enum import Enum
from price_forecast_suite_package.suite_base import PriceForecastBase
from price_forecast_suite_package import suite_feature_engineer_sg, suite_model, suite_data
import numpy as np
from datetime import datetime, timedelta

class Message(Enum):
  USE_DF_FETCH_MESSAGE = 'use df_fetch(df_name: string, data_path: string) to add dataframe into the df_list.'
  USE_DF_REMOVE_MESSAGE = 'use df_remove(df_name: string) to remove the dataframe from the df_list.'
  USE_DF_CHECK_MESSAGE = 'use df_display_all() to list all dataframe in the df_list.'
  USE_CHECK_DF_VALID_MESSAGE = 'use check_df_valid(df_name_list: string[]) to check if the dataframe loaded is valid for the training.'

class USEP_LONG(PriceForecastBase):
  def __init__(self, case_name, node_id = '', env = 'localtest', df_name = '', target_column = '', date_column = '', demand_column = None, predict_point = 96, log_level = 0):
    super().__init__(case_name, env)
    self.target_column = 'mean_30'
    self.feature_columns = ['DATE', 'Close/Last', 'RNGC1', 'humidity', 'windspeedKmph', 'RNGC1_-30', 'Close/Last_-30', 'mean_30']
    self.df_dict = {}
    self.model_type = 'lstm'
    self.log_level = log_level
  
  # ------------------------------- loading in data [add, check, remove]----------------------------
  def df_fetch(self, path_pre = '', log_level = 0):
    df = super().df_fetch(df_name = 'usep-fromsql', data_path = path_pre + 'USEP/USEP-2022.csv')
    brent = super().df_fetch(df_name = 'brent-df', data_path = path_pre + 'BrentPrice.csv')
    gas = super().df_fetch(df_name = 'gas-df', data_path = path_pre + 'future/Gas_Future.csv')
    weather = super().df_fetch(df_name = 'weather-df', data_path = path_pre + 'weather/sg_weather.csv')
    self.df_dict = { 'df' : df, 'brent' : brent, 'gas' : gas, 'weather': weather }

  # ----- feature engineer ------ 
  def feature_engineer(self, feature_columns = [], target_column = 'mean_30', log_level = 0):
    self.train_df = suite_feature_engineer_sg.sg_long_term_feature_engineer(df_dict = self.df_dict, 
                                                                            feature_columns = self.feature_columns, 
                                                                            target_column = self.target_column)
  
  def check_train_df(self):
    print(self.train_df)
  
  # ------  train model ---------------
  def train_model(self, start_index = '2017-01-01', end_index = '2021-11-30', model_path = '', enable_optuna = False, n_trials = 2):
    super().generate_model_path(model_path)
    print('out', self.model_path)
    if self.model_type in ['xgb']:
      self.model = suite_model.xgb_with_optuna(df = self.train_df, 
                                             label_column = self.target_column, 
                                             column_set_index = 'DATE', start_index = start_index, end_index = end_index, 
                                             save_model = True, model_path = self.model_path, 
                                             enable_optuna = enable_optuna, n_trials = n_trials)
    if self.model_type in ['lstm', 'tcn', 'transformer']:
      self.model = suite_model.model_with_data_split(df = self.train_df.copy(), 
                                                   label_column = self.target_column, 
                                                   column_set_index = 'DATE',
                                                   train_start = start_index, 
                                                   train_end = end_index,
                                                   look_back = 30, 
                                                   look_forward = 30, 
                                                   print_model_summary = False,
                                                   epochs = 500, patience = 10,
                                                   early_stop = True, 
                                                   save_model = True, model_path = self.model_path,
                                                   save_weight = False, checkpoint_path = './checkpoint', show_loss = True,
                                                   enable_optuna = enable_optuna, epochs_each_try = 8, n_trials = n_trials,
                                                   n_neurons = [128, 64],
                                                   model_name = self.model_type)
    print('----- Completed traning -----')
  
  def get_model(self):
    return self.model
  
  # ----- predict ----- -------------------------------
  def predict(self, model, start_index = '2021-01-01', end_index = ''):
    self.feature_engineer(self.feature_columns, target_column = 'mean_30')
    start_d = (datetime.strptime(start_index, '%Y-%m-%d') - timedelta(days = 31)).strftime('%Y-%m-%d')
    end_d = (datetime.strptime(start_index, '%Y-%m-%d') + timedelta(days = 30)).strftime('%Y-%m-%d')
    if self.model_type in ['xgb']:
      self.predict_df = suite_data.predict_data(df = self.train_df, target_column = self.target_column, look_back = 30, 
                                                start_index = start_index, end_index = end_index, date_column = 'DATE')
      # self.model = model #
      prediction =  self.model.predict(self.predict_df)
    if self.model_type in ['lstm', 'tcn', 'transformer']:
      self.predict_df = suite_data.predict_data_for_nn(df = self.train_df.copy(), 
                                                     target_column = 'mean_30', 
                                                     start_index = start_d,
                                                     end_index = end_d,
                                                     look_back = 30, 
                                                     date_column = 'DATE')
      # self.model = model
      prediction = suite_model.predict_result(predict_data_list = [self.predict_df], 
                                            model_path=[self.model], 
                                            model_type=[self.model_type], 
                                            divideby = [1])
    self.predict_result = prediction[0]
  
  def display_predict(self):
    print(self.predict_result)
  
  def get_predict(self):
    print(self.predict_result)

  # -------- support function -------------------
  def display_hint(self, log_level = 0, msg = []):
    self.log_level = log_level
    if self.log_level == 1:
      for item in Message:
        if item in msg:
          print(item.value)
