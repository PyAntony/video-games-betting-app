
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render
from django.urls import reverse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.db import IntegrityError

from .models import Room, Game, Message

from . import helpers as hp

# to mark if a new message has been saved
NEW_SAVED_MSG = dict()


def index(request):

    if request.user.is_authenticated:

        action = hp.get_action(request)

        context = hp.get_context(action=action, msg='')
        return render(request, "rooms/index.html", context)

    context = hp.get_context(action='', msg='')
    return render(request, "rooms/index.html", context)


def register_view(request):

    if request.method == 'GET':
        return HttpResponseRedirect(reverse("index"))

    # If POST request
    try:
        user = hp.register_new_user(request)

        login(request, user)
        return HttpResponseRedirect(reverse("index"))

    except IntegrityError:

        msg = 'Username already exists. Try again.'
        context = hp.get_context(action='register-error', msg=msg)
        return render(request, "rooms/index.html", context)


def login_view(request):

    if request.method == 'GET':

        action = hp.get_action(request) + ' show-login'

        context = hp.get_context(action=action, msg='')
        return render(request, "rooms/index.html", context)

    # If POST request: try to authenticate
    user = authenticate(request,
                        username=request.POST['user'],
                        password=request.POST['pass'])

    # login user if it exists in database
    if user is not None:

        login(request, user)
        return HttpResponseRedirect(reverse("index"))

    # if invalid credentials
    else:

        msg = 'Invalid credentials. Try again.'
        context = hp.get_context(action='login-error', msg=msg)
        return render(request, "rooms/index.html", context)


@login_required
def logout_view(request):

    logout(request)
    return HttpResponseRedirect(reverse("index"))


@login_required
def create_room(request):

    if request.method == 'GET':
        return HttpResponseRedirect(reverse("index"))

    try:
        Room.objects.create(user=request.user,
                            name=request.POST['room_name'],
                            description=request.POST['room_desc'])

        return HttpResponseRedirect(reverse("index"))

    except IntegrityError:

        msg = 'Room name exists. Try again.'
        action = hp.get_action(request) + ' create_room-error'

        context = hp.get_context(action=action, msg=msg)
        return render(request, "rooms/index.html", context)


@login_required
def show_my(request, obj_type):

    objects, command = '', ''

    if obj_type == 'rooms':
        objects = hp.get_rooms(id=request.user.id)
        command = 'show-my-rooms'

    if obj_type == 'games':
        objects = Game.objects.filter(creator__id=request.user.id)
        command = 'show-my-games'

    context = hp.get_context(action='welcome-g ' + command,
                             my_objects=objects,
                             msg='')

    return render(request, "rooms/index.html", context)


def filter_rooms(request):

    if request.method == 'POST':

        field = request.POST['field-selected']
        value = request.POST['exact-match']

        rooms = hp.get_rooms('', field, value)
        msg = 'No rooms found.' if not rooms else ''

        context = hp.get_context(action=hp.get_action(request),
                                 rooms=rooms,
                                 msg=msg)

        return render(request, "rooms/index.html", context)

    # If GET request
    return HttpResponseRedirect(reverse("index"))


def sort_rooms(request):

    if request.method == 'POST':

        field = request.POST['field-selected']
        order = '-' if request.POST['order'] == 'desc' else ''
        size = int(request.POST['len'])

        rooms = Room.objects.order_by(order + field)[:size]

        context = hp.get_context(action=hp.get_action(request),
                                 rooms=rooms,
                                 msg='')

        return render(request, "rooms/index.html", context)

    # If GET request
    return HttpResponseRedirect(reverse("index"))


def room_view(request, room_name):

    err_msg = ''
    if '_validation_error_' in room_name:

        err_msg = room_name.split('_validation_error_')[1]
        room_name = room_name.split('_validation_error_')[0]

    msgs = Message.objects.filter(room__name=room_name).order_by('-created_at')
    games = Game.objects.filter(room__name=room_name)
    room_obj = Room.objects.get(name=room_name)

    context = hp.get_context(action=hp.get_action(request),
                             messages=hp.prepare_messages(msgs),
                             room_name=room_name,
                             username=request.user.username,
                             video_games=list(Game.GAMES_AVAILABLE),
                             games=games,
                             stream='',
                             validation_msg=err_msg,
                             admin=room_obj.user.username)

    return render(request, "rooms/room.html", context)


@login_required
def save_message(request):

    if request.method == 'POST':

        msg = request.POST['msg']
        room_name = request.POST['room_name']
        room_obj = hp.get_rooms('', 'name', room_name)[0]

        hp.save_messages(msg, request.user, room_obj)
        NEW_SAVED_MSG[room_name] = True

        return HttpResponseRedirect(
            reverse("room_view", kwargs={'room_name': room_name})
        )


@login_required
def delete_room(request, room_name):

    Room.objects.get(name=room_name).delete()

    return HttpResponseRedirect(reverse("index"))


@login_required
def create_game(request):

    if request.method == 'POST':

        room_name = request.POST['room_name']
        msg = hp.validate_form(request)

        if msg == 'OK':
            hp.create_game(request)
        else:
            room_name = room_name + '_validation_error_' + msg

        return HttpResponseRedirect(
            reverse("room_view", kwargs={'room_name': room_name})
        )

    # If GET request
    return HttpResponseRedirect(reverse("index"))


def chat_post(request):

    if request.method == "POST":

        msg = request.POST['chat_msg']
        room_name = request.POST['chat_room']
        room_obj = hp.get_rooms('', 'name', room_name)[0]

        hp.save_messages(msg, request.user, room_obj)
        NEW_SAVED_MSG[room_name] = True

        response = {'msg': msg, 'username': request.user.username}
        return JsonResponse(response)

    # If NOT Post
    return HttpResponse('Request must be POST.')


def messages_ajax(request, room_name):

    found = room_name in NEW_SAVED_MSG.keys()

    if found and NEW_SAVED_MSG[room_name]:

        msgs = Message.objects.filter(room__name=room_name)
        messages = hp.prepare_messages(msgs.order_by('-created_at'))

        NEW_SAVED_MSG[room_name] = False

        context = {
            'username': request.user.username,
            'messages': messages
        }

        return render(request, 'rooms/messages_ajax.html', context)

    # If NO messages found
    return HttpResponse('No new messages.')

