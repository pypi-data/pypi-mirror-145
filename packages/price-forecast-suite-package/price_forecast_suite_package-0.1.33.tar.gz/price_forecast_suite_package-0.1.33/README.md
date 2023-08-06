## price_forecast_suite_package

A library containing common tools for data processing, feature engineering and model training and prediction.

***package***:  - /dist/price_forecast_suite_package-0.0.31-py3-none-any.whl

Pick a supported environment and install the package.
```  
pip install price_forecast_suite_package-0.0.31-py3-none-any.whl
```

Document:  
[document for using the library](http://wiki.envisioncn.com/display/~le.zhang/DS+Common+Tool)  
  

## Functions included in data processing:

### 1. remove_outlier  
Helps filter outlier from a specified column, and will return a new dataframe 
```
def remove_outlier(df, column_name, n_outlier=0.25):
    ...
    return new_df
``` 
Arguments table
|**Argument Name**|**Data Type**|**Required/Optional**|**Default Value**|
|:---|:---|:---|:---| 
|df|DataFrame|Required|-|  
|column_name|string|Required|-|
|n_outlier|float|Optional|0.25|
 
  
### 2. add_period_to_time  
Used to add 'period' column as a time interval into the 'date' column
```
def add_period_to_time(df, 
                       date_column_name='DATE', 
                       period_column_name='PERIOD', 
                       period_minutes=30):
    ...
    return new_df
```
Arguments table
|**Argument Name**|**Data Type**|**Required/Optional**|**Default Value**|
|:---|:---|:---|:---|  
|df|dataframe|Required|-|  
|date_column_name|string|Optional|'DATE'|  
|period_column_name|string|Optional|'PERIOD'|  
|period_minutes|int|Optional|30|  

  
### 3. show_draft_plot
Used to display the plot for a list of data, this function has no return.
```
def show_draft_plot(datas, x_label, title, legend, picture_size=[18, 5]):
    ...
```
|**Argument Name**|**Data Type**|**Required/Optional**|**Default Value**|
|:---|:---|:---|:---|  
|datas|nparray[]|Required |-|  
|x_label|nparray[]|Required ***same length as the list of data***|-|  
|title|string|Optional|''|  
|picture_size|[int, int]|Optional|[18,5]|     
  
example:  
```
from ds_common_tool import suite_data  
  
lstmModel = dasuite_data.show_draft_plot(datas = [df['column1'], df['column2']], x_label = df.index, title='Compare 2 features values', legend=['column1_data', 'column2_data'], picture_size=[18, 5])
``` 
  
### 4. get_n_rolling
Get N days rolling mean/max/min/median  
```
def get_n_rolling(df, target_column_name, n = 30, method = 'mean') :
    ...
    return new_df
```
  
|**Argument Name**|**Data Type**|**Required/Optional**|**Default Value**|
|:---|:---|:---|:---|  
|df|DataFrame|Required|-|  
|target_column_name|string|Required|-|  
|n|int|Optional|30|  
|method|string|Optional, accpect: 'mean', 'max', 'min', 'median', 'std'|'mean'|     
  
  
### 5. read_data_external
Used for reading external dataframes 
```
def read_data_external(df,  main_df, date_column = 'DATE', fillna_limit_n=5):
    ...
    return new_df
```

|**Argument Name**|**Data Type**|**Required/Optional**|**Default Value**|
|:---|:---|:---|:---|  
|df|DataFrame|Required|-|  
|main_df|DataFrame|Required|-| 
|date_column|string[]|Optional|'DATE'|   
|fillna_limit_n|int|Optional|5|     
   
### 6. merge_dfs
Used for merging multiple dataframes
```
def merge_dfs(df_list = [], on_column = 'DATE', method_na = 'dropna', fill_customize_value = 0):
    ...
    return new_df
```
|**Argument Name**|**Data Type**|**Required/Optional**|**Default Value**|
|:---|:---|:---|:---|  
|df_list|DataFrame[]|Required ***NOTE:*** first item should be the main target df|-|  
|on_column|string|Optional|'DATE'|        
|method_na|string|Optional, accept: 'dropna', 'fill_customize'|'dropna'| 
|fill_customize_value|int|Optional, only needed if method_na='fill_customize'|0| 

  
### 7. shift_row
Add a new shifted column to the dataframe based on an existing column 
```
def shift_row(df, target_columns, shift_n_list = [], method_na = 'dropna'):
    ...
    return new_df
```

|**Argument Name**|**Data Type**|**Required/Optional**|**Default Value**|
|:---|:---|:---|:---| 
|df|dataframe|Required|-|
|target_columns|string|Required|-|
|shift_n_list|int[]|Optional, **Note:** Number of shifts required, e.g. [-20, -30]|[]|
|method_na|dataframe|Optional, accept: 'bfill', 'ffill'|'dropna'|

### 8. get_trend_mean
Add 'Month', 'WeekOfYear' and 'DayOfWeek' as dummy variables to dataframe
```
def get_trend_mean(df, date_column_name = 'DATE'):
    ...
    return new_df
```
  
|**Argument Name**|**Data Type**|**Required/Optional**|**Default Value**|
|:---|:---|:---|:---| 
|df|dataframe|Required|-|
|date_column_name|str[]|Optional|'DATE'|

### 9. get_dummy
Add dummy variables based on a specified column 
```
def get_dummy(df, dummy_columns = ['PERIOD']):
    ...
    return new_df
```
  
|**Argument Name**|**Data Type**|**Required/Optional**|**Default Value**|
|:---|:---|:---|:---| 
|df|dataframe|Required|-|
|dummy_columns|str[]|Optional|['Period']|


### 10. switch_y_column
Move the label_column to the last column
```
def switch_y_column(df, column_name):
    ...
    return new_df
```
|**Argument Name**|**Data Type**|**Required/Optional**|**Default Value**|
|:---|:---|:---|:---| 
|df|dataframe|Required|-|
|column_name|string|Required|-|

### 11. time_split_dataset
TimeSeriesSplit the test data into test and validation data
```
time_split_dataset(X, y, split_n = 30, print_shape=True):
    ...
    return X_train_seq, y_train_seq, X_val_seq, y_val_seq
```
|**Argument Name**|**Data Type**|**Required/Optional**|**Default Value**|
|:---|:---|:---|:---| 
|X|nparray|Required|-|
|y|nparray|Required|-|
|Split_n|int|Optional|30|
|print_shape|bool|Optional|True|

### 12. get_df_sql
Get data from SQL
```
get_df_sql(query, engine_path):
    ...
    return result_df
```
|**Argument Name**|**Data Type**|**Required/Optional**|**Default Value**|
|:---|:---|:---|:---| 
|query|string|Required|-|
|engine_path|string|Required|-|




## Functions included in model:

### 1. model_with_data_split
```
def model_with_data_split(df, 
                          label_column, 
                          train_start, train_end, 
                          look_back, look_forward, 
                          column_set_index = 'DATE', split_n = 30, 
                          n_neurons = [128], 
                          transformer_args = [5, 256, 256, 256], 
                          print_model_summary = True, 
                          dropout = 0.5, 
                          epochs = 30, patience = 5, 
                          early_stop = True, 
                          save_model = False, model_path = '', checkpoint_path = '', 
                          model_name = 'lstm', 
                          enable_optuna = False, epochs_each_try = 10, n_trials = 10, 
                          show_loss = True)

```
Arguments Table

|**Argument Name**|**Data Type**|**Required/Optional**|**Default Value**|
|:---|:---|:---|:---|  
|df|Dataframe|Required|-|
|label_column|string|Required|-|
|train_start|Same as index|Required|-|
|train_end|Same as index|Required|-|
|look_back|int|Required|-|
|look_forward|int|Required|-|
|column_set_index|string|Optional|'DATE'|
|split_n|int|Optional|30|
|n_neurons|int[]|Optional|[128]|
|transformer_args|int[]|Optional|[5, 256, 256, 256]|
|print_model_summary|bool|Optional|True|
|dropout|float|Optional|0.5|
|epochs|int|Optional|30|
|patience|int|Optional|5|
|early_stop|bool|Optional|True|
|save_model|bool|Optional ***Note:*** If True, both model_path and checkpoint_path must be given|False|
|model_path|string|Optional|''|
|checkpoint_path|string|Optional|''|
|model_name|string|Optional|'lstm'|
|enable_optuna|bool|Optional|False|
|epcochs_each_try|int|Optional|10|
|n_trials|int|Optional|10|
|show_loss|bool|Optional|True|


### 2. linear_model_with_optuna

```
linear_model_with_optuna(df, 
                         label_column, 
                         column_set_index = 0, 
                         start_index = '', 
                         end_index = '', 
                         print_data_shape = True, 
                         save_model = False, 
                         model_path = '', 
                         enable_optuna = True, 
                         n_trials = 20, 
                         model_name = 'elasticnet', 
                         alpha = 0.1, 
                         l1 = 0.5)
```
Arguments Table

|**Argument Name**|**Data Type**|**Required/Optional**|**Default Value**|
|:---|:---|:---|:---|  
|df|DataFrame|Required|-|
|column_set_index|string|Optional|0|
|start_index|string|Optional|''|
|end_index|string|Optional|''|
|print_data_shape|bool|Optional|True|
|save_model|bool|Optional|False|
|model_path|bool|Optional, Required if save_model=True|''|
|enable_optuna|bool|Optional|True|
|n_trials|int|Optional|20|
|model_name|string|Optional|'elasticnet'|
|alpha|int|Optional|0.1|
|l1|int|Optional|0.5|

### 3. xgb_with_optuna
```
xgb_with_optuna(df, 
                label_column, 
                column_set_index = 0, 
                start_index = '0', 
                end_index = '1', 
                save_model = False, 
                model_path = '', 
                enable_optuna = True, 
                n_trials =10)
```
Arguments Table

|**Argument Name**|**Data Type**|**Required/Optional**|**Default Value**|
|:---|:---|:---|:---|  
|df|DataFrame|Required|-|
|label_column|string|Required|-|
|column_set_index|string|Optional|0|
|start_index|string|Optional|'0'|
|end_index|string|Optional|'1'|
|save_model|bool|Optional|False|
|model_path|bool|Optional, Required if save_model=True|''|
|enable_optuna|bool|Optional|True|
|n_trials|int|Optional|10|

### 4. test_result
```
test_result(df, 
            target_column , 
            model_path=[], 
            model_type=[], 
            look_back = 1, 
            look_forward = 1, 
            display_metrix = True, 
            display_plot = True, 
            display_title = '', 
            display_legend = ['pred', 'real'])
```
Arguments Table

|**Argument Name**|**Data Type**|**Required/Optional**|**Default Value**|
|:---|:---|:---|:---|  
|df|DataFrame|Required|-|
|target_column|string|Required|-|
|model_path|model|Optional|[]|
|model_type|str[]|Optional, accpet: 'lstm', 'tcn', 'transformer'|[]|
|look_back|int|Optional|1|
|look_forward|int|Optional|1|
|display_metrix|bool|Optional|True|
|display_plot|bool|Optional|True|
|display_title|string|Optional|''|
|display_legend|str[]|Optional|['pred', 'real']|

### 5. predict_result
```
predict_result(predict_data_list = [], 
                model_path=[], 
                model_type=['lstm'])
```
Arguments Table

|**Argument Name**|**Data Type**|**Required/Optional**|**Default Value**|
|:---|:---|:---|:---|  
|predict_data_list|int[]|Optional|[]|
|model_path|model|Optional|[]|
|model_type|str[]|Optional, accept: ['lstm', 'tcn', 'transformer']|['lstm']|


## Functions included in feature_engineer:

### 1. sg_long_term_feature_engineering
```
sg_long_term_feature_engineering(df, 
                                brent_df, 
                                gas_df, 
                                weather_df, 
                                filter_columns, 
                                target_column)
```

Arugments Table
|**Argument Name**|**Data Type**|**Required/Optional**|**Default Value**|
|:---|:---|:---|:---|  
|df|DataFrame|Required|-|
|brent_df|DataFrame|Required|-|
|gas_df|DataFrame|Required|-|
|weather_df|DataFrame|Required|-|
|filter_columns|string|Required|-|
|target_column|string|Required|-|

### 2. sg_short_term_feature_engineering
```
sg_short_term_feature_engineering(dpr_df, 
                                    reg_df, 
                                    advisory_df_dummy, 
                                    targetvariable, 
                                    main_features)
```

Arugments Table
|**Argument Name**|**Data Type**|**Required/Optional**|**Default Value**|
|:---|:---|:---|:---|  
|dpr_df|DataFrame|Required|-|
|reg_df|DataFrame|Required|-|
|advisory_df_dummy|DataFrame|Required|-|
|targetvariable|string|Required|-|
|main_features|list|Required|-|

### 3. shandong_feature_engineering
```
shandong_feature_engineering(data, 
                            feature_columns, 
                            start_index, 
                            end_index, 
                            predict=False)
```
Arugments Table
|**Argument Name**|**Data Type**|**Required/Optional**|**Default Value**|
|:---|:---|:---|:---|  
|data|DataFrame|Required|-|
|feature_columns|str[]|Required|-|
|start_index|string|Required|-|
|end_index|string|Required|-|
|predict|bool|Optional|False|












### OLD ###
### 1. lstm model customized  
### suite_model.lstm_model_custmize(look_back, look_forward, n_features, dropout=0.5, print_summary=False, n_neurons = [128])  
  
|parameter|data type|description|default value|  
|:---|:---|:---|:---|  
|**look_back**|int|input size|-|  
|**look_forward**|int|output size|-|  
|**n_features**|int|number of features|-|  
|**dropout**|float|range (0,1)|0.5| 
|**n_neurons**|int[]|number of neurons in each layer, eg. [256, 128, 64]|[128]| 
|**print_summary**|boolean|True: print model summary. |False|    
|**return**|Model|lstm model|-|  
  
example:    
```
from ds_common_tool import suite_model  
  
lstmModel = suite_model.lstm_model_custmize(look_back=30, look_forward=30, n_features=4, dropout=0.5, print_summary=False, n_neurons = [128])
```  

### 2. train the model  
### suite_model.train_model(model, X_train_seq, y_train_seq, X_val_seq, y_val_seq, epochs=100, early_stop = True, patience=10, save_model = False, model_path='', checkpoint_path='', show_loss = True)  
   
|parameter|data type|description|default value|  
|:---|:---|:---|:---|  
|**model**|int|input size|-|  
|**X_train_seq**|same type as model||-|  
|**y_train_seq**|same type as model||-|  
|**X_val_seq**|same type as model||-| 
|**y_val_seq**|same type as model||-| 
|**epochs**|int epochs for traning||100|    
|**early_stop**|boolean|True: to use early_stop|True|     
|**patience**|int| range(10, +), patience needed if early_stop=True|10|  
|**save_model**|boolean|True: save model and weight|False|  
|**model_path**|string|path where the model is saved, e.g. model_path = '../../model/LSTM_longterm_usep.hdf5'|''|  
|**checkpoint_path**|string|path where the checkpoint(weight) is saved, e.g. checkpoint_path = '../../model/checkpoint/cp-lstm-longterm-usep.ckpt'|''|  
|**show_loss**|boolean|True: plot loss for each epoch|True|  
|**return**|Model|updated model|-|  
  
example:    
```
from ds_common_tool import suite_model  
  
lstmModel = suite_model.train_model(lstmModel, X_train_seq, y_train_seq, X_val_seq, y_val_seq, 
                          epochs=3, 
                          early_stop = True, 
                          patience=3, 
                          save_model = True, 
                          model_path = '../../model/LSTM_longterm_usep.hdf5',
                          show_loss = True)
```  

### 3. LSTM model with split sequences
### suite_model.lstm_model_with_data_split(df, label_column, train_start, train_end, test_start, test_end, look_back, look_forward, column_set_index = 0,split_n = 30, lstm_n_neurons = [128], print_model_summary = True, dropout = 0.5, epochs = 30, patience = 5,early_stop = True, save_model = False, model_path = '', checkpoint_path = '', show_loss = True, show_result_plot = True, plot_title = '',evauate_metric = ['mape']) 
   
|parameter|data type|description|default value|  
|:---|:---|:---|:---|  
|df|Dataframe|df to be processed|-|
|label_column|nparray[]|target column for prediction|-|
|train_start|string|Starting train date|-|
|train_end|string|Ending train date|-|
|test_start|string|Starting test date|-|
|test_end|string|Ending test date|-|
|look_back|int|input size|-|
|look_forward|int|output size|-|
|column_set_index|int|Set an index column to specified index|0|
|split_n|int|Number of splits for TimeSeriesSplit|30|
|lstm_n_neurons|int[]|Neurons needed per layer|[128]|
|print_model_summary|bool|Print summary if True|True|
|dropout|float|range(0, 1)|0.5|
|epochs|int|Number of epochs|30|
|patience|int|Patience for early_stop|5|
|early_stop|bool|Enable early_stop if True|True|
|save_model|bool|Enable to save model ***Note:*** If True, both model_path and checkpoint_path must be given|False|
|model_path|string|Path to save model|''|
|checkpoint_path|string|Path to save checkpoint|''|
|show_loss|bool|Loss plot will be printed if True|True|
|show_result_plot|bool|Result plot will be shown if True|True|
|plot_title|string|Include plot title|''|
|evaluate_metric|str[]|Metrics to be evaluate|['mape']|
|**return**|Model, mae, mape, prediction|-|-|  

example:    
```
from ds_common_tool import suite_model 
  
lstmModel, mae, mape, prediction_data = suite_model.lstm_model_with_data_split(df = all_data, 
                                                                               label_column = 'mean_30', 
                                                                               train_start = '2017-02-01', 
                                                                               train_end = '2020-12-31', 
                                                                               test_start = '2020-12-01', 
                                                                               test_end = '2021-01-31', 
                                                                               look_back = 31, 
                                                                               look_forward = 31, 
                                                                               column_set_index = 'DATE',
                                                                               split_n = 30, 
                                                                               lstm_n_neurons = [128, 64],
                                                                               print_model_summary = True,
                                                                               dropout = 0.5,
                                                                               epochs = 30,
                                                                               patience = 5,
                                                                               early_stop = True,
                                                                               save_model = False,
                                                                               show_loss = True,
                                                                               show_result_plot = True,
                                                                               plot_title = '',
                                                                               evauate_metric = ['mape'])
```  

### 4. Check metrics: mae, mape
### check_result_metric(y_true, y_pred, methods=['mae'], print_result=True)

|parameter|data type|description|default value|  
|:---|:---|:---|:---| 
|y_true|nparray|Same type as model|-|
|y_pred|nparray|Same type as model|-|
|methods|str[]|Specify metrics in a list. Available metrics: ['mae', 'mape']|['mae']|
|print_result|bool|Print result if True|True|

### 5. TCN
### tcn_model(look_back, n_features, look_forward, batch_size=None, print_summary=True, n_neurons=[128])

|parameter|data type|description|default value|  
|:---|:---|:---|:---| 
|look_back|int|Input size|-|
|n_features|int|Number of features|-|
|look_forward|int|Output size|-|
|batch_size|int|Specifies batch size|None|
|print_summary|bool|Print if True|True|
|n_neurons|int[]|To specify number of neurons|[128]|

### 6. LSTM with Optuna
### optuna_lstm(epochs_each_try, n_trials, look_back, look_forward, n_features, X_train_seq, y_train_seq, X_val_seq, y_val_seq, print_best_trail = True)

|parameter|data type|description|default value|  
|:---|:---|:---|:---| 
|epochs_each_try|int|Number of epochs to run during each trial|-|
|n_trials|int|Number of trials to run for Optuna|-|
|look_back|int|Input size|-|
|look_forward|int|Output size|-|
|n_features|int|Number of features|-|
|X_train_seq|Same type as model||-|
|y_train_seq|Same type as model||-|
|X_val_seq|Same type as model||-|
|y_val_seq|Same type as model||-|
|print_best_trial|bool|Print out the best trial if True|True|
|**return**|List of neurons, dropout|-|-| 

example:    
```
from ds_common_tool import suite_model 
  
n_neurons, dropout = suite_model.optuna_lstm(epochs_each_try = 5, 
                                 n_trials = 10, 
                                 look_back = 31, 
                                 look_forward = 31, 
                                 n_features = 82, 
                                 X_train_seq = X_train_seq, 
                                 y_train_seq = y_train_seq, 
                                 X_val_seq = X_val_seq, 
                                 y_val_seq = y_val_seq, 
                                 print_best_trail = True)
```  

## [pypi](https://pypi.org/project/ds-common-tool/#description)
