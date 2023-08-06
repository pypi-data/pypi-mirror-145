# some data processing function #

import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from sklearn.model_selection import TimeSeriesSplit
import seaborn as sns
import numpy as np
from utils_for_ds.message import Message

def create_date_df(startDate = '20210101', endDate = '20210101'):
    format_pattern = '%Y%m%d'
    difference = (datetime.strptime(endDate, format_pattern) - datetime.strptime(startDate, format_pattern))
    if difference.days < 0:
        print(Message.WRONG_DATE_INPUT.value)
        return False
    date_list = [datetime.strftime(x, '%Y-%m-%d') for x in list(pd.date_range(start = startDate, end= endDate))]
    date_pd = pd.DataFrame(date_list)
    date_pd.rename(columns={0:'DATE'}, inplace= True)
    date_pd = date_pd.sort_values(by='DATE')
    date_pd['DATE'] = pd.to_datetime(date_pd['DATE'], infer_datetime_format=True)
    return date_pd

def sg_holiday_feature(holiday_df, startDate = '20200101', endDate = '20210101'):
  date_pd = create_date_df(startDate = startDate, endDate = endDate)
  holiday_df.rename(columns = {'Date':'DATE'}, inplace = True)
  holiday_df =holiday_df.sort_values(by='DATE')
  holiday_df['DATE'] = pd.to_datetime(holiday_df['DATE'], infer_datetime_format=True)
  df = date_pd.merge(holiday_df, on='DATE', how = 'left')
  df['Holiday'] = df['Holiday'].fillna('Non-Holiday')
  df = df[['DATE', 'Holiday']]
  df_dummy = pd.get_dummies(df, columns = ['Holiday'])
  return df_dummy

def get_dummy_value(df, dummy_columns):
  df_dummy = pd.get_dummies(df, columns = dummy_columns)
  return df_dummy

def get_date_dummy(df, date_column = 'DATE'):
  df = df.sort_values(by = date_column)
  df[date_column] = pd.to_datetime(df[date_column], infer_datetime_format=True)
  df['month'] = df[date_column].dt.month
  df['dayofmonth'] = df[date_column].dt.days_in_month
  df['weekofyear'] = df[date_column].map(lambda x:x.isocalendar()[1])
  df['dayofweek'] = df[date_column].map(lambda x:x.dayofweek+1)
  raw_data_dummy = pd.get_dummies(df, columns=[ 'month', 'weekofyear', 'dayofweek', 'dayofmonth'])
  return raw_data_dummy

def display_heatmap(df, show_font = False, show_square = True, picture_size = [18, 18]):
  plt.figure(figsize=picture_size, dpi=100)
  if show_square:
    sns.heatmap(data = df.corr(), vmax=0.3, annot=show_font, fmt='.2f')
  else:
    sns.heatmap(data = df.corr(), vmax=0.3, annot=False, fmt=".2f", mask=np.triu(np.ones_like(df.corr(), dtype=np.bool)), square=True, linewidths=.1)

def show_draft_plot(datas, x_label, title, legend, picture_size=[18, 5], shape = []):
    if shape == []:
        shape = np.zeros(len(datas), dtype=np.int64) 
    plt.rcParams["figure.figsize"] = picture_size
    for i in range(len(datas)):
        if shape[i] == 0 or shape[i] == 'line':
            plt.plot(x_label, datas[i], label=legend[i])
        if shape[i] == 1 or shape[i] == 'dot':
            plt.plot(x_label, datas[i], 'o', label=legend[i])
    plt.title(title)
    plt.legend(loc="best", shadow=True)
    plt.xticks(rotation= 45)
    plt.grid()
    plt.show()

def switch_y_column(df, column_name):
    c = df[column_name]
    new_df = df.drop(columns=column_name, axis=1)
    new_df.insert(new_df.shape[1], column_name, c)
    return new_df

def split_sequence(sequence, look_back = 30, look_forward = 30, print_shape = True):
    X, y = list(), list()
    loop_len = sequence.shape[0]
    for i in range(1, loop_len):
        end_ix = i + look_back # fing the end of the x parten
        out_end_ix = end_ix + look_forward - 1
        if out_end_ix > loop_len:
            break
        seq_x, seq_y = sequence[i - 1 : end_ix-1,  :-1], sequence[end_ix-1 : out_end_ix, -1]
        X.append(seq_x)
        y.append(seq_y)
    if print_shape:
        print('shape of seq_x : ', np.array(X).shape)
        print('shape of seq_y : ', np.array(y).shape)
    return np.array(X), np.array(y)

def time_split_dataset(X, y, split_n = 30, print_shape=True):
    tscv = TimeSeriesSplit(max_train_size = None, n_splits = split_n)
    for train_index, val_index in tscv.split(X):
        X_train_seq, X_val_seq = X[train_index], X[val_index]
        y_train_seq, y_val_seq = y[train_index], y[val_index]
    if print_shape:
        print('Training set shape', X_train_seq.shape, y_train_seq.shape)
        print('Validation set shape', X_val_seq.shape, y_val_seq.shape)
    return X_train_seq, y_train_seq, X_val_seq, y_val_seq

def predict_data_for_nn(df, target_column, look_back = 30, date_column = 'DATE'):
  df = df.sort_values(by = date_column)
  pred_x = df.set_index(date_column)
  pred_x = pred_x.drop(columns = [target_column]).iloc[-look_back:]
  X = np.asarray(pred_x).astype(np.float)
  X = X.reshape(1, X.shape[0], X.shape[1])
  return X

def set_label(df, label_column):
  label_list = np.unique(df[label_column])
  df[label_column] = df[label_column].map(lambda x: np.argwhere(label_list == x)[0][0])
  return df, label_list

