import os

import cachetools
import pandas as pd

from google_ads_api.arbitrary_query import arbitrary_google_ads_query
from dotenv import dotenv_values
from bayesian_testing.experiments import BinaryDataTest
from general_google_ads_analytics.df_utils import add_divided_column, normalize_cost_micros
import statsmodels.api as sm

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

def run_bayes_test(df: pd.DataFrame, group_by_col: str, group_by_value: str, totals_col_name: str, positive_col_name: str, segment_column_name: str, segment_name: str,
                   total_segment_val: int,
                   positive_segment_val: int) -> float:
    """
    :param df: source dataframe that you can run queries on
    :param group_by_col: the column, like campaign name, that you're testing the segment performance _against_. So you can test mobile performance against campaign as a whole
    :param group_by_value: the current groupby value. Like campaign name
    :param totals_col_name: the column that holds the total value. So for example if you want to see CPA difference, you need to have cost as the total
    :param positive_col_name: the column that shows positives. For example, conversions would go with cost
        :param segment_column_name: the segment name, like "mobile" gives our bayes test a name

    :param segment_name: the segment name, like "mobile" gives our bayes test a name
    :param total_segment_val: the total value of the segment, like cost
    :param positive_segment_val: the positives of the segment, like conversions
    :return: the bayesian probability of being better
    """
    # filter down to the groupby value, like a campaign name
    only_group_by_value = df[(df[group_by_col] == group_by_value) & (df[segment_column_name] != segment_name)]
    # get the sum
    groupby_sum = only_group_by_value.groupby(group_by_col).sum()
    z_test_result = calculate_proportions_z_test(v1_total=groupby_sum[totals_col_name][0], v1_success=groupby_sum[positive_col_name][0], v2_total=total_segment_val,
                                                 v2_success=positive_segment_val)
    return z_test_result


def calculate_bayes_test_results(v1_name: str, v1_totals: int, v1_positives: int, v2_name: str, v2_totals: int, v2_positives: int) -> int:
    bayes_test = BinaryDataTest()
    bayes_test.add_variant_data_agg(v1_name, v1_totals, v1_positives)
    bayes_test.add_variant_data_agg(v2_name, v2_totals, v2_positives)
    result = bayes_test.probabs_of_being_best(sim_count=20000, seed=52)
    return result[v2_name]


def calculate_proportions_z_test(v1_total: int, v1_success: int, v2_total: int, v2_success: int) -> float:
    if 0 in [v1_total, v1_success, v2_success, v2_total]:
        return 0
    (ztest_value, pscore) = sm.stats.proportions_ztest(count=[v1_success, v2_success],
                                                       nobs=[v1_total, v2_total])
    return pscore


def analyze_segment_performance_against_baseline_in_campaign(df: pd.DataFrame, totals_col_name: str, positive_col_name: str, group_by_col: str, segment_name: str) -> pd.DataFrame:
    df[f'{positive_col_name}_better'] = df.apply(lambda row: run_bayes_test(
        df=df,
        group_by_col=group_by_col,
        group_by_value=row[group_by_col],
        totals_col_name=totals_col_name,
        positive_col_name=positive_col_name,
        segment_name=segment_name,
        total_segment_val=row[totals_col_name],
        positive_segment_val=row[positive_col_name],
        segment_column_name=segment_name,
    ), axis=1)
    return df


if __name__ == "__main__":
    # all functions should run assuming the python_code/ folder as root
    os.chdir("../")
    config = dotenv_values(".env.sensitive")
    metrics = ['metrics.clicks', 'campaign.name', 'metrics.conversions', 'metrics.impressions', 'metrics.all_conversions_value', 'metrics.cost_micros',
               'metrics.search_top_impression_share',
               'metrics.search_absolute_top_impression_share']
    from_arg = 'campaign'
    where_arg = "segments.date BETWEEN '2022-01-01' AND '2022-06-01'"

    device_metrics = metrics + ["segments.device"]

    device_df = arbitrary_google_ads_query(account_id=config['account_id'],
                                           mcc_id=config['mcc_id'],
                                           select=device_metrics,
                                           from_arg=from_arg,
                                           where_argument=where_arg, order_by=None)
    device_df = normalize_cost_micros(device_df)

    device_df = add_divided_column(device_df, [
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

    device_df = analyze_segment_performance_against_baseline_in_campaign(device_df, totals_col_name="metrics.clicks", positive_col_name="cpa",
                                                                         group_by_col="campaign.name", segment_name="segments.device")

    device_df.sort_values(inplace=True, by=['campaign.name'])

    print(device_df)

    try:
        print("hello world")
    except Exception as e:
        print(e)
