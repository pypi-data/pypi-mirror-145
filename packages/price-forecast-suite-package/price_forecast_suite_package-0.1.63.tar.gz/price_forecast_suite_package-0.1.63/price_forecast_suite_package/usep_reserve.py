from enum import Enum
from price_forecast_suite_package.suite_base import PriceForecastBase
from price_forecast_suite_package import suite_feature_engineer_sg, suite_model, suite_data
import numpy as np

class Message(Enum):
  USE_DF_FETCH_MESSAGE = 'use df_fetch(df_name: string, data_path: string) to add dataframe into the df_list.'
  USE_DF_REMOVE_MESSAGE = 'use df_remove(df_name: string) to remove the dataframe from the df_list.'
  USE_DF_CHECK_MESSAGE = 'use df_display_all() to list all dataframe in the df_list.'
  USE_CHECK_DF_VALID_MESSAGE = 'use check_df_valid(df_name_list: string[]) to check if the dataframe loaded is valid for the training.'

class USEP_RESERVE(PriceForecastBase):
  def __init__(self, case_name = 'usep_reserve', node_id = '', env = 'localtest', df_name = '', target_column = '', date_column = '', demand_column = None, predict_point = 96, log_level = 0):
    super().__init__(case_name, env)
    self.df_dic = {}
    self.target_column = 'CONRES_PRICE'
    self.feature_columns = []
    self.model_type = 'xgb'
    self.log_level = log_level
    self.display_hint(log_level, msg = [Message.USE_DF_FETCH_MESSAGE, Message.USE_DF_CHECK_MESSAGE])
  
  # ------------------------------- loading in data [add, check, remove]----------------------------
  def df_fetch(self, path_pre = '', log_level = 0):
    usep_df = super().df_fetch(df_name = 'usep-fromsql', data_path = path_pre + "USEPDemandhalfhour.csv")
    advisory_df = super().df_fetch(df_name = 'advisory-fromsql', data_path = path_pre + "advisory_df_dummy.csv")
    reg_df = super().df_fetch(df_name = 'usep-reg', data_path = path_pre + "RegPriceHalfHour.csv")
    conres_df = super().df_fetch(df_name = 'usep-conres', data_path = path_pre + "ConresPriceHalfHour.csv")
    
    self.df_dic = { 'usep_data' : usep_df, 'advisory_data': advisory_df, 'usep_reg': reg_df, 'conres_data':conres_df }

  def df_display_all(self, log_level = 0):
    print(self.usep_df)
    print(self.advisory_df)
    print(self.reg_df)

  # ----- feature engineer ------
  def feature_engineer(self, log_level = 0):
    self.train_df = suite_feature_engineer_sg.sg_reserve_feature_engineer(self.df_dic)
  
  # ------  train model ---------------
  def train_model(self, start_index = '2021-01-01', end_index = '2021-06-30', model_path = '', n_trials = 10, enable_optuna = True):
    super().generate_model_path(model_path)
    print('out', self.model_path)
    if self.model_type in ['xgb']:
      self.model = suite_model.xgb_with_optuna(df = self.train_df, 
                                             label_column = self.target_column, 
                                             column_set_index = 'DATE', start_index = start_index, end_index = end_index, 
                                             save_model = True, model_path = self.model_path, 
                                             enable_optuna = enable_optuna, n_trials = n_trials)
    if self.model_type in ['linear']:
      self.model = suite_model.linear_model_with_optuna(df = self.train_df, 
                                                        label_column = self.target_column,
                                                        column_set_index = 'DATE', 
                                                        start_index = start_index, end_index = end_index, 
                                                        print_data_shape = False, 
                                                        save_model = True, model_path = self.model_path, 
                                                        enable_optuna = True, 
                                                        n_trials = 20, 
                                                        model_name = 'elasticnet', 
                                                        alpha = 0.1, 
                                                        l1 = 0.5)
    print('----- Completed traning -----')
  
  def get_model(self):
    return self.model
  
  # ----- predict ----- -------------------------------
  def predict(self, model, data = None, path_pre = '', start_index = '2020-02-01', end_index = '2022-02-03'):
    self.df_fetch(path_pre)
    self.feature_engineer()
    self.predict_df = self.train_df
    if self.model_type in ['xgb', 'linear']:
      self.predict_df = suite_data.predict_data(df = self.train_df, target_column = self.target_column, look_back = 48, 
                                                start_index = start_index, end_index = end_index, date_column = 'DATE')
      self.model = model #
      prediction =  self.model.predict(self.predict_df)
    if self.model_type in ['lstm', 'tcn', 'transformer']:
      self.predict_df = suite_data.predict_data_for_nn(df = self.train_df, target_column = self.target_column, look_back = 48, 
                                                     start_index = start_index, end_index = end_index, date_column = 'DATE')
      self.model = model
      prediction = suite_model.predict_result(predict_data_list = [self.predict_df] , 
                                            model_path = [self.model], 
                                            model_type = [self.model_type], 
                                            divideby = [10])
      prediction = prediction[0]
    self.predict_result =  prediction
  
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
