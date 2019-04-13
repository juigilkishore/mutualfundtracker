# mutualfundtracker
Track Mutual Funds 

only lumpsum as of now

Setup: Install the required packages at requirements.txt in a virtual environment

1. Fill the lumpsum.yml.sample as per your investment
2. venv/bin/python app.py
3. Access the APIs to get the current market value

Ex:

1.  "http://localhost:5000/investments/": "display the net investments"
2.  "http://localhost:5000/investments?folio=FOLIO_NUM": "display the investments on FOLIO_NUM"
3.  "http://localhost:5000/investments?scheme_id=SCHEME_ID": "display the SCHEME_ID investments" 
4.  "http://localhost:5000/investments?scheme_id=SCHEME_ID&folio=FOLIO_NUM": "display the SCHEME_ID investments on FOLIO"
5.  "http://localhost:5000/investments?fund_house_id=FUND_HOUSE_ID": "display the investments under FUND_HOUSE_ID"
6.  "http://localhost:5000/schemes/": "list the investment schemes"

TODO
1. Estimate the market value

