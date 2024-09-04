from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.views import LoginView as BaseLoginView, LogoutView as BaseLogoutView
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DetailView
from django.views.generic.base import RedirectView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.utils import timezone
from .models import Article, Favourite
from .forms import EmptyForm, ArticleForm
from django.utils.translation import gettext as _

# Home view
def home(request):
    return render(request, 'articles/home.html')

# Redirect from home to articles list
class HomeRedirectView(RedirectView):
    url = reverse_lazy('article_list')

# Article list view
class ArticleListView(ListView):
    model = Article
    template_name = 'articles/article_list.html'
    context_object_name = 'articles'

    def get_queryset(self):
        """Return the list of articles ordered by published_date."""
        return Article.objects.all().order_by('-published_date')

# Custom login view
class LoginView(BaseLoginView):
    template_name = 'articles/login.html'
    form_class = AuthenticationForm

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
class FavouritesListView(LoginRequiredMixin, ListView):
    model = Favourite
    template_name = 'articles/favourites.html'  # Asegúrate de que el template exista y esté correctamente configurado
    context_object_name = 'favourites'

    def get_queryset(self):
        # Filtra favoritos por el usuario autenticado
        return Favourite.objects.filter(user=self.request.user)

# User registration view
class RegisterView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'articles/register.html'
    
    def get_success_url(self):
        return reverse_lazy('home')
    
    def dispatch(self, request, *args, **kwargs):
        # Restricción para redirigir usuarios autenticados
        if request.user.is_authenticated:
            return redirect('home')  # Redirige a 'home' o a otra vista que prefieras
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.instance
        if not self.request.user.is_authenticated:
            from django.contrib.auth import login
            login(self.request, user)
        return response

# View for publishing articles
class PublishArticleView(CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'articles/publish_article.html'
    success_url = reverse_lazy('article_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        if not form.instance.published_date:
            form.instance.published_date = timezone.now()
        return super().form_valid(form)

# View for adding articles to favourites
class AddToFavouriteView(FormView):
    form_class = EmptyForm
    template_name = 'articles/add_to_favourite.html'

    def form_valid(self, form):
        article_id = self.kwargs.get('pk')
        article = get_object_or_404(Article, pk=article_id)
        user = self.request.user

        if not Favourite.objects.filter(user=user, article=article).exists():
            Favourite.objects.create(user=user, article=article)
        
        return redirect(self.get_success_url())

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER', '/')



