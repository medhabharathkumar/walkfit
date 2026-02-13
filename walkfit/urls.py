from .import views
from django.urls import path

urlpatterns=[
    path('',views.index,name='index'),
    path('index/',views.index,name='index'),
    path('home/',views.home,name='home'),
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('profile/',views.profile,name='profile'),
    path('editprofile/',views.editprofile,name='editprofile'),
    path('logout/',views.logout,name='logout'),
    path('listvideo/', views.video_list, name='listvideo'),
    path('addvideo/', views.video_add, name='addvideo'),
    path('fitness_tracker/', views.fitness_tracker, name='fitness_tracker'),
    path('adlogin/',views.adminlogin,name='adlogin'),
    path('adhome/',views.adhome,name='adhome'),
    path('userlist/',views.userlist,name='userlist'),
    path('deleteuser/<int:id>/',views.deleteuser,name='deleteuser'),
    path('deletevideo/<int:id>/',views.deletevideo,name='deletevideo'),
    path('manage_reminder/', views.manage_reminder, name='manage_reminder'),
    path('get_daily_reminder/', views.get_daily_reminder, name='get_daily_reminder'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('spotify/', views.spotify, name='spotify'),
    path('feedback/', views.feedback, name='feedback'),
    path('feedback_list/', views.feedback_list, name='feedback_list'),
    path('feedback_delete/<int:id>/', views.feedback_delete, name='feedback_delete'),
    path('healthchart/',views.healthchart,name='healthchart'),

]
