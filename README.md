# mutualfundtracker
Track Mutual Funds 

only lumpsum as of now

Setup: Install the required packages at requirements.txt in a virtual environment

1. Fill the lumpsum.yml.sample as per your investment
2. venv/bin/python app.py
3. Access the APIs to get the current market value

Ex:

1.  "http://localhost:5000/investments/"                            - "display the net investments"
2.  "http://localhost:5000/investments?list=1"                      - "list the invested schemes"
3.  "http://localhost:5000/investments/<SCHEMEID>/"                 - "display the <SCHEMEID> investments"
4.  "http://localhost:5000/investments/<SCHEMEID>?folio=<FOLIONUM>" - "display the <SCHEMEID> on <FOLIONUM> investment"

TODO
1. Calculate XIRR
2. Estimate the market value
3. sip investments

