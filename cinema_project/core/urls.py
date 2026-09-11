from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TicketViewSet, MovieViewSet, health_check, movies_by_hall

router = DefaultRouter()
router.register(r'tickets', TicketViewSet)
router.register(r'movies', MovieViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('health/', health_check),
    path('halls/<int:hall_id>/movies/', movies_by_hall),
]