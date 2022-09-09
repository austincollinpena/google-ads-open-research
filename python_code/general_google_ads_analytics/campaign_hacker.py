import os

import cachetools
import pandas as pd

from google_ads_api.arbitrary_query import arbitrary_google_ads_query
from dotenv import dotenv_values
from bayesian_testing.experiments import BinaryDataTest
from general_google_ads_analytics.df_utils import add_divided_column, normalize_cost_micros, convert_impression_data
from statsmodels.stats.weightstats import ztest as ztest
from statsmodels.stats.weightstats import ttest_ind
from typing import Optional
import statistics

from typing import List


# TODO:
#
#
# device
# gender
# locations
# day
# hour
# age
# undefined vs defined

def run_bayes_test(time_series_df: pd.DataFrame, group_by_col: str, group_by_value: str, segment_column_name: str,
                   segment_name: str, analysis_column_name: str) -> float:
    """
    :param df: source dataframe that you can run queries on
    :param time_series_df: this enables us to get the individual values to run our z test
    :param group_by_col: the column, like campaign name, that you're testing the segment performance _against_. So you can test mobile performance against campaign as a whole
    :param group_by_value: the current groupby value. Like campaign name
    :param segment_column_name: the segment name, like "mobile" gives our bayes test a name
    :param segment_name: the segment name, like "mobile" gives our bayes test a name
    :param analysis_column_name: like "cpa" or "roas"
    :return: the bayesian probability of being better
    """
    # filter down to the groupby value, like a campaign name and segment name
    # for example, this might be comparing Campaign A mobile vs Campaign A without mobile

    # TODO: You can't just use ROAS or CPA because it's a proportion

    excluding_group_value = time_series_df[(time_series_df[group_by_col] == group_by_value) & (time_series_df[segment_column_name] != segment_name)]
    including_group_value = time_series_df[(time_series_df[group_by_col] == group_by_value) & (time_series_df[segment_column_name] == segment_name)]

    pvalue = calculate_t_test(excluding_group_value[analysis_column_name].values.tolist(), including_group_value[analysis_column_name].values.tolist())
    return pvalue


def calculate_bayes_test_results(v1_name: str, v1_totals: int, v1_positives: int, v2_name: str, v2_totals: int, v2_positives: int) -> int:
    bayes_test = BinaryDataTest()
    bayes_test.add_variant_data_agg(v1_name, v1_totals, v1_positives)
    bayes_test.add_variant_data_agg(v2_name, v2_totals, v2_positives)
    result = bayes_test.probabs_of_being_best(sim_count=20000, seed=52)
    return result[v2_name]


def calculate_proportions_z_test(v1_values: List[float], v2_values: List[float]) -> float:
    (test_statistic, p_value) = ztest(v1_values, v2_values)
    return p_value


def calculate_t_test(v1_values: List[float], v2_values: List[float]) -> float:
    if not v1_values or not v2_values:
        return 0
    v1_mean = statistics.mean(v1_values)
    v2_mean = statistics.mean(v2_values)

    (tstat, pvalue, df) = ttest_ind(v1_values, v2_values)

    if v2_mean > v1_mean:  # means the segment beats the average
        return 1 - pvalue

    return pvalue


def add_percent_better(df: pd.DataFrame, group_by_col: str, group_by_value: str, segment_column_name: str, segment_name: str, count_col: str, success_col: str) -> float:
    # TODO: use count and success col
    excluding_group_value = df[(df[group_by_col] == group_by_value) & (df[segment_column_name] != segment_name)]
    including_group_value = df[(df[group_by_col] == group_by_value) & (df[segment_column_name] == segment_name)]
    excluding_group_mean = statistics.mean(excluding_group_value[analysis_column_name].values.tolist())
    including_group_mean = statistics.mean(including_group_value[analysis_column_name].values.tolist())
    return 1 - (including_group_mean / excluding_group_mean)


def analyze_segment_performance_against_baseline_in_campaign(df: pd.DataFrame, time_series_df: pd.DataFrame, analysis_col_name: str, group_by_col: str,
                                                             segment_name: str) -> pd.DataFrame:
    df[f'{analysis_col_name}_likelihood_better'] = df.apply(lambda row: run_bayes_test(
        time_series_df=time_series_df,
        group_by_col=group_by_col,
        group_by_value=row[group_by_col],
        segment_name=row[segment_name],
        segment_column_name=segment_name,
        analysis_column_name=analysis_col_name
    ), axis=1)
    df[f'{analysis_col_name}_percent_better'] = df.apply(lambda row: add_percent_better(
        df=df,
        group_by_col=group_by_col,
        group_by_value=row[group_by_col],
        segment_name=row[segment_name],
        segment_column_name=segment_name,
        analysis_column_name=analysis_col_name
    ), axis=1)
    return df


def get_campaign_segments(filter_campaign: Optional[str], segment_names: Optional[List[str]] = None) -> pd.DataFrame:
    config = dotenv_values(".env.sensitive")

    if segment_names is None:
        segment_names = ['segments.device', 'segments.ad_network_type', 'segments.day_of_week', 'segments.hour']

    # Build the Google Ads base query
    metrics = ['metrics.clicks', 'campaign.name', 'metrics.conversions', 'metrics.impressions', 'metrics.all_conversions_value', 'metrics.cost_micros',
               'metrics.search_top_impression_share', 'segments.date', 'metrics.search_impression_share', 'metrics.search_absolute_top_impression_share']

    from_arg = 'campaign'
    where_arg = "segments.date BETWEEN '2022-01-01' AND '2022-06-01'"
    if filter_campaign:
        where_arg = f'segments.date BETWEEN "2022-01-01" AND "2022-06-01" AND campaign.name = "{filter_campaign}"'

    all_segment_df = pd.DataFrame()

    for segment in segment_names:
        metrics_including_segment = metrics + [segment]

        # Customize it for Device
        segment_time_series = arbitrary_google_ads_query(account_id=config['account_id'],
                                                         mcc_id=config['mcc_id'],
                                                         select=metrics_including_segment,
                                                         from_arg=from_arg,
                                                         where_argument=where_arg, order_by=None)

        segment_time_series = convert_impression_data(segment_time_series)

        segment_df = segment_time_series.groupby(by=["campaign.name", segment]).sum()
        segment_df.reset_index(inplace=True)

        # Add some analysis columns for both segmented_df and time_series_segmented_df
        segment_time_series = normalize_cost_micros(segment_time_series)
        segment_df = normalize_cost_micros(segment_df)

        segment_time_series = add_divided_column(segment_time_series, [
            {
                'divide_left': 'cost',
                'divide_right': 'metrics.conversions',
                'new_name': 'cpa'
            },
            {
                'divide_left': 'metrics.all_conversions_value',
                'divide_right': 'cost',
                'new_name': 'roas'
            },
        ])

        segment_df = add_divided_column(segment_df, [
            {
                'divide_left': 'cost',
                'divide_right': 'metrics.conversions',
                'new_name': 'cpa'
            },
            {
                'divide_left': 'metrics.all_conversions_value',
                'divide_right': 'cost',
                'new_name': 'roas'
            },
        ])

        segment_df = analyze_segment_performance_against_baseline_in_campaign(df=segment_df, time_series_df=segment_time_series,
                                                                              analysis_col_name="roas",
                                                                              group_by_col="campaign.name", segment_name=segment)

        segment_df['revenue_after_ad_spend'] = segment_df['metrics.all_conversions_value'] - segment_df['cost']
        segment_df['segment_value'] = segment_df[segment]
        segment_df['segment_name'] = segment
        del segment_df[segment]
        segment_df.sort_values(inplace=True, by=['campaign.name'])

        all_segment_df = pd.concat([all_segment_df, segment_df])

    return all_segment_df


def run_campaign_hacker():
    all_segment_df = get_campaign_segments("AP | Orlando | Locksmith Alpha")
    all_segment_df.head()
    all_segment_df.to_csv("./campaign-hacker.csv")
    return


if __name__ == "__main__":
    # all functions should run assuming the python_code/ folder as root
    os.chdir("../")
    run_campaign_hacker()
