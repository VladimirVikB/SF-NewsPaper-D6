from django.forms import ModelForm

from .models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['category', 'post_title', 'post_text', 'post_author', 'post_category']
