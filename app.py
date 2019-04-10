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
    help_txt["http://localhost:5000/schemes/"] = "list the investment schemes"
    help_txt["http://localhost:5000/investments/"] = "display the net investments"
    help_txt["http://localhost:5000/investments?scheme_id=SCHEME_ID"] = "display the SCHEME_ID investments"
    help_txt["http://localhost:5000/investments?folio=FOLIO_NUM"] = "display the investments on FOLIO_NUM"
    help_txt["http://localhost:5000/investments?scheme_id=SCHEME_ID&folio=FOLIO_NUM"] = \
        "display the SCHEME_ID investments on FOLIO"
    return jsonify(help_txt)


@app.route('/investments/')
def get_investments():
    scheme_id = queryflask.args.get('scheme_id')
    folio = queryflask.args.get('folio')
    ret_val = portfolio.get_investment_json(scheme_id=scheme_id, folio=folio)
    return jsonify(ret_val)


@app.route('/schemes/')
def list_investments():
    ret_val = portfolio.list_all_schemes()
    return jsonify(ret_val)


if __name__ == '__main__':
    host = "0.0.0.0"
    port = "5000"
    app.run(host=host, port=port)
