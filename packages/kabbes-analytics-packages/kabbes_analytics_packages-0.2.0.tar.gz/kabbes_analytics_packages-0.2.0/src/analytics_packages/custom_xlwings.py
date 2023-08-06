"""
These are all very outdated, wrote these several years ago. There are probably much better ways to achieve what you need to
-James
"""

import xlwings as xw
import pandas as pd
import sys
import analytics_packages.custom_pandas as cpd

def get_ws(wb, sheet = 'Sheet1'):

    sheet = remove_slash_from_ws_name(sheet)
    sheet_names = get_book_sheets_names( wb )

    if sheet not in sheet_names:
        add_sheet(sheet, wb)

    ws = wb.sheets[sheet]
    return ws

def get_wb(book_name):

    try:
        return xw.Book(book_name)
    except:
        wb = xw.Book(None)
        wb.save(book_name)
        return wb

def get_book_sheets( wb ):

    return wb.sheets

def get_book_sheets_names( wb ):

    names = []
    sheets = get_book_sheets( wb )

    for sheet in sheets:
        names.append( sheet.name )

    return names

def add_sheet(sheet_name, work_book):

    '''adds sheet to workbook'''

    sheet_name = remove_slash_from_ws_name(sheet_name)
    work_book.sheets.add(sheet_name)

def delete_sheet(ws):

    try:
        ws.delete()
    except:
        pass

def sort_ws(ws, column_alphas):

    '''takes active ws and list of column alphas and sorts worksheet'''

    df = df_from_rows( get_rows(ws) )
    headers = get_column_headers_from_alpha(df, column_alphas)
    df = cpd.sort_df(df, headers)
    #print (headers)
    #print (df)
    write_df_to_ws(ws, df)

def write_df_to_ws(ws, df):

    header = df.columns.tolist()
    rows = [ header ]

    for i in range(len(df)):
        rows.append( list(df.iloc[i]) )

    write_2d(ws, rows)


def get_df_from_ws(ws):

    df = df_from_rows( get_rows(ws))
    return df

def df_from_rows(rows):

    df = pd.DataFrame(rows[1:], columns = rows[0])
    return df

def get_rows(ws, top_left_cell = (1,1), bottom_right = None):

    if bottom_right == None:
        bottom_right = (full_range(ws).last_cell.row, full_range(ws).last_cell.column)
    rows = ws.range( top_left_cell, bottom_right ).options(ndim = 2).value
    return rows

def write_2d(ws, rows, top_left_cell = (1,1)):

    ws.range(top_left_cell).expand().value = rows

def remove_slash_from_ws_name(string, replace = True, char = '-'):

    if replace:
        return string.replace('/', char)
    else:
        return string.replace( '/','')

def full_range(ws):

    rng = ws.range('A1').expand()
    return rng

def row_to_col(row):

    if len(row) == 1:
        return row

    col = []
    for i in row:
        col.append( [i])
    return col

def keep_these_rows(df, locs):

    df = df.loc(locs)
    return df

def get_column(ws, col_index, nested = True):

    '''gets a column from the ws'''
    col = []
    if nested:
        for row in get_rows(ws):
            col.append([ row[col_index] ] )

    else:
        for row in get_rows(ws):
            col.append( row[col_index] )
    return col

def write_df_col_to_ws(ws, df, col_index, col_name):

    '''writes a df column to a certain column number in the ws'''

    values = df[col_name]
    try:
        values = values.tolist()
    except:
        values = []
    values.insert(0, col_name)
    #print (values)
    values_col = row_to_col(values)
    #print (values_col)

    write_2d(ws, values_col, top_left_cell = (1, col_index + 1))

def clear_all(ws):

    rows = get_rows(ws)
    blank = [[None, ] * len(rows[0]), ] * len(rows)
    write_2d(ws, blank)

def alpha_from_index(integer):

    '''Takes a 0-based index (integer) and returns the corresponding column header'''

    lengths = [1,2,3,4,5,6,7]
    contained_in_lengths = []
    for i in lengths:
        contained_in_lengths.append(26 ** i)

    integer += 1

    integer_copy = integer
    num_digits = lengths[-1]
    for i in range(len(contained_in_lengths)):
        integer_copy -= contained_in_lengths[i]

        if integer_copy <= 0:
            num_digits = i + 1
            break

    digits = ['',] * num_digits
    alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    breakdown = [0,] * num_digits
    digits = [0,] * num_digits
    for i in range(num_digits):

        breakdown[i] = integer % (contained_in_lengths[i])
        if breakdown[i] == 0:
            breakdown[i] = contained_in_lengths[i]
        integer -= breakdown[i]
        digits[i] = breakdown[i] / (26**i)

    string = ''
    digits.reverse()
    for i in digits:
        string += alpha[int(i) - 1]
    return string

def alphas_from_index_list(ints):

    final = []
    for i in ints:
        final.append(alpha_from_index(i))
    return final

def column_index_from_alphas(string):

    list = []
    for i in string:
        list.append(i.upper())

    alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    multiplier = 0
    final = 0
    for i in range(len(list)):

        new_mult = 26**i
        #1, 26, 676

        place = (i+1) * -1
        index = alpha.index( list[place] )
        index += 1
        final += (index * new_mult)

    return (final - 1)

def get_column_headers_from_alpha(df, list_of_alphas):

    inds = []
    for i in list_of_alphas:
        inds.append(column_index_from_alphas(i))

    df_headers = []
    cols = df.columns.tolist()
    #print (cols)
    #print (len(cols))

    for i in range(len(list_of_alphas)):
        df_headers.append(cols[ inds[i] ])
        #print (inds[i])

    return df_headers



def combine_string_columns(df, col1, col2, new_column):

    '''Returns df with new column that has a compiled string of col1 and col2'''

    df[new_column] = df[col1].map(str) + df[col2].map(str)
    return df

def alpha_from_column_names(df, strings):

    cols = df.columns.tolist()

    alphas = []
    for i in strings:
        a = cols.index(i)
        alphas.append( alpha_from_index(a) )

    return alphas

def change_cell_color(ws, top_left_cell, cell_color, bottom_right_cell = None):

    '''changes a range of cells a certain color'''
    if bottom_right_cell == None:
        bottom_right_cell = top_left_cell
    ws.range(top_left_cell, bottom_right_cell).color = cell_color
