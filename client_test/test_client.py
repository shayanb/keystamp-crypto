import requests
import sys



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






test_upload()
test_upload(file_url="https://avatars3.githubusercontent.com/u/147330?v=3&s=52")