from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.utils import timezone
from django.views.generic import ListView

from .models import Room, Music, UserProfile
from .forms import UserCreationForm, RoomAdd, MusicFormAdd, LoginForm

template = 'player/index.html'
success_url = 'player/main.html'

def logout(request):
    logout(request)
    return render(request, template)


def index(request):
    error_mes = 'User not exist'
    form_user = UserCreationForm()
    form_room = RoomAdd()
    form_login = LoginForm()
    if 'room' in request.POST:
        form_room = RoomAdd(request.POST)
        if form_room.is_valid():
            info = form_room.cleaned_data
            Room.objects.create(number_room=info['room_num'])
    if 'reg' in request.POST:
        form_user = UserCreationForm(request.POST)
        if form_user.is_valid():
            user = form_user.cleaned_data
            form_user.save(user)
            return render(request, success_url, {'user': user})
    if 'login' in request.POST:
        form_login = LoginForm(request.POST)
        if form_login.is_valid():
            log_info = form_login.cleaned_data
            log = authenticate(username=log_info['username'], password=log_info['password'])
            if log is not None and log.is_active:
                login(request, log)
                return render(request, success_url, {'user': log_info, 'log': log})

    return render(request, template, {'form_room': form_room, 'form_user': form_user, 'form_login': form_login})


class Main(ListView):
    model = Music
    template_name = 'player/main.html'
    context_object_name = 'musics'


# def main(request, main):
#     music_form = MusicFormAdd()
#     # info = request.REQUEST
#     if 'add' in request.POST:
#         music_form = MusicFormAdd(request.POST)
#         if music_form.is_valid():
#             song = music_form.cleaned_data
#             # w = Music (title=song['title'], link=song['link'], author=user, pub_date=timezone.now(), room=room)
#             # w.save()
#             return render(request, template, {'song': song})

    # return render(request, template, {'music_form': music_form})

