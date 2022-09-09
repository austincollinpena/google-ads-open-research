import os
from general_google_ads_analytics.campaign_hacker import calculate_proportions_z_test


# TODO: measure by time series for each observation?
# And then measure revenue after ad spend?

if __name__ == "__main__":
    # all functions should run assuming the python_code/ folder as root
    os.chdir("../")
    z_test_result = calculate_proportions_z_test(v1_total=groupby_sum[totals_col_name][0], v1_success=groupby_sum[positive_col_name][0], v2_total=total_segment_val,
                                                 v2_success=positive_segment_val)
