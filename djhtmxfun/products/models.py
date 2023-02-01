from django.db import models


class Product(models.Model):
    class Status(models.IntegerChoices):
        ACTIVE = 1, "Active"
        INACTIVE = 2, "Inactive"
        ARCHIVED = 3, "Archived"

    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.PositiveSmallIntegerField(choices=Status.choices)

    class Meta:
        ordering = ("pk",)

    def __str__(self):
        return self.name
