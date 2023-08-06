from price_forecast_suite_package.suite_base import PriceForecastBase
import pytz
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
from sklearn.model_selection import KFold
import xgboost as xgb


class SHANDONG(PriceForecastBase):
  def __init__(self, case_name = 'shandong', node_id = '张家产', env = 'localtest', df_name = '', target_column = '', date_column = '', demand_column = None, predict_point = 96, log_level = 0):
    super().__init__(case_name, env)
    self.node_id = node_id
    self.df_dic = {}
    self.target_column = '日前_电价(元/MWh)'
    self.feature_columns = ['出清前_竞价空间1','hour','出清前_新能源预测','time','出清前_竞价空间1_max','出清前_竞价空间1_mean','出清前_竞价空间1_min']
    self.model_type = 'xgb'
    self.log_level = log_level
    self.group_id = None
    self.start_time = None
    self.end_time = None
    self.prdict_df = {}
    self.check_df_name_list = []
  
  # ------------------------------- loading in data [add, check, remove]----------------------------
  def df_fetch(self):
    self.site_df = super().df_fetch(df_name = 'shandong-site')
    group_num_dict = self.site_df.set_index(['SITE_NAME'])['GROUP_NUM'].to_dict()
    site_num_dict = self.site_df.set_index(['SITE_NAME'])['SITE_NUM'].to_dict()
    SITE_NUM = site_num_dict[self.node_id]
    GROUP_NUM = group_num_dict[self.node_id]
    self.group_id = GROUP_NUM
    self.end_date = datetime.now(tz = pytz.timezone('Asia/Shanghai'))+timedelta(days=1)
    self.start_time, self.end_time = self.__gettime(end_time = datetime.now(tz = pytz.timezone('Asia/Shanghai'))+timedelta(days=1))
    sql_query = "select * from tt_ods_group_supply_demand where GROUP_NUM  ='%s' and TRADE_TIME >= '%s' and TRADE_TIME < '%s'" % (GROUP_NUM, self.start_time, self.end_time)
    demand_df = super().df_fetch(df_name = 'shandong-demand', sql_query = sql_query)
    sql_query = "select * from tt_ods_site_clear where SITE_NUM  ='%s' and TRADE_TIME >= '%s' and TRADE_TIME < '%s'" % (SITE_NUM, self.start_time, self.end_time)
    price_df = super().df_fetch(df_name = 'shandong-price', sql_query = sql_query)
    self.df_dic = { 'demand' : demand_df, 'price': price_df }

  # ----- feature engineer ------
  def feature_engineer(self):
    data = self.__shandong_feature_engineer(df_dic = self.df_dic)
    self.train_df = data
  
  # ------  train model ---------------
  def train_model(self, model_path = '', enable_optuna = False):
    super().generate_model_path(model_path)
    print('out', self.model_path)
    self.model = self.__train_model(df = self.train_df, start_date = self.start_time, end_date = self.end_time, 
                                    feature_list = self.feature_columns, 
                                    label = self.target_column)
    print('----- Completed traning -----')
  
  # ----- predict ----- -------------------------------
  def predict(self, model = None, start_time = '', end_time = ''):
    time_gap = pd.Timedelta('8h') - pd.Timedelta('15min')
    start_date = (self.end_date - timedelta(days=1) - time_gap).strftime("%Y-%m-%d %H-%M-%S")
    end_date = (self.end_date - time_gap).strftime("%Y-%m-%d %H-%M-%S")
    sql_query = "select * from tt_ods_group_supply_demand where GROUP_NUM  ='%s' and TRADE_TIME >= '%s' and TRADE_TIME < '%s'" % (self.group_id, start_date, end_date)
    predict_df = super().df_fetch(df_name = 'shandong-demand', sql_query = sql_query)
    p_df = { 'demand' : predict_df }
    self.prdict_df = self.__feature_engineer_predict_shandong(df_dic = p_df)
    self.predict_result = self.__predict(self.model, self.prdict_df, self.feature_columns)

  def display_predict(self):
    print(self.predict_result)
  
  def get_predict(self):
    print(self.predict_result)
  
  def df_display_all(self):
    print(self.df_dic)
    
  def get_model(self):
    return self.model

  def __shandong_feature_engineer(self, df_dic):
    df_demand = df_dic['demand']
    df_price = df_dic['price']
    df_demand['PUBLISH_DAY'] = pd.to_datetime(df_demand['PUBLISH_DAY'])
    df_demand['TRADE_TIME'] = pd.to_datetime(df_demand['TRADE_TIME'])
    df_demand = df_demand.sort_values(by=['PUBLISH_DAY', 'TRADE_TIME'])
    save_cols = ['TRADE_TIME', 'LOAD_REGULATION', 'LOCAL_POWER_PLANT', 'TIE_LINE_LOAD', 'WIND', 'SOLAR',
                     'TEST_UNIT', 'STAND_BY_UNIT']
    change_cols = save_cols[1:]
    df_demand[change_cols] = df_demand[change_cols].astype('float')
    df_demand = df_demand[save_cols]
    df_demand.columns = ['timestamp', '出清前_直调负荷(MW)', '出清前_地方电厂发电总加(MW)', '出清前_联络线受电负荷(MW)', '出清前_风电总加(MW)',
                      '出清前_光伏总加(MW)', '出清前_试验机组总加(MW)', '出清前_自备机组总加(MW)']
    df_demand.index = df_demand['timestamp']
    df_demand = df_demand.drop(['timestamp'], axis=1)
    df_price = df_price[['TRADE_TIME', 'DA_CLEARING_PRICE']]
    df_price['TRADE_TIME'] = pd.to_datetime(df_price['TRADE_TIME'])
    df_price = df_price.sort_values(by=['TRADE_TIME'])
    save_cols = ['TRADE_TIME', 'DA_CLEARING_PRICE']
    change_cols = save_cols[1:]
    df_price[change_cols] = df_price[change_cols].astype('float')
    df_price = df_price[save_cols]
    df_price.columns = ['timestamp', '日前_电价(元/MWh)']
    df_price.index = df_price['timestamp']
    df_price = df_price.drop(['timestamp'], axis=1)
    data = pd.concat((df_demand.dropna(), df_price), 1)
    data.index=pd.to_datetime(data.index)
    data['出清前_竞价空间1'] = (data['出清前_直调负荷(MW)'] - data['出清前_联络线受电负荷(MW)'] - data['出清前_风电总加(MW)']
                         - data['出清前_光伏总加(MW)'] - data['出清前_地方电厂发电总加(MW)']
                         - data['出清前_试验机组总加(MW)'] - data['出清前_自备机组总加(MW)'])
    data['出清前_竞价空间2'] = (data['出清前_直调负荷(MW)'] - data['出清前_联络线受电负荷(MW)'] - data['出清前_风电总加(MW)']
                         - data['出清前_光伏总加(MW)'] - data['出清前_地方电厂发电总加(MW)'])
    data['出清前_新能源预测'] = data['出清前_风电总加(MW)'] + data['出清前_光伏总加(MW)']
    data['date'] = data.index.date
    data['hour'] = data.index.hour
    data['time'] = (data.index.minute + data.index.hour * 60) / 15
    for day, data_day in data.resample('D'):
        date = str(day.date())
        if len(data.loc[date]) > 0:
            data.loc[date, '出清前_竞价空间1_max'] = data_day['出清前_竞价空间1'].max()
            data.loc[date, '出清前_竞价空间1_min'] = data_day['出清前_竞价空间1'].min()
            data.loc[date, '出清前_竞价空间1_mean'] = data_day['出清前_竞价空间1'].mean()
    return data
  
  def __train_model(self, df, start_date, end_date, feature_list, label):
    model = [None,None,None,None,None]
    mask = df[feature_list + [label]].notna().all(axis=1).values
    df = df.loc[mask]
    unique = np.unique(df.index.date)
    mask = df[feature_list+[label]].notna().all(axis=1).values
    X_train = df.loc[mask][feature_list]
    y_train = df.loc[mask][label]
    folds = KFold(n_splits=5, shuffle=False)
    for fold_, (trn_idx, val_idx) in enumerate(folds.split(X_train)):
        model[fold_] = xgb.XGBRegressor(nthread=30).fit(X_train.iloc[trn_idx],y_train.iloc[trn_idx])
    return model
  
  def __feature_engineer_predict_shandong(self, df_dic):
    df_demand = df_dic['demand']
    df_demand['PUBLISH_DAY'] = pd.to_datetime(df_demand['PUBLISH_DAY'])
    df_demand['TRADE_TIME'] = pd.to_datetime(df_demand['TRADE_TIME'])
    df_demand = df_demand.sort_values(by=['PUBLISH_DAY', 'TRADE_TIME'])
    save_cols = ['TRADE_TIME', 'LOAD_REGULATION', 'LOCAL_POWER_PLANT', 'TIE_LINE_LOAD', 'WIND', 'SOLAR',
                     'TEST_UNIT', 'STAND_BY_UNIT']
    change_cols = save_cols[1:]
    df_demand[change_cols] = df_demand[change_cols].astype('float')
    df_demand = df_demand[save_cols]
    df_demand.columns = ['timestamp', '出清前_直调负荷(MW)', '出清前_地方电厂发电总加(MW)', '出清前_联络线受电负荷(MW)', '出清前_风电总加(MW)',
                      '出清前_光伏总加(MW)', '出清前_试验机组总加(MW)', '出清前_自备机组总加(MW)']
    df_demand.index = df_demand['timestamp']
    data = df_demand.drop(['timestamp'], axis=1)
    data['出清前_竞价空间1'] = (data['出清前_直调负荷(MW)'] - data['出清前_联络线受电负荷(MW)'] - data['出清前_风电总加(MW)']
                         - data['出清前_光伏总加(MW)'] - data['出清前_地方电厂发电总加(MW)']
                         - data['出清前_试验机组总加(MW)'] - data['出清前_自备机组总加(MW)'])
    data['出清前_竞价空间2'] = (data['出清前_直调负荷(MW)'] - data['出清前_联络线受电负荷(MW)'] - data['出清前_风电总加(MW)']
                         - data['出清前_光伏总加(MW)'] - data['出清前_地方电厂发电总加(MW)'])
    data['出清前_新能源预测'] = data['出清前_风电总加(MW)'] + data['出清前_光伏总加(MW)']
    data['shiqi'] = data.index
    data['时期'] = data['shiqi'].apply(lambda x: x.hour * 4 + x.minute // 15)
    data['hour']=data['时期']//4
    data['time']=data['时期']
    data['出清前_竞价空间1_max']=data['出清前_竞价空间1'].max()
    data['出清前_竞价空间1_min'] = data['出清前_竞价空间1'].min()
    data['出清前_竞价空间1_mean'] = data['出清前_竞价空间1'].mean()
    print(data)
    return data
  
  def __gettime(self, end_time, his_days = 15):
    start_date = datetime(end_time.year, end_time.month, end_time.day) - timedelta(days=his_days)
    end_date = datetime(end_time.year, end_time.month, end_time.day) +timedelta(days=1)
    time_gap = pd.Timedelta('8h') - pd.Timedelta('15min')
    start_date = (start_date - time_gap).strftime("%Y-%m-%d %H-%M-%S")
    end_date = (end_date - time_gap).strftime("%Y-%m-%d %H-%M-%S")
    return start_date, end_date
  
  def __predict(self, model, predict_df, feature_list):
    predictions_day = np.zeros(predict_df.shape[0])
    for each_model in model:
        predictions_day += each_model.predict(predict_df[feature_list]) / len(model)
    return predictions_day
  

