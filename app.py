from flask import Flask, jsonify
from flask import request as queryflask

from collections import OrderedDict
import load

portfolio = load.portfolio

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.route('/')
def display_help():
    help_txt = OrderedDict()
    help_txt["http://localhost:5000/investments/"] = "display the net investments"
    help_txt["http://localhost:5000/investments?list=1"] = "list the invested schemes"
    help_txt["http://localhost:5000/investments/SCHEME_ID/"] = "display the SCHEME_ID investments"
    help_txt["http://localhost:5000/investments/SCHEME_ID?folio=FOLIO_NUM"] = \
        "display the SCHEME_ID on FOLIO_NUM investment"
    return jsonify(help_txt)


@app.route('/investments/')
def get_all_investments():
    if queryflask.args.get('list'):
        ret_val = portfolio.list_all_schemes()
    else:
        ret_val = portfolio.get_investment_json()
    return jsonify(ret_val)


@app.route('/investments/<scheme_id>/')
def get_investments(scheme_id):
    folio = queryflask.args.get('folio')
    ret_val = portfolio.get_investment_json(scheme_id=scheme_id, folio=folio)
    return jsonify(ret_val)


if __name__ == '__main__':
    host = "0.0.0.0"
    port = "5000"
    app.run(host=host, port=port)
