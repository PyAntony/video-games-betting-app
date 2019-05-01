
from django_seed import Seed
from datetime import datetime, timedelta
import random

# django_seed doesn't work without this call
from django.core.wsgi import get_wsgi_application
get_wsgi_application()

from rooms.models import User, Room, Game

# NUMBERS TO INSERT
GAMERS_NUM = 20
NON_GAMERS_NUM = 60
ROOMS_NUM = 30
GAMES_NUM = 40


# GAMER USERS --------------------------------------------
seeder = Seed.seeder()

seeder.add_entity(User, GAMERS_NUM, {
    'is_staff': False,
    'is_active': False,
})

seeder.add_entity(Room, ROOMS_NUM, {
    'name': lambda x: (seeder.faker.text()[:12]).replace(' ', '-'),
    'participants': lambda x: random.randrange(0, 150)
})


def get_future_random_date():

    td = timedelta(days=random.randrange(0, 30),
                   hours=random.randrange(0, 24))

    return datetime.now() + td


seeder.add_entity(Game, GAMES_NUM, {
    'scheduled_at': lambda x: get_future_random_date(),
    'initial_bet': lambda x: random.randrange(0, 100),
    'status': 'P',
    'stream_link': 'no-link'
})

seeder.execute()

# Update gamers' profiles (they are created empty by default)
for user in User.objects.all():

    user.profile.bio = seeder.faker.text()
    user.profile.is_gamer = True
    user.profile.save()

# Fix games' creators and contenders
for game in Game.objects.all():

    game.creator = game.room.user
    game.save()

    if game.creator.username == game.contender.username:

        contenders = User.objects.exclude(username=game.creator.username)

        game.contender = random.choice(contenders)
        game.save()


# NON-GAMER USERS ------------------------------------------
seeder.add_entity(User, NON_GAMERS_NUM, {
    'is_staff': False,
    'is_active': False,
})

seeder.execute()
