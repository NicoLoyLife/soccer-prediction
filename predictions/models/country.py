from django.db import models
from django.utils.text import slugify


class Country(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name="Country Name", db_index=True)
    name_de = models.CharField(
        max_length=100, verbose_name="Country Name (German)", db_index=True
    )
    iso = models.CharField(
        max_length=2, verbose_name="ISO Code", help_text="ISO 3166-1 alpha-2 code"
    )
    iso_number = models.CharField(
        max_length=3, verbose_name="ISO Number", help_text="ISO 3166-1 numeric code"
    )
    slug = models.SlugField(
        max_length=100, verbose_name="Slug", db_index=True, unique=True
    )

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
