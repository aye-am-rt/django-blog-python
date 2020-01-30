from abc import ABC

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
# this is for loginRequired # decorator as we used in
# function based views this is for class based view same work. route guard.
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Post


# posts = [
#     {
#         'author': 'CoreyMS',
#         'title': 'Blog Post 1',
#         'content': 'First post content',
#         'date_posted': 'August 27, 2119'
#     },
#     {
#         'author': 'Jane Doe',
#         'title': 'Blog Post 2',
#         'content': 'Second post content',
#         'date_posted': 'August 28, 2119'
#     }
# ]


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


class PostListViews(ListView):
    model = Post
    # without doing anything than just declaring the model=Post will throw template 404 error.
    # by default it looks for <app>/<model>_<viewType>.html in this case it will be blog/post_list.html
    # but we can change the template we want django to look. we will set it to look to our  home template.
    template_name = 'blog/home.html'  # <app>/<model>_<viewType>
    context_object_name = 'posts'
    ordering = ['-date_posted']
    # we could have saved number of lines of code as compared to our function base home view
    # as above written , if we used defaults what django suggested.
    paginate_by = 5

    #  PAGINATOR THING WORKING --
    # (env) H:\django-new\cs-django\django_project>python manage.py shell
    # >>> from django.core.paginator import Paginator
    # >>> posts=['1','2','3','4','5','6','7','8']
    # >>> p=Paginator(posts,2)
    # >>> p.num_pages
    # >>> p1=p.page(1)
    # >>> p1
    # <Page 1 of 4>
    # >>> p1.object_list
    # ['1', '2']
    # >>> p1.has_previous()
    # False
    # >>> p1.has_next()
    # True
    # >>> p1.next_page_number()
    # 2


class PostDetailViews(DetailView):
    model = Post


class PostDeleteViews(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostCreateViews(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    # if you want to do redirect to any specific page after submission you can make
    # success_url attribute along with model and fields. eg to go to home page.

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PostCreateViews, self).form_valid(form=form)
    # this method i made after making post create view ,to be able to submit the new post because
    # before this method it will show an integrity error because the post getting created will have
    # no user defined added with them. that's why i override the form_valid method.
    # # there will be still error after that ..it will say that it doesnt has any redirect url after
    # # creating new post. but it is creating new post as you want to.MAKE A GET_ABSOLUTE_URL() METHOD TO SOLVE


class PostUpdateViews(LoginRequiredMixin, UserPassesTestMixin, UpdateView, ABC):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about_old(request):
    return HttpResponse('<h1> about page of blog </h1>')


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


# (InteractiveConsole)
# >>> import json
# >>> from blog.models import Post
# >>> with open('post.json') as f:
#     ...     posts_json=json.load(f)
# ...
# >>> for post in posts_json:
#     ...     ps=Post(title=post['title'], content=post['content'], author_id=post['user_id'])
# ...     ps.save()
# ...
# >>> exit()


class UserPostListViews(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewType>
    context_object_name = 'posts'
    #ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')
