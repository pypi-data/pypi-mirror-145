from django.conf.urls import url

from .views import payment, callback_view, pay_success, pay_failed

app_name = 'payments'

urlpatterns = [
    url(r'^(?P<uuid>[0-9a-f-]+)/pay/$', payment, name='payment'),
    url(r'^(?P<uuid>[0-9a-f-]+)/success/$', pay_success, name='pay-success'),
    url(r'^(?P<uuid>[0-9a-f-]+)/failed/$', pay_failed, name='pay-failed'),
    url(r'^verify/$', callback_view, name='call-back'),
]
