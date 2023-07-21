from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum


class Author(models.Model):
    autor_rating = models.IntegerField(default=0)
    author_user = models.OneToOneField(User, on_delete=models.CASCADE)


    def update_rating(self):
        posts_rating = self.posts.aggregate(Sum('post_rating'))['post_rating__sum'] or 0
        # comments_rating = self.comment_set.aggregate(Sum('comment_rating'))['comment_rating__sum'] or 0

        comments_rating = Comment.objects.filter(user_comment=self.author_user).aggregate(Sum('comment_rating'))[
                              'comment_rating__sum'] or 0
        comments_to_posts_rating = self.posts.aggregate(Sum('comment__comment_rating'))[
                                       'comment__comment_rating__sum'] or 0

        self.autor_rating = posts_rating * 3 + comments_rating + comments_to_posts_rating
        self.save()


class Category(models.Model):
    category_art = models.CharField(unique=True, max_length=255)
    subscribers = models.ManyToManyField(User, blank=True)  # подписчики

    def subscribe(self):
        pass

    def __str__(self):
        return f'{self.category_art}'


class Post(models.Model):
    article = 'AR'
    news = 'NW'
    CHOICE = [
        (article, 'Статья'),
        (news, 'Новость')
    ]

    category = models.CharField(max_length=2,
                                choices=CHOICE,
                                default=article)

    adding_time = models.DateTimeField(auto_now_add=True)
    post_title = models.CharField(max_length=255)
    post_text = models.TextField()
    post_rating = models.IntegerField(default=0)
    post_author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    post_category = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def preview(self):
        return self.post_text[:124] + '...'

    def get_absolute_url(self):
        return f'/news/{self.id}'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_categories')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='post_categories')

    def __str__(self):
        return f'{self.category}'


class Comment(models.Model):
    comment_text = models.TextField()
    adding_time = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)
    post_comment = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_comment = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()


class Appointment(models.Model):
    date = models.DateField(
        default=datetime.utcnow,
    )
    client_name = models.CharField(
        max_length=200
    )
    message = models.TextField()

    def __str__(self):
        return f'{self.client_name}: {self.message}'
