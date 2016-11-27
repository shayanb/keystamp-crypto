from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import keystamp_crypto.views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', keystamp_crypto.views.index, name='index'),

    url(r'^hashme$', keystamp_crypto.views.hashme, name='hashme'),

    url(r'^hashme_string', keystamp_crypto.views.sha256_text, name='sha256_text'),

    url(r'^generate_master_seed', keystamp_crypto.views.generate_osc_key, name='generate_osc_key'),

    url(r'^generate_firm_key', keystamp_crypto.views.get_firm_key, name='get_firm_key'),

    url(r'^generate_advisor_key', keystamp_crypto.views.get_advisor_key, name='get_advisor_key'),

    url(r'^notarize', keystamp_crypto.views.notarizeme, name='notarizeme'),

    url(r'^get_hash_from_bc', keystamp_crypto.views.get_hash_from_txid, name='get_hash_from_txid'),

    #    url(r'^listdocs', keystamp_crypto.views.list, name='list'),

    # url(r'^db', hello.views.db, name='db'),
   # url(r'^admin/', include(admin.site.urls)),
]
