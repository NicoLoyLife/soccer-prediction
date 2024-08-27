from django.db import models
from django.utils.text import slugify
from django.core.files import File
import requests
from io import BytesIO


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


class League(models.Model):
    name = models.CharField(max_length=100, verbose_name="League Name", db_index=True)
    full_name = models.CharField(
        max_length=100, verbose_name="Full League Name", db_index=True, unique=True
    )
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        verbose_name="Country",
        db_index=True,
        related_name="leagues",
    )
    image = models.URLField(max_length=500, verbose_name="Image URL")
    local_image = models.ImageField(
        upload_to="league_images/", null=True, blank=True, verbose_name="Local Image"
    )
    season = models.JSONField(verbose_name="Season Information")
    slug = models.SlugField(
        unique=False, max_length=100, verbose_name="Slug", db_index=True
    )
    matches_last_updated = models.DateTimeField(
        verbose_name="Matches Last Updated", null=True, blank=True
    )

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        # Setze den vollständigen Namen der Liga, falls dieser nicht bereits gesetzt ist
        if not self.full_name:
            self.full_name = f"{self.country.country_name} {self.name}"

        # Slug ohne den Länderteil des Namens generieren
        self.slug = slugify(self.name)

        # Logo von externer URL herunterladen und lokal speichern, falls noch nicht vorhanden
        if self.image and not self.local_image:
            response = requests.get(self.image)
            if response.status_code == 200:
                img_temp = BytesIO(response.content)
                self.local_image.save(f"{self.slug}.png", File(img_temp), save=False)

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "League"
        verbose_name_plural = "Leagues"
        ordering = ["full_name"]
