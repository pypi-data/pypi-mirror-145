import numpy as np
import pandas as pd

def get_optimal_dtype_int(data_col):
  max = data_col.max(); min = data_col.min()
  if max<=np.iinfo(np.int8).max and min >= np.iinfo(np.int8).min : return 'int8'
  elif max <=np.iinfo(np.int16).max and min >=np.iinfo(np.int16).min: return 'int16'
  elif max <=np.iinfo(np.int32).max and min >=np.iinfo(np.int32).min: return 'int32'
  else: return 'int64'

def get_optimal_dtype_float(data_col):
  max = data_col.max(); min = data_col.min()
  if max <=np.finfo(np.float16).max and min >= np.finfo(np.float16).min: return 'float16'
  elif max <=np.finfo(np.float32).max and min >=np.finfo(np.float32).min: return 'float32'
  else: return 'float64'

def get_optimal_dtype(data_col):
  if data_col.dtype == int: return get_optimal_dtype_int(data_col)
  elif data_col.dtype == float : return get_optimal_dtype_float(data_col)
  # elif data_col.dtype == np.dtype('O'): return 'object' 
  else: return data_col.dtype

def get_optimal_dtype_dict(function, path):
  df_temp = function(path)
  cols = df_temp.columns.tolist()
  dtypes = {col:get_optimal_dtype(df_temp[col]) for col in cols}
  dtypes_origin = {col:df_temp[col].dtype for col in cols}
  return dtypes, dtypes_origin, df_temp.memory_usage(deep = True).sum()/(1024**2) #MB 단위

def get_optimal_dtype_dict_by_data(data):
  cols = data.columns.tolist()
  dtypes = {col:get_optimal_dtype(data[col]) for col in cols}
  dtypes_origin = {col:data[col].dtype for col in cols}
  return dtypes, dtypes_origin, data.memory_usage(deep = True).sum()/(1024**2) #MB 단위

def print_storage_compress(dtypes, dtypes_origin, size, size_origin):
  for key in dtypes.keys():
    print(f"{key} : from {dtypes_origin[key]} to {dtypes[key]}")
  print("="*40)
  print(f"Result : {size_origin}MB -> {size}MB [{size/size_origin*100}%]")

def is_datetime(obj):
  import datetime
  date_format = ["%Y-%m-%d", "%Y/%m/%d", "%d %B, %Y", "%Y-%m-%d %H:%M:%S"]
  for f in date_format:
    try : 
      datetime.datetime.strptime(obj, f)
      return True
    except:
      return False

# 데이터 용량 최적화해서 다시 저장하는 함수
def compress_by_path(function, path, opt_print = False, date_auto = False, category_auto = False, json_path="dtypes.json"):
  dtypes, dtypes_origin, size_origin = get_optimal_dtype_dict(function, path)
  df_result = function(path, dtype=dtypes)

  #날짜 치환
  if date_auto:
    for key in dtypes.keys():
      if dtypes[key]!='object' or not is_datetime(df_result[key][0]):
        continue
      else:
        df_result[key] = pd.to_datetime(df_result[key])
        dtypes[key] = 'datetime'
  #카테고리 치환
  if category_auto:
    for key in dtypes.keys():
      if dtypes[key]!="object" or len(df_result[key].unique())>len(df_result)/5:
        continue
      else:
        df_result[key] = df_result[key].astype("category")
        dtypes[key] = 'category'
  #json으로 딕셔너리 저장
  import json
  json_data = json.dumps(dtypes)
  with open(json_path, "w") as a_file:
    json.dump(json_data, a_file)
  print(f"\n{json_path} 저장!")

  size = df_result.memory_usage(deep = True).sum()/(1024**2)
  if opt_print: print_storage_compress(dtypes, dtypes_origin, size, size_origin)
  return df_result

def compress(data, date_auto = False, category_auto = False, json_path="dtypes.json", opt_print = True):
  dtypes, dtypes_origin, size_origin = get_optimal_dtype_dict_by_data(data)
  for key in dtypes.keys():
    data[key] = data[key].astype(dtypes[key])
  #날짜 치환
  if date_auto:
    for key in dtypes.keys():
      if dtypes[key] !="object" or not is_datetime(data[key][0]):
        continue
      else:
        data[key] = pd.to_datetime(data[key])
        dtypes[key] = 'datetime'
  #카테고리 치환
  if category_auto:
    for key in dtypes.keys():
      if dtypes[key] !="object" or len(data[key].unique())>len(data)/5:
        continue
      else:
        data[key] = data[key].astype("category")
        dtypes[key] = 'category'
  #json으로 딕셔너리 저장
  import json
  json_data = json.dumps(dtypes)
  with open(json_path, "w") as a_file:
    json.dump(json_data, a_file)
  print(f"\n{json_path} 저장!")

  size = data.memory_usage(deep=True).sum()/(1024**2)
  if opt_print : print_storage_compress(dtypes, dtypes_origin, size, size_origin)
  return data

def read_data(function, data_path, json_path, nrows=""):
  import json
  with open(json_path, "r") as a_file:
    dtypes = json.loads(a_file)
    # dtypes = json.load(a_file).replace('\\', '')

  # dtypes_ = dtypes
  # print(dtypes_)

  # for key in dtypes_.keys():
  #   if dtypes_[key] == "datetime":
  #     dtypes_[key] = "object"
  
  #nrows는 여기 추가할 것
  if nrows=="":
    df_result = function(data_path, dtype=dtypes)
  else:
    df_result = function(data_path, dtype=dtypes, nrows=nrows)

  # for key in dtypes.keys():
  #   if dtypes[key] == "datetime":
  #     df_result[key] = pd.to_datetime(df_result[key])

  return df_result