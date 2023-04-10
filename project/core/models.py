from django.db import models

import uuid


class LegalEntity(models.Model):
    full_name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=30)
    ogrn = models.CharField(max_length=13)
    inn = models.CharField(max_length=11)
    address = models.TextField(max_length=200)

    class Meta:
        abstract = True


class Plaintiff(LegalEntity):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.short_name


class Defendant(LegalEntity):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.short_name


class Court(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField(max_length=200)

    def __str__(self):
        return self.name


class Case(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    number = models.CharField(max_length=30)
    court = models.ForeignKey(Court, on_delete=models.CASCADE)
    card = models.URLField(max_length=200, blank=True)
    plaintiff = models.ForeignKey(Plaintiff, on_delete=models.CASCADE)
    defendant = models.ForeignKey(Defendant, on_delete=models.CASCADE)

    def __str__(self):
        return self.number
