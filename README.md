# keystamp-crypto



need heroku project access
inside project directory run

local: `python manage.py runserver 0.0.0.0:5000`

Deply: `git push heroku master`

===========================


Test local: `python test_client.py`
Test heroku: `python test_client.py online`



# API

BASE_URL = https://reghackto.herokuapp.com

Endpoints:

```
# Hash file with SHA256
/hashme HTTP POST {"file_url" : URL}
response: {'status': 'success', 'hash': 'dbfdad915a13827c1684b39ff9875b24efaebd239f815f54e2263fbb217ad5d2'}
```


```
# Generate master seed for OSC
/generate_master_seed HTTP GET/POST
response {'status': 'success', 'xpub': 'xpub661MyMwAqRbcEkr1KVuZG4s7BXbGkoSjMGEGtPjFU976HPotfmmZMsssB9q2Gt9j6d4aNAVF2vgD3GB6fcufLxSWHz7TFkjgWmEsWMyE9PF', 'xprv': 'xprv9s21ZrQH143K2GmYDUNYtvvNdVknMLisz3Jg61Kduoa7QbUk8ETJp5ZPKrHPgNTgR2uCYgeXqVFgKCZpDsPjgXQM19A7j6vKaXncY58JLi2'}
```


```
# generate firm key using master (OSC) seed and firm_id (5 digit int)
/generate_firm_key HTTP POST {"osc_key": "OSC_XPRV" ,"firm_id": 12345}
response  {'status': 'success', "xpub": xpub, "xprv": xprv,'path' : 'path'}
```

```
# generate advisor key using firm key and advisor_id (5 digit int)
/generate_advisor_key HTTP POST {"firm_key": "FIRM_XPRV" ,"advisor_id": 12345}
response  {'status': 'success', "xpub": xpub, "xprv": xprv,'path' : 'path'}
```