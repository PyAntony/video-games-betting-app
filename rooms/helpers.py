
from .models import Room, Game, Message
from django.contrib.auth.models import User

from datetime import datetime as dt


def get_context(**kwargs):
    '''
    Returns all rooms and game objects. Additional
    parameters can be passed (to be used for html templates).
    '''
    objects = dict()

    if 'games' not in kwargs.keys():
        objects['games'] = Game.objects.all().order_by('scheduled_at')[:10]

    if 'rooms' not in kwargs.keys():
        # 10 rooms displayed by default. Rooms are sorted by date.
        objects['rooms'] = Room.objects.order_by('-created_at')[:10]

    return {**kwargs, **objects}


def get_rooms(id, other_field='', value=''):
    '''
    Get room by user ID or other_field (passing id='').
    Returns a QuerySet or empty string if not found.
    '''
    try:
        if other_field == 'gamer':
            return Room.objects.filter(user__username=value)
        elif other_field == 'name':
            return Room.objects.filter(name=value)
        else:
            # assumes id was passed
            return Room.objects.filter(user=id)

    except Room.DoesNotExist:
        return ''


def register_new_user(request):
    '''Register user or throw IntegrityError exception.'''

    user = User.objects.create_user(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                email=request.POST['email'],
                username=request.POST['username'],
                password=request.POST['password'],
                is_staff=False)

    user.profile.bio = request.POST['bio']
    user.profile.credit_card = request.POST['cc']
    user.profile.is_gamer = True if 'gamer' in request.POST.keys() else False
    user.profile.save()

    return user


def get_action(request, action=''):
    '''
    Prepares action as a context key to be used in templates.
    action: 'welcome-g' -> user is authenticated as a gamer
    action: 'welcome' -> user is authenticated as a gambler
    '''

    if request.user.is_authenticated:
        action = 'welcome-g' if request.user.profile.is_gamer else 'welcome'

    return action


def delete_messages(limit, room_obj):

    messages = Message.objects.filter(room=room_obj)

    if messages.count() > limit:

        msg = Message.objects.earliest('created_at')
        msg.delete()


def save_messages(msg, user_obj, room_obj, del_limit=40):

    Message.objects.create(room=room_obj,
                           user=user_obj,
                           text=msg)

    delete_messages(del_limit, room_obj)


def prepare_messages(messages, acc=[]):
    '''
    Prepare Message objects to be passed as tuples containing
    the username and text (to be used templates).
    '''
    if not messages:
        return acc

    dc = {'name': messages[0].user.username,
          'txt': messages[0].text}

    return prepare_messages(messages[1:], [dc] + acc)


def validate_form(request, form_name=''):

    try:
        User.objects.get(username=request.POST['contender'],
                         profile__is_gamer=True)

    except User.DoesNotExist:
        return "Gamer doesn't exist. Try again."

    date_time = request.POST['date'] + ' ' + request.POST['time']

    if dt.now() > dt.strptime(date_time, '%Y-%m-%d %H:%M'):
        return "Invalid date-time. Try again."

    return 'OK'


def create_game(request):

    room = Room.objects.get(name=request.POST['room_name'])
    creator = User.objects.get(username=request.user.username)
    contender = User.objects.get(username=request.POST['contender'])

    date_time = request.POST['date'] + ' ' + request.POST['time']
    scheduled_at = dt.strptime(date_time, '%Y-%m-%d %H:%M')

    Game.objects.create(
        creator=creator,
        contender=contender,
        room=room,
        scheduled_at=scheduled_at,
        initial_bet=request.POST['bet'],
        status='P',
        video_game=request.POST['vg'],
        stream_link=request.POST['stream']
    )
