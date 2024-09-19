from django.db import models
from django.utils.text import slugify
from django.core.files import File
from django.core.validators import MinValueValidator, MaxValueValidator
import requests
from io import BytesIO

from .league import League


class Competition(models.Model):
    id = models.IntegerField(primary_key=True)  # ID von der API
    tsapi_id = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="TSAPI ID"
    )  # Optionales API-spezifisches ID-Feld
    name = models.CharField(
        max_length=255, verbose_name="Competition Name"
    )  # Wettbewerbstitel
    league = models.ForeignKey(
        League,
        on_delete=models.CASCADE,
        related_name="competitions",
        verbose_name="League",
    )  # Beziehung zu League
    domestic_scale = models.IntegerField(
        null=True, blank=True, verbose_name="Domestic Scale"
    )  # Skala für nationalen Wettbewerb
    international_scale = models.IntegerField(
        null=True, blank=True, verbose_name="International Scale"
    )  # Skala für internationalen Wettbewerb
    status = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Status"
    )  # Wettbewerbsstatus
    format = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Format"
    )  # Format des Wettbewerbs
    division = models.IntegerField(
        null=True, blank=True, verbose_name="Division"
    )  # Ligadivision
    no_home_away = models.BooleanField(
        default=False, verbose_name="No Home and Away", null=True, blank=True
    )  # Kein Heim/Auswärtsspiel
    starting_year = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1900), MaxValueValidator(2100)],
        verbose_name="Starting Year",
    )  # Startjahr
    ending_year = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1900), MaxValueValidator(2100)],
        verbose_name="Ending Year",
    )  # Endjahr
    women = models.BooleanField(
        default=False, verbose_name="Women's Competition"
    )  # Frauenwettbewerb
    continent = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Continent"
    )  # Kontinent
    comp_master_id = models.IntegerField(
        null=True, blank=True, verbose_name="Competition Master ID"
    )  # Master ID des Wettbewerbs
    image = models.URLField(
        max_length=500, verbose_name="Image URL"
    )  # Bild von externer API
    local_image = models.ImageField(
        upload_to="competition_images/",
        null=True,
        blank=True,
        verbose_name="Local Image",
    )  # Lokale Bildspeicherung
    shortHand = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Short Hand"
    )  # Abkürzung des Wettbewerbs
    iso = models.CharField(
        max_length=14, blank=True, null=True, verbose_name="ISO"
    )  # ISO-Code des Landes
    type = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Type"
    )  # Typ des Wettbewerbs
    footystats_url = models.URLField(
        max_length=500, blank=True, null=True, verbose_name="Footystats URL"
    )  # URL zu Footystats
    season = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Season"
    )  # Saisoninformationen
    slug = models.SlugField(
        unique=False, blank=True, null=True
    )  # Slug für SEO und URLs
    matches_last_updated = models.DateTimeField(
        null=True, blank=True, verbose_name="Matches Last Updated"
    )  # Letztes Update der Spiele
    matchdetails_last_updated = models.DateTimeField(
        null=True, blank=True, verbose_name="Match Details Last Updated"
    )  # Letztes Update der Spieldetails

    def __str__(self):
        return f"{self.name} - {self.season}"

    def save(self, *args, **kwargs):
        # Slug ohne "/" im Saisonfeld generieren
        if self.season:
            self.slug = slugify(self.season.replace("/", "-"))

        # Bild von externer URL herunterladen und lokal speichern, falls noch nicht vorhanden
        if self.image and not self.local_image:
            response = requests.get(self.image)
            if response.status_code == 200:
                image_temp = BytesIO(response.content)
                self.local_image.save(f"{self.slug}.jpg", File(image_temp), save=False)

        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Competitions"
        ordering = ["season", "name"]
