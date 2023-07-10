from django.urls import path
from .views import RegisterView,LoginView,LogoutView
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static
from user.views import MemberView


router = DefaultRouter()
router.register("api/member",MemberView,basename='member')

urlpatterns = [
    
    path('register/',RegisterView.as_view()),
    path('login/',LoginView.as_view()),
    path('logout/',LogoutView.as_view()),

   
]+router.urls