from django.contrib import admin
from django.conf.urls import url, include
from . import views 

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^dashboard/', include('dashboard.urls'), name="dashboard"),
    url(r'^$', views.homepage, name="home")
]
