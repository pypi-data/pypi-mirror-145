from enum import Enum
from re import sub
from price_forecast_suite_package.suite_base import PriceForecastBase

class ENV(Enum):
  LOCAL_TEST = 'localtest'
  EAP = 'eap'

import importlib
from pathlib import Path

def import_all_modules_under_folder(folder_path: str, parent_module: str, recur: bool=True):
  folder = Path(folder_path)
  for sub_dir in folder.iterdir():
    if sub_dir.is_file() and str(sub_dir).endswith(".py"):
      importlib.import_module('.'.join([parent_module, sub_dir.parts[-1][:-3]]))
    elif recur and sub_dir.is_dir():
      import_all_modules_under_folder(sub_dir, parent_module + "." + sub_dir.parts[-1], recur=recur)

def get_all_subclasses(cls):
  all_subclasses = []
  for sub_cls in cls.__subclasses__():
    all_subclasses.append(sub_cls)
    all_subclasses.extend(get_all_subclasses(sub_cls))
  return all_subclasses

def get_class_under_folder(cls_str, parent_cls, folder_path, parent_module):
  # parent_module = ".".join(Path(folder_path).parts)
  import_all_modules_under_folder(folder_path, parent_module)
  all_cls = get_all_subclasses(parent_cls) + [parent_cls]
  return [cls for cls in all_cls if cls.__name__ == cls_str][0]

def get_forecast_subclass(cls_name: str):
  cur_folder = str(Path(__file__).parent)
  parent_module = Path(__file__).parent.parts[-1]
  cls = get_class_under_folder(cls_name, PriceForecastBase, cur_folder, parent_module)
  return cls

class SuitePrice():
  def __init__(self, case_name, node_id, env = ENV.LOCAL_TEST.value, df_name = '', target_column = '', date_column = '', demand_column = None, predict_point = 96, log_level = 0):
    self.case_name = case_name
    self.node_id = node_id
    self.env = env
    self.obj = None
    self.df_name = df_name
    self.target_column = target_column
    self.date_column = date_column
    self.demand_column = demand_column
    self.predict_point = predict_point
    
  def get_obj(self):
    class_name = self.case_name.upper()
    cls = get_forecast_subclass(class_name)
    self.obj = cls(self.case_name, self.node_id, self.env, self.df_name, self.target_column, self.date_column, self.demand_column, self.predict_point)
    return self.obj
