from django.urls import path, include
from rest_framework_nested import routers
from boards.views import BoardViewSet
from .views import ListViewSet

router = routers.SimpleRouter()
router.register(r'boards', BoardViewSet, basename='board')

boards_router = routers.NestedSimpleRouter(router, r'boards', lookup='board')
boards_router.register(r'lists', ListViewSet, basename='board-lists')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(boards_router.urls)),
]
