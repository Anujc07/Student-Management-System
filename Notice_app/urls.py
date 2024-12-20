from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
   
   path('Add-Notice', views.Add_Notice, name="Add_Notice"),
   path('Notice-List', views.Notice_List, name="Notice_List"),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)