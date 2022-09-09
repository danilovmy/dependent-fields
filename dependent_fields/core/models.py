from django.db import models


class Country(models.Model):

    name = models.CharField(max_length=255)

    def __str__(self, *args, **kwargs):
        return self.name or self.pk or super().__str__(*args, **kwargs)


class Region(models.Model):

    name = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True,)

    def __str__(self, *args, **kwargs):
        return self.name or self.pk or super().__str__(*args, **kwargs)


class Product(models.Model):

    name = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True,)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True,)

    def __str__(self, *args, **kwargs):
        return self.name or self.pk or super().__str__(*args, **kwargs)