import pandas as pd
from WeightedCorr import WeightedCorr
import numpy as np

# Helps filter so the loop in the future is much smaller
def get_top_n(df: pd.DataFrame, merge_on: str, max_results: int, sort_by: str) -> list[str]:
    df = df[[merge_on, sort_by]]
    df_merged = df.groupby([merge_on], as_index=False).sum()
    df_merged = df_merged.sort_values(by=[sort_by], ascending=False)
    return df_merged[merge_on].unique().tolist()[:max_results]

def merge_performance_auction_data(performance: pd.DataFrame, auction: pd.DataFrame) -> pd.DataFrame:
    merged_data = pd.merge(left=performance, right=auction, on=['Day', 'Ad group ID', 'Keyword ID'])
    merged_data['ctr'] = merged_data['Clicks'] / merged_data['Impr.']
    merged_data['cpa'] = merged_data['Cost'] / merged_data['Conversions']
    merged_data['overlap_impressions'] = merged_data['Search overlap rate'] * merged_data['Impr.']
    merged_data.set_index('Day')
    merged_data.fillna(0)
    return merged_data.reindex(sorted(merged_data.columns), axis=1)


def get_corr_data(df: pd.DataFrame, filter_keys: list[str], key_name: str, metric: str,
                        col_names_to_keep: list[str]) -> pd.DataFrame:
    """
    :param df: The merged dataframe with all of the data including auction insights and performance
    :param get_keys: a function, usually get_top_n() to get the list of keys for the analysis
    :param key_name: like Ad group ID
    :param metric: like CTR or CPA
    :param col_names_to_keep: When merging on the key_name after getting the correlation data, add these columns to the final dataframe. Like campaign name and ad group name
    :return:
    """
    corr_df = run_correlation(df, filter_keys, key_name, metric)
    named_corr_df = add_name_back_to_df(corr_df, df, 'id', key_name, col_names_to_keep)
    if metric == 'ctr':
        by_impact = sort_by_impact(named_corr_df, 'search_overlap_rate_correlation_weighted', 'overlap_impressions',
                                   100, True)
    else:
        by_impact = sort_by_impact(named_corr_df, 'search_overlap_rate_correlation_weighted', 'overlap_impressions',
                                   100, False)
    return by_impact


# run correlation compares domain impact on ad group level performance
def run_correlation(df: pd.DataFrame, identifier_list: list[str], identifier_key: str, metric: str) -> pd.DataFrame:
    df = df[[identifier_key, metric, 'Search overlap rate', 'Position above rate', 'Impr.', 'overlap_impressions',
             'Display URL domain']]
    df = df[df[identifier_key].isin(identifier_list)]
    df = df[(df['overlap_impressions'] != 0)]

    if metric == 'cpa':
        df = df.replace([np.inf, -np.inf], np.nan)
        df = df.dropna(how='all')

    filtered_df = df.groupby(by=['Display URL domain', identifier_key]).filter(lambda x: len(x) > 10)
    groups = filtered_df.groupby(by=['Display URL domain', identifier_key])
    corr_df = groups.apply(lambda x: pd.Series({
        'display_url_domain': x['Display URL domain'].iloc[0],
        'id': x[identifier_key].iloc[0],
        'search_overlap_rate_correlation_weighted': WeightedCorr(x=x['Search overlap rate'], y=x[metric],
                                                                 w=x['Impr.'])(),
        'overlap_impressions': x['overlap_impressions'].sum()
    }))
    # corr_df = pd.DataFrame(result_list)
    corr_df = corr_df.reset_index(drop=True)
    return corr_df.sort_values(by=['overlap_impressions'], ascending=False)


def add_name_back_to_df(corr_df: pd.DataFrame, full_df: pd.DataFrame, left_on: str, right_on: str,
                        col_name_to_keep: list[str]) -> pd.DataFrame:
    full_df = full_df.drop('overlap_impressions', axis=1)
    full_df = full_df[[right_on, *col_name_to_keep]].drop_duplicates()
    joined_df = pd.merge(corr_df, full_df, how='left', left_on=left_on, right_on=right_on)
    # corr_df.join(full_df, on=key, how='left')
    cols = corr_df.columns
    cols = [*cols, *col_name_to_keep]
    return joined_df[cols][:1000]


# Sort By Impact creates a dataframe where the impact is multiplied by the overlap impressions
def sort_by_impact(df: pd.DataFrame, impact_col_name: str, weight_col_name: str, nrows: int,
                   higher_is_better: bool) -> pd.DataFrame:
    df['effect'] = df[impact_col_name] * df[weight_col_name]
    if higher_is_better:
        return df.sort_values(by=['effect'])[:nrows]
    else:
        return df.sort_values(by=['effect'], ascending=False)[:nrows]
