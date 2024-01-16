from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone
from django.core.validators import MinLengthValidator
from django.contrib.sites.models import Site

from django.contrib.auth import get_user_model

User = get_user_model()

import uuid
import string

BASE62_CHARS = string.ascii_letters + string.digits
BASE62_BASE = len(BASE62_CHARS)

def encode_base62(number):
    result = ''
    while number > 0:
        number, remainder = divmod(number, BASE62_BASE)
        result = BASE62_CHARS[remainder] + result
    return result or BASE62_CHARS[0]

def decode_base62(encoded):
    result = 0
    for char in encoded:
        result = result * BASE62_BASE + BASE62_CHARS.index(char)
    return result


class DateTimeModel(models.Model):
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    deleted_at = models.DateTimeField(blank = True, null = True)

    class Meta:
        abstract = True

    def delete(self, hard = False, *args, **kwargs):
        if hard:
            super(DateTimeModel, self).delete(*args, **kwargs)
        else:    
            self.deleted_at = timezone.now()
            super(DateTimeModel, self).save(*args, **kwargs)


class ExpirationManager(models.Manager):

    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(expiration_date__gt=timezone.now())


class ShortURL(DateTimeModel):
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    original_url = models.URLField()
    short_part = models.CharField(max_length=20, blank=True, null=True)
    expiration_date = models.DateTimeField(null=True, blank=True)
    qr = models.ImageField(blank=True, null=True, upload_to='qr/')
    short_url = models.CharField(blank=True, null=True, max_length=400)

    objects = ExpirationManager()
    

    def is_expired(self):
        return self.expiration_date and self.expiration_date < timezone.now()
    
    def save(self, *args, **kwargs):
        if not self.short_part:
            unique_id = uuid.uuid4().int
            self.short_part = encode_base62(unique_id)
            while ShortURL.objects.filter(short_part=self.short_part).exists():
                unique_id = uuid.uuid4().int
                self.short_part = encode_base62(unique_id)

        current_site = Site.objects.get_current()
        self.short_url = f"http://{current_site.domain}/{self.short_part}/"

        if not self.expiration_date:
            self.expiration_date = timezone.now().date() + timezone.timedelta(days=3)

        super().save(*args, **kwargs)




    def __str__(self):
        return f"{self.original_url} -> {self.short_part}"


    class Meta:
        ordering = ('-created_at',)
