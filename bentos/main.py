import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


class PopulationData:
    """
    The ad exports data from an excel spreadsheet.
    When output, it shows a list of tables.
    The table (PopulationTable) can be accessed by the key.
    """
    def __init__(self, name_file=None, name_obj=None):
        if name_file is not None:
            self.bd = pd.ExcelFile(name_file)
            self.sheets = self.bd.sheet_names
        elif name_obj is not None:
            pass
        else:
            raise IOError("error")

    def __str__(self):
        s = ''
        for i in range(len(self.sheets)):
            s = s + f'[{i}] = "{self.sheets[i]}"\n'
        return str(s)

    def __getitem__(self, key):
        table = self.bd.parse(self.sheets[key], parse_dates=True)
        return PopulationTable(table)


class PopulationTable:
    """
    Add-on to the pandas class.
    """
    def __init__(self, object):
        self.table = object
        self.name_column_depth = 'Глубина, м'
        self.name_column_time = 'Дата'
        self.name_column_local = 'Характеристика (расстояние)'
        self.name_column_kind = 'Вид'

    def __add__(self, other):
        res = pd.concat([self.table, other.table])
        return PopulationTable(res)

    def __str__(self):
        return str(self.table)

    def print_columns(self):
        s = ''
        for i in range(len(self.table.columns)):
            s = s + f'[{i}] = "{self.table.columns[i]}"\n'
        print(s)

    def filter_columns(self, array_num):
        columns = self.get_columns_by_index(array_num)
        return PopulationTable(self.table[columns])

    def limit_depth(self, m=None, M=None):
        if (m is not None) and (M is not None):
            res = self.table[(self.table[self.name_column_depth] >= m) & (self.table[self.name_column_depth] <= M)]
        elif (m is None) and (M is not None):
            res = self.table[self.table[self.name_column_depth] <= M]
        elif (m is not None) and (M is None):
            res = self.table[self.table[self.name_column_depth] >= m]
        else:
            res = self.table
        self.table = res

    def plot(self, column_y, column_x=None, name='', stl='--'):
        if column_x is None:
            column_x = self.name_column_time
        y_col = self.get_columns_by_index([column_y])

        x0 = self.table[column_x]
        y0 = self.table[y_col[0]]

        plt.plot(x0, y0, stl, label=name)

    def get_array_dates(self, in_zero=False):
        res = self.table[self.name_column_time].array
        if in_zero is True:
            t_start = res[0]
            res = [(i - t_start).days for i in res]
        return res

    def get_val_in_time(self, date, column):
        columns = self.get_columns_by_index([column])
        df_t = self.table[self.table[self.name_column_time] == date]
        res = df_t[columns[0]].values
        return res[0][0]

    def max_samples_in(self, array_num_column):
        column = self.get_columns_by_index(array_num_column)
        series = self.table[column]
        res = series.max()
        return res

    def get_columns_by_index(self, array_num):
        return list(map(self.table.columns.__getitem__, array_num))
    
    def get_array_column(self, num_col):
        column = self.get_columns_by_index([num_col])[0]
        res = self.table[column].values
        return res

    def get_locals(self):
        res = self.table.groupby(self.name_column_local)[self.name_column_local].count().reset_index(name='Count')
        return PopulationTable(res).get_array_column(0)

    def print_locals(self):
        tbl = self.get_locals()
        for i in range(len(tbl)):
            print(f'[{i}] = {tbl[i]}')

    def get_kinds(self):
        res = self.table.groupby(self.name_column_kind)[self.name_column_kind].count().reset_index(name='Count')\
            .sort_values('Count', ascending=False)
        return PopulationTable(res).get_array_column(0)

    def print_kinds(self):
        tbl = self.get_kinds()
        for i in range(len(tbl)):
            print(f'[{i}] = {tbl[i]}')

    def limit_kind(self, num):
        kind = self.get_kinds()
        res = self.table[self.table[self.name_column_kind] == kind[num]]
        return PopulationTable(res)

    def limit_local(self, num):
        local = self.get_locals()
        res = self.table[self.table[self.name_column_local] == local[num]]
        return PopulationTable(res)

    def group_date(self):
        res = self.table.groupby(pd.Grouper(key=self.name_column_time, freq='1M')).mean().reset_index()

        res = res[~res[self.get_columns_by_index([1])[0]].isnull()]
        self.table = res

    def get_summer_and_winter(self):
        summer_num = (5, 6, 7, 8, 9, 10)
        summer = pd.DataFrame(columns=self.table.columns)
        winter = pd.DataFrame(columns=self.table.columns)
        tbl = self.table.reset_index(drop=True)
        w = 0
        s = 0
        for i in range(self.table.shape[0]):
            row = tbl.iloc[i]
            mount = row.iloc[0].date().month
            if mount in summer_num:
                summer.loc[s] = row
                s += 1
            else:
                winter.loc[w] = row
                w += 1
        tbl_summer = PopulationTable(summer)
        tbl_winter = PopulationTable(winter)
        return tbl_summer, tbl_winter 


def get_bd():
    """return bd bentos"""
    bd = PopulationData(name_file='bd.xls')
    tbl = bd[0] + bd[1] + bd[2] 
    return tbl


def get_tbl_date_t_info(num_column=11, tbl=get_bd()):
    """
    group tbl by data
    take column from tbl and return as np.array
    return time from 0 data column 
    return dates data column
    """
    tbl = tbl.filter_columns([0, num_column])  
    tbl.group_date() 
    
    dates = tbl.get_array_dates()
    t = tbl.get_array_dates(in_zero=True)
    times = np.array(t)
    info = tbl.get_array_column(1)
    data = np.array(info)
    return [tbl, dates, times, data]


TBL, DATES, TIMES, DATA = get_tbl_date_t_info()
