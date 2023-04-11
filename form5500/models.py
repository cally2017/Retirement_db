from django.db import models

# Create your models here.
class Form5500(models.Model):
    Sponsor_Name = models.CharField(("Sponsor_Name"), max_length=255)
    Sponsor_Street = models.CharField(("Sponsor_Street"), max_length=100)
    Sponsor_City = models.CharField(("Sponsor_City"), max_length=100)
    Sponsor_State = models.CharField(("Sponsor_State"), max_length=2)
    Sponsor_Zipcode = models.CharField(("Sponsor_Zipcode"), max_length=5)
    EIN = models.CharField(("EIN"), max_length=20)
    Participants = models.IntegerField("Participants")
    Plan_Asset = models.BigIntegerField("Plan_Asset")
    Broker_Name = models.CharField(("Broker_Name"), max_length=255)
    Provider_Name = models.CharField(("Provider_Name"), max_length=255)
    Industry_Description = models.CharField(("Industry_Description"), max_length=100)