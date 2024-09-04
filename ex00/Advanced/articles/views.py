
from django.contrib.auth.views import LoginView
from django.views.generic import ListView
from django.views.generic.base import RedirectView
from django.urls import reverse_lazy
from .models import Article
from .forms import CustomAuthenticationForm


class ArticleListView(ListView):
    model = Article
    template_name = 'articles/article_list.html'
    context_object_name = 'articles'

class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'articles/login.html'
    success_url = reverse_lazy('home')

class HomeRedirectView(RedirectView):
    url = reverse_lazy('articles')

