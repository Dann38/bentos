import numpy as np
from scipy.optimize import least_squares

START_NUMBER = 3
LIMIT_POPULATION = 500
GROWNTH_RATE = 0.001

def func_log(t, grownth_rate):
    limit_population = LIMIT_POPULATION
    start_number = START_NUMBER
    
    exponent = np.exp(grownth_rate*t)
    numerator = limit_population * start_number * exponent
    denumerator = limit_population + start_number * (exponent - 1)
    result = numerator / denumerator
    return result

def func_log_opt(params, t, f):
    grownth_rate = params[0]
    result = func_log(t, grownth_rate)
    return f - result


def get_grownth_rate(t_points, info):
    res = least_squares(func_log_opt, [GROWNTH_RATE], args=(t_points, info))
    print(res)
    return res.x[0]


def approximation(t_points, info):
    array1 = np.array([info[0]])
    t_array1 = np.array([t_points[0]])

    array2 = np.array([])
    t_array2 = np.array([])
    i = 0
    while (i < (len(t_points)-2)):
        a = ((t_points[i]-t_points[i+1])/t_points[-1]*45)**2 + (info[i]-info[i+1])**2
        b = ((t_points[i]-t_points[i+2])/t_points[-1]*45)**2 + (info[i]-info[i+2])**2
        if a < b:
            array1 = np.append(array1, info[i+1])
            t_array1 = np.append(t_array1, t_points[i+1])            
            
            array2 = np.append(array2, info[i+2])
            t_array2 = np.append(t_array2, t_points[i+2])
            i += 1
        else:
            array2 = np.append(array2, info[i+1])
            t_array2 = np.append(t_array2, t_points[i+1])
            
            array1 = np.append(array1, info[i+2])
            t_array1 = np.append(t_array1, t_points[i+2])
            i += 2

    return t_array1, array1
