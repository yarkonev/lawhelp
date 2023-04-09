from django.db import models


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
    

class Defendant(LegalEntity):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    
class Court(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField(max_length=200)    