from django.shortcuts import render
from django.http import HttpResponse
#import requests
import urllib2
from .models import Greeting
from .models import Document
import sys
import subprocess

import json
import hashlib
from pycoin.key.BIP32Node import BIP32Node

from pycoin.serialize import h2b, h2b_rev


#from pycoin.services.blockchain_info import spendables_for_address
from pycoin.tx import Tx
from pycoin.tx.script import tools
from pycoin.tx.tx_utils import sign_tx
from pycoin.tx.TxOut import TxOut, standard_tx_out_script
from binascii import hexlify
from pycoin.key import Key
from pycoin.tx import Spendable


import requests
import json

import os


COIN_NETWORK = "BTC" # XTN for testnet!

def sha256_checksum(file, block_size=65536):
    sha256 = hashlib.sha256()
    # with open(file,mode='r', buffering=-1) as f:
    for block in iter(lambda: file.read(block_size), b''):
        sha256.update(block)
    return sha256.hexdigest()




# Create your views here.
def index(request):
    return HttpResponse('#RegHackTo!')
    #return render(request, 'index.html')



def hashme(request):
    if request.method == 'POST':
        print "hashme: %s" %request.POST
        try:
            file_url = request.POST.get('file_url', "http://blog.theshayan.com/wp-content/uploads/2015/11/3-940x429.png")
            r = urllib2.urlopen(file_url)
        except Exception, e:
            print "failed to get url %s " %e
            return HttpResponse(json.dumps({"status":"failed", "reason": e.message}), content_type="application/json", status = 400)

        ret_json = {}
        if request.POST.get('file_url', None) is None:
            ret_json['file_url_missing'] = 'using_testimage'
            ret_json["status"] = "default"

        file_hash = sha256_checksum(r)
        ret_json["hash"] = file_hash
        ret_json["status"] = "success"
        print ret_json
        return HttpResponse(json.dumps(ret_json), content_type="application/json", status = 200)

    return HttpResponse(json.dumps({"error":"no Get request"}), content_type="application/json", status = 400)


def sha256_text(request):
    if request.method == 'POST':
        print "sha256_text: %s" % request.POST
        try:
            text = request.POST.get('text')
            sha256 = hashlib.sha256()
            sha256.update(text)
        except Exception, e:
            print "failed to get url %s " % e
            return HttpResponse(json.dumps({"status": "failed", "reason": e.message}), content_type="application/json",
                                status=400)

        return HttpResponse(json.dumps({"status": "success", "hash": sha256.hexdigest()}), content_type="application/json",
                                status=200)

    return HttpResponse(json.dumps({"error": "no Get request"}), content_type="application/json", status=400)


########################## Bitcoin Network stuff ##############################
def get_spendables_blockcypher(address, netcode = COIN_NETWORK, txn_limit=200, api_key=None, before_bh=None, confirmations=None):

    if netcode == "XTN":
        testnet = True
        BLOCKCYPHER_URL_ADDRESS = "https://api.blockcypher.com/v1/btc/test3/addrs/"

    if netcode == "BTC":
        coin_symbol='btc-testnet'
        BLOCKCYPHER_URL_ADDRESS = "https://api.blockcypher.com/v1/btc/main/addrs/"

    api_key = os.environ.get('blockcypher_api_key', None)

    print ("blockcypher spendable for %s" %address)

    url = BLOCKCYPHER_URL_ADDRESS + address + "?unspentOnly=true&token=%s&includeScript=true" %(api_key)


    try:
        request = requests.get(url)

        result = request.content
        result_json = json.loads(result)
        print "spendables: %s "% result_json
    except Exception, E:
        print ('Failed to fetch a url %s : %s' % (url, E))
        return []
        #raise ValueError('Failed to fetch a url %s - %s' % (url,data))

    all_spendables = []
    for txn in result_json.get("txrefs", []):
        unspent = {}
        unspent["tx_hash"] = txn.get("tx_hash")
        unspent["value"] = txn.get("value")
        unspent["index"] = txn.get("tx_output_n")
        unspent["script_hex"] = txn.get("script")
        all_spendables.append(unspent)
    return all_spendables



def broadcast_tx_blockcypher(signed_tx, netcode = COIN_NETWORK):
    '''
    alternative to chain.com method to broadcast transactions

    blockcypher.com

    '''
    if netcode == "XTN":
        testnet = True
        BLOCKCYPHER_URL_BROADCAST = "https://api.blockcypher.com/v1/btc/test3/txs/push"

    if netcode == "BTC":
        coin_symbol = 'btc-testnet'
        BLOCKCYPHER_URL_BROADCAST = "https://api.blockcypher.com/v1/btc/main/txs/push"

    api_key = os.environ.get('blockcypher_api_key', None)

    payload = {'token':api_key}
    payload['tx'] = signed_tx

    print "payload: %s" %payload
    try:
        request = requests.post(BLOCKCYPHER_URL_BROADCAST,
                            data=payload)

        result = request.content
    except Exception:
        print ('Failed to fetch a url %s - %s' % (BLOCKCYPHER_URL_BROADCAST,payload))
        #raise ValueError('Failed to fetch a url %s - %s' % (url,data))

    try:
        response_json = json.loads(result)
        print "blockcypher tx_hash %s" % response_json["tx"]["hash"]
        if "errors" in response_json:
            return False

        if "tx" in response_json:
            return response_json["tx"]["hash"]

    except Exception:
        print ("invalid broadcast respond from blockcypher: %s" % result)
        return False


########################## / Bitcoin Network stuff ##############################




########################## BIP32 stuff ##############################

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


def get_xprv_by_path(key, path, is_hardned = False):
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
    return {"xpub": xpub, "xprv": xprv}
    # print xpub
    # print xprv




def generate_osc_key(request):
    try:
        osc_key = create_newkey()
        ret_json = osc_key
        ret_json["status"] = "success"
        return HttpResponse(json.dumps(ret_json), content_type="application/json", status=200)
    except Exception, e:
        ret_json = {"status": "failed"}
        ret_json["message"] = e.message
        return HttpResponse(json.dumps(ret_json), content_type="application/json", status=400)



def get_firm_key(request):
    if request.method == 'POST':
        print "get_children_key: %s" % request.POST
        try:
            master_key = request.POST.get('osc_key', None)
            firm_id = str(request.POST.get('firm_id', None))
            path = "%s/%s" % (firm_id[:3] + "H", firm_id[3:] + "H")
        except Exception, e:
            print "failed get_firm_key: %s " %e
            ret_json = {"status": "failed"}
            ret_json["message"] = e.message
            return HttpResponse(json.dumps(ret_json), content_type="application/json", status=400)

        firm_key = get_xprv_by_path(master_key, path)
        ret_json = firm_key
        ret_json["status"] = "success"
        return HttpResponse(json.dumps(ret_json), content_type="application/json", status=200)


def get_advisor_key(request):
    if request.method == 'POST':
        print "get_advisor_key: %s" % request.POST
        try:
            master_key = request.POST.get('firm_key', None)
            firm_id = str(request.POST.get('advisor_id', None))
            path = "%s/%s" % (firm_id[:3], firm_id[3:])
        except Exception, e:
            print "failed get_advisor_key: %s " % e
            ret_json = {"status": "failed"}
            ret_json["message"] = e.message
            return HttpResponse(json.dumps(ret_json), content_type="application/json", status=400)

        advisor_key = get_xprv_by_path(master_key, path)
        ret_json = advisor_key
        ret_json["status"] = "success"
        return HttpResponse(json.dumps(ret_json), content_type="application/json", status=200)

########################## / BIP32 stuff ##############################



########################## OP RETURN ##############################

def get_key(privatekey):
    new_key = Key.from_text(privatekey)
    print ("Bitcoin Address %s " % new_key.bitcoin_address())
    return new_key

def op_return_this(privatekey, text, prefix = "KEYSTAMP:", bitcoin_fee = 10000):

    bitcoin_keyobj = get_key(privatekey)
    bitcoin_address = bitcoin_keyobj.bitcoin_address()

    message = hexlify(text.encode()).decode('utf8')

    ## Get the spendable outputs we are going to use to pay the fee
    all_spendables = get_spendables_blockcypher(bitcoin_address)
    spendables = []
    value = 0
    for unspent in all_spendables:
        while value < bitcoin_fee + 10000:
            coin_value = unspent.get("value")
            script = h2b(unspent.get("script_hex"))
            previous_hash = h2b_rev(unspent.get("tx_hash"))
            previous_index = unspent.get("index")
            spendables.append(Spendable(coin_value, script, previous_hash, previous_index))
            value += coin_value

    bitcoin_sum = sum(spendable.coin_value for spendable in spendables)
    if(bitcoin_sum < bitcoin_fee):
        print "ERROR: not enough balance: available: %s - fee: %s" %(bitcoin_sum, bitcoin_fee)
        return False

    ## Create the inputs we are going to use
    inputs = [spendable.tx_in() for spendable in spendables]
    ## If we will have change left over create an output to send it back
    outputs = []
    if (bitcoin_sum > bitcoin_fee):
        change_output_script = standard_tx_out_script(bitcoin_address)
        total_amout = bitcoin_sum - bitcoin_fee
        outputs.append(TxOut(total_amout, change_output_script))

        # home_address = standard_tx_out_script(bitcoin_address)
        # #TODO: it needs some love and IQ on input mananagement stuff
        # outputs.append(TxOut((bitcoin_sum - bitcoin_fee), home_address))

    ## Build the OP_RETURN output with our message
    if prefix is not None and len(message) + len(prefix) <= 80:
        message = prefix + message

    op_return_output_script = tools.compile("OP_RETURN %s" % message)
    outputs.append(TxOut(0, op_return_output_script))

    ## Create the transaction and sign it with the private key
    tx = Tx(version=1, txs_in=inputs, txs_out=outputs)
    # print tx.as_hex()
    # print spendables
    tx.set_unspents(spendables)
    sign_tx(tx, wifs=[privatekey])

    print "singed_tx: %s" %tx.as_hex()

    #TODO: uncomment this when its ready to push data to blockchian
    tx_hash = broadcast_tx_blockr(tx.as_hex())
    return tx_hash


def broadcast_tx_blockr(signed_tx):
    BLOCKR_URL_BROADCAST = "http://btc.blockr.io/api/v1/tx/push"
    url = BLOCKR_URL_BROADCAST
    data = json.dumps({"hex":signed_tx})
    try:
        request = requests.post(url, data=data)
        result = request.text
        print ("blockr raw response %s" %result)
    except Exception, E:
        print ('Failed to fetch a url %s - %s' % (E, url))
        return False

    try:
        response_json = json.loads(result)
        print("blocker tx_hash %s" % response_json["data"])
        if response_json.get("status", None) == "success":
            return response_json["data"]
        if response_json.get("status", None) == "fail":
            print json.dumps({"status":"fail","error":json.dumps(response_json).replace("\\","")})
            return False
    except Exception:
        print("invalid broadcast respond from blockr.io: %s" % result)
        return False




def notarizeme(request):
    if request.method == 'POST':
        print "notarizeme: %s" % request.POST
        try:
            text = request.POST.get('text', None)
            privatekey = os.environ.get('NOTARIZE_PRV', None)
        except Exception, e:
            print "failed notarizeme: %s " % e
            ret_json = {"status": "failed"}
            ret_json["message"] = e.message
            return HttpResponse(json.dumps(ret_json), content_type="application/json", status=400)

        if text is None or privatekey is None:
            print "failed noterizeme: text or privatekey is None "
            return HttpResponse(json.dumps({"status":"failed","message":"missing text or prvkey"}), content_type="application/json", status=400)

        if len(text) > 80:
            print "text is longer than 80 characters: %s : %s" %(len(text), text)
            return HttpResponse(json.dumps({"status":"failed","message":"text is longer than 80 characters"}), content_type="application/json", status=400)


        tx_hash = op_return_this(privatekey, text)

        if not tx_hash:
            return HttpResponse(json.dumps({"status":"failed","message":"failed to broadcast"}), content_type="application/json", status=400)

        return HttpResponse(json.dumps({"status":"success","tx_hash":tx_hash}), content_type="application/json", status=200)



########################## / OP RETURN ##############################
