from django.urls import path
from users.views import UserLoginView, UserLogout

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogout.as_view(), name='logout'),
]
