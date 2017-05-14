from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone


class Room(models.Model):
    number_room = models.IntegerField(verbose_name='# room')

    def __str__(self):
        return str(self.number_room)


class UserProfileManger(BaseUserManager):
    def create_user(self, username, password, room, email=None):
        if not username:
            raise ValueError('Users must have name')
        if not room:
            raise ValueError("Please specify a room's number")
        user = self.model(username=self.model.normalize_username(username), room=room)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, email=None):
        user = self.model(username=self.model.normalize_username(username),)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, default='0')
    first_name = models.CharField(max_length=10, blank=True)
    last_name = models.CharField(max_length=10, blank=True)
    email = models.EmailField(verbose_name='email address', blank=True)
    username = models.CharField(max_length=8, unique=True, error_messages={
            'unique': "This name busy, choose another name"
        }
    )
    is_superuser = models.BooleanField('superuser', default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['email']

    objects = UserProfileManger()

    def get_short_name(self):
        return self.first_name

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def has_module_perms(self, app_label):
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

    def has_perm(self, perm, obj=None):
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True


class Music(models.Model):
    title = models.CharField(max_length=13)
    link = models.URLField()
    author = models.ForeignKey(UserProfile, related_name='author')
    pub_date = models.DateField('date', default=timezone.now)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    vote = models.IntegerField(default=0)

    class Meta:
        unique_together = ('room', 'title')
