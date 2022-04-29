
from django.contrib import admin
from django.urls import path
# from django.conf.urls import include
from django.urls import include, re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'', include('blog.urls'))
]

 
