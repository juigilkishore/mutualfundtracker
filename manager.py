from datetime import datetime
import requests
from uuid import uuid1


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
        self._invested_value = round(float(kwargs.pop('amount')), 2)
        self.date_purchase = kwargs.pop('date_of_purchase')
        self.folio_number = kwargs.pop('folio')
        super().__init__(**kwargs)
        self.num_units = "0"
        self.mf_uuid = str(uuid1()).split('-')[0]
        self._set_num_of_units()

    def get_invested_value(self):
        return self._invested_value

    def get_mf_details_json(self):
        mf_details_json = {self.scheme_id: {
            "folio_number": self.folio_number, "date_of_purchase": self.date_purchase, "scheme_name": self.scheme_name,
            "fund_house_id": self.fund_id, "fund_house_name": self.fund_name}
        }
        return mf_details_json

    def _set_num_of_units(self):
        mf_api = MutualFundAPI(self.mf_api)
        nav_on_investment = mf_api.get_nav(self.date_purchase)
        self.num_units = round(float(self._invested_value) / float(nav_on_investment['nav']), 3)


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
            _k = "{scheme_id}::{mf_uuid}::{folio}".format(
                scheme_id=mf.scheme_id, mf_uuid=mf.mf_uuid, folio=mf.folio_number)
            self._portfolio_details[_k] = mf
            self._portfolio_invested_value[_k] = round(mf_invested, 2)
            self._portfolio_key_list.append(_k)

    def get_total_invested_value(self):
        return self.get_invested_value()

    def get_total_current_value(self):
        return self.get_current_value()

    def get_invested_value(self, scheme_id=None, folio=None):
        # TODO: Add validation for scheme_id and folio
        if scheme_id and folio:
            scheme_list = [k for k in self._portfolio_key_list if k.startswith(scheme_id) and k.endswith(folio)]
        elif scheme_id and not folio:
            scheme_list = [k for k in self._portfolio_key_list if k.startswith(scheme_id)]
        elif not scheme_id and folio:
            scheme_list = [k for k in self._portfolio_key_list if k.endswith(folio)]
        else:
            scheme_list = self._portfolio_key_list
        total = 0.0
        for _k in scheme_list:
            total = total + self._portfolio_invested_value[_k]
        return total

    def get_current_value(self, scheme_id=None, folio=None):
        # TODO: Add validation for scheme_id and folio
        nav_current = {'nav': None, 'date': datetime.today().strftime("%d-%m-%Y")}
        if scheme_id and folio:
            scheme_list = [k for k in self._portfolio_key_list if k.startswith(scheme_id) and k.endswith(folio)]
        elif scheme_id and not folio:
            scheme_list = [k for k in self._portfolio_key_list if k.startswith(scheme_id)]
        elif not scheme_id and folio:
            scheme_list = [k for k in self._portfolio_key_list if k.endswith(folio)]
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
        current_value, current_value_on = self.get_current_value(scheme_id=scheme_id, folio=folio)
        appreciation = round(current_value - self.get_invested_value(scheme_id=scheme_id, folio=folio), 2)
        return appreciation, current_value_on

    @staticmethod
    def _date_dt_obj(date):
        (dd, mm, yyyy) = date.split('-')
        return datetime(int(yyyy), int(mm), int(dd))

    def _get_cagr(self, scheme_id, folio):
        current_value, current_date = self.get_current_value(scheme_id=scheme_id, folio=folio)
        invested_value = self.get_invested_value(scheme_id=scheme_id, folio=folio)
        _k = "{scheme_id}::{folio}".format(scheme_id=scheme_id, folio=folio)
        date_purchase = self._portfolio_details[_k].date_purchase

        holding_period_obj = self._date_dt_obj(current_date) - self._date_dt_obj(date_purchase)
        holding_period_years = holding_period_obj.days / 365.0

        raise Exception("NOT IMPLEMENTED")
        # return round((((current_value/invested_value)**(1/holding_period_years)) - 1) * 100.0, 2)

    def list_all_schemes(self, scheme_id=None, folio=None):
        scheme_details_list = []
        for mf in self.mf_list:
            mf_details = mf.get_mf_details_json()
            if scheme_id and folio:
                if scheme_id == list(mf_details.keys())[0] and folio == list(mf_details.values())[0]['folio_number']:
                    scheme_details_list.append(mf_details)
            elif scheme_id and not folio:
                if scheme_id == list(mf_details.keys())[0]:
                    scheme_details_list.append(mf_details)
            elif not scheme_id and folio:
                if folio == list(mf_details.values())[0]['folio_number']:
                    scheme_details_list.append(mf_details)
            else:
                scheme_details_list.append(mf_details)
        return scheme_details_list

    def get_investment_json(self, scheme_id=None, folio=None):
        investment = self.get_invested_value(scheme_id=scheme_id, folio=folio)
        market_value, market_value_on = self.get_current_value(scheme_id=scheme_id, folio=folio)
        appreciation, _ = self.get_appreciated_value(scheme_id=scheme_id, folio=folio)
        interest = round(((appreciation/investment) * 100.0), 2)

        meta_data = self.list_all_schemes(scheme_id=scheme_id, folio=folio)
        x_meta_data = []
        for mf_data in meta_data:
            mf_scheme_id = list(mf_data.keys())[0]
            mf_data[mf_scheme_id].pop('fund_house_id')
            mf_data[mf_scheme_id].pop('fund_house_name')
            x_meta_data.append(mf_data)

        return_json = {"net_investment": investment, "market_value": market_value,
                       "appreciation": appreciation, "x_meta_data": x_meta_data,
                       "interest_percent": interest, "market_value_on": market_value_on}
        return return_json

    @staticmethod
    def merge_investment_json(result_json_list):
        net_investment_list = []
        market_value_list = []
        appreciation_list = []
        x_meta_data = []
        for result in result_json_list:
            net_investment_list.append(result.get('net_investment'))
            market_value_list.append(result.get('market_value'))
            appreciation_list.append(result.get('appreciation'))
            x_meta_data.extend(result.get('x_meta_data'))
        market_value_on = result_json_list[0].get('market_value_on')

        investment = sum(net_investment_list)
        market_value = sum(market_value_list)
        appreciation = sum(appreciation_list)
        interest = round(((appreciation/investment) * 100.0), 2)

        return_json = {"net_investment": investment, "market_value": market_value,
                       "appreciation": appreciation, "x_meta_data": x_meta_data,
                       "interest_percent": interest, "market_value_on": market_value_on}
        return return_json
