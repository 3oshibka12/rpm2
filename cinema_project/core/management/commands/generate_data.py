from django.core.management.base import BaseCommand
from core.models import Genre, Movie, CinemaHall, Showtime, Ticket
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Generate massive dummy data for database scaling tests'

    def handle(self, *args, **kwargs):
        self.stdout.write("Generating data...")
        
        # Создаем базовые сущности
        hall, _ = CinemaHall.objects.get_or_create(name="IMAX", capacity=200)
        movie, _ = Movie.objects.get_or_create(title="Dune 2", duration_minutes=160)
        showtime, _ = Showtime.objects.get_or_create(movie=movie, hall=hall, start_time=timezone.now())

        # Генерируем 10,000 билетов (для начала). На занятиях можно будет сделать 1_000_000
        tickets = []
        for i in range(10000):
            tickets.append(Ticket(
                showtime=showtime,
                customer_email=f"user{i}@example.com",
                price=random.choice([300.00, 450.00, 600.00]),
                status=random.choice(['PAID', 'CANCELED'])
            ))
        
        Ticket.objects.bulk_create(tickets)
        self.stdout.write(self.style.SUCCESS('Successfully generated 10,000 tickets!'))