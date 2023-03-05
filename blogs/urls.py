from django.urls import path
from . import views



urlpatterns=[
  
  path('list/',views.Bloglist.as_view()),
  path('addimage/<int:id>/',views.Addimage.as_view()),
  path('addlike/<int:id>/',views.LikeApi.as_view()),
  path('dislike/<int:id>/',views.DislikeApi.as_view()),
  
]