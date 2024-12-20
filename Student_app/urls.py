from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login', views.login_view, name = "login_view"),
    path('', views.Logout, name='Logout'),
    path('Create-User', views.create_user, name = 'create_user'),

    path('Add-Student', views.Add_Student, name="Add_Student"),
    path('Student-List', views.Student_List, name="Student_List"),
    path('student/edit/<int:student_id>/', views.Edit_Student, name='Edit_Student'),
    path('student/delete/<int:student_id>/', views.Delete_Student, name='Delete_Student'),

    path('Add-Program', views.Add_Program, name="Add_Program"),
    path('Program-List', views.Program_List, name="Program_List"),
    path('program/edit/<int:program_id>/', views.Edit_Program, name='Edit_Program'),
    path('program/delete/<int:program_id>/', views.Delete_Program, name='Delete_Program'),

    
    path('Add-Branch', views.Add_Branch, name="Add_Branch"),
    path('Branch-List', views.Branch_List, name="Branch_List"),
    path('edit/<int:branch_id>/', views.edit_branch, name='edit_branch'),
    path('delete/<int:branch_id>/', views.delete_branch, name='delete_branch'),


    path('Add-Teacher', views.Add_Teacher, name="Add_Teacher"),
    path('Teacher-List', views.Teacher_List, name="Teacher_List"),
    path('teacher/edit/<int:teacher_id>/', views.edit_teacher, name='Edit_Teacher'),

    path('Add-Subject', views.Add_Subject, name="Add_Subject"),
    path('Subject-List', views.subject_list, name="subject_list"),
    path('subject/edit/<int:subject_id>/', views.edit_subject_view, name='edit_subject_view'),


    path('Get-Student', views.Get_Students, name="Get_Students"),
    path('Save-Attendance', views.Save_Attendance, name="Save_Attendance"),

    path('Add-Book-Type', views.Add_Book_Type, name="Add_Book_Type"),


]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)