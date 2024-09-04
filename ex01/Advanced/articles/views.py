# views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.views.generic.base import RedirectView
from django.contrib.auth.views import LoginView, LogoutView as BaseLogoutView
from django.urls import reverse_lazy

from .models import Article, UserFavouriteArticle
from .forms import CustomAuthenticationForm

# Home view
def home(request):
    return render(request, 'articles/home.html')

# Article list view
class ArticleListView(ListView):
    model = Article
    template_name = 'articles/article_list.html'
    context_object_name = 'articles'

# Custom login view
class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'articles/login.html'
    success_url = reverse_lazy('home')

# Publication list view (articles by the logged-in user)
class PublicationListView(ListView):
    model = Article
    template_name = 'articles/publications.html'
    context_object_name = 'articles'

    def get_queryset(self):
        return Article.objects.filter(author=self.request.user)

# Article detail view
class ArticleDetailView(DetailView):
    model = Article
    template_name = 'articles/article_detail.html'
    context_object_name = 'article'

# Custom logout view
class LogoutView(BaseLogoutView):
    next_page = reverse_lazy('home')

# Favourite list view
class FavouritesListView(ListView):
    template_name = 'articles/favourites.html'
    context_object_name = 'favourites'

    def get_queryset(self):
        user = self.request.user
        favourite_articles = UserFavouriteArticle.objects.filter(user=user).values_list('article', flat=True)
        return Article.objects.filter(id__in=favourite_articles)
