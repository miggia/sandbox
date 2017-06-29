# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 2017

@author: AParmiggiani

This script loads and processes an Excel file containing test data acquired
with the Zwick-Roell TextExpert program.

Multiple test runs are first resampled, and averaged and finally plotted.

"""

import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
from matplotlib import pyplot as plt
plt.style.use('ggplot')

# load Excel file with pandas
xl = pd.ExcelFile("17-06-15_08mm_cable_traction_test.xlsx")
# initialize dat matrices list
dml = []
# maximum sample number, maximum x (deformation) value and rounding step
msn, mdv, rs = 0, 0.0, 100
# parse all sheets and get the maximum number of samples and deformation value
# while storing data in a list
for sheet in xl.sheet_names[3:]:
    df = xl.parse(sheet).values[2:]
    if len(df) > msn: msn = len(df)
    if df[0,-1] > mdv: mdv = df[0,-1]
    dml.append(df)

# create new list of x values. The number is rounded the the closest int with
# the rounding step value
xv = np.linspace(0.001,mdv,(msn + rs-1)//rs*rs)
# computation of cleaned data matrices with resampling data
cdm = []
for df in dml:
    f = interp1d(df[:,0], df[:,1], bounds_error = False)
    cdm.append(f(xv))

## hand tweaking of data
# removing flawed experimental data
cdm.pop(4)
cdm.pop(2)
# casting list as array
cdm = np.asarray(cdm,dtype = 'float64')
# last plot element (extracted by hand)
lpe = 905
# computation of average behaviour, and standard deviation
mv, sv = np.nanmean(cdm[:,:lpe], axis=0), np.nanstd(cdm[:,:lpe], axis=0)

## plotting 
# select plot color
c = 'C1'
plt.fill_between(xv[:lpe], mv-sv, mv+sv, 
                 color = c, alpha = 0.25, label = 'std. dev')
plt.plot(xv[:lpe],mv, color = c, linewidth=2, label = 'average')
for df in cdm:
    plt.plot(xv,df, color = c, linewidth = 0.5, alpha = 0.5)
# legend and labels
plt.legend()
plt.xlabel('deformation [mm]')
plt.ylabel('force [N]')