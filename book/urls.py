from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import BookView,BorrowedBookView



router = DefaultRouter()
router.register('api/book',BookView, basename='book')
router.register('bookaproval',BorrowedBookView,basename='aproval')

urlpatterns = [
    
   
]+router.urls