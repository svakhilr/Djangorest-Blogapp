from django.shortcuts import render
from rest_framework import response
from rest_framework import generics
from .serializers import BlogSerialiser,ImageSerialiser
from .models import Blog,Images,Likes,Dislikes
from rest_framework.views import  APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum

from django.core.paginator import Paginator
from rest_framework.pagination import PageNumberPagination
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.

# class PostViewSet(viewsets.ModelViewSet):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer

# class BlogCreateAPIView(generics.CreateAPIView):
#     queryset = Blog.objects.all()
#     serializer_class = BlogSerialiser




class Bloglist(APIView,PageNumberPagination):
    permission_classes = [IsAuthenticated]
    

    page_size = 3 
    def get(self,request):
        
        blog=Blog.objects.annotate(total_weight=Sum('tags__weight')).order_by('-total_weight')
        results = self.paginate_queryset(blog, request, view=self)
        print(blog)
        print(results)
        serializer = BlogSerialiser(results ,many=True)
        print(serializer.data)
        return self.get_paginated_response(serializer.data)
    
    def post(self,request):
        if request.user.is_superuser:
            serialiser = BlogSerialiser(data=request.data)
            if serialiser.is_valid(raise_exception=True):
                serialiser.save()
                return Response(serialiser.data)
            else:
                return Response({'message':'not valid'})
        return Response({"message":"not an admin"})  


class Addimage(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request,id):
        if request.user.is_superuser:
            
            try:
              blog = Blog.objects.get(id=id)
            except:
                return Response({"message":"Invalid blog id"},status=status.HTTP_400_BAD_REQUEST)
            image=request.FILES.get('images', None)
            serialiser = ImageSerialiser(data={'image':image})
            if serialiser.is_valid(raise_exception=True):
                images = request.FILES.getlist('images')
                for image in images:
                    Images.objects.create(image=image, blog=blog)
            return Response({"message":"success"},status=status.HTTP_201_CREATED)
        return Response({"message":"only admin is allowed"},status=status.HTTP_401_UNAUTHORIZED)   


class LikeApi(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request,id):
        user = request.user
        blog= Blog.objects.get(id=id)
        if blog:
            bloglikeduser = blog.bloglike.all().values_list('user', flat = True) 
            if request.user.id in bloglikeduser:
                return Response({"message":"Already liked the post"},status=status.HTTP_400_BAD_REQUEST) 
            else:
                blogdislikeuser = blog.blogdislike.all().values_list('user',flat=True)
                if blogdislikeuser:
                    blog.blogdislike.delete()
                    blog.total_dislikes-=1
                    blog.save()
                blog.total_likes+=1
                Likes.objects.create(user=user,blog=blog) 
                blog.save() 
                srialiser= BlogSerialiser(blog)
                return Response({"message":"successfully liked","post":srialiser.data},status=status.HTTP_200_OK)
        else:
            return Response({"message":"blog not found"},status=status.HTTP_400_BAD_REQUEST)    

            
class DislikeApi(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request,id):
        user= request.user
        
        if Blog.objects.filter(id=id).exists():
            blog = Blog.objects.get(id=id)
            blogdislikeduser = blog.blogdislike.all().values_list('user', flat = True)
            if blogdislikeduser:
                return Response({"message":"you have already disliked the post"},status=status.HTTP_400_BAD_REQUEST)
            else:
                bloglikeduser = blog.bloglike.all().values_list('user', flat = True)
                if bloglikeduser:
                    blog.total_likes-=1
                    blog.save()

                blog.total_dislikes+=1
                blog.save()
                Dislikes.objects.create(user=user,blog=blog)
                srialiser= BlogSerialiser(blog)
                return Response({"message":"successfully disliked","post":srialiser.data},status=status.HTTP_200_OK)
        else:
            return Response({"message":"blog not found"},status=status.HTTP_400_BAD_REQUEST)
