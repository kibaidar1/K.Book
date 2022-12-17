from rest_framework import status, filters
from rest_framework.permissions import AllowAny, DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView, get_object_or_404
from .models import User, Book, Page
from .permissions import IsAuthorOrReadOnly, IsPageAuthorOrReadOnly
from .serializers import AuthorsSerializer, BookSerializer, PageSerializer, RegistrationUserSerializer, MyBookSerializer


class RegistrationUserView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationUserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = RegistrationUserSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = f'{request.data["username"]}, you are registered'
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = serializer.errors
            return Response(data)


class MyBooksViewSet(ModelViewSet):
    serializer_class = MyBookSerializer
    permission_classes = [DjangoModelPermissions, IsAuthorOrReadOnly]
    lookup_field = 'slug'

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        return Book.objects.filter(author=self.request.user)


class PageRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = PageSerializer
    permission_classes = [DjangoModelPermissions, IsPageAuthorOrReadOnly]
    lookup_field = 'page_number'

    def get_queryset(self):
        book_slug = self.kwargs['book_slug'].lower()
        book = get_object_or_404(queryset=Book, author=self.request.user, slug=book_slug)
        return Page.objects.filter(book=book)


class PageCreateAPIView(CreateAPIView):
    permission_classes = [DjangoModelPermissions, IsPageAuthorOrReadOnly]
    queryset = Page.objects.all()
    serializer_class = PageSerializer


class ReadOnlyBooksViewSet(ReadOnlyModelViewSet):
    search_fields = ['author__username', 'name', 'created_at', 'pages__content']
    filter_backends = (filters.SearchFilter,)
    permission_classes = [DjangoModelPermissions]
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'slug'


class ReadOnlyFavoriteBooksViewSet(ReadOnlyModelViewSet):
    search_fields = ['author__username', 'name', 'created_at', 'page__content']
    filter_backends = (filters.SearchFilter,)
    permission_classes = [DjangoModelPermissions]
    serializer_class = BookSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return Book.objects.filter(users=self.request.user)


class FavoriteBooksAPIView(APIView):
    bad_request_message = 'The book is already in favorites'

    def post(self, request):
        book = get_object_or_404(Book, slug=request.data.get('slug'))
        if request.user not in book.users.all():
            request.user.favorite_books.add(book)
            return Response({'detail': 'Favorite book added'}, status=status.HTTP_200_OK)
        return Response({'detail': self.bad_request_message}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        book = get_object_or_404(Book, slug=request.data.get('slug'))
        if request.user in book.users.all():
            request.user.favorite_books.remove(book)
            return Response({'detail': 'Favorite book removed'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'detail': self.bad_request_message}, status=status.HTTP_400_BAD_REQUEST)


class ReadOnlyAuthorsViewSet(ReadOnlyModelViewSet):
    permission_classes = [DjangoModelPermissions]
    queryset = User.objects.filter(role='Author')
    serializer_class = AuthorsSerializer
    lookup_field = 'username'

