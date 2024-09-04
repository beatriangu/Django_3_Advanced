from django.urls import path
from .views import (
    home,
    HomeRedirectView,
    ArticleListView,
    CustomLoginView,
    PublicationListView,
    ArticleDetailView,
    LogoutView,
    FavouritesListView,
    RegisterView,
    PublishArticleView,
    AddToFavouriteView
)

urlpatterns = [
    path('', home, name='home'),
    path('', HomeRedirectView.as_view(), name='home_redirect'),
    path('articles/', ArticleListView.as_view(), name='articles'),
    path('articles/<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('articles/publish/', PublishArticleView.as_view(), name='publish_article'),
    path('publications/', PublicationListView.as_view(), name='publications'),
    path('favourites/', FavouritesListView.as_view(), name='favourites'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('add-to-favourite/<int:pk>/', AddToFavouriteView.as_view(), name='add_to_favourite'),
]
