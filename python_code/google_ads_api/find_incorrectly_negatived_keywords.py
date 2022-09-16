import os

import pandas as pd

from google_ads_api.get_negatives import get_negatives
from google_ads_api.arbitrary_query import arbitrary_google_ads_query
from dotenv import dotenv_values


def get_improper_negatives():
    negatives = get_negatives()
    config = dotenv_values(".env.sensitive")
    search_terms_over_threshold = arbitrary_google_ads_query(
        account_id=config['account_id'],
        mcc_id=config['mcc_id'],
        select=['segments.keyword.info.text', 'campaign.name', 'search_term_view.search_term', 'metrics.clicks', 'metrics.cost_micros', 'metrics.impressions',
                'metrics.conversions'],
        from_arg='search_term_view',
        where_argument="metrics.conversions > 0",
        order_by=None,
    )
    negatives['search_term'] = negatives['search_term'].str.lower
    improperly_negatived_keywords = pd.DataFrame()
    for row in negatives.itertuples():
        neg_keyword = str(row.negative_keyword)
        match_type = str(row.match_type)
        campaign = str(row[1])
        keyword_list = str(row[6])
        excluded_keywords = None
        if match_type == 'EXACT':
            excluded_keywords = search_terms_over_threshold[
                (search_terms_over_threshold['search_term_view.search_term'] == neg_keyword)
                &
                (search_terms_over_threshold['campaign.name'] == campaign)
                ].copy(deep=True)

        if match_type == 'PHRASE':
            excluded_keywords = search_terms_over_threshold[
                (search_terms_over_threshold['search_term_view.search_term'].str.contains(neg_keyword))
                &
                (search_terms_over_threshold['campaign.name'] == campaign)
                ].copy(deep=True)

        if match_type == 'BROAD':
            broad_keyword_components = neg_keyword.split(" ")
            regex_string = [f'(?=.*\\b{word}\\b)' for word in broad_keyword_components]
            regex_string = r"".join(regex_string)
            regex_string = regex_string + ".*"
            excluded_keywords = search_terms_over_threshold[
                (search_terms_over_threshold['search_term_view.search_term'].str.contains(regex_string, regex=True))
                &
                (search_terms_over_threshold['campaign.name'] == campaign)
                ].copy(deep=True)

        if excluded_keywords is None or excluded_keywords.empty:
            continue
        excluded_keywords['negative_keyword'] = neg_keyword
        excluded_keywords['keyword_list'] = keyword_list
        improperly_negatived_keywords = pd.concat([improperly_negatived_keywords, excluded_keywords])

    print(search_terms_over_threshold)


if __name__ == "__main__":
    os.chdir("../")
    get_improper_negatives()
