from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User  # one to many relationship
from django.urls import reverse, reverse_lazy


# >>> python manage.py sqlmigrate blog 0001


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    # date_posted = models.DateTimeField(auto_now=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    # this is i am making after PostCreateViews making in views. the difference btw redirect and reverse
    # is that reverse just returns the url as string to view, while redirect will redirect you to that url.

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

# python manage.py shell
# >>> from blog.models import Post
# >>> from django.contrib.auth.models import User
# >>> User.objects.all()
# <QuerySet [<User: rte>]>
# >>> User.objects.first()
# <User: rte>
# >>> User.objects.filter(username='rte')
# <QuerySet [<User: rte>]>
# >>> User.objects.filter(username='rte').first()
# <User: rte>
# >>>

# >>> user=User.objects.filter(username='rte').first()
# >>> user
# <User: rte>
# >>> user.id
# 1
# >>> user.pk
# 1
# >>> Post.objects.all()
# <QuerySet []>
# >>> post1=Post(title="blog 1", content= "this is first post from shell by rte and datetime is default saved", author=user)
# >>> post1.save()
# >>> Post.objects.all()
# <QuerySet [<Post: Post object (1)>]>

# >>> post=Post.objects.first()
# >>> post
# <Post: blog 1>
# >>> post.date_posted
# datetime.datetime(2020, 1, 25, 11, 35, 36, 161779, tzinfo=<UTC>)
# >>> post.title
# 'blog 1'
# >>> post.author
# <User: rte>
# >>> post.author.email
# 'rte@gmail.com'
# >>> user.post_set.all()
# <QuerySet [<Post: blog 1>, <Post: blog 2>]>
# >>>
