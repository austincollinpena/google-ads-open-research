import pandas as pd
from comp_analysis.utils import merge_performance_auction_data, get_corr_data, get_top_n


def clean_percents(row):
    if '< 10' in row:
        return .1
    if row == " --":
        return 0
    return float(row.rstrip('%')) / 100

def load_csv(file_name: str, clean_percent_names: list[str]) -> pd.DataFrame:
    converter = {key: clean_percents for (key) in clean_percent_names}
    return pd.read_csv(file_name, converters=converter, thousands=",", parse_dates=["Day"])

def run_comp_analysis(performance_data_csv: str, auction_data_csv: str):
    performance_data_df = load_csv(performance_data_csv, ['Search overlap rate', 'Position above rate', 'Top of page rate', 'Search outranking share', 'Abs. Top of page rate', 'Search Impr. share (Auction Insights)'])
    auction_data_df = load_csv(auction_data_csv, ['Search overlap rate', 'Position above rate', 'Top of page rate', 'Search outranking share', 'Abs. Top of page rate', 'Search Impr. share (Auction Insights)'])
    merged_data = merge_performance_auction_data(performance_data_df, auction_data_df)
    ad_group_ctr = get_corr_data(
        df=merged_data,
        filter_keys=get_top_n(merged_data, 'Ad group ID', 10, 'Cost'),
        key_name='Ad group ID',
        metric='ctr',
        col_names_to_keep=['Campaign_x', 'Ad group_x'],
    )
    ad_group_cpa = get_corr_data(
        df=merged_data,
        filter_keys=get_top_n(merged_data, 'Ad group ID', 10, 'Cost'),
        key_name='Ad group ID',
        metric='cpa',
        col_names_to_keep=['Campaign_x', 'Ad group_x'],
    )
    ad_group_ctr.to_csv("../git_ignored_data/ad_group_ctr.csv")
    ad_group_cpa.to_csv("../git_ignored_data/ad_group_cpa.csv")


if __name__ == '__main__':
    run_comp_analysis("../git_ignored_data/perf.csv", "../git_ignored_data/auction.csv")