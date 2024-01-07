from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'), #
    path('login/', views.login_view, name='login'), #
    path('logout/', views.logout_view, name='logout'), ##
    path('password_reset/', views.password_reset, name='password_reset'), #
    path('about/', views.about_us, name='about_us'), #
    path('contact/', views.contact, name='contact'), #
    path('edit_profile/', views.edit_profile, name='edit_profile'), #
    path('upload_program/', views.upload_program, name='upload_program'), #
    path('program/<int:program_id>/', views.program_detail, name='program_detail'), #
    path('program/<int:program_id>/edit/', views.edit_program, name='edit_program'), #
    path('program/<int:program_id>/delete/', views.delete_program, name='delete_program'), #
    path('program/<int:program_id>/comment/', views.add_comment, name='add_comment'), #
    path('program/<int:program_id>/complaint/', views.submit_complaint, name='submit_complaint'), #
    path('search/', views.search, name='search'), #
    path('user/<int:user_id>/block/', views.block_user, name='block_user'), #
    path('rules/', views.rules, name='rules'), #
    path('change_theme/', views.change_theme, name='change_theme'), #
    path('manage_users/', views.manage_users, name='manage_users'), #
    path('manage_programs/', views.manage_programs, name='manage_programs'), #
    path('view_complaints/', views.view_complaints, name='view_complaints'), #
    path('manage_moderators/', views.manage_moderators, name='manage_moderators'), #
    path('user/<str:username>/', views.user_profile, name='user_profile'), #
    path('user/<str:username>/programs/', views.user_programs, name='user_programs'), #
    # Головна сторінка
    path('', views.home, name='home'),
]
