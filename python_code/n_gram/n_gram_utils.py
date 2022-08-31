import nltk
import ray
import unicodedata
import re
import pandas as pd


def basic_clean(text):
    """
    A simple function to clean up the data. All the words that
    are not designated as a stop word is then lemmatized after
    encoding and basic regex parsing are performed.
    """
    # wnl = nltk.stem.WordNetLemmatizer()
    # stopwords = nltk.corpus.stopwords.words('english')
    text = (unicodedata.normalize('NFKD', text)
            .encode('ascii', 'ignore')
            .decode('utf-8', 'ignore')
            .lower())
    words = re.sub(r'[^\w\s]', '', text).split()
    return words
    # don't remove stop words
    # return [wnl.lemmatize(word) for word in words if word not in stopwords]



# Commit 9a1c5a409ef1aba5446c80d18487b811fdd873b2 shows how to use ray for multiprocessing
# message is "parallel ray"

@ray.remote
def create_dataframe_of_ngram_stats_positive_and_negative(all_search_term_data_dict, all_search_term_data_dict_efficient, gram_vecs, df_columns, campaign_name):
    # get stats from the n gram (all_grams[campaign_name] gets the n grams)
    dict_with_ngram_stats = create_dataframe_of_ngram_stats(all_search_term_data_dict, gram_vecs)
    dict_with_ngram_stats_efficient = create_dataframe_of_ngram_stats(all_search_term_data_dict_efficient, gram_vecs)

    # create the dataframes
    ngram_analysis_from_search_terms = pd.DataFrame.from_dict(dict_with_ngram_stats, orient='index', columns=df_columns)
    ngram_analysis_from_search_terms = ngram_analysis_from_search_terms.reset_index().rename(columns={'index': 'Search term'})

    ngram_analysis_from_search_terms_efficient = pd.DataFrame.from_dict(dict_with_ngram_stats_efficient, orient='index', columns=df_columns)
    ngram_analysis_from_search_terms_efficient = ngram_analysis_from_search_terms_efficient.reset_index().rename(columns={'index': 'Search term'})

    # merge the dataframes
    merged = ngram_analysis_from_search_terms.merge(ngram_analysis_from_search_terms_efficient, left_on='Search term', right_on='Search term', how='left',
                                                    suffixes=['', '_efficient'])

    merged.set_index('Search term', inplace=True)
    merged['campaign'] = campaign_name
    return merged


# Takes in a dictionary of the n gram dataframe and all the gram vecotrs
# also takes in more_efficient_search_term_data_dict (which can be empty) that shows the outcome if low ROAS
# items are excluded
#
def create_dataframe_of_ngram_stats(all_search_term_data_dict, gram_vecs):
    # This is where everything is held:
    gram_dict_with_values = {}

    # loop through all the grams
    for search_term_row in all_search_term_data_dict:
        # loop through the dict and see if the gram is found in the data
        # If it's found the first time
        for gram in gram_vecs:
            if search_term_row['Search term'] == gram or gram + " " in search_term_row['Search term'] or " " + gram in \
                    search_term_row['Search term']:

                # First iteration add to the object

                # TODO: Need to get the matching record from the more_efficient_search_term_data_dict

                if gram not in gram_dict_with_values.keys():
                    gram_dict_with_values[gram] = {
                        'count': 1,
                        'Impr.': search_term_row['Impr.'],
                        'Clicks': search_term_row['Clicks'],
                        'Cost': search_term_row['Cost'],
                        'Conversions': search_term_row['Conversions'],
                        'Conv. value': search_term_row['Conv. value'],
                        'top_impressions': search_term_row['Impr.'] * search_term_row['Impr. (Top) %'],
                        'abs_top_impressions': search_term_row['Impr.'] * search_term_row['Impr. (Abs. Top) %']
                    }

                # other times
                else:
                    gram_dict_with_values[gram]['count'] += 1
                    gram_dict_with_values[gram]['Impr.'] += search_term_row['Impr.']
                    gram_dict_with_values[gram]['Clicks'] += search_term_row['Clicks']
                    gram_dict_with_values[gram]['Cost'] += search_term_row['Cost']
                    gram_dict_with_values[gram]['Conv. value'] += search_term_row['Conv. value']
                    gram_dict_with_values[gram]['Conversions'] += search_term_row['Conversions']
                    gram_dict_with_values[gram]['top_impressions'] += (
                            search_term_row['Impr.'] * search_term_row['Impr. (Top) %'])
                    gram_dict_with_values[gram]['abs_top_impressions'] += (
                            search_term_row['Impr.'] * search_term_row['Impr. (Abs. Top) %'])

    return gram_dict_with_values
