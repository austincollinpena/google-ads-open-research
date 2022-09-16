import pandas as pd
import os
from typing import Optional
from google_ads_api.arbitrary_query import arbitrary_google_ads_query
from dotenv import dotenv_values


def get_negatives() -> pd.DataFrame:
    config = dotenv_values(".env.sensitive")
    negatives_by_campaign = arbitrary_google_ads_query(
        account_id=config['account_id'],
        mcc_id=config['mcc_id'],
        select=['campaign.name', 'campaign_criterion.keyword.text', 'campaign.id',
                'campaign_criterion.keyword.match_type'],
        from_arg='campaign_criterion',
        where_argument="campaign_criterion.type = 'KEYWORD' AND campaign_criterion.negative = TRUE",
        order_by=None,
    )
    negative_lists_associated_with_a_campaign = arbitrary_google_ads_query(
        account_id=config['account_id'],
        mcc_id=config['mcc_id'],
        select=['campaign.id', 'campaign.name', 'shared_set.name', 'shared_set.id'],
        from_arg='shared_set',
        where_argument="shared_set.type = 'NEGATIVE_KEYWORDS'",
        order_by=None,
    )
    shared_set_ids = negative_lists_associated_with_a_campaign['shared_set.id'].unique().tolist()
    shared_set_id_str = ", ".join(str(e) for e in shared_set_ids)
    negative_keywords_in_lists = arbitrary_google_ads_query(
        account_id=config['account_id'],
        mcc_id=config['mcc_id'],
        select=['shared_criterion.keyword.text', 'shared_criterion.keyword.match_type', 'shared_set.id'],
        from_arg='shared_criterion',
        where_argument=f"shared_set.id IN ({shared_set_id_str})",
        order_by=None,
    )

    campaign_list_id_and_associated_neg_kws = pd.merge(negative_keywords_in_lists, negative_lists_associated_with_a_campaign, on='shared_set.id', how='left')

    campaign_list_id_and_associated_neg_kws['negative_keyword'] = campaign_list_id_and_associated_neg_kws['shared_criterion.keyword.text']
    negatives_by_campaign['negative_keyword'] = negatives_by_campaign['campaign_criterion.keyword.text']
    del negatives_by_campaign['campaign_criterion.keyword.text']
    del campaign_list_id_and_associated_neg_kws['shared_criterion.keyword.text']

    campaign_list_id_and_associated_neg_kws['match_type'] = campaign_list_id_and_associated_neg_kws['shared_criterion.keyword.match_type']
    negatives_by_campaign['match_type'] = negatives_by_campaign['campaign_criterion.keyword.match_type']
    del campaign_list_id_and_associated_neg_kws['shared_criterion.keyword.match_type']
    del negatives_by_campaign['campaign_criterion.keyword.match_type']

    all_campaign_negatives = pd.concat([negatives_by_campaign, campaign_list_id_and_associated_neg_kws])
    return all_campaign_negatives


if __name__ == "__main__":
    os.chdir("../")
    get_negatives()
