from django.urls import path

from . import views

urlpatterns = [
    path('auth/login', views.login),
    path('auth/logout', views.logout),
    path('auth/me', views.get_user_details),
    path('user/reward', views.reward_user),
    path('user/thank', views.thank_user),
    path('user/give-achievement', views.give_achievement),

    path('achievement/my', views.get_my_achievements),
    path('achievement/all', views.get_all_achievements),

    path('challenge/my', views.get_my_challenges),
    path('challenge/all', views.get_all_challenges)
]