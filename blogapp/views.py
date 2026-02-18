from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from blogapp.forms import ArticleForm
from blogapp.models import Article

# Create your views here.


def _style_form_fields(form):
    for name, field in form.fields.items():
        existing_class = field.widget.attrs.get("class", "")
        field.widget.attrs["class"] = f"{existing_class} form-control".strip()
        if name == "username":
            field.widget.attrs.setdefault("placeholder", "Enter your username")
        if name in ["password", "password1", "password2"]:
            field.widget.attrs.setdefault("placeholder", "Enter your password")
    return form


def home_view(request):
    Articles = Article.objects.all().order_by('-created_at')
    featured_article = Articles.first()
    context = {
        "articles": Articles,
        "featured_article": featured_article,
    }
    return render(request, "home.html", context)


def about_view(request):
    return render(request, "about.html")


def contact_view(request):
    return render(request, "contact.html")


def categories_view(request):
    return render(request, "categories.html")


def archive_view(request):
    articles = Article.objects.all().order_by("-created_at")
    return render(request, "archive.html", {"articles": articles})


def authors_view(request):
    authors = User.objects.filter(articles__isnull=False).distinct().order_by("username")
    return render(request, "authors.html", {"authors": authors})


def author_profile_view(request, username):
    author = get_object_or_404(User, username=username)
    articles = author.articles.all().order_by("-created_at")
    return render(request, "author_profile.html", {"author_profile": author, "articles": articles})


def search_view(request):
    return render(request, "search.html")


def newsletter_view(request):
    return render(request, "newsletter.html")


def faq_view(request):
    return render(request, "faq.html")


def privacy_view(request):
    return render(request, "privacy.html")


def terms_view(request):
    return render(request, "terms.html")


def not_found_preview_view(request):
    return render(request, "404.html", status=404)


def custom_404_view(request, exception):
    return render(request, "404.html", status=404)


def connexion_view(request):
    if request.method == "POST":
        form = _style_form_fields(AuthenticationForm(request, data=request.POST))
        form.is_valid()
        user = form.get_user()
        if user is not None:
            login(request, user)
            return redirect("blogapp:home")
    else:
        form = _style_form_fields(AuthenticationForm())
    return render(request, "connexion.html", {"form": form})


def register_view(request):
    if request.method == "POST":
        form = _style_form_fields(UserCreationForm(request.POST))
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("blogapp:home")
    else:
        form = _style_form_fields(UserCreationForm())
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
        form = _style_form_fields(ArticleForm(request.POST))
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect("blogapp:home")
    else:
        form = _style_form_fields(ArticleForm())
    return render(request, "articles/create_update_article.html", {"form": form, "action": "create"})
    

@login_required
def update_article_view(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.user != article.author:
        return redirect("blogapp:article_detail", pk=article.pk)
    if request.method == "POST":
        form = _style_form_fields(ArticleForm(request.POST, instance=article))
        if form.is_valid():
            form.save()
            return redirect("blogapp:article_detail", pk=article.pk)
    else:
        form = _style_form_fields(ArticleForm(instance=article))
    return render(request, "articles/create_update_article.html", {"form": form, "action": "update"})
    

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
    related_articles = (
        Article.objects.filter(author=article.author)
        .exclude(pk=article.pk)
        .order_by("-created_at")[:3]
    )
    context = {
        "article": article,
        "related_articles": related_articles,
    }
    return render(request, "articles/article_detail.html", context)
