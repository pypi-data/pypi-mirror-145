from django.conf.urls import url, include
from . import views
from dashboard.app import *

app_name = "APPNAME"

# => Base
urlpatterns = [
    url('^[/]?$', views.index, name="index"),    
]

catalogspec = catalog.get_spec()
register_app_instance(
    appmod="enrichapp.dashboard.catalog",
    namespace="catalog",
    rootnamespace=app_name,
    urlpatterns=urlpatterns,
    spec=catalogspec)

#from . import persona
#searchspec = persona.get_spec()
#register_app_instance(
#    appmod="enrichapp.dashboard.persona",
#    namespace="persona",
#    rootnamespace=app_name,
#    urlpatterns=urlpatterns,
#    spec=searchspec)
#
