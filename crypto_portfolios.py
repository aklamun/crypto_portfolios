# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 16:55:04 2018

@author: ariahKlages-Mundt
"""

def cluster_returns(cluster, pct_df):
    #note this fn treats NaN as not part of average
    pct_df = pd.DataFrame(pct_df)
    return pct_df[cluster].mean(axis=1)

def portfolio_returns(clusters, pct_df):
    rets = pd.DataFrame(index=pct_df.index)
    for clus in clusters:
        ind = clusters.index(clus)
        rets[ind] = cluster_returns(clus, pct_df)
    return rets.mean(axis=1)

def cum_returns(rets, start_amount):
    data = rets.dropna()
    crets = [start_amount]
    for ret in data:
        nxt = crets[-1]*(1+ret)
        crets.append(nxt)
    return pd.Series(crets[1:], index=data.index)

eq_wt_rets = portfolio_returns([pct_df.columns], pct_df)
eq_wt_crets = cum_returns(eq_wt_rets, 100)
BTC_rets = portfolio_returns([['BTC']], pct_df)
BTC_crets = cum_returns(BTC_rets, 100)
clustered_rets = portfolio_returns(partitions_tick, pct_df)
clustered_crets = cum_returns(clustered_rets, 100)