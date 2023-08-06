#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
This function generates random data by using Fuzzy Theory, especially based on small size samples.
The output random data are generated according to a specified or automatically selected membership function (given by the parameter "distribution").
The user should set the maximum and minimum values of the output random data (given by the parameters "max" and "min", repsectively)
The user should set the characteristic value of the output random data corresponding to the member degree of 1 (given by the parameter "unity")
and the parameter value when the membership degree is 1 as well as the upper and lower limits of the parameter can be set by the user.

The main function is getFuzzy(distribution, x, n, max, min, unity).
Input Parameters
distribution : type of distribution for calculating the memership function, should be 'Triangle','Normal','Trapezoid' or 'Auto' (which automatically selects the optimized distribution from the front 3 distributions)
x : input sample data, should be an array
n : number of the output random data
max : the maximum of the output random data
min : the minimum of the output random data
unity : the characterisitic value of the output random data, indicating the value corresponding to memership degree of 1


In case of any questions, please drop emails to cqian@buaa.edu.cn (Dr. C. Qian)
                                                                   
                                          Yuhang Li, Yutong Jiang, Haoxin Gu, Wenjuan Li and Cheng Qian*
                                        School of Reliability and Systems Engineering, Beihang University
                                                                        2022-2-12
'''

import math
import random
import numpy as np


def get_n(list):
    """
   Get the number of groups
   :param list:original sample data
   :param return:the number of groups
   """
    if len(list) <= 2:
        return 1
    if 2 < len(list) <= 5:
        return 2
    if len(list) >= 6:
        return len(list) // 3 + 1


def get_xi(n, min, fuzzylength):
    """
   Get the median of each interval
   :param n:the number of groups
   :param min:the min of 
   :param fuzzylength:the interval length
   :param return:the median of interval 
   """
    i = 1
    xn = []
    while i <= n:
        xn.append(min + fuzzylength / n * (i - 0.5))
        i = i + 1
    return xn


def get_ui(n, list, xn, fuzzylength):
    """
   Get the membership degree of each interval 
   :param n:the number of groups
   :param list:the number of groups
   :param xn:the median of interval 
   :param fuzzylength:the interval length
   :param return:Membership of the interval 
   """
    un = [0] * n
    for i in range(0, len(list)):
        for t in range(0,n):
         if list[i] < xn[t]-fuzzylength/n/2:   
            un[t-1]=un[t-1]+1
            break
         if t==n-1:
            un[t]=un[t]+1
            break
    max_n = max(un)
    for i in range(0, n):
        un[i] = un[i] / max_n
    return un


def fuzzylength(x, fmax, fmin):
    """
   Estimate the interval length from the original data
   :param x:original sample data
   :param fmax:The maximum value that has been set
   :param fmin:The minimum value that has been set
   :param return:the interval length
   """
    actual_max = max(x) + (max(x) - min(x)) / len(x)
    actual_min = min(x) - (max(x) - min(x)) / len(x)
    if fmax != -1000:
        actual_max = fmax
    if fmin == -1000:
        actual_min = fmin
    return actual_max - actual_min


def f_max(x, fmax):
    if fmax == -1000:
        return max(x) + (max(x) - min(x)) / len(x)
    else:
        return fmax


def f_min(x, fmin):
    if fmin == -1000:
        return min(x) - (max(x) - min(x)) / len(x)
    else:
        return fmin


def auto(x, xi, ui, n, minf, maxf, unity):
    """
   By comparing the residuals of various types of membership with the membership obtained through grouping, and judging which type of membership function to choose
   :param x:original sample data
   :param xi:the median of interval 
   :param ui:Membership of the interval 
   :param n:Number of generated numbers
   :param minf:The minimum value of the interval
   :param maxf:The maximum value of the interval
   :param return:Sampling by getting the distribution 
   """
    a, b = get_Trapezoid_c(x, maxf, minf)
    c = get_triangle_c(x, maxf, minf, unity)
    avg, std = get_normal(x, unity)
    panding1 = sum(math.pow(func_triangle(xi[i], c, minf, maxf) - ui[i], 2) for i in range(len(xi)))
    panding2 = sum(math.pow(func_normal(xi[i], avg, std) - ui[i], 2) for i in range(len(xi)))
    panding3 = sum(math.pow(func_Trapezoid(xi[i], a, b, minf, maxf) - ui[i], 2) for i in range(len(xi)))
    distri = min(panding1, panding2, panding3)
    if distri == panding1:
        distribution = 'Triangle'
    if distri == panding2:
        distribution = 'Normal'
    if distri == panding3:
        distribution = 'Trapezoid'
    return getFuzzy(distribution, x, n, maxf, minf, unity)


def get_triangle_c(x, fmax, fmin, unity):
    """
   Moment estimation method to obtain the c value of triangular distribution 
   :param x:original sample data
   :param fmax:The maximum value that has been set
   :param fmin:The minimum value that has been set
   :param unity:The value of membership is 1
   :param return:the c value of triangular distribution
   """
    if unity == -1000:
        return np.mean(x) * 3 - f_min(x, fmin) - f_max(x, fmax)
    else:
        return unity


def get_Trapezoid_c(x, fmax, fmin):
    """
   Find the dividing point of the trapezoidal membership function 
   :param x:original sample data
   :param fmax:The maximum value that has been set
   :param fmin:The minimum value that has been set
   :param return:the dividing point of the trapezoidal membership function 
   """
    maxf = f_max(x, fmax)
    minf = f_min(x, fmin)
    fuzzylength = maxf - minf
    if len(x) <= 4:
        a = maxf + fuzzylength / 4
        b = minf - fuzzylength / 4
    else:
        a = x[len(x) // 4-1] + (x[len(x) // 4 ] - x[len(x) // 4-1]) * (len(x) / 4 - len(x) // 4)
        b = x[len(x) * 3 // 4 - 2] + (x[len(x) * 3 // 4-1] - x[len(x) * 3 // 4 - 2]) * (len(x) * 3 / 4 - len(x) * 3 // 4)
    return a, b


def get_normal(x, unity):
    """
    Get the parameters of the normal membership function
    :param x:original sample data
    :param unity:The value of membership is 1
    :param return:the parameters of a normal membership function
    """
    if unity == -1000:
        return np.mean(x), np.std(x)
    else:
        return unity, np.std(x)


def func_triangle(x, c, min, max):
    """
   Obtain the membership degree of x in the triangular membership function
   :param x:original sample data
   :param c:c value of triangular distribution 
   :param min:Minimum value of triangle
   :param max:Maximum value of triangle
   :param return:Degree of membership of the value
   """
    if c <= x <= max:
        return (x - max) / (c - max)
    elif min <= x <= c:
        return (x - min) / (c - min)
    else:
        return 0


def func_Trapezoid(x, a, b, min, max):
    """
   Obtain the degree of membership of the trapezoidal membership function 
   :param x:value
   :param a :Left dividing point of trapezoid
   :param b :Right dividing point of trapezoid
   :param min :Minimum value of trapezoid
   :param max :Maximum value of trapezoid
   :param return :Degree of membership of the value
   """
    if min <= x <= a:
        return (x - min) / (a - min)
    elif a <= x <= b:
        return 1
    elif b <= x <= max:
        return (x - max) / (b - max)
    else:
        return 0


def func_normal(x, avg, sig):
    """
   Calculate the degree of membership belonging to the normal distribution
   :param x :value
   :param avg :average value
   :param sig :variance
   :param return :Degree of membership of the value
   """
    b = -(np.power(x - avg, 2) / 2 / np.power(sig, 2))
    return np.exp(b)


def FuzzySampling(x, distribution, n, min, max, unity):
    """
   Sampling function (acceptance rejection method) 
   :param x :original sample data
   :param distribution :Type of distribution 
   :param n :Number of generated numbers
   :param min :The minimum value of the interval
   :param max :The maximum value of the interval
   :param unity:The value of membership is 1
   :param return :Array of sampled values
   """
    size = int(1e+5)
    a = np.random.uniform(min, max, size)

    if distribution == 'Triangle':
        c = get_triangle_c(x, max, min, unity)
        s = 1 / ((max - min) / 2)
        t = [func_triangle(o, c, min, max) for o in a]

    if distribution == 'Normal':
        average, sigma = get_normal(x, unity)
        s = func_normal(average, average, sigma)
        t = [func_normal(h, average, sigma) for h in a]

    if distribution == 'Trapezoid':
        c, b = get_Trapezoid_c(x, max, min)
        t = [func_Trapezoid(h, c, b, min, max) for h in a]

    yangben = np.random.uniform(0, 1, size)
    FuzzySampling = a[yangben < t]  # Random numbers less than the sampling distribution value will be accepted
    FuzzySampling.sort()
    fuzzy = np.round(random.sample(list(FuzzySampling), n), 2)
    return fuzzy


def getFuzzy(distribution, x, n, max, min, unity):
    """
   Obtain and sample the membership image of the sample
   :param distribution:Type of distribution 
   :param x :original sample data
   :param n :Number of generated numbers
   :param max:The maximum value that has been set
   :param min:The minimum value that has been set
   :param unity:The value of membership is 1
   :param return :Array of sampled values
   """
    k = get_n(x)
    x.sort()
    fmin = f_min(x, min)
    fmax = f_max(x, max)
    fuzzylength = fmax - fmin
    if fmin == fmax:
        fuzzy = [fmin for _ in range(k)]
        return fuzzy
    elif distribution == 'Auto':
        xi = get_xi(k, fmin, fuzzylength)
        ui = get_ui(k, x, xi, fuzzylength)
        return auto(x, xi, ui, n, fmin, fmax, unity)
    fuzzy = FuzzySampling(x, distribution, n, fmin, fmax, unity)
    print('Distribution for the random data: ', distribution)
    print('Output sample: ', fuzzy)
    return fuzzy


if __name__ == '__main__':
    x = [10.2, 13.5, 11.6, 9.9, 10.7, 9.8, 11.5]
    distribution = 'Auto'
    n = 20
    fmax = -1000
    fmin = -1000
    unity = -1000
    getFuzzy(distribution, x, n, fmax, fmin, unity)
