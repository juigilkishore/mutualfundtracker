from datetime import datetime
import requests


class MutualFundAPI(object):
    """
    """
    def __init__(self, url):
        self.mf_api = url

    def get_current_nav(self):
        response = requests.get(self.mf_api)
        data = response.json()
        return data['data'][0]

    def get_nav(self, date=None):
        if not date:
            return self.get_current_nav()
        response = requests.get(self.mf_api)
        data = response.json()
        for d in data['data']:
            if d['date'] == date:
                return d


class FundHouse(object):
    """"""

    def __init__(self, **kwargs):
        self.fund_id = kwargs.get('fund_house_id')
        self.fund_name = kwargs.get('fund_house_name')


class Scheme(FundHouse):
    """"""

    def __init__(self, **kwargs):
        self.scheme_id = kwargs.pop('scheme_id')
        self.scheme_name = kwargs.pop('scheme_name')
        self.mf_api = kwargs.pop('scheme_api')
        super().__init__(**kwargs)


class MutualFund(Scheme):
    """"""

    def __init__(self, **kwargs):
        self.num_units = kwargs.pop('units')
        self.date_purchase = kwargs.pop('date_of_purchase')
        self.folio_number = kwargs.pop('folio')
        super().__init__(**kwargs)
        self._invested_value = None
        self._set_invested_value()

    def get_invested_value(self):
        return self._invested_value

    def get_mf_details_json(self):
        mf_details_json = {self.scheme_id: {
            "folio_number": self.folio_number, "date_of_purchase": self.date_purchase, "scheme_name": self.scheme_name,
            "fund_house_id": self.fund_id, "fund_house_name": self.fund_name}
        }
        return mf_details_json

    def _set_invested_value(self):
        mf_api = MutualFundAPI(self.mf_api)
        nav_on_investment = mf_api.get_nav(self.date_purchase)
        self._invested_value = float(nav_on_investment['nav']) * float(self.num_units)
        self._invested_value = round(self._invested_value, 2)


class Portfolio(object):
    """"""

    def __init__(self, *mf_list):
        self.num_investments = len(mf_list)
        self.mf_list = mf_list[0]
        self._portfolio_details = {}
        self._portfolio_invested_value = {}
        self._portfolio_key_list = []
        self._calculate_invested_value()

    def _calculate_invested_value(self):
        for mf in self.mf_list:
            mf_invested = mf.get_invested_value()
            _k = "{scheme_id}::{folio}".format(scheme_id=mf.scheme_id, folio=mf.folio_number)
            self._portfolio_details[_k] = mf
            self._portfolio_invested_value[_k] = round(mf_invested, 2)
            self._portfolio_key_list.append(_k)

    def get_total_invested_value(self):
        return self.get_invested_value()

    def get_total_current_value(self):
        return self.get_current_value()

    def get_invested_value(self, scheme_id=None, folio=None):
        # TODO: Add validation for scheme_id
        if scheme_id and folio:
            scheme_list = ["{scheme_id}::{folio}".format(scheme_id=scheme_id, folio=folio)]
            if scheme_list[0] not in self._portfolio_key_list:
                raise Exception("Invalid Folio {0} provided".format(folio))
        elif scheme_id:
            scheme_list = [k for k in self._portfolio_key_list if k.startswith(scheme_id)]
        else:
            scheme_list = self._portfolio_key_list
        total = 0.0
        for _k in scheme_list:
            total = total + self._portfolio_invested_value[_k]
        return total

    def get_current_value(self, scheme_id=None, folio=None):
        # TODO: Add validation for scheme_id
        nav_current = {'nav': None, 'date': datetime.today().strftime("%d-%m-%Y")}
        if scheme_id and folio:
            scheme_list = ["{scheme_id}::{folio}".format(scheme_id=scheme_id, folio=folio)]
            if scheme_list[0] not in self._portfolio_key_list:
                raise Exception("Invalid Folio {0} provided".format(folio))
        elif scheme_id:
            scheme_list = [k for k in self._portfolio_key_list if k.startswith(scheme_id)]
        else:
            scheme_list = self._portfolio_key_list
        total = 0.0
        for _k in scheme_list:
            mf = self._portfolio_details[_k]
            mf_api = MutualFundAPI(mf.mf_api)
            nav_current = mf_api.get_current_nav()
            total = total + float(nav_current['nav']) * float(mf.num_units)
        return round(total, 2), nav_current['date']

    def get_appreciated_value(self, scheme_id=None, folio=None):
        current_value = self.get_current_value(scheme_id=scheme_id, folio=folio)
        appreciaton = round(current_value[0] - self.get_invested_value(scheme_id=scheme_id, folio=folio), 2)
        return appreciaton, current_value[-1]

    def get_xirr(self, scheme_id=None, folio=None):
        pass

    def list_all_schemes(self):
        scheme_details_list = []
        for mf in self.mf_list:
            scheme_details_list.append(mf.get_mf_details_json())
        return scheme_details_list

    def get_investment_json(self, scheme_id=None, folio=None):
        investment = self.get_invested_value(scheme_id=scheme_id, folio=folio)
        market_value = self.get_current_value(scheme_id=scheme_id, folio=folio)
        appreciation = self.get_appreciated_value(scheme_id=scheme_id, folio=folio)
        scheme_id_list_full = []
        folio_id_list_full = []
        folio_id_list_partial = []
        for mf_dict in self.list_all_schemes():
            sid = list(mf_dict.keys())[0]
            _folio = list(mf_dict.values())[0]['folio_number']
            scheme_id_list_full.append(sid)
            folio_id_list_full.append(_folio)
            if scheme_id == sid and not folio:
                folio_id_list_partial.append(_folio)
        if scheme_id and folio:
            scheme_id_list = [scheme_id]
            folio_id_list = [folio]
        elif scheme_id:
            scheme_id_list = [scheme_id]
            folio_id_list = folio_id_list_partial
        else:
            scheme_id_list = scheme_id_list_full
            folio_id_list = folio_id_list_full

        return_json = {"total_investment": investment, "market_value": market_value[0], "date": market_value[1],
                       "appreciation": appreciation[0], "scheme_ids": scheme_id_list, "folios": folio_id_list}
        return return_json
