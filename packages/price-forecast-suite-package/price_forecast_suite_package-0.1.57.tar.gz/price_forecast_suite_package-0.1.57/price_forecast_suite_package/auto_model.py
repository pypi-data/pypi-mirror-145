from price_forecast_suite_package.suite_base import PriceForecastBase
from price_forecast_suite_package import suite_data, suite_model
import numpy as np
import pandas as pd

class AUTO_MODEL(PriceForecastBase):
  def __init__(self, case_name = 'auto_model', node_id = '', env = 'localtest', log_level = 0):
    super().__init__(case_name, env)
    self.node_id = node_id
    self.df = None
    self.target_column = None
    self.date_column = 'DATE'
    self.demand_column = None
    self.model_type = 'xgb'
    self.log_level = log_level
    self.start_time = None
    self.end_time = None
    self.prdict_df = None
  
  def df_fetch(self, df_name = '', path_pre = '', log_level = 0):
    self.df = super().df_fetch(df_name = df_name, data_path = path_pre)
  
  def pre_precessing(self, target_column = 'PRICE', date_column = 'DATE'):
    self.target_column = target_column
    self.date_column = date_column
    self.df = self.df.set_index(self.date_column)

  def process_demand(self, demand_column = None):
    self.demand_column = demand_column
    if demand_column is not None:
      mean = self.df[demand_column].mean()
      for i in range(1, 30):
        self.df['DEMAND_D'+str(i)] = self.df[demand_column]
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
  
  def select_model(self, predict_pint = 48, enable_optuna = True, n_trials = 10):
    model1, res1, res_display_1 = suite_model.xgb_model_select(df = self.df, label_column = self.target_column, enable_optuna = True, n_trials = n_trials, metric_methods = ['mape', 'smape'])
    model2, res2, res_display_2 = suite_model.linear_model_select(df = self.df, label_column = self.target_column, enable_optuna = True, n_trials = n_trials, metric_methods = ['mape', 'smape'])
    print('xgb:', res1, res_display_1)
    print('linear:', res2, res_display_2)
    if res2['mape'] < res1['mape']:
      self.model = model2
    self.model = model1

    

  