from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MyBooksViewSet, PageCreateAPIView, RegistrationUserView, \
    PageRetrieveUpdateDestroyAPIView, ReadOnlyAuthorsViewSet, ReadOnlyBooksViewSet, FavoriteBooksAPIView, \
    ReadOnlyFavoriteBooksViewSet

router = DefaultRouter()
router.register('my_books', MyBooksViewSet, basename='my_books')
router.register('books', ReadOnlyBooksViewSet, basename='books')
router.register('authors', ReadOnlyAuthorsViewSet, basename='authors')
router.register('get_favorite_books', ReadOnlyFavoriteBooksViewSet, basename='favorite_books')


urlpatterns = [
    path("", include(router.urls)),
    path('registration/', RegistrationUserView.as_view(), name='registration'),
    path('my_books/<slug:book_slug>/create_page/', PageCreateAPIView.as_view()),
    path('my_books/<slug:book_slug>/<int:page_number>/', PageRetrieveUpdateDestroyAPIView.as_view()),
    path('favorite_books/', FavoriteBooksAPIView.as_view()),
]
