from price_forecast_suite_package.suite_base import PriceForecastBase
import pandas as pd
from datetime import datetime, timedelta
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from scipy.interpolate import UnivariateSpline
import numpy as np
import pytz
import scipy.stats
import math
from price_forecast_suite_package import suite_feature_engineer_tt
# from eapdataset import Dataset

class ColumnsName:
    TIMESTAMP = 'timestamp'
    PUBLISH_DAY = '发布时间'
    SYS_LOAD = '系统负荷'
    DAYAHEAD_LINE_PLAN = '日前联络线计划'
    NEW_ENERGY = '新能源预测'
    SYS_LOAD_AFTER = '系统负荷_出清后'
    DAYAHEAD_LINE_PLAN_AFTER = '日前联络线计划_出清后'
    NEW_ENERGY_AFTER = '新能源预测_出清后'
    SYS_LOAD_REAL = '系统负荷_实际'
    DAYAHEAD_LINE_PLAN_REAL = '日前联络线计划_实际'
    NEW_ENERGY_REAL = '新能源预测_实际'
    PRICE_SPACE = '竞价空间'
    PRICE_SPACE_AFTER = '竞价空间'
    PROVINCE_DAYAHEAD_PRICE = '全省日前均价'
    PROVINCE_REALTIME_PRICE = '全省实时均价'
    DAYAHEAD_PRICE = '日前电价'
    DAYAHEAD_PRICE_PRED = '日前电价预测值'
    REALTIME_PRICE = '实时电价'
    REALTIME_PRICE_PRED = '实时电价预测值'

# -----------------------------------------------------------------------------
# ---------------------------  BaseModel -------------------------------------
class BaseModel:
  def __init__(self, name):
    self.name = name
  def build(self):
    print('must implement "%s" by subclass' % self.build.__name__)
  def fit(self, X_train, y_train):
    print('must implement "%s" by subclass' % self.fit.__name__)
  def predict(self, X_test):
    print('must implement "%s" by subclass' % self.predict.__name__)

# -----------------------------------------------------------------------------
# ---------------------------  DataLoader -------------------------------------
class SortSplineLinear(BaseModel):
  def __init__(self, name='sort_spline_linear', is_0=False, s=None):
    super(SortSplineLinear, self).__init__(name=name)
    # 是否对低于火电最小的非0电价进行处理
    self.is_0 = is_0
    # sum((w[i] * (y[i]-spl(x[i])))**2, axis=0) <= s
    self.s = s
    self.sort_spline_linear = None
    self.is_normalize = False
    self.X_train = None
    self.y_train = None
  def build(self):
    pass
  def fit(self, X_train, y_train):
    self.X_train = X_train
    self.y_train = y_train
    X_train = X_train.copy()
    y_train = y_train.copy()
    self.build()
    if len(X_train.shape) > 1:
      X_train = X_train.reshape((-1,))
    # 是否对低于火电最小的非0电价进行处理
    if self.is_0:
      if y_train.min() == 0:
        fire_min = X_train[y_train == 0].max()
        if sum(y_train[X_train <= fire_min] == 0) > sum(y_train[X_train <= fire_min] != 0):
          y_train[X_train <= fire_min] = 0
    X_train.sort()
    y_train.sort()
    self.sort_spline_linear = UnivariateSpline(X_train, y_train, k=1, s=self.s)
  def predict(self, X_test):
    if len(X_test.shape) > 1:
      X_test = X_test.reshape((-1,))
    y_pred = self.sort_spline_linear(X_test)
    # 对预测做后处理，防止拟合斜率过大造成的影响
    if X_test.max() > self.X_train.max():
      if self.sort_spline_linear(X_test.max() + 1000) - self.y_train.max() > 500:
        y_pred[X_test > self.X_train.max()] = self.y_train.max()
    return y_pred


# -----------------------------------------------------------------------------
# ---------------------------  DataLoader -------------------------------------
class DataLoader:
    __pool = None  # 创建私有成员变量，连接池对象
    def __init__(self):
      self.group_num = 'SPIC_14'
      self.province_code = 14
    def read_gx_data_before(self, group_num, sta_date, end_date):
      sta_date, end_date = self.get_time_range(sta_date, end_date)
      sql = "select * from %s where GROUP_NUM = '%s' and TRADE_TIME >= '%s' and TRADE_TIME <= '%s' " \
              "and PUBLISH_DAY = date(TRADE_TIME + interval 8 hour - interval 15 minute - interval 2 day)" % \
              ('tt_ods_group_supply_demand', group_num, sta_date, end_date)
      from eapdataset import Dataset
      dataset = Dataset.get_by_name('shandong-demand')
      data = dataset.to_pandas_dataframe(use_cached_result=False, query = sql)
      if len(data) > 0:
        # 对时间戳统一加8小时,减15分钟转换成00:00:00作为第一个点
        data['TRADE_TIME'] = data['TRADE_TIME'].apply(lambda x: pd.to_datetime(x) + timedelta(hours=8) - timedelta(minutes=15))
        return data

    def read_gx_data_after(self, group_num, sta_date, end_date):
      sta_date, end_date = self.get_time_range(sta_date, end_date)
      sql = "select * from %s where GROUP_NUM = '%s' and TRADE_TIME >= '%s' and TRADE_TIME <= '%s' " \
              "and PUBLISH_DAY = date(TRADE_TIME + interval 8 hour - interval 15 minute - interval 1 day)" % \
              ('tt_ods_group_supply_demand', group_num, sta_date, end_date)
      from eapdataset import Dataset
      dataset = Dataset.get_by_name('shandong-demand')
      data = dataset.to_pandas_dataframe(use_cached_result=False, query = sql)
      if len(data) > 0:
        # 对时间戳统一加8小时,减15分钟转换成00:00:00作为第一个点
        data['TRADE_TIME'] = data['TRADE_TIME'].apply(lambda x: pd.to_datetime(x) + timedelta(hours=8) - timedelta(minutes=15))
        return data

    def read_gx_data_real(self, sta_date, end_date):
      sta_date, end_date = self.get_time_range(sta_date, end_date)
      sql = "select * from %s where PROVINCE_CODE = '%s' and TRADE_TIME >= '%s' and TRADE_TIME <= '%s' " % \
              ('tt_ods_group_supply_demand_real', 14, sta_date, end_date)
      from eapdataset import Dataset
      dataset = Dataset.get_by_name('shanxi-price')
      data = dataset.to_pandas_dataframe(use_cached_result=False, query = sql)
      gx_real = pd.DataFrame()
      if len(data) > 0:
        # 对时间戳统一加8小时,减15分钟转换成00:00:00作为第一个点
        data['TRADE_TIME'] = data['TRADE_TIME'].apply(lambda x: pd.to_datetime(x) + timedelta(hours=8) - timedelta(minutes=15))
        gx_real[ColumnsName.TIMESTAMP] = data['TRADE_TIME']
        gx_real[ColumnsName.NEW_ENERGY_REAL] = data['NEW_ENERGY']
        gx_real[ColumnsName.SYS_LOAD_REAL] = data['LOAD_REGULATION']
        gx_real[ColumnsName.DAYAHEAD_LINE_PLAN_REAL] = data['TIE_LINE_LOAD']
      return gx_real

    def read_gx_data(self, sta_date, end_date, gx_flag):
      gx_data = pd.DataFrame()
      if gx_flag:
        data = self.read_gx_data_after(self.group_num, sta_date, end_date)
        if len(data) > 0:
          gx_data[ColumnsName.TIMESTAMP] = data['TRADE_TIME']
          gx_data[ColumnsName.NEW_ENERGY_AFTER] = data['NEW_ENERGY']
          gx_data[ColumnsName.SYS_LOAD_AFTER] = data['LOAD_REGULATION']
          gx_data[ColumnsName.DAYAHEAD_LINE_PLAN_AFTER] = data['TIE_LINE_LOAD']
      else:
        data = self.read_gx_data_before(self.group_num, sta_date, end_date)
        if len(data) > 0:
          gx_data[ColumnsName.TIMESTAMP] = data['TRADE_TIME']
          gx_data[ColumnsName.NEW_ENERGY] = data['NEW_ENERGY']
          gx_data[ColumnsName.SYS_LOAD] = data['LOAD_REGULATION']
          gx_data[ColumnsName.DAYAHEAD_LINE_PLAN] = data['TIE_LINE_LOAD']
      return gx_data

    def read_site_attr_data(self, node_id):
      sql = "select * from %s where NODE_TYPE = '%s'" % ('tt_ods_site', node_id)
      from eapdataset import Dataset
      dataset = Dataset.get_by_name('shanxi-price')
      data = dataset.to_pandas_dataframe(use_cached_result=False, query = sql)
      return data

    def read_province_price_data(self, sta_date, end_date, data_source='realtime'):
      sta_time, end_time = self.get_time_range(sta_date, end_date)
      province_sql = "select * from %s where TRADE_TIME >= '%s' and TRADE_TIME <= '%s' \
                and DATA_SOURCE = '%s' and PROVINCE_CODE = '%s'" \
                       % ('tt_ods_province_clear', sta_time, end_time, \
                          data_source, self.province_code)
      from eapdataset import Dataset
      dataset = Dataset.get_by_name('shanxi-price')
      province_data = dataset.to_pandas_dataframe(use_cached_result=False, query = province_sql)
      province_price_data = pd.DataFrame()
      if len(province_data) > 0:
        # 对时间戳统一加8小时,减15分钟转换成00:00:00作为第一个点
        province_price_data[ColumnsName.TIMESTAMP] = province_data['TRADE_TIME'].apply(lambda x: pd.to_datetime(x) + timedelta(hours=8) - timedelta(minutes=15))
        province_price_data[ColumnsName.PROVINCE_DAYAHEAD_PRICE] = province_data['PROVINCE_DA_AVG_CLEARING_PRICE']
        province_price_data[ColumnsName.PROVINCE_REALTIME_PRICE] = province_data['PROVINCE_ID_AVG_CLEARING_PRICE']
      return province_price_data

    def read_node_price_data(self, node_id, sta_date, end_date, data_source='realtime', algorithm_type='envision'):
      site_attr_data = self.read_site_attr_data(node_id)
      site_num = site_attr_data[site_attr_data['SITE_NAME'].apply(lambda x: 'QA' and 'DEMO' not in x)].iloc[0]['SITE_NUM']
      sta_time, end_time = self.get_time_range(sta_date, end_date)
      dayahead_sql = "select * from %s where SITE_NUM = '%s' and \
                TRADE_TIME >= '%s' and TRADE_TIME <= '%s' \
                and DATA_SOURCE = '%s' and ALGORITHM_TYPE = '%s'" \
                       % ('tt_ods_site_day_ahead_price', site_num, sta_time, end_time, \
                          data_source, algorithm_type)
      from eapdataset import Dataset
      dataset = Dataset.get_by_name('shanxi-price')
      dayahead_data = dataset.to_pandas_dataframe(use_cached_result=False, query = dayahead_sql)
      realtime_sql = "select * from %s where SITE_NUM = '%s' and \
                TRADE_TIME >= '%s' and TRADE_TIME <= '%s' \
                and DATA_SOURCE = '%s' and ALGORITHM_TYPE = '%s'" \
                       % ('tt_ods_site_day_within_price', site_num, sta_time, end_time, \
                          data_source, algorithm_type)
      dataset = Dataset.get_by_name('shanxi-price')
      realtime_data = dataset.to_pandas_dataframe(use_cached_result=False, query = realtime_sql)
      dayahead_price_data = pd.DataFrame()
      if len(dayahead_data) > 0:
        # 对时间戳统一加8小时,减15分钟转换成00:00:00作为第一个点
        dayahead_price_data[ColumnsName.TIMESTAMP] = dayahead_data['TRADE_TIME'].apply(lambda x: pd.to_datetime(x) + timedelta(hours=8) - timedelta(minutes=15))
        dayahead_price_data[ColumnsName.DAYAHEAD_PRICE] = dayahead_data['DA_CLEARING_PRICE_BEFORE_REDUCE']
        dayahead_price_data[ColumnsName.DAYAHEAD_PRICE_PRED] = dayahead_data['DA_CLEARING_PRICE_FORECAST_BEFORE_REDUCE']
      realtime_price_data = pd.DataFrame()
      if len(realtime_data) > 0:
        # 对时间戳统一加8小时,减15分钟转换成00:00:00作为第一个点
        realtime_price_data[ColumnsName.TIMESTAMP] = realtime_data['TRADE_TIME'].apply(lambda x: pd.to_datetime(x) + timedelta(hours=8) - timedelta(minutes=15))
        realtime_price_data[ColumnsName.REALTIME_PRICE] = realtime_data['ID_CLEARING_PRICE_BEFORE_REDUCE']
        realtime_price_data[ColumnsName.REALTIME_PRICE_PRED] = realtime_data['ID_CLEARING_PRICE_FORECAST_BEFORE_REDUCE']
      price_data = pd.merge(dayahead_price_data, realtime_price_data, on='timestamp', how='outer')
      return price_data

    @staticmethod
    def get_time_range(sta_date, end_date):
      sta_time = (datetime(year=sta_date.year, month=sta_date.month, day=sta_date.day, hour=0,
                             minute=15, second=0) - timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
      end_time = (datetime(year=end_date.year, month=end_date.month, day=end_date.day, hour=23,
                             minute=45, second=0) -
                    timedelta(hours=8) + timedelta(minutes=15)).strftime("%Y-%m-%d %H:%M:%S")
      return sta_time, end_time

#------------------------------------------------------------------------------
#----------------------------  DataProcessing  --------------------------------
class DataProcessing:
    def __init__(self, is_normalize, price_min=None, price_max=None):
      self.min_max_scaler = MinMaxScaler()
      self.one_hot_encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)
      self.is_normalize = is_normalize
      self.price_min = price_min
      self.price_max = price_max
    @staticmethod
    def hand_craft_feat(df, use_clearing_after=False):
      price_space = ColumnsName.PRICE_SPACE
      if use_clearing_after:
        df[price_space] = df[ColumnsName.SYS_LOAD_AFTER] - \
                              df[ColumnsName.DAYAHEAD_LINE_PLAN_AFTER] - df[ColumnsName.NEW_ENERGY_AFTER]
      else:
        df[price_space] = df[ColumnsName.SYS_LOAD] - df[ColumnsName.DAYAHEAD_LINE_PLAN] - df[ColumnsName.NEW_ENERGY]
      df['15min'] = df.timestamp.apply(lambda x: (x.hour * 60 + x.minute) // 15)
      df['hour'] = df['timestamp'].dt.hour
      df['weekday'] = df['timestamp'].dt.weekday
      df['day'] = df.timestamp.dt.day
      df['date'] = df.timestamp.dt.date
      df['month'] = df.timestamp.dt.month
      df['is_night'] = df['timestamp'].dt.hour.apply(lambda x: 1 if x in [17, 18, 19, 20, 21, 22, 23] else 0)
      # 差分特征
      df['price_space_diff'] = df[price_space].shift(1).fillna(method="ffill")
      # 竞价空间相关特征
      df['bins'] = pd.cut(df[price_space], bins=[0, 15000, 30000, 100000], labels=[0, 1, 2])
      df['%s_log' % price_space] = np.exp(df[price_space] / 35000)
      df['%s_poly' % price_space] = df[price_space] ** 3
      df['%s_sqrt' % price_space] = np.sqrt(df[price_space])
      # 构造单天特征
      def day_feat(column_name, func):
        group = df.groupby(by='date').agg({column_name: func})
        day_feature = df['date'].apply(lambda x: group[column_name][x])
        return day_feature
      df['sum_square'] = day_feat(price_space, lambda x: sum(x ** 2) / 1e10)
      df['quantile'] = day_feat(price_space, lambda x: np.quantile(x, q=0.1))
      df['min_space_day'] = day_feat(price_space, lambda x: min(x))
      df['max_space_day'] = day_feat(price_space, lambda x: max(x))
      df['max/min'] = df['max_space_day'] / (df['max_space_day'] - df['min_space_day'])
      df['max_renew'] = day_feat(ColumnsName.NEW_ENERGY, lambda x: max(x))
      def ll(a, b):
        if a <= 25000 and b <= 32000:
          return 0
        if a > 25000 and b <= 32000:
          return 1
        if a <= 25000 and b > 32000:
          return 2
        if a > 25000 and b > 32000:
          return 3
      df['magic'] = df.apply(lambda x: ll(x.min_space_day, x.max_space_day), axis=1)
      return df
    def data_split(self, df, continuous_features, categorical_features, label, is_train=True):
      if is_train:
        if self.is_normalize:
          continuous_array = self.min_max_scaler.fit_transform(df[continuous_features])
          y = (df[label].values - self.price_min) / (self.price_max - self.price_min)
        else:
          continuous_array = df[continuous_features].values
          y = df[label].values
          categorical_array = self.one_hot_encoder.fit_transform(df[categorical_features])
      else:
        if self.is_normalize:
          continuous_array = self.min_max_scaler.transform(df[continuous_features])
        else:
          continuous_array = df[continuous_features].values
        categorical_array = self.one_hot_encoder.transform(df[categorical_features])
        y = None
      return np.hstack((continuous_array, categorical_array)), y


#------------------------------------------------------------------------------------------------
# ---------------------------  PriceForecaster ----------------------
class PriceForecaster:
  def __init__(self, model, simple_date_select, pred_col, continuous_features, categorical_features, clearing_after_train=True):
    self.ml_model = model
    self.simple_date_select = simple_date_select
    self.pred_col = pred_col
    self.continuous_features = continuous_features
    self.categorical_features = categorical_features
    self.clearing_after_train = clearing_after_train
    # 价格范围
    self.price_min = 0
    self.price_max = 1500
    # 电价截断处理阈值
    self.cut_off = 20
    # 训练集回溯N天
    self.N = 40
    # 数据处理模块
    self.data_process = DataProcessing(self.ml_model.is_normalize, self.price_min, self.price_max)
  def get_hist_data(self, pred_date, node_id=None):
    dl = DataLoader()
    # [sta_date, end_date]
    sta_date = pred_date - timedelta(days=self.N)
    end_date = pred_date - timedelta(days=1)
    gx_data_after = dl.read_gx_data(sta_date, end_date, gx_flag=True)
    gx_data_before = dl.read_gx_data(sta_date, end_date, gx_flag=False)
    gx_data_all = pd.merge(gx_data_after, gx_data_before, on='timestamp', how='outer')
    if node_id is None:
      price_data = dl.read_province_price_data(sta_date, end_date)
    else:
      province_price_data = dl.read_province_price_data(sta_date, end_date)
      node_price_data = dl.read_node_price_data(node_id, sta_date, end_date)
      price_data = pd.merge(node_price_data, province_price_data, on='timestamp', how='outer').reset_index(drop=True)
      price_data.loc[price_data[np.isnan(price_data[ColumnsName.DAYAHEAD_PRICE])].index, ColumnsName.DAYAHEAD_PRICE] = \
        price_data.loc[price_data[np.isnan(price_data[ColumnsName.DAYAHEAD_PRICE])].index, ColumnsName.PROVINCE_DAYAHEAD_PRICE]
      price_data.loc[price_data[np.isnan(price_data[ColumnsName.REALTIME_PRICE])].index, ColumnsName.REALTIME_PRICE] = \
        price_data.loc[price_data[np.isnan(price_data[ColumnsName.REALTIME_PRICE])].index, ColumnsName.PROVINCE_REALTIME_PRICE]
    data = pd.merge(gx_data_all, price_data[[ColumnsName.TIMESTAMP, self.pred_col]], on='timestamp', how='outer')
    data.dropna(how='all', inplace=True, axis=1)
    data.dropna(how='any', inplace=True, axis=0)
    data.reset_index(drop=True, inplace=True)
    return data
  def train(self, pred_date, node_id, pred_gx):
    df_lib = self.get_hist_data(pred_date, node_id)
    df_lib.loc[df_lib[self.pred_col] <= self.cut_off, self.pred_col] = self.price_min
    times_train = self.simple_date_select(df_lib, pred_date, pred_gx, self.pred_col)
    self.data_process.hand_craft_feat(df_lib, use_clearing_after=self.clearing_after_train)
    df_train = df_lib[df_lib[ColumnsName.TIMESTAMP].isin(times_train)].reset_index(drop=True)
    X_train, y_train = self.data_process.data_split(df_train, self.continuous_features, self.categorical_features, self.pred_col, is_train=True)
    self.ml_model.fit(X_train, y_train)
    return self.ml_model
  def predict(self, pred_gx):
    self.data_process.hand_craft_feat(pred_gx, use_clearing_after=False)
    X_test, _ = self.data_process.data_split(pred_gx, self.continuous_features, self.categorical_features, self.pred_col, is_train=False)
    price_pred = self.ml_model.predict(X_test)
    if self.ml_model.is_normalize:
      price_pred = price_pred * (self.price_max - self.price_min) + self.price_min
    # 结果后处理
    price_pred[price_pred < self.cut_off] = self.price_min
    price_pred[price_pred < self.price_min] = self.price_min
    price_pred[price_pred > self.price_max] = self.price_max
    price_pred = price_pred.round(2)
    return price_pred
#-----------------------------------------------------------------------------------

    
class SHANXI_TEST(PriceForecastBase):
  def __init__(self, case_name = 'shanxi_test', node_id = '织女泉', env = 'localtest', df_name = '', target_column = '', date_column = '', demand_column = None, predict_point = 96, log_level = 0):
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
  def predict(self, start_index, end_index = '', input_data = None):
    TUNE_TH = 5000
    start_time = start_index
    end_time = start_time
    '''
    sql_query = "select * from tt_ods_group_supply_demand where GROUP_NUM  ='%s' and TRADE_TIME >= '%s' and TRADE_TIME < '%s'" % (self.group_id, start_time, end_time)
    data = super().df_fetch(df_name = 'shandong-demand', sql_query = sql_query)
    data_1 = pd.DataFrame()
    data_1['timestamp'] = data['TRADE_TIME']
    data_1['新能源预测'] = data['NEW_ENERGY']
    data_1['系统负荷'] = data['LOAD_REGULATION']
    data_1['日前联络线计划'] = data['TIE_LINE_LOAD']
    data = data_1
    '''
    r = input_data
    data = pd.DataFrame(r['data']['ndarray'], columns=r['data']['names'])
    spot_date = datetime.strptime(data.date[0], '%Y-%m-%d')
    data['timestamp'] = pd.date_range(spot_date, periods=len(data), freq='15min')
    data.drop(columns=['date', 'period'], inplace=True)
    data.rename(columns={'predTransmit': ColumnsName.DAYAHEAD_LINE_PLAN,
                             'predDemand': ColumnsName.SYS_LOAD,
                             'renew': ColumnsName.NEW_ENERGY}, inplace=True)
    data.loc[(data[ColumnsName.NEW_ENERGY] < TUNE_TH), ColumnsName.NEW_ENERGY] -= 1000
    if len(data) > 0:
      data['TRADE_TIME'] = data['TRADE_TIME'].apply(lambda x: pd.to_datetime(x) + timedelta(hours=8) - timedelta(minutes=15))
    pred_col = ColumnsName.PROVINCE_DAYAHEAD_PRICE
    continuous_features = [ColumnsName.PRICE_SPACE]
    categorical_features = []
    self.model = PriceForecaster(SortSplineLinear(name='日前节点V11'), self.simple_date_select_v5, pred_col, continuous_features, categorical_features)
    spot_date = datetime.strptime(start_index, '%Y-%m-%d')
    self.model.train(spot_date.date(), None, data)
    pred_price = self.model.predict(pred_gx = data)
    self.predict_df = pred_price

  def display_predict(self):
    print(self.predict_result)
  
  def get_predict(self):
    print(self.predict_result)
  
  def df_display_all(self):
    print(self.df_dic)
    
  def get_model(self):
    return self.model
  
  def gettime(self, end_time, his_days = 15):
    start_date = datetime(end_time.year, end_time.month, end_time.day) - timedelta(days=his_days)
    end_date = datetime(end_time.year, end_time.month, end_time.day) +timedelta(days=1)
    time_gap = pd.Timedelta('8h') - pd.Timedelta('15min')
    start_date = (start_date - time_gap).strftime("%Y-%m-%d %H-%M-%S")
    end_date = (end_date - time_gap).strftime("%Y-%m-%d %H-%M-%S")
    return start_date, end_date
  
  def add_field(self, df, use_clearing_after=False):
    if use_clearing_after:
      df[ColumnsName.SYS_LOAD] = df[ColumnsName.SYS_LOAD_AFTER].values.copy()
      df[ColumnsName.DAYAHEAD_LINE_PLAN] = df[ColumnsName.DAYAHEAD_LINE_PLAN_AFTER].values.copy()
      df[ColumnsName.NEW_ENERGY] = df[ColumnsName.NEW_ENERGY_AFTER].values.copy()
    # 竞价空间字段
    df[ColumnsName.PRICE_SPACE] = df[ColumnsName.SYS_LOAD] - df[ColumnsName.DAYAHEAD_LINE_PLAN] - df[ColumnsName.NEW_ENERGY]
    # 添加日期字段
    df['date'] = df[ColumnsName.TIMESTAMP].dt.date

  def get_kde(self, x_array, data_array):
    res_list = []
    for x in x_array:
      bandwidth = 1.05 * np.std(data_array) * (len(data_array) ** (-1 / 5))
      def gauss(_x):
        return (1 / math.sqrt(2 * math.pi)) * math.exp(-0.5 * (_x ** 2))
      N = len(data_array)
      res = 0
      if len(data_array) == 0:
        return 0
      for i in range(len(data_array)):
        res += gauss((x - data_array[i]) / bandwidth)
      res /= (N * bandwidth)
      res_list.append(res)
    return res_list

  def fb_dist(self, df_lib, df_pred, by='竞价空间', n_days=2):
    df_lib = df_lib.copy()
    df_pred = df_pred.copy()
    space_pred = df_pred[by].values
    def x_gen(a):
        return np.linspace(min(a), max(a), 100)
    x_array = x_gen(space_pred)
    space_ked = self.get_kde(x_array, space_pred)
    func = lambda x: scipy.stats.wasserstein_distance(x_gen(x.values), x_array, self.get_kde(x_gen(x.values), x.values), space_ked)
    group_lib = df_lib.groupby(by='date').agg({by: func})
    price_space_sim = group_lib[by].sort_values()
    return price_space_sim[: n_days].index.tolist(), price_space_sim.values[: n_days]
  
  def find_piece_data(self, lib_series, pred_array):
    lib_series_min, lib_series_max = lib_series.min(), lib_series.max()
    pred_array_min, pred_array_max = pred_array.min(), pred_array.max()
    if lib_series_max >= pred_array_max:
      right = lib_series[lib_series >= pred_array_max].min()
    else:
      right = lib_series_max
    if lib_series_min <= pred_array_min:
      left = lib_series[lib_series <= pred_array_min].max()
    else:
      left = lib_series_min
    select_index = lib_series[(lib_series >= left) & (lib_series <= right)].index
    return select_index

  def simple_date_select_v5(self, df_lib, date_pred, df_pred, target, use_clearing_after=True):
    df_lib = df_lib.reset_index(drop=True).copy()
    df_pred = df_pred.reset_index(drop=True).copy()
    self.add_field(df_lib, use_clearing_after=use_clearing_after)
    self.add_field(df_pred)
    start_day_dataset = date_pred - timedelta(days=40)
    end_day_dataset = date_pred - timedelta(days=1)
    date_select = pd.date_range(start_day_dataset, end_day_dataset, freq='D').date
    date_select_filter = list(filter(lambda x: x in df_lib.date.unique(), date_select))
    date_select_filter = sorted(date_select_filter, reverse=True)
    # 计算预测日竞价空间与前一天差距，决定是否选用相似日模块
    try:
      diff_price_space = self.fb_dist(df_lib[df_lib.date.isin([date_pred - timedelta(days=1)])],
                                   df_pred,
                                   by=ColumnsName.PRICE_SPACE,
                                   n_days=1)[1][0]
      if diff_price_space > 7200:
        diff_new_energy = self.fb_dist(df_lib[df_lib.date.isin([date_pred - timedelta(days=1)])],
                                      df_pred,
                                      by=ColumnsName.NEW_ENERGY,
                                      n_days=1)[1][0]
        if diff_new_energy > 6000:
          date_select = pd.date_range(date_pred - timedelta(days=14), date_pred - timedelta(days=1), freq='D').date
          df_lib_ = df_lib[df_lib.date.isin(date_select)]
          date_select = self.fb_dist(df_lib_, df_pred, by=ColumnsName.PRICE_SPACE, n_days=14)[0]
          date_select_filter = list(filter(lambda x: x in df_lib.date.unique(), date_select))
    except:
      pass
    price_space_pred = df_pred[ColumnsName.PRICE_SPACE].values
    select_price_space_max, select_price_space_min = None, None
    select_target_max, select_target_min = None, None
    index_train = pd.Index([])
    for i, d in enumerate(date_select_filter):
        day_price_space = df_lib.loc[df_lib.date.isin([d]), ColumnsName.PRICE_SPACE]
        day_select_index = self.find_piece_data(day_price_space, price_space_pred)
        if select_price_space_max is None:
            index_train = index_train.append(day_select_index)
        else:
            day_select_price_space = day_price_space[day_price_space.index.isin(day_select_index)]
            if select_target_max >= 1500:
                drop_index = day_select_price_space[day_select_price_space >= select_price_space_min].index
            elif select_target_min <= 0:
                drop_index = day_select_price_space[day_select_price_space <= select_price_space_max].index
            else:
                drop_index = day_select_price_space[(day_select_price_space <= select_price_space_max) & (day_select_price_space >= select_price_space_min)].index
            index_train = index_train.append(day_select_index.drop(drop_index))
        if len(index_train) == 0:
            continue
        select_price_space = df_lib[df_lib.index.isin(index_train)][ColumnsName.PRICE_SPACE].values
        select_target = df_lib[df_lib.index.isin(index_train)][target].values
        select_price_space_max = select_price_space.max()
        select_price_space_min = select_price_space.min()
        select_target_max = select_target.max()
        select_target_min = select_target.min()
        # 终止条件
        min_stop_limit = select_price_space_min <= price_space_pred.min() or select_target_min <= 0
        max_stop_limit = select_price_space_max >= price_space_pred.max() or select_target_max >= 1500
        if min_stop_limit and max_stop_limit:
            break
        # 剪枝策略停止搜索条件
        if min_stop_limit and (date_pred - d).days >= 15 and (select_price_space_max >= price_space_pred.max() - 1000):
            break
    timestamps_train = df_lib[df_lib.index.isin(index_train)][ColumnsName.TIMESTAMP]
    return timestamps_train