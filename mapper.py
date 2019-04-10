"""

"""

_ = {"<FUND_CODE>": {
    "fund_house_name": "<FUND_HOUSE_NAME>",
    "schemes": [
        {"scheme_code": "<SCHEME_CODE1>", "scheme_name": "<SCHEME_NAME1>", "mf_api": "<URL1>"},
        {"scheme_code": "<SCHEME_CODE2>", "scheme_name": "<SCHEME_NAME2>", "mf_api": "<URL2>"},
    ]
}
}


mapping = {}

scheme_keys = ("scheme_code", "scheme_name", "mf_api")

icici_bluechip = ("ICICIBLUECHIP_DG", "ICICI Prudential Bluechip Fund Direct Plan Growth",
                  "https://api.mfapi.in/mf/120586")
icici_bank_psu = ("ICICIBANKPSU_DG", "ICICI Prudential Banking and PSU Debt Fund Direct Plan Growth",
                  "https://api.mfapi.in/mf/120256")

mapping["ICICI"] = {"fund_house_name": "ICICI Prudential Mutual Fund",
                    "schemes": [dict(zip(scheme_keys, icici_bluechip)), dict(zip(scheme_keys, icici_bank_psu))]
                    }

sbi_dynamic_bond = ("SBIDYNBND_DG", "SBI Dynamic Bond Fund - DIRECT PLAN - Growth",
                    "https://api.mfapi.in/mf/119671")

mapping["SBI"] = {"fund_house_name": "SBI Mutual Fund",
                  "schemes": [dict(zip(scheme_keys, sbi_dynamic_bond))]
                  }

absl_tax_relief = ("ABSLTAXRELIEF96", "Aditya Birla Sun Life Tax Relief 96 Growth Direct Plan",
                   "https://api.mfapi.in/mf/119544")

mapping["ABSL"] = {"fund_house_name": "Aditya Birla Sun Life Mutual Fund",
                   "schemes": [dict(zip(scheme_keys, absl_tax_relief))]}

mirae_india_equity = ("MIRAEINDEQUITY_DG", "Mirae Asset India Equity Fund - Direct Plan - Growth",
                      "https://api.mfapi.in/mf/118825")

mapping["MIRAE"] = {"fund_house_name": "Mirae Asset Mutual Fund",
                    "schemes": [dict(zip(scheme_keys, mirae_india_equity))]}

uti_bond = ("UTIBND_DG", "UTI Bond Fund-Growth - Direct", "https://api.mfapi.in/mf/120689")
uti_gilt = ("UTIGILT_DG", "UTI - GILT FUND - Direct Plan - Growth Option", "https://api.mfapi.in/mf/120792")

mapping["UTI"] = {"fund_house_name": "UTI Mutual Fund",
                  "schemes": [dict(zip(scheme_keys, uti_bond)), dict(zip(scheme_keys, uti_gilt))]}


def get_scheme_details(fid, sid):
    fund_details = mapping.get(fid)
    if not fund_details:
        raise Exception("Fund unavailable")

    fname = fund_details.get("fund_house_name")
    fschemes = fund_details.get("schemes")
    (sname, mfapi) = [(s.get("scheme_name"), s.get("mf_api")) for s in fschemes if s.get("scheme_code") == sid][0]
    if (sname, mfapi) == (None, None):
        raise Exception("Scheme unavailable")

    scheme_details = {'fund_house_id': fid, 'fund_house_name': fname,
                      'scheme_id': sid, 'scheme_name': sname, 'scheme_api': mfapi}
    return scheme_details
