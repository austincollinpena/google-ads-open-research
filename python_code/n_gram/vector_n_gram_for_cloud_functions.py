import logging

import pandas as pd
import os
import time
from nltk import word_tokenize
from nltk.util import everygrams
from python_code.n_gram.save_multiple_dataframes_into_excel_doc import save_multiple_dataframes_into_excel_doc
from typing import List
from interface_with_gcp.cloud_storage.upload_file import upload_file


def p2f(x):
    if x == " --":
        return 0
    return float(x.strip('%')) / 100


# prepare_data reads the csv document and returns with the correct columns
def prepare_data(data_for_analysis: str) -> pd.DataFrame:
    search_term_data = pd.read_csv(data_for_analysis, thousands=",", converters={'Impr. (Top) %': p2f, 'Impr. (Abs. Top) %': p2f})
    columns = ['Search term', 'Campaign', 'Ad group', 'Clicks', 'Impr.', 'Cost', 'Conversions', 'Conv. value', 'Impr. (Top) %', 'Impr. (Abs. Top) %']
    search_term_data = search_term_data[columns]
    search_term_data.dropna(subset=['Impr.'], inplace=True)
    return search_term_data


# create_negatived_frame makes a dataframe copy with low ROAS terms removed
def create_efficient_dataframe(roas_or_cpa_target: int, search_term_data: pd.DataFrame, filter_on_roas=True, ) -> pd.DataFrame:
    """
    :param roas_or_cpa_target: sets the target to filter
    :param search_term_data: dataframe of search term data
    :param filter_on_roas: boolean for if the person wants to filter on roas or
    :return: pd.Dataframe that's more efficient
    """
    if filter_on_roas:
        search_term_data['roas'] = search_term_data['Conv. value'] / search_term_data['Cost']
        low_value_search_terms_excluded = search_term_data[search_term_data['roas'] > roas_or_cpa_target]
        return low_value_search_terms_excluded
    else:
        search_term_data['cpa'] = search_term_data['Conversions'] / search_term_data['Cost']
        low_value_search_terms_excluded = search_term_data[search_term_data['cpa'] > roas_or_cpa_target]
        return low_value_search_terms_excluded


def vector_generate_exploded_grams(df: pd.DataFrame) -> pd.DataFrame:
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


def vector_n_grams_cloud_functions(roas_target, data_for_analysis, account_name, save_locally):
    try:

        tic = time.perf_counter()
        # Generate data for all of the terms
        search_term_data = prepare_data(data_for_analysis)
        exploded_ngram_dataframe = vector_generate_exploded_grams(search_term_data)
        campaign_grouped = group_campaign_level_data(exploded_ngram_dataframe)

        # generate data for efficient terms
        effecient_search_term_data = create_efficient_dataframe(roas_target, search_term_data)

        exploded_efficient_ngram_dataframe = vector_generate_exploded_grams(effecient_search_term_data)

        campaign_grouped_efficient = group_campaign_level_data(exploded_efficient_ngram_dataframe)

        merged = campaign_grouped.merge(campaign_grouped_efficient,
                                        left_on=['n_gram', 'Campaign'],
                                        right_on=['n_gram', 'Campaign'],
                                        how='left',
                                        suffixes=['', '_efficient'])
        merged['gram_count'] = merged['n_gram'].str.count(" ") + 1

        merged.sort_values(by=['cost'], inplace=True, ascending=False)

        individual_dfs = generate_dataframe_list('Campaign', 'gram_count', merged)

        temp_file = save_multiple_dataframes_into_excel_doc(individual_dfs, save_locally=save_locally, account_name=account_name)
        if save_locally:
            pd.set_option('display.width', 800)
            pd.options.display.max_rows = 50
            pd.set_option('display.max_columns', 15)
            print(merged.head(50))
            return
        upload_file(temp_file.name, temp_file, 'access-cloud-storage-buckets', 'temporary-ads-data-storage')
        toc = time.perf_counter()
        print(f"Finished in {toc - tic:0.4f} seconds")

    except Exception as e:
        print(e)
        logging.exception(e)


if __name__ == "__main__":
    os.chdir("../")
    vector_n_grams_cloud_functions(2.2, "./n_gram/git_ignored_data/search_terms_6-1_8-31.csv", "prolock-7_05", True)
