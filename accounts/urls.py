from django.urls import path
from . import views



urlpatterns=[
  path('',views.UsersAPIView.as_view()),
  path('login/',views.UserloginView.as_view())
]