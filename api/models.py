from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Group(models.Model):
    title = models.CharField('Имя', max_length=200, help_text='Введите имя группы.\
                            Максимум 200 симоволов.')
    slug = models.SlugField('Адрес', max_length=50, unique=False,
                            help_text='Введите адрес группы.\
                            Максимум 50 симоволов.')
    description = models.TextField('Описание', help_text='Введите описание')

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="posts")
    group = models.ForeignKey(Group, on_delete=models.SET_NULL,
                              blank=True, null=True, related_name='posts',
                              db_index=True, help_text='Группа')

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name="comments")
    text = models.TextField()
    created = models.DateTimeField("Дата добавления",
                                   auto_now_add=True,
                                   db_index=True)

    def __str__(self):
        return self.text


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='follower', null=False,
                             db_index=True)
    following = models.ForeignKey(User, on_delete=models.CASCADE,
                                  related_name='following', null=False,
                                  db_index=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'following'],
                                    name='unique_follow'),
        ]
