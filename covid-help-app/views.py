from django.db.models.fields import TextField
from django.http import request
from django.http.response import Http404
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.models import User
from django.views.generic.detail import DetailView
from requests.api import post
from .models import Post,Comments
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView,CreateView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from .covid_related_data import *
from .serialization import PostSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class AllPostListView(ListView):
    model = Post
    template_name = 'CovidHelp/index.html'
    context_object_name = 'posts'
    ordering = ['-date']
    paginate_by = 10
    cases = total_cases
    death = total_death
    recoveries = total_recoveries
    vaccinated = total_vaccinated_people
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cases'] =  self.cases
        context['death'] =  self.death
        context['recoveries'] =  self.recoveries
        context['vaccinated'] = self.vaccinated
        return context


class UserAllPostListView(ListView):
    model = Post
    template_name = 'CovidHelp/user_post.html'
    context_object_name = 'posts'
    paginate_by = 10
    cases = total_cases
    death = total_death
    recoveries = total_recoveries
    vaccinated = total_vaccinated_people
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cases'] =  self.cases
        context['death'] =  self.death
        context['recoveries'] =  self.recoveries
        context['vaccinated'] = self.vaccinated
        return context
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date')


class PostDetailView(DetailView):
    model = Post
    cases = total_cases
    death = total_death
    recoveries = total_recoveries
    vaccinated = total_vaccinated_people
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cases'] =  self.cases
        context['death'] =  self.death
        context['recoveries'] =  self.recoveries
        context['vaccinated'] = self.vaccinated
        return context

class CreateNewPost(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'help_type']
    cases = total_cases
    death = total_death
    recoveries = total_recoveries
    vaccinated = total_vaccinated_people
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cases'] =  self.cases
        context['death'] =  self.death
        context['recoveries'] =  self.recoveries
        context['vaccinated'] = self.vaccinated
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    cases = total_cases
    death = total_death
    recoveries = total_recoveries
    vaccinated = total_vaccinated_people
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cases'] =  self.cases
        context['death'] =  self.death
        context['recoveries'] =  self.recoveries
        context['vaccinated'] = self.vaccinated
        return context
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about_view(request):
    return render(request,'CovidHelp/about.html')


class CommentsView(LoginRequiredMixin,CreateView):
    cases = total_cases
    death = total_death
    recoveries = total_recoveries
    vaccinated = total_vaccinated_people
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cases'] =  self.cases
        context['death'] =  self.death
        context['recoveries'] =  self.recoveries
        context['vaccinated'] = self.vaccinated
        return context
    model = Comments
    template_name = 'CovidHelp/add_comment.html'
    ordering = ['-date']
    fields = ['name','date','content']
    paginate_by = 10
    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)
    
class CommentDetailView(ListView):
    cases = total_cases
    death = total_death
    recoveries = total_recoveries
    vaccinated = total_vaccinated_people
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cases'] =  self.cases
        context['death'] =  self.death
        context['recoveries'] =  self.recoveries
        context['vaccinated'] = self.vaccinated
        return context
    model = Comments
    template_name = 'CovidHelp/comment_response.html'
    context_object_name = 'comments'
    paginate_by = 10
    def get_queryset(self):
        post = get_object_or_404(Post, id=self.kwargs.get('pk'))
        return Comments.objects.filter(post=post).order_by('-date')
    
class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    cases = total_cases
    death = total_death
    recoveries = total_recoveries
    vaccinated = total_vaccinated_people
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cases'] =  self.cases
        context['death'] =  self.death
        context['recoveries'] =  self.recoveries
        context['vaccinated'] = self.vaccinated
        return context
    model = Comments
    template_name = 'CovidHelp/comment_update.html'
    fields = ['name', 'date','content']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.post.author:
            return True
        return False

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    cases = total_cases
    death = total_death
    recoveries = total_recoveries
    vaccinated = total_vaccinated_people
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cases'] =  self.cases
        context['death'] =  self.death
        context['recoveries'] =  self.recoveries
        context['vaccinated'] = self.vaccinated
        return context
    model = Comments
    success_url = '/'
    def test_func(self):
        comment= self.get_object()
        if self.request.user == comment.post.author:
            return True
        return False

class PostRestApi(APIView):
    def get_object(self):
        try:
            return Post.objects.get(help_type=self.kwargs.get('help_type')) 
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, **kwargs):
        posts = self.get_object() 
        serializer = PostSerializer(posts)
        return Response(serializer.data)