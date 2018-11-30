# -*- coding: utf-8 -*-
"""
Created on Fri Dec 29 16:29:11 2017

@author: ariahKlages-Mundt

Note: follows http://scikit-learn.org/stable/auto_examples/covariance/plot_sparse_cov.html
"""

import numpy as np
from scipy import linalg
from sklearn.covariance import GraphLassoCV, ledoit_wolf
import matplotlib.pyplot as plt


pct_df = combined_df.pct_change()

#filter out NaN rows
data = pct_df.dropna(axis = 0)

# normalize data for relationship estimation
data = data - data.mean()
data /= data.std()

# Sparse Inverse Covariance Estimation
model = GraphLassoCV(max_iter=2000)
model.fit(data)
cov_ = model.covariance_
prec_ = model.precision_

# Compare with Ledoit wolf
lw_cov_, _ = ledoit_wolf(data)
lw_prec_ = linalg.inv(lw_cov_)

#form partial correlation matrix
n = len(prec_)
bayes_net = np.zeros((n,n))
for i in range(n):
    for j in range(n):
        if i == j:
            continue
        else:
            bayes_net[i,j] = -prec_[i,j]/np.sqrt(prec_[i,i]*prec_[j,j])