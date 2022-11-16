import os
import random
from string import ascii_lowercase

from django.db import models
from django.dispatch import receiver


class Client(models.Model):

    class Sex(models.TextChoices):
        FEMALE = ('F', 'Женщина')
        MALE = ('M', 'Мужчина')

    born = models.DateField('Родился')
    sex = models.CharField('Пол', max_length=1, choices=Sex.choices)
    photo = models.ForeignKey('ClientsPhoto', on_delete=models.SET_DEFAULT, null=True, blank=True,
                              default=None, related_name='client', verbose_name='Фото')
    f_name = models.CharField('Имя', max_length=256)
    l_name = models.CharField('Фамилия', max_length=256)
    created = models.DateTimeField('Создано', auto_now_add=True)
    updated = models.DateTimeField('Обновлено', auto_now=True)

    def save(self, **kwargs):
        super().save(**kwargs)
        if not self._state.adding:
            ClientsPhoto.objects.filter(client__isnull=True).prefetch_related('client').all().delete()


@receiver([models.signals.post_delete, models.signals.post_save], sender=Client)
def auto_delete_client_photos_on_change(**kwargs):
    """
    Удаление записей в модели ClientsPhoto которые не имеют связи c Client
    """
    ClientsPhoto.objects.filter(client__isnull=True).prefetch_related('client').all().delete()


def clients_photo_path(instance, filename):
    img_name = ''.join(random.choice(ascii_lowercase) for _ in range(16))
    img_ext = filename.split('.')[-1]
    return f"clients_photo/{img_name}.{img_ext}"


class ClientsPhoto(models.Model):
    file = models.ImageField('Файл', upload_to=clients_photo_path)
    created = models.DateTimeField('Создано', auto_now_add=True)
    updated = models.DateTimeField('Обновлено', auto_now=True)


@receiver(models.signals.post_delete, sender=ClientsPhoto)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Физическое удаление файла при удалении его записи в БД
    """
    if os.path.exists(instance.file.path) and os.path.isfile(instance.file.path):
        os.remove(instance.file.path)
