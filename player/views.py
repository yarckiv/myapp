from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.views.generic import ListView, TemplateView

from .models import Room, Music
from .forms import UserCreationForm, RoomAdd, MusicFormAdd, LoginForm


class Index(TemplateView):
    template_name = 'player/index.html'
    form_user = UserCreationForm()
    form_room = RoomAdd()
    form_login = LoginForm()

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        context = {'form_user': self.form_user, 'form_room': self.form_room, 'form_login': self.form_login}
        return context


def add_room(request):
    form_room = RoomAdd(request.POST)
    if form_room.is_valid():
        info = form_room.cleaned_data
        Room.objects.create(number_room=info['room_num'])
        return redirect('/pl/')

def registr_user(request):
    form_user = UserCreationForm(request.POST)
    if form_user.is_valid():
        user = form_user.cleaned_data
        form_user.save(user)
        reg = authenticate(username=user['username'], password=user['password'])
        login(request, reg)
        return render(request, 'player/main.html')


def login_user(request):
    username = request.POST['username']
    password = request.POST['password']
    log = authenticate(username=username, password=password)
    if log is not None and log.is_active:
        login(request, log)
        return render(request, 'player/main.html')
    else:
        return render(request, 'player/index.html')

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
