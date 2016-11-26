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


