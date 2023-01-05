import pandas as pd
from typing import Optional
from google_ads_api.make_client import make_client
import os
from dotenv import dotenv_values
import hashlib
from os.path import exists

from python_code.google_ads_api.arbitrary_query import arbitrary_google_ads_query


def get_campaign_performance_by_conversion_action():
    config = dotenv_values(".env.sensitive")
    cost_data = arbitrary_google_ads_query(account_id=config['account_id'], mcc_id=config['mcc_id'],
                                           select=["metrics.cost_micros", "segments.date"],
                                           from_arg="campaign",
                                           where_argument="segments.date BETWEEN '2022-01-01' AND '2022-10-01'",
                                           order_by=None)

    cost_data = cost_data.groupby('segments.date').sum()
    cost_data.reset_index(inplace=True)

    conversion_data = arbitrary_google_ads_query(account_id=config['account_id'], mcc_id=config['mcc_id'],
                                                 select=["metrics.all_conversions", "conversion_action.name", "segments.date"],
                                                 from_arg="conversion_action",
                                                 where_argument="conversion_action.name = 'Sent [GCLID]' AND segments.date BETWEEN '2022-01-01' AND '2022-10-01'",
                                                 order_by=None)

    conversion_data['sent count'] = conversion_data['metrics.all_conversions']
    del conversion_data['metrics.all_conversions']

    # mql_data = arbitrary_google_ads_query(account_id=config['account_id'], mcc_id=config['mcc_id'],
    #                                       select=["metrics.all_conversions", "conversion_action.name", "segments.date"],
    #                                       from_arg="conversion_action",
    #                                       where_argument="conversion_action.name = 'MQL [GCLID]' AND segments.date BETWEEN '2022-01-01' AND '2022-10-01'",
    #                                       order_by=None)
    #
    # mql_data['mql count'] = mql_data['metrics.all_conversions']
    # del mql_data['metrics.all_conversions']

    merged = cost_data.merge(conversion_data, how='left', on='segments.date')
    merged.to_csv("./scratch_ignored/rolling_averages/git_ignored_data/by_conversion_action_name.csv")


if __name__ == "__main__":
    # all functions should run assuming the python_code/ folder as root
    os.chdir("../")
    get_campaign_performance_by_conversion_action()
