from rest_framework import viewsets
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from django.db import connection
from django.db.models import Sum, Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .models import Ticket, Movie
from .serializers import TicketSerializer, MovieSerializer

# Health Check (Пункт 17)
@api_view(['GET'])
def health_check(request):
    try:
        connection.ensure_connection()
        return Response({"status": "ok", "database": "connected"})
    except Exception as e:
        return Response({"status": "error", "database": str(e)}, status=500)

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    
    # Фильтрация и сортировка (Пункт 12)
    filterset_fields = ['status', 'showtime__movie']
    ordering_fields = ['created_at', 'price']

    # JOIN-запрос 1: Билеты с инфой о фильме и зале (Django ORM делает INNER JOIN)
    @action(detail=False, methods=['get'])
    def with_details(self, request):
        tickets = Ticket.objects.select_related('showtime__movie', 'showtime__hall')[:50]
        data = [{"ticket_id": t.id, "movie": t.showtime.movie.title, "hall": t.showtime.hall.name} for t in tickets]
        return Response(data)

    # Агрегация (Пункт 11): Общая выручка и количество проданных билетов по статусам
    @action(detail=False, methods=['get'])
    def stats(self, request):
        stats = Ticket.objects.values('status').annotate(
            total_revenue=Sum('price'),
            total_tickets=Count('id')
        )
        return Response(stats)

# JOIN-запрос 2: Поиск фильмов, которые показывают в конкретном зале
@api_view(['GET'])
def movies_by_hall(request, hall_id):
    movies = Movie.objects.filter(showtime__hall_id=hall_id).distinct()
    return Response(MovieSerializer(movies, many=True).data)