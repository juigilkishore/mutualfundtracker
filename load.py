import yaml

import mapper
import manager


# load the funds from the lumpsum.yml

with open('lumpsum.yml.sample', 'r') as fyml:
    fund_config = yaml.load(fyml, Loader=yaml.FullLoader)

INVESTMENTS = []

for fund_house_id, fund_scheme_list in fund_config.items():
    for scheme_info in fund_scheme_list:
        scheme_id = list(scheme_info.keys())[0]
        scheme_details_yaml = scheme_info[scheme_id]
        scheme_details_api = mapper.get_scheme_details(fund_house_id, scheme_id)
        scheme_details = {**scheme_details_yaml, **scheme_details_api}
        scheme = manager.MutualFund(**scheme_details)
        INVESTMENTS.append(scheme)

portfolio = manager.Portfolio(INVESTMENTS)
