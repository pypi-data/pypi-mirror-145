import pandas as pd
from datetime import datetime, timedelta
import copy
import pytz
from datetime import datetime, timedelta
import numpy as np
from sklearn.model_selection import KFold
import xgboost as xgb

def shandong_feature_engineer(df_dic):
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

def train_model(df, start_date, end_date, feature_list, label):
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

def feature_engineer_predict_shandong(df_dic):
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
    return data

def gettime(end_time, his_days = 15):
    start_date = datetime(end_time.year, end_time.month, end_time.day) - timedelta(days=his_days)
    end_date = datetime(end_time.year, end_time.month, end_time.day) +timedelta(days=1)
    time_gap = pd.Timedelta('8h') - pd.Timedelta('15min')
    start_date = (start_date - time_gap).strftime("%Y-%m-%d %H-%M-%S")
    end_date = (end_date - time_gap).strftime("%Y-%m-%d %H-%M-%S")
    return start_date, end_date

def predict(model, predict_df, feature_list):
    predictions_day = np.zeros(predict_df.shape[0])
    for each_model in model:
        predictions_day += each_model.predict(predict_df[feature_list]) / len(model)
    return predictions_day
