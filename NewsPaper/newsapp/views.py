from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from .models import Post
from django.core.paginator import Paginator
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin


class PostList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'  # имя списка в котором лежат все объекты
    paginate_by = 2  #вывод по 10 новостей
    form_class = PostForm


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'  # название объекта ghgfh


class PostSearch(ListView):
    model = Post
    template_name = 'post_search.html'
    context_object_name = 'posts'  # имя списка в котором лежат все объекты
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context

class PostAdd(CreateView):
    template_name = 'post_add.html'
    form_class = PostForm


class PostEdit(LoginRequiredMixin, UpdateView):
    template_name = 'post_edit.html'
    form_class = PostForm
    success_url = '/news/'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDelete(DeleteView):
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'