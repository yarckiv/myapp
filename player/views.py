from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.views.generic import ListView

from .models import Room, Music
from .forms import UserCreationForm, RoomAdd, MusicFormAdd, LoginForm


def index(request):
    template_name = 'player/index.html'
    success_url = 'player/main.html'
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
            reg = authenticate(username=user['username'], password=user['password'])
            login(request, reg)
            return render(request, success_url)
    if 'login' in request.POST:
        form_login = LoginForm(request.POST)
        if form_login.is_valid():
            log_info = form_login.cleaned_data
            log = authenticate(username=log_info['username'], password=log_info['password'])
            if log is not None and log.is_active:
                login(request, log)
                return render(request, success_url)
    return render(request, template_name, {'form_room': form_room, 'form_user': form_user, 'form_login': form_login})


def main(request, main):
    template_name = "player/main.html"
    template = 'player/index.html'
    if not request.user.is_authenticated:
        return render(request, template)
    else:
        return render(request, template_name)


def addmusic(request):
    template_name = 'player/add_music.html'
    form = MusicFormAdd()
    author = request.user
    if 'add' in request.POST:
        form = MusicFormAdd(request.POST)
        if form.is_valid():
            info = form.cleaned_data
            title = info['title']
            link = info['link']
            message = "You successfully added song {0} from {1}".format(title, link)
            music = Music(title=title, link=link, author=author, room=author.room)
            music.save()
            return render(request, template_name, {'message': message})
    return render(request, template_name, {'form': form, "author": author})


class allMusic(ListView):
    context_object_name = 'allmusic'
    template_name = 'player/allmusic.html'

    def get_queryset(self):
        return Music.objects.filter(room__number_room=str(self.request.user.room))
