# mutualfundtracker
Track Mutual Funds 

only lumpsum as of now

Setup: Install the required packages at requirements.txt in a virtual environment

1. Fill the lumpsum.yml.sample as per your investment
2. venv/bin/python app.py
3. Access the APIs to get the current market value

{
  "http://localhost:5000/investments/": "display the net investments", 
  "http://localhost:5000/investments/SCHEME_ID/": "display the SCHEME_ID investments", 
  "http://localhost:5000/investments/SCHEME_ID?folio=FOLIO_NUM": "display the SCHEME_ID on FOLIO_NUM investment", 
  "http://localhost:5000/investments?list=1": "list the invested schemes"
}
