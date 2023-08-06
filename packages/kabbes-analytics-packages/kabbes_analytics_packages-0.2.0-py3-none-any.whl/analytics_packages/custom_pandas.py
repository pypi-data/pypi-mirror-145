"""
These are all very outdated, wrote these several years ago. There are probably much better ways to achieve what you need to
-James
"""

import pandas as pd
import matplotlib.pyplot as plt
import collections
import numpy as np
import datetime
import sys
from dateutil.relativedelta import relativedelta

def get_df(file_name, **params):
    '''Read csv file from local directory: return dataframe'''

    df = pd.read_csv(file_name, **params)
    return df

def df_change_row_ind_col_value(df, index, column, new_val):
    df.loc[index, column] = new_val
    return df

def value_counts_in_df(df, col):

    return df[col].value_counts()

def map_df_column_to_dict(df, col, dict, new_col):

    df[new_col] = df[col].map(dict)
    return df


def move_last_column_to_first(df):

    cols = df.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    df = df[cols]
    return df

def prep_datetime(df, time_col, dt_col, format = '%Y-%m-%d %H:%M:%S'):

    df[dt_col] = df[time_col].apply(lambda x: datetime.datetime.strptime(x, format) )
    return df

def fill_nans(df, value_to_fill):

    df = df.fillna(value_to_fill)
    return df

def get_date_and_time():

    return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

def df_replace(df, value_to_change, to_fill):

    df = df.replace(value_to_change, to_fill)
    return df

def and_gate_many_cols(df, columns, col_name):

    col1 = columns[0]
    col2 = columns[1]
    cols_added = []
    for i in range(len(columns) - 2):

        bool_num = 'bool' + str(i)
        join = bool_num + ': ' + col1 + '/' + col2
        cols_added.append(join)
        df[join] = df[col1] & df[col2]

        col1 = join
        col2 = columns[2 + i]


    df[col_name] = df[col1] & df[col2]
    df = drop_these_cols(df, cols_added)
    print ('cols added')
    print (cols_added)
    print ('after dropping')
    #print (df)
    return df


def combine_all_string_columns(df, columns, new_column):

    '''combines all columns contained in list found in df and renames it new column'''
    col1 = columns[0]
    col2 = columns[1]
    cols_added = []
    for i in range(len(columns) - 2):

        join = 'join' + str(i)
        cols_added.append(join)
        df = combine_string_columns(df, col1, col2, join)

        col1 = join
        col2 = columns[2 + i]


    #last join
    df = combine_string_columns(df, col1, col2, new_column)
    #print (df)
    df = drop_these_cols(df, cols_added)
    #print (df)
    return df

def new_df_with_value_in_col(df, col, val, opposite = False):


    if not opposite:
        new_df = df.loc[df[col] == val]
        return new_df

    if opposite:
        new_df = df.loc[df[col] != val]
        return new_df


def split_df_into_equal_time(df, time_chunk, datetime_col, format = 'seconds'):


    '''returns dfs after being split into separate dfs by a time separator
    example: starting from time 0, separate into chunks of 3 weeks at a time

    ISOTIME
    '''

    if format == 'minutes':
        time_chunk *= 60
    if format == 'hours':
        time_chunk *= 3600
    if format == 'days':
        time_chunk *= (3600 * 24)
    if format == 'weeks':
        time_chunk *= (3600 * 24 * 7)

    start_time = df.loc[ df.index[0], datetime_col]
    end_time = df.loc[ df.index[-1], datetime_col]
    time = start_time
    new_time = start_time

    dfs = []

    while new_time < end_time:

        #add the respective delta time to the new time
        if format == 'months':
            new_time = time + relativedelta(months = time_chunk)
        elif format == 'years':
            new_time = time + relativedelta(years = time_chunk)
        else:
            new_time = time + datetime.timedelta(seconds = time_chunk)

        #filter where time < df < new_time
        new_df = filter_df_by_dates(df, datetime_col, lower_datetime = time, upper_datetime = new_time, low_inc = True, up_inc = False)

        if new_time >= end_time:
            new_df = filter_df_by_dates(df, datetime_col, lower_datetime = time, upper_datetime = new_time, low_inc = True, up_inc = True)

        time = new_time
        dfs.append(new_df)

    return dfs

def split_by_time_filter(df, how = 'hours', new_poss_values = []):

    '''returns dfs which have been sifted based on hours/days/months etc
    refer to params.py -> time_splits for reference

    df1                      df2
    customer     hour        customer     hour
    0            0           0            1
    1            0           1            1
    2            0           2            1
    '''

    time_splits = {'data_dict': ['possible_values','xlabels','df_col'],
    'seconds': [list(range(60)), list(range(60)), 'SECOND'],
    'minutes': [list(range(60)), list(range(60)), 'MINUTE'],
    'hours': [list(range(24)), list(range(24)), 'HOUR'],
    'day_nums': [list(range(1,32)), list(range(1, 32)), 'DAY'],
    'days': [list(range(7)), ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'], 'WEEKDAY'],
    'weeks': [list(range(1,53)), list(range(1,53)), 'WEEK'],
    'months': [list(range(1,13)), ['January', 'February','March','April','May','June','July','August','September','October','November','December'], 'MONTH'],
    'years': [list(range(0, 10000)), list(range(0, 10000)), 'YEAR' ]
    }

    possible_values = time_splits[how][0] #list
    xlabels = time_splits[how][1] #list
    how_col = time_splits[how][2] #string

    dfs = []
    if new_poss_values != []:
        possible_values = new_poss_values

    for value in possible_values:

        new_df = df[ df[how_col] == value  ]
        dfs.append(new_df)

    return dfs


def filter_df_by_dates(df, date_col_dt, lower_datetime = None, upper_datetime = None, low_inc = True, up_inc = False):

    '''takes in a pandas df and returns one being filtered by lower and upper dates'''

    low = df.loc[df.index[0], date_col_dt ]
    high = df.loc[df.index[-1], date_col_dt ]

    if lower_datetime == None:
        print ('Enter info for lower datetime')
        lower_datetime = get_datetime_input()

        #if it goes below the bound
        if lower_datetime < low:
            lower_datetime = low

    if upper_datetime == None:
        print ('Enter info for upper datetime')
        upper_datetime = get_datetime_input()

        #if it goes above the bound
        if upper_datetime > high:
            upper_datetime = high

    if upper_datetime < lower_datetime:
        upper_datetime, lower_datetime = lower_datetime, upper_datetime
        print ('switching upper and lower datetimes')

    if low_inc:
        filtered = df[ df[date_col_dt] >= lower_datetime]
    else:
        filtered = df[ df[date_col_dt] > lower_datetime]

    if up_inc:
        filtered = filtered[  filtered[date_col_dt] <= upper_datetime ]
    else:
        filtered = filtered[  filtered[date_col_dt] < upper_datetime ]

    return filtered

def df_datetime_to_time_cols(df, datetime_col ,extra = False):

    df['YEAR'] = df[datetime_col].apply(lambda x: x.year)
    df['MONTH'] = df[datetime_col].apply(lambda x: x.month)
    df['DAY'] = df[datetime_col].apply(lambda x: x.day)
    df['HOUR'] = df[datetime_col].apply(lambda x: x.hour)
    df['MINUTE'] = df[datetime_col].apply(lambda x: x.minute)
    df['SECOND'] = df[datetime_col].apply(lambda x: x.second)

    if extra:

        df['WEEKDAY'] = df[datetime_col].apply( lambda x: x.weekday() )

    return df

def sort_df(df, columns, ascend = True, na_pos = 'last'):

    df = df.sort_values(columns, ascending = ascend, na_position = na_pos)
    return df


def map_df_col_to_new_id(df, col, new_col_name, df2, id_col, map_col):

    map_dict = dict_from_two_columns(df2, id_col, map_col)
    df = map_df_column_to_dict(df, col, map_dict, new_col_name)
    return df

def dict_from_two_columns(df, key_col, val_col):

    #In [9]: pd.Series(df.Letter.values,index=df.Position).to_dict()
    #Out[9]: {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e'}
    a = pd.Series(df[val_col].values, index = df[key_col]).to_dict()
    return a


def replace_in_df(dataframe, column, to_find, to_replace):

    '''Replaces list or string "to_find" with list or string "to_replace"
    Looks up all instances in "column" found in the dataframe and replaces them
    Returns dataframe'''

    assert type(column) == str

    if type(to_find) == str:
        to_find = [to_find]

    if type(to_find) == list:

        if type(to_replace) == list:
            assert len(to_replace) == len(to_find) #replace them based on index match
            # to_find = ['USA','GB'] to_replace = ['United States','Great Britain']

        else:
            #in this case all the instances in to_find will be replaced with the string to_replace
            a = to_replace
            to_replace = [a, ] * len(to_find)

        for i in range(len(to_find)):
            item = to_find[i]
            replace = to_replace[i]
            dataframe.loc[ dataframe[column] == item, column  ] = replace

    return dataframe

def keep_these_cols(df, cols):
    '''Returns dataframe with columns 'cols' '''
    return df[cols]

def drop_these_cols(df, cols):
    '''Returns dataframe without columns 'cols' '''
    return df.drop(cols, axis = 1)

def keep_these_rows(df, rows):
    '''Returns dataframe with index values contained in 'rows' '''
    return df.loc(rows)

def drop_these_rows(df, rows):
    '''Returns dataframe without 'rows' based on index value'''
    return df.drop(rows)


def rename_cols(df, existing, new):

    '''renames cols found in 'existing' to match those found in "new" '''

    if type(existing) == str:
        existing = [existing]
    if type(new) == str:
        new = [new]

    assert len(existing) == len(new)

    for i in range(len(existing)):
        df = df.rename(index = str, columns = {existing[i] : new[i]})

    return df


def multiple_filters(df, columns, two_dim_list):

    '''columns = ['Age','Name']
    two_dim_list = [ [21, 25], ['James','Michael'] ]

    this function sends back the df with age values of 21 and 25 and name values of james and michael
    '''

    new_df = df

    for col_num in range(len(columns)):

        col = columns[col_num]
        dfs = []
        for criteria in two_dim_list[col_num]:

            df = new_df[ new_df[col] == criteria ]
            dfs.append(df)

        if dfs != []:
            new_df = pd.concat(dfs)

    return new_df

def ceiling_filter(df, max_val, column):
    '''Returns df with values below 'max_val' found in 'column' '''
    df = df[  df[column] <= max_val  ]
    return df

def floor_filter(df, min_val, column):
    '''Returns df with values above 'min_val' found in 'column' '''
    df = df[  df[column] >= min_val  ]
    return df

def boxplot(df, column_with_values, group_by = None):
    '''Shows a boxplot values found in 'column_with_values' with the option to group by another column'''

    if type(group_by) == str:
        df.boxplot(column = column_with_values, by = group_by)
    else:
        df.boxplot(column = column_with_values)

def add_to_bottom(df, column_names, values):

    '''Adds to bottom of dataframe based on 'column_names' and 2D list 'values.' See append_to_df_with_df for appending dfs'''

    assert len(values) == len(column_names)

    if type(column_names) == str:
        column_names = [column_names]
    if type(values) == str:
        values = [values]

    dictionary = {}
    for i in range(len(values)):
        dictionary[column_names[i]] = values[i]

    df = append_to_df_with_df(df, dict_to_df(dictionary))
    return df


def check_column_in_list(df, column, list, new_column):
    '''returns a dataframe with a boolean value in new column if the row had one of those value or not'''

    df[new_column] = df[column].isin(list)
    return df


def append_to_df_with_df(og_df, new_df, reset_ind = True):

    '''Appends 'og_df' with 'new_df' and returns new'''
    return og_df.append(new_df, ignore_index = reset_ind)

def grab_rows_with_certain_values(df, column, values, return_not_in_values = False):

    '''Returns a version of the dataframe where every row in "column" contains a value found in list"values"'''

    if return_not_in_values: #this means we want only the values that are not contained in the values list

        if type(values) == list:
            #print ( df.loc[~df[column].isin(values)] )
            df = df.loc[~df[column].isin(values)]
        else:
            df = df.loc[df[column] != values]

    else: #only those not in the values list

        if type(values) == list:
            #print ( df.loc[df[column].isin(values)] )
            df = df.loc[df[column].isin(values)]
        else:
            df = df.loc[df[column] == values]


    return df

def violin_plot(df, column, filter_column = None, min_val = None, max_val = None, mult = 1, add = 0):

    '''Displays a violin plot of the values found in "column" filtered by optional param "filter_column"'''

    if min_val != None:
        df = floor_filter(df, min_val, column)
    if max_val != None:
        df = ceiling_filter(df, max_val, column)

    df[column] = df[column] * mult
    df[column] = df[column] + add
    if filter_column != None:
        a = sns.violinplot(x = df[filter_column], y = df[column], inner = 'quartiles')
    else:
        a = sns.violinplot(y = df[column], inner = 'quartiles')
    plt.show()

def get_unique_values(df, col):
    return df[col].unique()



def dict_to_df(dictionary):

    '''Return a dataframe from 'dictionary' '''
    df = pd.DataFrame(dictionary)
    return df

def value_counts_df(original_dataframe, column = None):

    '''This function outputs a dataframe with counts of the unique values for each column from the input dataframe (function argument).
    The counts are given for each column of the input dataframe - in the output a column with
    unique values is paired with another column with the counts for the unique values'''
    df_dict = dict()
    if column == None:
        for i in original_dataframe.columns:
            series_value_counts = original_dataframe[i].value_counts()
            dict_value_key = series_value_counts.name+"_value"
            dict_count_key = series_value_counts.name+"_count"
            df_dict[dict_value_key] = list(series_value_counts.index)
            df_dict[dict_count_key] = list(series_value_counts.values)
    else:
        i = column
        series_value_counts = original_dataframe[i].value_counts()
        dict_value_key = series_value_counts.name+"_value"
        dict_count_key = series_value_counts.name+"_count"
        df_dict[dict_value_key] = list(series_value_counts.index)
        df_dict[dict_count_key] = list(series_value_counts.values)

    return pd.DataFrame(collections.OrderedDict([(key,pd.Series(values)) for key,values in df_dict.items()]))


def histogram( two_dim_list, x_axis_titles, legend_labels, x_label, y_label, graph_title, text_size = 11, axesfont = 26, titlesize = 32, opacity = .6  ):

    '''Prints a histogram: two_dim_list variable should contain n-number (number of differnt colored series to plot) of lists of numerical values l-length long.
    x_axis_titles is a list of strings l-length long
    legend labels is a list of strings to the number of lists contained in two_dim_list
    ex: two_dim_list = [ [.1, .4, .3, .2], [.2, .4, .3, .1], [.2, .3, .3, .2] ], x_axis_titles = ['Pepperoni','Sausage','Cheese','Vegetable'], legend_labels = ['under 20 years old','20-50','50+']
    '''


    division_list = two_dim_list
    all_col = x_axis_titles

    plt.style.use('ggplot')

    n_groups = len(all_col)
    x_index_list = all_col
    x_axis_ticklabels = all_col

    fig, ax = plt.subplots()
    index = np.arange(n_groups)

    bar_width = ( 1 / len(division_list) ) - ( .1 / len(division_list) )
    colors = ['r','g','b','c','y']


    for i in range(len(division_list)):

        a = ax.bar(index + bar_width * i, division_list[i], bar_width, alpha = opacity, color = colors[i], label = legend_labels[i])


    plt.xlabel(x_label, weight = 'bold', fontsize = axesfont)
    plt.ylabel(y_label, weight = 'bold', fontsize = axesfont)
    plt.suptitle(graph_title, weight = 'bold', fontsize = titlesize )
    ax.set_xticks(index + bar_width / 2)
    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(text_size)

    #for i in range(len(x_axis_ticklabels)):
    #    x_axis_ticklabels[i] = '\n'.join(x_axis_ticklabels[i].split(':'))

    ax.set_xticklabels( x_axis_ticklabels )
    ax.legend()

    plt.show()
