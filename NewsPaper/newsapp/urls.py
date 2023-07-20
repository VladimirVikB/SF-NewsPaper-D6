from django.urls import path

from .views import AppointmentView
from .views import PostList, PostDetail, PostSearch, PostAdd, PostEdit, PostDelete, PostCategoryView
from .views import subscribe_to_category, unsubscribe_from_category

urlpatterns = [
    path('', PostList.as_view(), name='post_list'),  # т.к. сам по себе это класс, то нам надо представить
    # этот класс в виде view. Для этого вызываем метод as_view
    path('<int:pk>', PostDetail.as_view()),
    path('search/', PostSearch.as_view()),
    path('add/', PostAdd.as_view()),
    path('<int:pk>/edit', PostEdit.as_view()),
    path('<int:pk>/delete', PostDelete.as_view()),
    path('make_app/', AppointmentView.as_view(), name='make_app'),
    path('category/<int:pk>', PostCategoryView.as_view(), name='category'), # Ссылка на категории
    path('subscribe/<int:pk>', subscribe_to_category, name='subscribe'), # Ссылка на подписчиков
    path('unsubscribe/<int:pk>', unsubscribe_from_category, name='unsubscribe'), # Ссылка на отписку
]
