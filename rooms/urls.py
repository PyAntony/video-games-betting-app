
from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register_view, name="register_view"),
    path("login", views.login_view, name="login_view"),
    path("logout", views.logout_view, name="logout_view"),
    path("create_room", views.create_room, name="create_room"),
    path("show_my/<str:obj_type>", views.show_my, name="show_my"),
    path("filter_rooms", views.filter_rooms, name="filter_rooms"),
    path("sort_rooms", views.sort_rooms, name="sort_rooms"),
    path("room_view/<str:room_name>", views.room_view,
         name="room_view"),
    path("save_message", views.save_message, name="save_message"),
    path("delete_room/<str:room_name>", views.delete_room,
         name="delete_room"),
    path("create_game", views.create_game, name="create_game"),
    path("chat_post/", views.chat_post, name="chat_post"),
    path("messages_ajax/<str:room_name>", views.messages_ajax,
         name="messages_ajax")
]
