from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.views.generic import ListView, CreateView, DetailView
from django.views.generic.base import RedirectView
from django.contrib.auth.views import LoginView, LogoutView as BaseLogoutView
from django.urls import reverse_lazy
from django import forms
from django.contrib import messages
from .models import Article, Favourite
from .forms import CustomAuthenticationForm, EmptyForm  # Asegúrate de que EmptyForm esté importado aquí


# Home view
def home(request):
    return render(request, 'articles/home.html')

class HomeRedirectView(RedirectView):
    url = reverse_lazy('articles')

# Article list view
class ArticleListView(ListView):
    model = Article
    template_name = 'articles/article_list.html'
    context_object_name = 'articles'

# Custom login view
class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'articles/login.html'
    success_url = reverse_lazy('publish_article')

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
        favourite_articles = Favourite.objects.filter(user=user).values_list('article', flat=True)
        return Article.objects.filter(id__in=favourite_articles)


class RegisterView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'articles/register.html'
    
    def get_success_url(self):
        return reverse_lazy('home')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.instance
        if not self.request.user.is_authenticated:
            from django.contrib.auth import login
            login(self.request, user)
        return response

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'synopsis', 'content']

class PublishArticleView(CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'articles/publish_article.html'
    success_url = reverse_lazy('articles')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class AddToFavouriteView(CreateView):
    model = Favourite
    form_class = EmptyForm  # Usa un formulario vacío o un formulario que solo maneje CSRF token
    template_name = 'articles/add_to_favourite.html'

    def form_valid(self, form):
        article_id = self.kwargs.get('pk')
        article = get_object_or_404(Article, pk=article_id)
        user = self.request.user

        # Verifica si el artículo ya está en favoritos
        if not Favourite.objects.filter(user=user, article=article).exists():
            form.instance.user = user
            form.instance.article = article
            form.save()  # Guarda la instancia en la base de datos
            return redirect(self.get_success_url())
        else:
            # Redirige de nuevo si el artículo ya está en favoritos
            return redirect(self.request.META.get('HTTP_REFERER', '/'))

    def get_success_url(self):
        # Redirige de nuevo a la página de detalles del artículo
        return self.request.META.get('HTTP_REFERER', '/')
