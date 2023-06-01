# SF_NewsPЧто вы должны сделать в консоли Django?
from newsapp.models import *
from django.contrib.auth.models import User

Создать двух пользователей (с помощью метода User.objects.create_user).

 user1 = User.objects.create(username='Bob', first_name='Bobby', password='password1')
 user2 = User.objects.create(username='Jack', first_name='Mitchel', password='password2')

Создать два объекта модели Author, связанные с пользователями.

author1 = Author.objects.create(author_user=user1)
author2 = Author.objects.create(author_user=user2)

Добавить 4 категории в модель Category.

 category1 = Category.objects.create(category_art='Спорт')
 category2 = Category.objects.create(category_art='Политика')
 category3 = Category.objects.create(category_art='Образование')
 category4 = Category.objects.create(category_art='Искусство')

Добавить 2 статьи и 1 новость.

post_art = Post.objects.create(category='AR', post_title='Искусство', post_text='Текст статьи Искусство', post_rating=0, post_author=author1)
post_sport = Post.objects.create(category='AR', post_title=' Спорт ', post_text='Текст статьи Спорт ', post_rating=0, post_author=author2)
post_news = Post.objects.create(category=' NW ', post_title=' Новость ', post_text=' Текст новости ', post_rating=0, post_author=author2) 

Присвоить им категории (как минимум в одной статье/новости должно быть не меньше 2 категорий).

 post_art.post_category.add(category4)
 post_sport.post_category.add(category1)
 post_news.post_category.add(category2, category2)
 post_news.post_category.add(category2, category3)

Создать как минимум 4 комментария к разным объектам модели Post (в каждом объекте должен быть как минимум один комментарий).

 comment1 = Comment.objects.create(comment_text='Комментарий 1 ХО ХО', comment_rating=12, post_comment=post_art, user_comment=user1)  
 comment2 = Comment.objects.create(comment_text ='Комментарий 2 ДА ДА', comment_rating =3, post_comment = post_art, user_comment =user2)
 comment3 = Comment.objects.create(comment_text ='Комментарий 3 НО НО', comment_rating =8, post_comment = post_sport, user_comment =user1)
 comment4 = Comment.objects.create(comment_text ='Комментарий 4 ОГО', comment_rating =5, post_comment =post_news, user_comment =user2)

Применяя функции like() и dislike() к статьям/новостям и комментариям, скорректировать рейтинги этих объектов.

Post.objects.get(pk=1).like()
 post_art.like()
 post_art.like()
 post_sport.dislike()
 post_news.like()
 post_news.dislike()
 Comment.objects.get(pk=1).like()
 comment1.like()
 comment2.dislike()
 comment3.like()
 comment4.like()
 Comment.objects.get(pk=2).like()

Обновить рейтинги пользователей.

Author.objects.get(author_user=User.objects.get(username='Bob')).update_rating()
Author.objects.get(author_user=User.objects.get(username='Jack')).update_rating()

Вывести username и рейтинг лучшего пользователя (применяя сортировку и возвращая поля первого объекта).

best_author = Author.objects.order_by('-autor_rating').first()
print(best_author.author_user, best_author.autor_rating)
print(f'Лучший пользователь: { best_author.author_user }, рейтинг: { best_author.autor_rating }')

Вывести дату добавления, username автора, рейтинг, заголовок и превью лучшей статьи, основываясь на лайках/дислайках к этой статье.

best_post = Post.objects.order_by('-post_rating').first()
print(f'Дата добавления: {best_post.adding_time}, автор: {best_post. post_author}, рейтинг: {best_post.post_rating}, заголовок: {best_post.post_title}, превью: {best_post.preview()}')

Вывести все комментарии (дата, пользователь, рейтинг, текст) к этой статье.

comments = Comment.objects.filter(post_comment=best_post)
for comment in comments:
...     print(f'Дата: {comment.adding_time}, пользователь: {comment.user_comment}, рейтинг: {comment.comment_rating}, текст: {comment.comment_text}')