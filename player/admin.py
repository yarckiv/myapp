from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin

from .models import Room, UserProfile, Music
from .forms import UserCreationForm, UserChangeForm


class MusicInline(admin.TabularInline):
    model = Music


class MyUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('username', "first_name", 'last_name', 'email', 'is_staff')
    list_filter = ('is_superuser',)
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    filter_horizontal = ()
    fieldsets = (
        ('General', {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Room', {'classes': ('wide',),
                  'fields': ('room',)}),
    )
    # inlines = [
    #     MusicInline
    # ]
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password',),
        }),
    )


class RoomAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['number_room']}),
    ]

    inlines = [
        MusicInline
    ]


admin.site.register(UserProfile, MyUserAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.unregister(Group)
