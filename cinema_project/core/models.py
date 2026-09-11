from django.db import models

class Genre(models.Model):
    name = models.CharField(max_length=100)

class Movie(models.Model):
    title = models.CharField(max_length=200)
    duration_minutes = models.IntegerField()
    genres = models.ManyToManyField(Genre) # Many-to-Many

class CinemaHall(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()

class Showtime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE) # One-to-Many
    hall = models.ForeignKey(CinemaHall, on_delete=models.CASCADE)
    start_time = models.DateTimeField()

class Ticket(models.Model):
    STATUS_CHOICES = [('PAID', 'Paid'), ('CANCELED', 'Canceled')]
    
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE)
    customer_email = models.EmailField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PAID')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['status', '-created_at'], name='idx_ticket_stat_creat')
        ]