from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('get-branches/<int:program_id>/', views.get_branches, name='get_branches'),
    path('get-students/<int:branch_id>/<int:program_id>/<int:semester>/', views.get_students, name='get_students'),


    path('Add-Fee', views.Add_Fee, name="Add_Fee"),
    path('Fees-List', views.Std_Fees_List, name='Std_Fees_List'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)