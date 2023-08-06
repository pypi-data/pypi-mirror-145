from price_forecast_suite_package.suite_base import PriceForecastBase
from price_forecast_suite_package import suite_data, suite_model
import numpy as np
import pandas as pd

class AUTO_MODEL(PriceForecastBase):
  def __init__(self, case_name = 'auto_model', node_id = '', env = 'localtest', df_name = '', target_column = 'PRICE', date_column = 'DATE', demand_column = None, predict_point = 48, log_level = 0):
    super().__init__(case_name, env)
    self.node_id = node_id
    self.df = None
    self.df_name = df_name
    self.target_column = target_column
    self.date_column = date_column
    self.demand_column = demand_column
    self.model_type = None
    self.predict_point = predict_point
    self.log_level = log_level
    self.start_time = None
    self.end_time = None
    self.prdict_df = None
  
  def df_fetch(self, path_pre = '', log_level = 0):
    self.df = super().df_fetch(df_name = self.df_name, data_path = path_pre)
  
  # ----- feature engineer ------
  def feature_engineer(self):
    self.df = self.df.set_index(self.date_column)
    if self.demand_column is not None:
      mean = self.df[self.demand_column].mean()
      for i in range(1, 30):
        self.df['DEMAND_D'+str(i)] = self.df[self.demand_column]
    c_array = self.df.columns.values
    data = { 'column_name' : c_array }
    df_0 = pd.DataFrame(data)
    df_1 = pd.DataFrame(data)
    distance1 = []
    distance2 = []
    for item in c_array:
      x = self.df[item]
      y = self.df['USEP']
      distance1.append(suite_data.euclidean(x, y))
      distance2.append(suite_data.manhattandean(x, y))
    df_0['euclidean'] = distance1
    df_0['manhattandean'] = distance2
    distance1 = []
    distance2 = []
    distance3 = []
    for item in c_array:
      x = self.df[item]
      y = self.df['USEP']
      distance1.append(suite_data.pearsonrSim(x, y))
      distance2.append(suite_data.kendalltauSim(x, y))
      distance3.append(suite_data.cosSim(x, y))
    df_1['pearsonrSim'] = distance1
    df_1['kendalltauSim'] = distance2
    df_1['cosSim'] = distance3
    df_col = df_0.sort_values('euclidean')
    a1 = df_col['column_name'].iloc[0:5]
    df_col = df_0.sort_values('manhattandean')
    a2 = df_col['column_name'].iloc[0:5]
    df_col = df_1.sort_values('pearsonrSim')
    a3 = df_col['column_name'].iloc[-5:]
    df_col = df_1.sort_values('kendalltauSim')
    a4 = df_col['column_name'].iloc[-5:]
    df_col = df_1.sort_values('cosSim')
    a5 = df_col['column_name'].iloc[-5:]
    arr = np.hstack([a1, a2, a3, a4, a5])
    arr = np.unique(arr)
    self.df = self.df[arr]
    return arr
  
  def train_model(self, enable_optuna = True, n_trials = 10, model_path = ''):
    model_arr = []
    mae_arr = []
    mape_arr = []
    if self.env == 'eap':
      model, res, res_display = suite_model.xgb_model_select(df = self.df, label_column = self.target_column, enable_optuna = enable_optuna, n_trials = n_trials, metric_methods = ['mae','mape', 'smape'])
      model_arr.append(model)
      mae_arr.append(res['mae'])
      mape_arr.append(res['mape'])
    model, res, res_display = suite_model.linear_model_select(df = self.df, label_column = self.target_column, enable_optuna = enable_optuna, n_trials = n_trials, metric_methods = ['mae','mape', 'smape'])
    model_arr.append(model)
    mae_arr.append(res['mae'])
    mape_arr.append(res['mape'])
    model, res, res_display = suite_model.lstm_model_select(df = self.df, label_column = self.target_column, look_back = self.predict_point, look_forward = self.predict_point, enable_optuna = enable_optuna, n_trials = n_trials, metric_methods = ['mae', 'mape', 'smape'])
    model_arr.append(model)
    mae_arr.append(res['mae'])
    mape_arr.append(res['mape'])
    model, res, res_display = suite_model.tcn_model_select(df = self.df, label_column = self.target_column, look_back = self.predict_point, look_forward = self.predict_point, enable_optuna = enable_optuna, n_trials = n_trials, metric_methods = ['mae', 'mape', 'smape'])
    data = {
      'mape': mape_arr,
      'mae': mae_arr,
      'type': ['xgb', 'linear', 'lstm', 'tcn']
    }
    df = pd.DataFrame(data)
    print(df)
    index = df.idxmin()['mape']
    print(index)
    self.model = model_arr[index]
    self.model_type = data['type'][index]
  
  def predit(self, model = None):
    self.model = model
    if self.model_type in ['xgb', 'linear']:
      self.predict_df = suite_data.predict_data_linear(df = self.train_df, target_column = self.target_column, look_back = self.predict_point)
      prediction =  self.model.predict(self.predict_df)
    if self.model_type in ['lstm', 'tcn', 'transformer']:
      self.predict_df = suite_data.predict_data_dl(df = self.train_df, target_column = self.target_column, look_back = self.predict_point)
      prediction = suite_model.predict_result(predict_data_list = [self.predict_df] , 
                                            model_path = [self.model], 
                                            model_type = [self.model_type], 
                                            divideby = [10])
      prediction = prediction[0]
    self.predict_result = prediction

    

  