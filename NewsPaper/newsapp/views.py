from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post
from django.core.paginator import Paginator
from .filters import PostFilter


class PostList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'  # имя списка в котором лежат все объекты
    paginate_by = 2  #вывод по 10 новостей

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'  # название объекта ghgfh
