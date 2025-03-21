# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .forms import RegisterForm,PostForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView,FormView
from .models import Post,Comment


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("profile")  # Redirect to profile after registration
    else:
        form = RegisterForm()
    return render(request, "blog/register.html", {"form": form})

@login_required
def profile(request):
    return render(request, "blog/profile.html")



# List all posts
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'  # Default: blog/post_list.html
    context_object_name = 'posts'
    ordering = ['-published_date']

# View a single post
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

# Create a new post
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# Update an existing post
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

# Delete a post
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    


class CommentCreateView(LoginRequiredMixin, FormView):


    template_name = "blog/add_comment.html"
    form_class = CommentForm

    def form_valid(self, form):
        post = get_object_or_404(Post, id=self.kwargs["post_id"])
        comment = form.save(commit=False)
        comment.post = post
        comment.author = self.request.user
        comment.save()
        return redirect("post-detail", pk=post.id)


class CommentUpdateView(LoginRequiredMixin, UpdateView):


    model = Comment
    form_class = CommentForm
    template_name = "blog/edit_comment.html"

    def get_object(self, queryset=None):
        return get_object_or_404(Comment, id=self.kwargs["comment_id"], author=self.request.user)

    def get_success_url(self):
        return reverse_lazy("post_detail", kwargs={"pk": self.object.post.id})


class CommentDeleteView(LoginRequiredMixin, DeleteView):

    model = Comment
    template_name = "blog/post_detail.html"

    def get_object(self, queryset=None):
        return get_object_or_404(Comment, id=self.kwargs["comment_id"], author=self.request.user)

    def get_success_url(self):
        return reverse_lazy("post_detail", kwargs={"pk": self.object.post.id})

