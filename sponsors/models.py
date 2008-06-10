from django.db import models

# Create your models here.
LEVEL_CHOICES = (
    ('Diamond', 'Diamond'),
    ('Sapphire', 'Sapphire'),
    ('Emerald', 'Emerald'),
    ('General', 'General'),
)

class Level(models.Model):
    name = models.CharField(max_length=150,choices=LEVEL_CHOICES, db_index=True)
    order = models.IntegerField(default=10)

    def __unicode__(self):
        return self.name

    class Admin:
        list_display = ('name', 'order')

class Sponsor(models.Model):
    company = models.CharField(max_length=150)
    contact = models.CharField(max_length=150)
    email = models.EmailField(blank=True,null=True)
    url = models.CharField(max_length=250)
    about = models.TextField(blank=True,null=True)
    level = models.ForeignKey(Level,blank=True,null=True)
    sm_logo = models.CharField(max_length=255,blank=True,null=True)
    lg_logo = models.CharField(max_length=255,blank=True,null=True)

    class Admin:
        list_display = ('company', 'contact', 'level')
