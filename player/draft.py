class Index(View):
    template_name = 'player/index.html'

    def get(self, request):
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
        return render(request, self.template_name, {'form_room': form_room, 'form_user': form_user, 'form_login': form_login})
