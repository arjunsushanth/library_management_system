from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import BorrowedBookView,BookListView,BookCreateView,BookUpdateView,BookDeleteView,BorrowedBookListView,BookTranscationView,BookBorrowAproveRejectView



router = DefaultRouter()
router.register('borrowedbooks',BorrowedBookView,basename='borrowedbooks'),
router.register('booktranscation',BookTranscationView,basename='booktranscation'),


urlpatterns = [
    path('booklist',BookListView.as_view(),name='book_list'),
    path('bookcreate',BookCreateView.as_view(),name='book_create'),
    path('bookupdate/<int:pk>/',BookUpdateView.as_view(), name='book_update'),
    path('delete/<int:pk>/',BookDeleteView.as_view(),name='book_delete'),
    path('borrowedbooklist/',BorrowedBookListView.as_view(),name='borrowedbook_list'),
    path('aprovalreject/<int:pk>/',BookBorrowAproveRejectView.as_view(),name='aproval_reject')
    
   
]+router.urls