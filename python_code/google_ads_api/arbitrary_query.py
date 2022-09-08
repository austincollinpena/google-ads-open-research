import pandas as pd
from typing import Optional
from google_ads_api.make_client import make_client
import os
from dotenv import dotenv_values


def create_where_string(where_argument: Optional[str]) -> Optional[str]:
    if where_argument is None:
        return ""
    return f'WHERE {where_argument}'


def create_order_by_string(order_by: Optional[str]) -> Optional[str]:
    if order_by is None:
        return ""
    return f'ORDER BY {order_by}'


def arbitrary_google_ads_query(account_id: str, mcc_id: Optional[str], select: list[str], from_arg: str, where_argument: Optional[str],
                               order_by: Optional[str]) -> Optional[pd.DataFrame]:
    """
    :param account_id: the ID of the Google account you're requesting. Format 12345678
    :param mcc_id: if you only have access to this account through your MCC, pass through your MCC ID
    :param select: what you are selecting from here: https://developers.google.com/google-ads/api/docs/query/overview
    :param from_arg: List of resources found here: https://developers.google.com/google-ads/api/reference/rpc/v11/Campaign
    :param where_argument: Filter your query. Pass through a condition like "metrics.clicks > 2"
    :param order_by: Order your query. Pass through an argument like "metrics.clicks DESC"
    :return: returns a dataframe with your "select" terms as the column names
    """

    query = f'SELECT ' + \
            f'{", ".join(select)} ' + \
            f'FROM {from_arg} ' + \
            f'{create_where_string(where_argument)} ' + \
            f'{create_order_by_string(order_by)} '

    client = make_client(mcc_id)
    ga_service = client.get_service("GoogleAdsService")
    # Issues a search request using streaming.
    search_request = client.get_type("SearchGoogleAdsStreamRequest")
    # Set the account ID
    search_request.customer_id = account_id
    # Set the query to the search_request
    search_request.query = query
    # Create the stream
    stream = ga_service.search_stream(search_request)

    result_dict = []

    for batch in stream:
        for row in batch.results:

            result = {}
            for criteria in select:
                # the row is not subscriptable so we need to use getattr for dynamic queries
                first_level_key = criteria.split(".")[0]
                second_level_key = criteria.split(".")[1]
                row_attribute = getattr(row, first_level_key)
                value_attribute = getattr(row_attribute, second_level_key)
                if hasattr(value_attribute, 'name'):
                    value_attribute = getattr(value_attribute, 'name')

                result[criteria] = value_attribute
            result_dict.append(result)

    if not result_dict:
        return None

    return pd.DataFrame(result_dict)


if __name__ == "__main__":
    # all functions should run assuming the python_code/ folder as root
    os.chdir("../")
    config = dotenv_values(".env.sensitive")
    df = arbitrary_google_ads_query(account_id=config['account_id'], mcc_id=config['mcc_id'], select=["search_term_view.search_term", "metrics.clicks", "campaign.name"],
                                    from_arg="search_term_view",
                                    where_argument="metrics.clicks > 100",
                                    order_by=None)
    print(df)
