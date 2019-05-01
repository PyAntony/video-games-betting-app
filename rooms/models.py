
from django.db import models
from django.contrib.auth.models import User


class Room(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True, blank=False)
    description = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    participants = models.IntegerField(default=0)


class Message(models.Model):

    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Game(models.Model):

    GAMES_AVAILABLE = (
        ('PES', 'Pro-Soccer 2019'),
        ('LoL', 'League of Legends'),
        ('CS', 'Counter Strike'),
        ('SF5', 'Street Fighter V')
    )
    GAME_STATUS = (
        ('P', 'pending'),
        ('U', 'upcoming'),
        ('C', 'closed'),
    )

    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='creator')

    contender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='contender')

    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    scheduled_at = models.DateTimeField(null=False)
    initial_bet = models.IntegerField(null=False)
    status = models.CharField(max_length=1, choices=GAME_STATUS)
    video_game = models.CharField(max_length=3, choices=GAMES_AVAILABLE)
    stream_link = models.TextField(blank=False, default='no-link')
