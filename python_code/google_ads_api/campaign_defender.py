import pandas as pd
import os
from typing import Optional
from google_ads_api.arbitrary_query import arbitrary_google_ads_query
from dotenv import dotenv_values


def campaign_defender() -> pd.DataFrame:
    config = dotenv_values(".env.sensitive")
    all_search_terms = arbitrary_google_ads_query(
        account_id=config['account_id'],
        mcc_id=config['mcc_id'],
        select=['search_term_view.search_term', 'campaign.name', 'ad_group.name'],
        from_arg='search_term_view',
        where_argument=None,
        order_by=None,
    )
    all_search_terms.to_csv("./scratch_ignored/ssd_account_perf/search_terms.csv")
    return all_search_terms


if __name__ == "__main__":
    os.chdir("../")
    campaign_defender()
