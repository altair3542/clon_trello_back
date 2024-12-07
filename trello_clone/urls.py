"""
URL configuration for trello_clone project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
from rest_framework_nested import routers
from boards.views import BoardViewSet
from lists.views import ListViewSet
from cards.views import CardViewSet

router = routers.SimpleRouter()
router.register(r'boards', BoardViewSet, basename='board')

boards_router = routers.NestedSimpleRouter(router, r'boards', lookup='board')
boards_router.register(r'lists', ListViewSet, basename='board-lists')

lists_router = routers.NestedSimpleRouter(boards_router, r'lists', lookup='list')
lists_router.register(r'cards', CardViewSet, basename='list-cards')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/users/', include('users.urls')),

    path('api/', include(router.urls)),
    path('api/', include(boards_router.urls)),
    path('api/', include(lists_router.urls)),
]

