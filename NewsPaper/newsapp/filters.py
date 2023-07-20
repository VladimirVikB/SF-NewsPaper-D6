from django_filters import FilterSet

from .models import Post


class PostFilter(FilterSet):
    class Meta:
        model = Post
        fields = {
            'post_title': ['icontains'],
            'adding_time': ['gt'],
            'post_author__author_user': ['exact']
        }