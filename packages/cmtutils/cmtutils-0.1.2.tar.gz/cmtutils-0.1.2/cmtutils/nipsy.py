# Utility functions for processing NIPS reviews.
import datetime as dt
import pandas as pd
import numpy as np
import requests
import os

from cmtutils.config import *

# Date of different review events.
events = {}
# Time stamps from CMT are on separate time? If so add here
offset = dt.timedelta(hours=0)
events['reviews'] = dt.datetime(2014, 7, 21, 23, 59) + offset
events['rebuttal_start'] = dt.datetime(2014, 8, 3, 23, 59) + offset
events['rebuttal_ends'] = dt.datetime(2014, 8, 11, 23, 59) + offset
events['start_teleconference'] = dt.datetime(2014, 8, 19, 23, 59) +offset
events['decisions_despatched'] = dt.datetime(2014, 9, 5, 23, 59) + offset

# Date range across which we have review information.
review_date_range = pd.date_range('2014/07/01', periods=72, freq='D')
review_store = os.path.expandvars(config.get('review data', 'directory'))
review_file = os.path.expandvars(config.get('review data', 'file'))
final_decisions_file = os.path.expandvars(config.get('review data', 'final_decisions'))
outlet_name_mapping = os.path.expandvars(config.get('review data', 'outlet_name_mapping'))

def load_semantic_ids():
    """Load in the semantic scholar ids."""
    id = pd.read_excel(os.path.join(review_store,
                                    final_decisions_file), 
                       sheet_name="Semantic Impact", 
                       converters={"ID" : int})
    return id.set_index(id['ID'].apply(str))

def load_decisions():
    """Load in the final decisions ids."""
    decisions = pd.read_excel(os.path.join(review_store,
                                    final_decisions_file), 
                       sheet_name="Final Decisions", 
                       converters={"index" : int})
    return decisions.set_index(decisions['index'].apply(str))

def load_citation_counts(date="2021-06-11"):
    """Load in the semantic scholar citation counts stored in a given date."""
    return pd.read_pickle(os.path.join(review_store,
                                       date+'-semantic-scholar-cites.pickle'))

def augment_decisions(decisions):
    """Add some useful column to the decisions data frame."""
    def avg_vals(vals):
        if type(vals) is not str:
            return np.NaN

        lvals = vals.split(",")
        return np.mean([float(val) for val in lvals])
    col_list = ['quality', 'impact', 'calibrated_quality', 'confidence']
    for col in col_list:
        decisions['average_' + col] = decisions[col].apply(avg_vals)
    decisions['accept'] = ((decisions.Status=="Poster") | (decisions.Status=="Spotlight") | (decisions.Status=="Oral"))
    decisions['reject'] = (decisions.Status=="Reject")
    decisions['all'] = pd.Series(data=True, index=decisions.index)
        
def join_decisions_citations(decisions, citations):
    joindf = decisions.join(citations)
    # Set papers with no venue but with ArXiv ID as having ArXiv venue
    joindf.loc[(joindf.venue=='') & (~pd.isna(joindf.arxivId)),'venue'] = "ArXiv"
    joindf.loc[(joindf.venue==''),'venue'] = "None"
    joindf['reject_not_arxiv'] = ((joindf.Status=="Reject") & (joindf.venue != "ArXiv") & (joindf.venue != "None"))
    joindf['reject_arxiv'] = ((joindf.Status=="Reject") & (joindf.venue == "ArXiv"))
    joindf['published'] = ((joindf.accept) | (joindf.reject_not_arxiv))
    return joindf

def get_scholar(url, timeout):
    """Get paper information from semantic scholar"""
    r = requests.get(url, timeout=timeout)

    if r.status_code == 200:
        data = r.json()
        if len(data) == 1 and 'error' in data:
            data = {}
        return data
    elif r.status_code == 429:
        raise requests.exceptions.ConnectionRefusedError('HTTP status 429 Too Many Requests.')

def download_citation_counts(citations_dict = None, semantic_ids = None, timeout=20):
    """Download citation counts from semantic scholar."""
    key_missing = []
    if citations_dict is None:
        citations_dict = {}

    if semantic_ids is None:
        semantic_impact = load_semantic_impact()
        
    paper_semantic = {}
    for index, s2crid in semantic_ids['S2CRID'].items():
        if s2crid != "?" and not np.isnan(s2crid):
            paper_semantic[str(index)] = str(s2crid)        

    for key in paper_semantic:
        if key not in citations_dict or citations_dict[key] == {} or citations_dict[key] is None:
            try:
                citations_dict[key] = get_scholar('https://api.semanticscholar.org/v1/paper/CorpusID:'+paper_semantic[key].strip(), timeout=timeout)
                if citations_dict[key] != {} and citations_dict[key] is not None:
                    print("Added key ", key, " of ID ", paper_semantic[key])
                else:
                    print("Failed to add ", key, " of ID ", paper_semantic[key])
                    key_missing.append(key)
            except requests.exceptions.ReadTimeout as e:
                key_missing.append(key)
                print("Read time out for key ", key)

    for key in paper_semantic:
        if key in citations_dict:
            if citations_dict[key] == {} or citations_dict[key] is None:
                del citations_dict[key]
    return citations_dict
        

        
def load_review_history():
    """Load in the history of the NIPS reviews."""

    # return load of pickled reviews.
    return pd.io.pickle.read_pickle(os.path.join(review_store, review_file))

def reviews_before(reviews, date):
    "Give a review snapshot of reviews before a certain date."
    indices = (((reviews.LastUpdated<=date) & (reviews.LastSeen>date))
               | ((reviews.LastUpdated<=date) & (reviews.LastSeen.isnull())))
    return reviews[indices].sort_values(by='LastUpdated').drop_duplicates(subset=['Email', 'ID'], keep='last')

def reviews_status(reviews, datetime, column=None):
    """Give a snapshot of the reviews at any given time. Use multi-index across ID
    and Email"""

    if column is not None:
        return reviews_before(reviews, datetime).set_index(['ID', 'Email'])[column].sort_index()
    else:
        return reviews_before(reviews, datetime).set_index(['ID', 'Email']).sort_index()





def late_early_values(reviews, column):
    "Compute a statistic for late reviews and a statistic for early reviews"
    first_entered = reviews.sort_values(by='LastUpdated', ascending=False).drop_duplicates(subset=['ID', 'Email'],keep='last').sort_values(by='LastUpdated')
    cat1 = first_entered[column][first_entered.LastUpdated<events['reviews']]
    cat2 = first_entered[column][(first_entered.LastUpdated>events['reviews'])& (first_entered.LastUpdated < events['rebuttal_start'])]

    return cat1, cat2


# def top_papers(reviews):
#     """Compute the top review levels."""
#     for date in review_date_range:
        
