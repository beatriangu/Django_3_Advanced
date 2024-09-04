from django.urls import path
from .views import home, ArticleListView, PublicationListView, ArticleDetailView, FavouritesListView, CustomLoginView, LogoutView

urlpatterns = [
    path('', home, name='home'),  # Página de inicio
    path('articles/', ArticleListView.as_view(), name='article_list'),  # Lista de artículos
    path('publications/', PublicationListView.as_view(), name='publications'),  # Publicaciones del usuario
    path('article/<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),  # Detalle del artículo
    path('favourites/', FavouritesListView.as_view(), name='favourites'),  # Artículos favoritos
    path('login/', CustomLoginView.as_view(), name='login'),  # Página de login
    path('logout/', LogoutView.as_view(), name='logout'),  # Página de logout
]

