from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
   path('Add-Books', views.Create_Book, name="Create_Book"),
   path('Assign-Book', views.Assign_Book, name="Assign_Book"),
   path('Book-List', views.Book_List, name="Book_List"),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)