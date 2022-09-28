import logging

import pandas as pd
import os
import time

from n_gram.save_multiple_dataframes_into_excel_doc import save_multiple_dataframes_into_excel_doc, save_multiple_dataframes_into_excel_pd_native, \
    save_multiple_dataframes_into_excel_pyexcelerate
from typing import List
from pandarallel import pandarallel
from send_mailgun.send_email import send_email

from interface_with_gcp.cloud_storage.get_file import generate_signed_url_for_object


def p2f(x):
    if x == " --" or x == "--":
        return 0
    return float(x.strip('%')) / 100


# prepare_data reads the csv document and returns with the correct columns
def prepare_data(data_for_analysis: str, filter_on_roas: bool) -> pd.DataFrame:
    search_term_data = pd.read_csv(data_for_analysis, thousands=",", converters={'Impr. (Top) %': p2f, 'Impr. (Abs. Top) %': p2f})

    if filter_on_roas:
        columns = ['Search term', 'Campaign', 'Ad group', 'Clicks', 'Impr.', 'Cost', 'Conversions', 'Conv. value', 'Impr. (Top) %', 'Impr. (Abs. Top) %']
        search_term_data = search_term_data[columns]
        search_term_data.dropna(subset=['Impr.'], inplace=True)
    else:
        columns = ['Search term', 'Campaign', 'Ad group', 'Clicks', 'Impr.', 'Cost', 'Conversions', 'Impr. (Top) %', 'Impr. (Abs. Top) %']
        search_term_data = search_term_data[columns]
        search_term_data.dropna(subset=['Impr.'], inplace=True)
        search_term_data['Conv. value'] = 0
    print(f'processing {len(search_term_data.index)} rows')
    return search_term_data


# create_negatived_frame makes a dataframe copy with low ROAS terms removed
def create_efficient_dataframe(roas_or_cpa_target: float, search_term_data: pd.DataFrame, filter_on_roas=True, ) -> pd.DataFrame:
    """
    :param roas_or_cpa_target: sets the target to filter
    :param search_term_data: dataframe of search term data
    :param filter_on_roas: boolean for if the person wants to filter on roas or
    :return: pd.Dataframe that's more efficient
    """
    if filter_on_roas:
        search_term_data = search_term_data.sort_values(by='Cost', ascending=False)
        search_term_data['roas'] = search_term_data['Conv. value'] / search_term_data['Cost']
        low_value_search_terms_excluded = search_term_data[search_term_data['roas'] > roas_or_cpa_target]
        return low_value_search_terms_excluded
    else:
        search_term_data['cpa'] = search_term_data['Cost'] / search_term_data['Conversions']
        low_value_search_terms_excluded = search_term_data[search_term_data['cpa'] < roas_or_cpa_target]
        return low_value_search_terms_excluded


# On a dataset with 1.2 million search terms using parallel (unsurprisingly) reduced processing time from 98.6539 to 26 seconds

def vector_generate_exploded_grams_parallel(df: pd.DataFrame) -> pd.DataFrame:
    from nltk.util import everygrams
    from nltk import word_tokenize
    if len(df.index) > 5000:
        pandarallel.initialize(use_memory_fs=False)
        from nltk import word_tokenize
        from nltk.util import everygrams
        df = df.copy(deep=True)
        df['n_gram'] = df['Search term'] \
            .str.replace(",", "", regex=False) \
            .str.replace(".", "", regex=False) \
            .str.replace("!", "", regex=False) \
            .str.replace("?", "", regex=False) \
            .str.replace(":", "", regex=False) \
            .parallel_apply(
            lambda x: list(map(" ".join, everygrams(word_tokenize(x), max_len=6)))
        )
    else:
        df = df.copy(deep=True)
        df['n_gram'] = df['Search term'] \
            .str.replace(",", "", regex=False) \
            .str.replace(".", "", regex=False) \
            .str.replace("!", "", regex=False) \
            .str.replace("?", "", regex=False) \
            .str.replace(":", "", regex=False) \
            .apply(
            lambda x: list(map(" ".join, everygrams(word_tokenize(x), max_len=6)))
        )

    return df.explode('n_gram')


def vector_generate_exploded_grams(df: pd.DataFrame) -> pd.DataFrame:
    from nltk import word_tokenize
    from nltk.util import everygrams
    df = df.copy(deep=True)
    df['n_gram'] = df['Search term'] \
        .str.replace(",", "", regex=False) \
        .str.replace(".", "", regex=False) \
        .str.replace("!", "", regex=False) \
        .str.replace("?", "", regex=False) \
        .str.replace(":", "", regex=False) \
        .apply(
        lambda x: list(map(" ".join, everygrams(word_tokenize(x), max_len=6)))
    )
    return df.explode('n_gram')


def group_campaign_level_data(df: pd.DataFrame) -> pd.DataFrame:
    campaign_grouped = group_df_on_grams(df,
                                         ['n_gram', 'Campaign'])
    return campaign_grouped


def group_df_on_grams(df: pd.DataFrame, group_on_columns: list) -> pd.DataFrame:
    return df.groupby(group_on_columns, as_index=False).agg(
        Clicks=("Clicks", "sum"),
        conversion_value=("Conv. value", "sum"),
        conversions=("Conversions", "sum"),
        cost=("Cost", "sum"),
        impressions=("Impr.", "sum"),
        n_gram_count=("n_gram", "count")
    )


def generate_dataframe_list(split_on_one: str, split_on_two: str, df: pd.DataFrame) -> list[pd.DataFrame]:
    """
    :param split_on: list of keys to split on
    :param df: master dataframe
    :return: list of dataframes
    """
    list_of_dfs: List[pd.DataFrame] = []
    split_one_values = df[split_on_one].unique()
    split_two_values = df[split_on_two].unique()
    for split_one in split_one_values:
        for split_two in split_two_values:
            filtered_df = df[(df[split_on_one] == split_one) & (df[split_on_two] == split_two)]
            if filtered_df.empty:
                continue
            list_of_dfs.append(filtered_df)

    return list_of_dfs


def vector_n_grams_cloud_functions(roas_target: float, filter_on_roas: bool, data_for_analysis: str, email: str, save_locally: bool):
    try:
        tic = time.perf_counter()

        # Generate data for all of the terms
        search_term_data = prepare_data(data_for_analysis, filter_on_roas)
        exploded_ngram_dataframe = vector_generate_exploded_grams(search_term_data)

        campaign_grouped = group_campaign_level_data(exploded_ngram_dataframe)

        # generate data for efficient terms
        effecient_search_term_data = create_efficient_dataframe(roas_target, search_term_data, filter_on_roas)

        exploded_efficient_ngram_dataframe = vector_generate_exploded_grams(effecient_search_term_data)

        campaign_grouped_efficient = group_campaign_level_data(exploded_efficient_ngram_dataframe)

        merged = campaign_grouped.merge(campaign_grouped_efficient,
                                        left_on=['n_gram', 'Campaign'],
                                        right_on=['n_gram', 'Campaign'],
                                        how='left',
                                        suffixes=['', '_efficient'])
        merged['gram_count'] = merged['n_gram'].str.count(" ") + 1

        merged.sort_values(by=['cost'], inplace=True, ascending=False)
        toc = time.perf_counter()
        print(f"Finished ngrams in {toc - tic:0.4f} seconds")
        individual_dfs = generate_dataframe_list('Campaign', 'gram_count', merged)

        excelerate = time.perf_counter()
        file_name = save_multiple_dataframes_into_excel_pyexcelerate(individual_dfs, save_locally=save_locally, account_name=email)
        excelerate_end = time.perf_counter()
        print(f'excelerate wrote pdf and uploaded file in: {excelerate_end - excelerate:0.4f} seconds')

        pre_signed_url = generate_signed_url_for_object("access-cloud-storage-buckets", "temporary-ads-data-storage", file_name)

        if not save_locally:
            send_email(email, "Your N Gram Analysis Is Ready",
                       f'Here is the link: {pre_signed_url}\n\nIt will expire in 24 hours so please download it now.\n\nRespond to this email for to give feedback')

        if save_locally:
            pd.set_option('display.width', 800)
            pd.options.display.max_rows = 50
            pd.set_option('display.max_columns', 15)
            print(merged.head(50))
            return
        toc = time.perf_counter()
        print(f"Finished saving after {toc - tic:0.4f} seconds")

    except Exception as e:

        print(e)
        logging.exception(e)
        if not save_locally:
            send_email(email, "Your N Gram Analysis Error Failed", "We're not sure what happened yet, but we're investigating.")
            send_email("me@austinpena.com", f'Your N Gram Analysis Error Failed For {email}', repr(e))


if __name__ == "__main__":
    os.chdir("../")
    vector_n_grams_cloud_functions(10, True, "./n_gram/git_ignored_data/mgaman.csv", "me@austinpena.com", True)
