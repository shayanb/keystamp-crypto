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

### Hashing

```
# Hash file with SHA256
/hashme HTTP POST {"file_url" : URL}
response: {'status': 'success', 'hash': 'dbfdad915a13827c1684b39ff9875b24efaebd239f815f54e2263fbb217ad5d2'}
```
```
# Hash string with SHA256
/hashme_string HTTP POST {"text" : "lorem test text"}
response: {'status': 'success', 'hash': 'dbfdad915a13827c1684b39ff9875b24efaebd239f815f54e2263fbb217ad5d2'}
```


### Key generation
```
# Generate master seed for OSC (Note that this end point might take longer to response, as it generates entropy for address generation)
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



### Notarization
```
# notarize and save the text to the Bitcoin blockchain. text is limited to 80 characters
/notarizeme HTTP POST {'text':'FINAL_HASH_TO_BE_SAVED_TO_BC'}
response {"status":"success","tx_hash":'915a13827c1684b39ff9875b24efaebd239f815f54e2263fbb217ad5d'}
```

