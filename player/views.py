from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.views.generic import ListView, TemplateView

from .models import Room, Music
from .forms import UserCreationForm, RoomAdd, MusicFormAdd, LoginForm


class Index(TemplateView):
    template_name = 'player/index.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(
            form_user=UserCreationForm(),
            form_room=RoomAdd(),
            form_login=LoginForm()
        )
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form_login = LoginForm(request.POST, request=request) if 'login' in request.POST else LoginForm()
        form_login.is_valid()

        form_user = UserCreationForm(request.POST) if 'reg' in request.POST else UserCreationForm()
        if form_user.is_valid():
            form_user.save()
            messages.add_message(request, messages.INFO, 'User has been created')

        form_room = RoomAdd(request.POST if 'room' in request.POST else None)
        if form_room.is_valid():
            Room.objects.create(number_room=form_room.cleaned_data['room_num'])
            messages.add_message(request, messages.INFO, 'Room has been created')

        context = self.get_context_data(
            form_login=form_login,
            form_user=form_user,
            form_room=form_room
        )

        return self.render_to_response(context)


def add_room(request):
    form_room = RoomAdd(request.POST)
    if form_room.is_valid():
        info = form_room.cleaned_data
        Room.objects.create(number_room=info['room_num'])
        return redirect('player:player')


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


class Main(TemplateView):
    template_name = "player/main.html"
    template = 'player/index.html'


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
