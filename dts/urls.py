from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('groups', GroupListView.as_view(), name="group-list"),
    path('user', UserListView.as_view(), name='user-list'),
    path('user/me', UserAuth.as_view(), name='user-me'),
    path('login', LoginView.as_view(), name='login'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('user/create', RegisterView.as_view(), name='register'),
    path('user/<int:id>', UserDetailView.as_view(), name='user-detail'),
    path('user/update/<int:pk>', UpdateUserView.as_view(), name='update_user'),
    path('user/delete/<int:pk>', DeleteUserView.as_view(), name='delete_user'),
    
    path('landingpage' , LandingPage.as_view()),

    path('hero', HeroList.as_view()),
    path('hero/active/<int:home_id>', HeroActive.as_view()),
    path('hero/create', HeroCreate.as_view()),
    path('hero/update/<int:pk>', HeroUpdate.as_view()),
    path('hero/delete/<int:pk>', HeroDelete.as_view()),

    path('pricing', PriceList.as_view()),
    path('pricing/create', PriceCreate.as_view()),
    path('pricing/update/<int:pk>', PriceUpdate.as_view()),
    path('pricing/delete/<int:pk>', PriceDelete.as_view()),

    path('service', ServiceList.as_view()),
    path('service/<int:service_id>', ServiceDetailView.as_view()),
    path('service/create', ServiceCreate.as_view()),
    path('service/update/<int:pk>', ServiceUpdate.as_view()),
    path('service/delete/<int:pk>', ServiceDelete.as_view()),

    path('portofolio', PortofolioList.as_view()),
    path('portofolio/create', PortofolioCreate.as_view()),
    path('portofolio/update/<int:pk>', PortofolioUpdate.as_view()),
    path('portofolio/delete/<int:pk>', PortofolioDelete.as_view()),

    path('contact', ContactList.as_view()),
    path('contact/create', ContactCreate.as_view()),
    path('contact/delete/<int:pk>', ContactDelete.as_view()),

    path('partnership', PartnershipList.as_view()),
    path('partnership/create', PartnershipCreate.as_view()),
    path('partnership/update/<int:pk>', PartnershipUpdate.as_view()),
    path('partnership/delete/<int:pk>', PartnershipDelete.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
