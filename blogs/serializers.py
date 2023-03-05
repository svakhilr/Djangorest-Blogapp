from rest_framework import serializers
from .models import Tag,Blog,Likes


class TagSerialiser(serializers.Serializer):
    name = serializers.CharField()
    weight = serializers.IntegerField()

class ImageSerialiser(serializers.Serializer):
    image =  serializers.ImageField()

    

class BlogSerialiser(serializers.Serializer):
    tags = TagSerialiser(many=True)
    images =ImageSerialiser(source='blog',many= True,read_only=True)
    # liked_by_user = serializers.SerializerMethodField(read_only=True)
    # disliked_by_user = serializers.SerializerMethodField(read_only=True)

    
    id = serializers.IntegerField(read_only=True)
    tittle = serializers.CharField()
    description = serializers.CharField()
    total_likes = serializers.IntegerField(read_only=True)
    total_dislikes = serializers.IntegerField(read_only=True)
    # liked_by_user = serializers.SerializerMethodField(read_only=True)
    # disliked_by_user = serializers.SerializerMethodField(read_only=True)

    # Tags=tags
    

    

    def create(self, validated_data):
        tags_data = validated_data.pop('tags')
        post = Blog.objects.create(**validated_data)
        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(**tag_data)
            post.tags.add(tag, through_defaults={'weight': tag_data['weight']})
        return post
    
    # def get_liked_by_user(self, obj):
    #     request = self.context.get('request', None)
    #     if request.user.is_authenticated:
    #         return Likes.objects.filter(id=request.user.id).exists()
    #     return False

    # def get_disliked_by_user(self, obj):
    #     request = self.context.get('request', None)
    #     if request.user.is_authenticated:
    #         return obj.blogdislike.filter(id=request.user.id).exists()
    #     return False