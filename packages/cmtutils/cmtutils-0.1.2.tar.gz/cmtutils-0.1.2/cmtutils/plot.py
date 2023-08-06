import datetime as dt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cmtutils.nipsy as nipsy

import scipy

three_figsize = (10, 3)
two_figsize = (10, 5)
one_figsize = (5, 5)
big_figsize = (7, 7)
wide_figsize = (7, 3.5)
big_wide_figsize = (10, 6)


def deadlines(ax):
    "Plot the deadlines for the different reviewing stages"
    for event in nipsy.events.keys():
        plt.axvline(nipsy.events[event])
    ylim = ax.get_ylim()
    yval = ylim[0] + (ylim[1]-ylim[0])/2
    for key, val in nipsy.events.items():
        ax.text(val, yval, key.replace("_", " "), rotation=90 )

def evolving_statistic(reviews, column, window=4, ax=None):
    "Plot a particular review statistic mean as it evolves over time."
    first_entered = reviews.sort_values(by='LastUpdated', ascending=False).drop_duplicates(subset=['ID', 'Email'],keep='last').sort_values(by='LastUpdated')

    df = pd.DataFrame(index=nipsy.review_date_range, columns=[column + ' mean',
                                                        column + ' std',
                                                        'Number of Reviews'])
    for date in nipsy.review_date_range:
        indices = (first_entered.LastUpdated<date+dt.timedelta(window/2.)) & (first_entered.LastUpdated>date-dt.timedelta(window/2.))
        df['Number of Reviews'][date] = indices.sum()
        if indices.sum()>2:
            df[column + ' mean'][date] = first_entered[column][indices].mean()
            df[column + ' std'][date] = 2*np.sqrt(first_entered[column][indices].var()/indices.sum())
        else:
            df[column + ' mean'][date] = np.NaN
    df[column + ' mean'].plot(yerr=df[column + ' std'], ax=ax)
    deadlines(ax)

    return ax
    #indices = (reviews.LastUpdated<events['reviews'])

def late_early(cat1, cat2, column, ylim, ax=None):
    """Plot late and early statistics for different reviewer scores."""
    print("On time reviewers", column + ":", cat1.mean(), '+/-', 2*np.sqrt(cat1.var()/cat1.count()))
    print("Chased reviewers", column + ":", cat2.mean(), '+/-', 2*np.sqrt(cat2.var()/cat2.count()))
    
    if ax is None:
        fig, ax = plt.subplots()
    ax.bar([0.6, 1.6],
           [cat1.mean(), cat2.mean()],
           color ='y', width = 0.8,
           yerr=[2*np.sqrt(cat1.var()/cat1.count()), 2*np.sqrt(cat2.var()/cat2.count())])
    ax.set_ylim(ylim[0], ylim[1])
    ax.set_title('Mean ' + column + ' for Reviews')
    ax.set_xticks([1, 2])
    ax.set_xticklabels(['On time reviews', 'Late Reviews'])
    from scipy.stats import ttest_ind
    vals = ttest_ind(cat1, cat2)
    print("t-statistic is", vals[0], "and p-value is", vals[1])


def log_one_citations(column, decisions, filt=None, ax=None):
    if ax is None:
        fig, ax = plt.subplots(figsize=big_wide_figsize)
    full_index = pd.Series(data=False, index=decisions.index)
    for ind, symbol in zip(
            [decisions.accept, decisions.reject_not_arxiv, decisions.reject_arxiv],
            ['gs', 'g^', 'bv']
            ):
        if filt is not None:
            index = (filt & ind)
        else:
            index = ind
        full_index = (index | full_index)
        xvals = decisions.loc[index][column]
        xvals += scipy.stats.laplace.rvs(scale=0.2, loc=0, size=xvals.shape)
        yvals = np.log10(1+decisions.loc[index]['numCitedBy'])
        yvals += scipy.stats.laplace.rvs(scale=0.1, loc=0, size=yvals.shape)
        ax.plot(xvals, yvals, symbol)
    ax.set_xlabel(column.replace("_", " "))
    ax.set_ylabel(r"log10(1+citations)")
    ax.set_xticks([])
    ax.set_yticks([])
    cor = decisions.loc[full_index][column].corr(np.log(1+decisions.loc[full_index]['numCitedBy']))
    ax.set_title("correlation: {cor:.2g}".format(cor=cor))
    return ax

def citation_correlation(joindf, column, numvals=100, ax=None):
    corrdf = joindf.loc[joindf.published]
    minval = corrdf["average_calibrated_quality"].min()
    maxval = corrdf["average_calibrated_quality"].max()
    threshrange = np.linspace(minval, maxval, numvals)
    corvals1 = np.zeros(threshrange.shape)
    corvals2 = np.zeros(threshrange.shape)
    for i, thresh in enumerate(threshrange):
        corvals1[i] = corrdf.loc[corrdf.average_calibrated_quality>thresh][column].corr(np.log(1+corrdf.loc[corrdf.average_calibrated_quality>thresh]['numCitedBy']))
        corvals2[i] = corrdf.loc[corrdf.average_calibrated_quality<thresh][column].corr(np.log(1+corrdf.loc[corrdf.average_calibrated_quality<thresh]['numCitedBy']))

    if ax is None:
        fig, ax = plt.subplots(figsize=big_wide_figsize)
    ax.plot(threshrange, corvals1, 'k-', linewidth=3)
    ax.plot(threshrange, corvals2, 'k--', linewidth=3)
    ax.axhline(0)
    ax.set_xlabel("quality threshold")
    ax.set_ylabel("correlation")
    ax.set_title("correlation between citations and " + column.replace("_", " "))
    return ax

def num_accepts(joindf, numvals=100, ax=None):
    corrdf = joindf.loc[((joindf.published) & (~joindf.numCitedBy.isna()))]
    minval = corrdf["average_calibrated_quality"].min()
    maxval = corrdf["average_calibrated_quality"].max()
    threshrange = np.linspace(minval, maxval, numvals)
    numpapers = np.zeros(threshrange.shape)
    for i, thresh in enumerate(threshrange):
        numpapers[i] = corrdf.loc[corrdf.average_calibrated_quality>thresh]['paper_title'].count()
    if ax is None:
        fig, ax = plt.subplots(figsize=big_wide_figsize)
    ax.plot(threshrange, numpapers, 'k-', linewidth=3)
    ax.axhline(414)
    ax.set_xlabel("quality threshold")
    ax.set_ylabel("number of papers")
    return ax
