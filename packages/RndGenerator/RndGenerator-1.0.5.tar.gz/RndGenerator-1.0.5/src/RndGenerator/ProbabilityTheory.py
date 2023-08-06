#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
This function generates random data by using the maximum likelihood method.
The output random data is assumed to follow a distribution by either user input or automatically determined.

The main function is getProbability(x, distribution, n).
Input Parameters
x : original sample data,should be an array
distribution : distribution of the output random data, should be 'Normal' , 'Weibull' , 'Expon' , 'LogNorm' or 'Auto' (which automatically selects the optimized distribution from the front 4 distributions)
n : number of the output random data


In case of any questions, please drop emails to cqian@buaa.edu.cn (Dr. C. Qian)
                                                                   
                                          Yutong Jiang, Yuhang Li, Haoxin Gu, Wenjuan Li and Cheng Qian*
                                        School of Reliability and Systems Engineering, Beihang University
                                                                        2022-2-12
'''

import random
import numpy as np
import scipy.stats as stats
import math


def ProbabilityAuto(x, n):
    """
    Choose the best distribution form according to AIC
    :param x:original sample data
    :param n:number of data required
    :return: sample data generated under the chosen distribution
    """
    param1 = ProbabilityParam(x, 'Normal')
    AICNorm = 2*2 - 2*sum(stats.norm.logpdf(x, param1[0], param1[1]))
    param2 = ProbabilityParam(x, 'LogNorm')
    AICLogNorm = 2*2 - 2 * sum(stats.lognorm.logpdf(x, param2[0], param2[1], param2[2]))
    param3 = ProbabilityParam(x, 'Weibull')
    AICWeibull = 2*2 - 2 * sum(stats.exponweib.logpdf(x, 1, param3[1], loc=0, scale=param3[3]))
    param4 = ProbabilityParam(x, 'Expon')
    AICExpon = 2*2 - 2*sum(stats.expon.logpdf(x, scale=param4[1]))
    minAIC = min(AICNorm, AICLogNorm, AICWeibull, AICExpon)
    if minAIC == AICNorm:
        distribution = 'Normal'
    if minAIC == AICLogNorm:
        distribution = 'LogNorm'
    if minAIC == AICWeibull:
        distribution = 'Weibull'
    if minAIC == AICExpon:
        distribution = 'Expon'

    return getProbability(x, distribution, n)


def ProbabilitySampling(x, distribution, n):
    """
    Sampling Algorithm
    :param x:original sample data
    :param distribution:distribution used in the MLE method,should be 'Uniform', 'Normal' , 'Weibull' , 'Expon' or 'LogNorm'
    :param n:number of data required
    :return:new data sample generated
    """
    min = np.min(x)
    max = np.max(x)
    if min == max:
        return [min for _ in range(n)]

    if distribution == 'Uniform':
        return [np.round(random.uniform(min, max), 2)for _ in range(n)]

    if distribution == 'Normal':
        param = ProbabilityParam(x, 'Normal')
        return [np.round(random.normalvariate(param[0], param[1]), 2)for _ in range(n)]

    if distribution == 'LogNorm':
        s, loc, scale = ProbabilityParam(x, 'LogNorm')
        return [np.round(random.lognormvariate(math.log(scale), s), 2)for _ in range(n)]

    if distribution == 'Weibull':
        param = ProbabilityParam(x, 'Weibull')
        return [np.round(random.weibullvariate(param[3], param[1]), 2)for _ in range(n)]

    if distribution == 'Expon':
        param = ProbabilityParam(x, 'Expon')
        return [np.round(random.expovariate(1/param[1]), 2)for _ in range(n)]


def ProbabilityParam(x, distribution):
    """
    Parametric Fitting Function
    :param x:original sample data
    :param distribution:distribution used in the MLE method,should be 'Normal' , 'Weibull' , 'Expon' or 'LogNorm'
    :return:fitted parameter values
    """
    if distribution == 'Normal':
        return [np.mean(x), np.std(x)]

    if distribution == 'LogNorm':
        s, loc, scale = stats.lognorm.fit(x, floc=0)
        return [s, loc, scale]

    if distribution == 'Weibull':
        WeibullParam = stats.exponweib.fit(x, floc=0, f0=1)
        return WeibullParam

    if distribution == 'Expon':
        ExponParam = stats.expon.fit(x, floc=0)
        return ExponParam


def getProbability(x, distribution, n):
    """
    Main function, calculate and print the result.
    :param x: original sample data
    :param distribution: distribution used in the MLE method,should be 'Normal' , 'Weibull' , 'Expon' , 'LogNorm' or 'Auto'
    :param n: number of data required
    :return: new data sample generated
    """
    if distribution == 'Auto':
        return ProbabilityAuto(x, n)

    print('Distribution for the random data: ', distribution)
    print('Output sample: ', ProbabilitySampling(x, distribution, n))
    return ProbabilitySampling(x, distribution, n)


if __name__ == '__main__':
    x = [77.05, 36.8, 114.07, 46.35, 44.41,
         35.1, 92.01, 197.42, 76.82, 16.95, 18.5]
    distribution = 'Auto'
    n = 11
    getProbability(x, distribution, n)
