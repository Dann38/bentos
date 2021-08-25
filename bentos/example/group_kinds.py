import main as m
from scipy.interpolate import interp1d
import numpy as np

COLUMN_DATA = 4
DEVIATIONS = 0.1
BD = m.get_bd()

def similarity(num_1, num_2):
    try:
        kind_1 = BD.limit_kind(num_1)
        kind_2 = BD.limit_kind(num_2)


        kind_1.group_date()
        kind_2.group_date()
    
        t1 = kind_1.get_array_dates(in_zero=True)
        t2 = kind_2.get_array_dates(in_zero=True)
        t = np.array(list(set(t1) | set(t2)))
    
        t.sort()
    
        end = min(t1[-1], t2[-1])
        end_index,  = np.where(t == end)
        print(end_index)
        t = t[:end_index[0]]

        d1 = kind_1.get_array_column(COLUMN_DATA)
        d2 = kind_2.get_array_column(COLUMN_DATA)
    
        f1 = interp1d(t1, d1, kind='linear')
        f2 = interp1d(t2, d2, kind='linear')

        res = f1(t) - f2(t)
        amp = res.max()-res.min()

        delta = max(abs(d1.max()-d2.min()), abs(d1.min()-d2.max())) * DEVIATIONS
        return (amp, delta)
    except:
        return (1//DEVIATIONS + 1, 1)

