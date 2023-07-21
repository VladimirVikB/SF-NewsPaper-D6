from datetime import datetime

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import resolve
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView

from .filters import PostFilter
from .forms import PostForm
from .models import Appointment
from .models import Post, Category

DEFAULT_FROM_EMAIL = settings.DEFAULT_FROM_EMAIL

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

class PostAdd(PermissionRequiredMixin, CreateView):
    template_name = 'post_add.html'
    form_class = PostForm
    permission_required = ('newsapp.add_post')


class PostEdit(PermissionRequiredMixin, UpdateView):
    template_name = 'post_edit.html'
    form_class = PostForm
    success_url = '/news/'
    permission_required = ('newsapp.change_post')

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDelete(DeleteView):
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'


class PostCategoryView(ListView):
    model = Post
    template_name = 'newsapp/category.html'
    context_object_name = 'news'  # это имя списка, в котором будут лежать все объекты,
    # его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон
    ordering = ['-dateCreation']  # сортировка
    paginate_by = 10  # поставим постраничный вывод в один элемент

    def get_queryset(self):
        self.id = resolve(self.request.path_info).kwargs['pk']
        c = Category.objects.get(id=self.id)
        queryset = Post.objects.filter(postCategory=c)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        category = Category.objects.get(id=self.id)
        subscribed = category.subscribers.filter(email=user.email)
        if not subscribed:
            context['category'] = category
        return context


@login_required
def subscribe_to_category(request, pk):  # подписка на категорию
    user = request.user
    category = Category.objects.get(id=pk)

    if not category.subscribers.filter(id=user.id).exists():
        category.subscribers.add(user)
        email = user.email
        html = render_to_string(
            'mail/subscribed.html',
            {
                'category': category,
                'user': user,
            },
        )
        msg = EmailMultiAlternatives(
            subject=f'Подписка на {category} на сайте News Paper',
            body='',
            from_email=DEFAULT_FROM_EMAIL,  # в settings.py
            to=[email, ],  # список получателей
        )
        msg.attach_alternative(html, 'text/html')

        try:
            msg.send()
        except Exception as e:
            print(e)
        return redirect(request.META.get('HTTP_REFERER'))
        # return redirect('news_list')
    return redirect(request.META.get('HTTP_REFERER'))  # возвращает на страницу, с кот-й поступил запрос


@login_required
def unsubscribe_from_category(request, pk):  # отписка от категории
    user = request.user
    c = Category.objects.get(id=pk)

    if c.subscribers.filter(id=user.id).exists():  # проверяем есть ли у нас такой подписчик
        c.subscribers.remove(user)  # то удаляем нашего пользователя
    # return redirect('http://127.0.0.1:8000/')
    return redirect(request.META.get('HTTP_REFERER'))


class AppointmentView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'news_app/make_app.html', {})

    def post(self, request, *args, **kwargs):
        appointment = Appointment(
            date=datetime.strptime(request.POST['date'], '%Y-%m-%d'),
            client_name=request.POST['client_name'],
            message=request.POST['message'],
        )
        appointment.save()

        return redirect('news:make_app')