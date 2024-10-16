from django.urls import path
from .views import (
    HomeRedirectView,
    ArticleListView,
    ArticleDetailView,
    LoginView,
    LogoutView,
    RegisterView,
    PublicationListView,
    PublishArticleView,
    FavouritesListView,
    AddToFavouriteView,
)

urlpatterns = [
    path('', HomeRedirectView.as_view(), name='home'),  # This should map to '/'
    path('list/', ArticleListView.as_view(), name='article_list'),
    path('<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('publications/', PublicationListView.as_view(), name='publications'),
    path('publish/', PublishArticleView.as_view(), name='publish_article'),
    path('favourites/', FavouritesListView.as_view(), name='favourites'),
    path('add-to-favourite/<int:pk>/', AddToFavouriteView.as_view(), name='add_to_favourite'),
]




