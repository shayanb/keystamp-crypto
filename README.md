# keystamp-crypto


need heroku project access
Inside project directory run

locally:
```
export NOTARIZE_PRV=MAIN_NOTARIZER_PRIVATE_KEY
export blockcypher_api_key=blockcypher_api_key
python manage.py runserver 0.0.0.0:5000
```

Deply:
```
git push heroku master
heroku config:set NOTARIZE_PRV=MAIN_NOTARIZER_PRIVATE_KEY
heroku config:set blockcypher_api_key=blockcypher_api_key

```
===========================


Test local server: `python test_client.py local`

Test heroku: `python test_client.py`


## API

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
response {"status":"success","txid":'THE_TRANSACTION_ID_OF_THE_TRANSACTION_CONTAINING_THE_HASH'}
```


### Validation
```
# retreive hash stored in txid
/get_hash_from_bc HTTP POST {'txid': 'THE_TRANSACTION_ID_OF_THE_TRANSACTION_CONTAINING_THE_HASH'}
response {"status":"success","hash": 'THE_HASH_OF_THE_SAVED_DOCUMENT_IN_BLOCKCHAIN'}
```

```
# verify if a file (file_url) and a txid has the same hash. (Note: Verified is the final flag that should be checked)
/validate_file_url HTTP POST {'file_url': "http://site.com/image.jpg", 'txid': '915a13827c1684b39ff9875b24efaebd239f815f54e2263fbb217ad5d'}
response {'status':success',  'verified':True, 'txid_hash':'THE_HASH_THAT_WAS_SAVED_TO_BC','file_url_hash':'HASH_OF_THE_FILE' ,'file_url': "http://site.com/image.jpg", 'txid': '915a13827c1684b39ff9875b24efaebd239f815f54e2263fbb217ad5d'}
```
Did we just cryptographically proved `THE_HASH_THAT_WAS_SAVED_TO_BC = HASH_OF_THE_FILE` ? return verified # :)


## make it do this for you
```
# gets the final puzzle pieces and puts them together
/notarize_this HTTP POST
{'file_url':'http://site.com/contract.pdf', 'advisor_signature':'SIGNATURE_OF_DOCUMENTHASH_USER_RECEIPT_WITH_ADVISORS_PRIVATE_KEY', 'client_authorization':'TWILLIO_CODE_OR_ANY_OTHER_AUTHORIZATION_RECEIPT'}
note that you can send `file_hash` instead of `file_url`
response: {"status": "success", "keystamp":"HASH_OF_FINAL_KEY_THAT_IS_SAVED_ON_BC", "txid": tx_hash, "final_key": 'FILE_HASH:POST:TWILLIO_CODE_OR_ANY_OTHER_AUTHORIZATION_RECEIPT'.encode('utf-8') }
```
