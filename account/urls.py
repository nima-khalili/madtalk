from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
    path('trainer_register/', views.TrainerRegister.as_view()),
    path('customer_register/', views.CustomerRegister.as_view()),
    path('login/', views.UserLogin.as_view()),
    path('logout/', views.UserLogout.as_view()),
    path('profile/', views.UserProfile.as_view()),
    path('edit_user/', views.UserEdit.as_view()),
    path('follow/<int:user_id>/', views.UserFollow.as_view()),
    path('unfollow/<int:user_id>/', views.UserUnfollow.as_view()),
    path('schedule_write/<int:user_id>/', views.UserScheduleWrite.as_view()),
    path('schedule_see/<int:user_id>/', views.UserScheduleSee.as_view()),
    path('list_exercise/', views.ListExercise.as_view()),
]
