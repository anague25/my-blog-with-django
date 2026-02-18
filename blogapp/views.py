from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from blogapp.forms import ArticleForm
from blogapp.models import Article

# Create your views here.


def home_view(request):
    Articles = Article.objects.all().order_by('-created_at')
    context = {
        "articles": Articles
    }
    return render(request, "home.html", context)


def connexion_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        form.is_valid()
        user = form.get_user()
        if user is not None:
            login(request, user)
            return redirect("blogapp:home")
    else:
        form = AuthenticationForm()
    return render(request, "connexion.html", {"form": form})


def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("blogapp:home")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})


# def register_view(request):
#    if request.method == 'POST':
#     form = UserCreationForm(request.POST)
#     if form.is_valid():
#         form.save()
#         username = form.cleaned_data.get('username')
#         password = form.cleaned_data.get('password1')
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return render(request,'home.html')


#     return render(request,'register.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect("blogapp:home")


# manage articles crud

@login_required
def create_article_view(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect("blogapp:home")
    else:
        form = ArticleForm()
        return render(request, "articles/create_update_article.html", {"form": form,'action': 'create'})
    

@login_required
def update_article_view(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.user != article.author:
        return redirect("blogapp:article_detail", pk=article.pk)
    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect("blogapp:article_detail", pk=article.pk)
    else:
        form = ArticleForm(instance=article)
        return render(request, "articles/create_update_article.html", {"form": form,'action': 'update'})
    

@login_required
def delete_article_view(request, id):    
    article = get_object_or_404(Article, id=id)
    if request.user != article.author:
        return redirect("blogapp:article_detail", pk=article.pk)
    if request.method == "POST":
        article.delete()
        return redirect("blogapp:home")
    else:
        return render(request, "articles/confirmation_delete_article.html", {"article": article})


@login_required
def article_detail_view(request, pk):
    article = get_object_or_404(Article, pk=pk)
    context = {
        "article": article
    }
    return render(request, "articles/article_detail.html", context)