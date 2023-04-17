import uuid

from django.db import models


class LegalEntity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=30)
    ogrn = models.CharField(max_length=13, unique=True)
    inn = models.CharField(max_length=11, unique=True)
    address = models.TextField(max_length=200)

    class Meta:
        abstract = True
        

class LegalInstitution(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=6)
    address = models.TextField(max_length=200)
    account = models.TextField(max_length=500, blank=True)

    class Meta:
        abstract = True


class Plaintiff(LegalEntity):
    def __str__(self):
        return self.short_name


class Defendant(LegalEntity):
    def __str__(self):
        return self.short_name


class Court(LegalInstitution):
    compensation = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    region_id = models.CharField(max_length=2)
    region_name = models.TextField(max_length=100)
    relevant_on = models.DateField()
    
    def __str__(self):
        return self.name
    
    
class AppealsCourt(LegalInstitution):
    def __str__(self):
        return self.name
    

class Case(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    number = models.CharField(max_length=30, blank=True, unique=True)
    court = models.ForeignKey(Court, on_delete=models.CASCADE)
    appeals_court = models.ForeignKey(AppealsCourt, on_delete=models.CASCADE, blank=True)
    card = models.URLField(max_length=200, blank=True, unique=True)
    plaintiff = models.ForeignKey(Plaintiff, on_delete=models.CASCADE)
    defendant = models.ForeignKey(Defendant, on_delete=models.CASCADE)
    overall_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    gp_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        unique_together = (
            'court', 'id'
        )

    def __str__(self):
        return f"{self.plaintiff.short_name} - {self.defendant.short_name}"
