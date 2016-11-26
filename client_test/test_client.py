import requests
import sys
from pycoin.key.BIP32Node import BIP32Node
import subprocess


# zx9pu8Q3BZxRZhRLj
# 138.197.141.252


COIN_NETWORK = "BTC"

'''
BASE_URL = https://reghackto.herokuapp.com

Endpoints:

# Hash file with SHA256
/hashme HTTP POST {"file_url" : URL}
response: {'status': 'success', 'hash': 'dbfdad915a13827c1684b39ff9875b24efaebd239f815f54e2263fbb217ad5d2'}

'''

try:
    if sys.argv[1] == "online":
        URL = "https://reghackto.herokuapp.com/"
    else:
        URL = "http://127.0.0.1:5000"
except:
    URL = "http://127.0.0.1:5000"
    pass



#headers = {'Referer':'google.com'}

def test_upload(file_url = None, URL = URL):
    URL += "/hashme"
    # if file_url is None
    r = requests.post(URL, data={"file_url": file_url}) #headers=headers)
    print "%s \t %s" %(r.status_code, r.content)
    r_json = r.json()
    if r_json.get("hash") == "4f24f0fcc34d95d713ce4068a6105d18625a37f19dfa906bbdd561db6da6e018" \
            or r_json.get("file_url_missing", None) is None:
        print "PASSED"
    else:
        print "FAILED"



def get_address_by_path(key, path):
    '''
    gets key = xpub or xpriv and path
    returns JSON
    xprv: {"address":"1qwerty...", "priv_key":"Kqwert...", "path":"1/2"}
    xpub: {"address":"1qwerty...", "priv_key":None, "path":"1/2"}
    '''
    da_key = BIP32Node.from_wallet_key(key)
    btc_address = da_key.subkey_for_path(path).bitcoin_address()
    btc_private = da_key.subkey_for_path(path).wif()
    return {"address":btc_address, "priv_key":btc_private, "path":path}



def get_xprv_by_path(key, path):
    da_key = BIP32Node.from_wallet_key(key)
    xprv = da_key.subkey_for_path(path).wallet_key(as_private=True)
    xpub = da_key.subkey_for_path(path).wallet_key()
    return {"xpub": xpub, "xprv": xprv, "path": path}



def gpg_entropy():
    try:
        output = subprocess.Popen(
            ["gpg", "--gen-random", "2", "64"], stdout=subprocess.PIPE).communicate()[0]
        return output
    except OSError:
        sys.stderr.write("warning: can't open gpg, can't use as entropy source\n")
    return b''


def get_entropy():
    entropy = bytearray()
    try:
        entropy.extend(gpg_entropy())
    except Exception:
        print("warning: can't use gpg as entropy source")
    try:
        entropy.extend(open("/dev/random", "rb").read(64))
    except Exception:
        print("warning: can't use /dev/random as entropy source")
    entropy = bytes(entropy)
    if len(entropy) < 64:
        raise OSError("can't find sources of entropy")
    return entropy



def create():
    max_retries = 64
    for _ in range(max_retries):
        try:
            return BIP32Node.from_master_secret(get_entropy(), netcode=COIN_NETWORK)
        except ValueError as e:
            continue
    raise e


def create_newkey(name = None):
    bip32_key = create()
    xpub = bip32_key.wallet_key(as_private=False)
    xprv = bip32_key.wallet_key(as_private=bip32_key.is_private())
    print xpub
    print xprv

    get_address_by_path(xprv, "1/2")



def get_osc_key(URL = URL):
    URL += "/generate_master_seed"
    r = requests.get(URL).json()
    print r
    return r


def get_firm_key(master_seed, firm_id, URL=URL):
    URL += '/generate_firm_key'
    r = requests.post(URL, data={'osc_key': master_seed, 'firm_id': firm_id}).json()
    print r
    return r


def get_advisor_key(firm_key, advisor_id, URL= URL):
    URL += '/generate_advisor_key'
    r = requests.post(URL, data={'firm_key': firm_key, 'advisor_id': advisor_id}).json()
    print r
    return r

import hashlib

def sha256_checksum(text, block_size=65536):
    sha256 = hashlib.sha256()
    # with open(file,mode='r', buffering=-1) as f:

    sha256.update(text)
    return sha256.hexdigest()


#mist TEsts
#create_newkey()
# firm_id = "12345"
# print  "%s/%s" % (firm_id[:3], firm_id[3:])

print sha256_checksum("H/DIn8uA1scAuKLlCx+/9LnAcJtwQQ0PmcPrJUq90aboLv3fH5fFvY+vmbfOSFEtGarznYli6ShPr9RXwY9UrIY=")





# TEST SUIT
# test_upload()
# test_upload(file_url="https://avatars3.githubusercontent.com/u/147330?v=3&s=52")
# osc_key = get_osc_key()
# firm_key = get_firm_key(master_seed = osc_key.get("xprv"), firm_id = "32143")
# advisor_key = get_advisor_key(firm_key = firm_key.get("xprv"), advisor_id="12366")
#

