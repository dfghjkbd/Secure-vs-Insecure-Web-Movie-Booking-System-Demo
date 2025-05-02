from django.urls import path
from . import views


urlpatterns = [
    path('', views.frontpage, name='frontpage'),
    path('signup/', views.signup_page, name='signup'),
    path('signup_user/', views.signup_user, name='signup_user'),
    path('login/', views.login_page, name='login'),
    path('login_user/', views.login_user, name='login_user'),
   # path('logout/', views.user_logout, name='logout'),
    path('welcome/', views.welcome, name='welcome'),
    path('movies/', views.list_movies, name='list_movies'),
    path('book/', views.book_movie, name='book_movie'),
     path('submit-feedback/', views.submit_feedback, name='submit_feedback'),
    
    path('feedback/', views.feedback_page, name='feedback'),
]