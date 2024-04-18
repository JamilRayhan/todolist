from django.contrib import admin
from django.urls import path, include
from App_login import views
urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/',include('App_login.urls')),
    path('api-auth/', include('rest_framework.urls'))
]
