from price_forecast_suite_package.suite_base import PriceForecastBase
from price_forecast_suite_package import suite_feature_engineer_tt, suite_model, suite_data
import pytz
from datetime import datetime, timedelta


class SHANXI(PriceForecastBase):
  def __init__(self, case_name = 'shanxi', node_id = '织女泉', env = 'localtest', df_name = '', target_column = '', date_column = '', demand_column = None, predict_point = 96, log_level = 0):
    super().__init__(case_name, env)
    self.node_id = node_id
    self.df_dic = {}
    self.target_column = '日前_电价(元/MWh)'
    self.feature_columns = ['出清前_竞价空间1','hour','出清前_新能源预测','time','出清前_竞价空间1_max','出清前_竞价空间1_mean','出清前_竞价空间1_min']
    self.model_type = 'xgb'
    self.log_level = log_level
    self.group_id = None
    self.check_df_name_list = []
  
  # ------------------------------- loading in data [add, check, remove]----------------------------
  def df_fetch(self):
    self.site_df = super().df_fetch(df_name = 'shanxi-site')
    group_num_dict = self.site_df.set_index(['SITE_NAME'])['GROUP_NUM'].to_dict()
    site_num_dict = self.site_df.set_index(['SITE_NAME'])['SITE_NUM'].to_dict()
    SITE_NUM = site_num_dict[self.node_id]
    GROUP_NUM = group_num_dict[self.node_id]
    end_time = datetime.now(tz = pytz.timezone('Asia/Shanghai'))+timedelta(days=1)
    start_time, end_time = suite_feature_engineer_tt.gettime(end_time = end_time)
    sql_query = "select * from tt_ods_group_supply_demand where GROUP_NUM  ='%s' and TRADE_TIME >= '%s' and TRADE_TIME < '%s'" % (GROUP_NUM, start_time, end_time)
    demand_df = super().df_fetch(df_name = 'shandong-demand', sql_query = sql_query)
    sql_query = "select * from tt_ods_site_clear where SITE_NUM  ='%s' and TRADE_TIME >= '%s' and TRADE_TIME < '%s'" % (SITE_NUM, start_time, end_time)
    price_df = super().df_fetch(df_name = 'shandong-price', sql_query = sql_query)
    self.df_dic = { 'demand' : demand_df, 'price': price_df }

  # ----- feature engineer ------
  
  def feature_engineer(self):
    data = suite_feature_engineer_tt.shandong_feature_engineer(df_dic = self.df_dic)
    self.train_df = data
  
  # ------  train model ---------------
  def train_model(self):
    self.model = suite_feature_engineer_tt.train_model(df = self.predict_df, 
                                                       start_date = self.start_index, 
                                                       end_date = self.end_date, 
                                                       feature_list = self.feature_columns, 
                                                       label = self.target_column)
    print('----- Completed traning -----')
  
  # ----- predict ----- -------------------------------
  def predict(self, start_time, end_time):
    sql_query = "select * from tt_ods_group_supply_demand where GROUP_NUM  ='%s' and TRADE_TIME >= '%s' and TRADE_TIME < '%s'" % (self.group_id, start_time, end_time)
    self.predict_df = super().df_fetch(df_name = 'shandong-demand', sql_query = sql_query)
    self.prdict_df = suite_feature_engineer_tt.feature_engineer_predict_shandong(df_demand = self.demand_df,
                                                               feature_columns = self.feature_columns, 
                                                               label_column = self.target_column)
    self.predict_result = suite_feature_engineer_tt.predict(self.model, self.predict_df, self.feature_columns)

  def display_predict(self):
    print(self.predict_result)
  
  def get_predict(self):
    print(self.predict_result)
  
  def df_display_all(self):
    print(self.df_dic)
    
  def get_model(self):
    return self.model
