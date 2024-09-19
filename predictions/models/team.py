from django.db import models
from django.utils.text import slugify
from django.core.files import File
import requests
from io import BytesIO

from .country import Country
from .competition import Competition


class Team(models.Model):
    id = models.IntegerField(primary_key=True)  # ID von der API
    name = models.CharField(max_length=255, verbose_name="Team Name")
    clean_name = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Clean Name"
    )  # Bereinigter Teamname ohne Sonderzeichen
    english_name = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="English Name"
    )
    short_hand = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Short Hand"
    )
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, verbose_name="Country", related_name="teams"
    )  # Verknüpfung mit Country-Modell
    founded = models.IntegerField(
        null=True, blank=True, verbose_name="Founded Year"
    )  # Gründungsjahr
    image = models.URLField(
        max_length=500, verbose_name="Image URL"
    )  # Bild von externer API
    local_image = models.ImageField(
        upload_to="team_images/", null=True, blank=True, verbose_name="Local Image"
    )  # Lokales Bild
    flag_element = models.URLField(
        max_length=500, blank=True, null=True, verbose_name="Flag Element"
    )  # Flaggenbild
    url = models.URLField(max_length=500, verbose_name="URL")
    full_name = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Full Name"
    )
    alt_names = models.JSONField(
        verbose_name="Alternative Names", blank=True, null=True
    )
    official_sites = models.JSONField(
        verbose_name="Official Sites", blank=True, null=True
    )
    slug = models.SlugField(unique=False, blank=True, null=True)
    data_last_updated = models.DateTimeField(
        null=True, blank=True, verbose_name="Last Data Update"
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(
                self.clean_name or self.name
            )  # Fallback auf den Namen, falls clean_name nicht gesetzt ist

        # Bild von externer URL herunterladen und lokal speichern, falls noch nicht vorhanden
        if self.image and not self.local_image:
            response = requests.get(self.image)
            if response.status_code == 200:
                img_temp = BytesIO(response.content)
                self.local_image.save(f"{self.slug}.jpg", File(img_temp), save=False)

        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Teams"
        ordering = ["name"]


class TeamSeason(models.Model):
    team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="seasons", verbose_name="Team"
    )
    season = models.CharField(max_length=255, verbose_name="Season")
    clean_season = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Clean Season"
    )
    table_position = models.IntegerField(
        null=True, blank=True, verbose_name="Table Position"
    )
    performance_rank = models.IntegerField(
        null=True, blank=True, verbose_name="Performance Rank"
    )
    risk = models.IntegerField(null=True, blank=True, verbose_name="Risk")
    season_format = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Season Format"
    )
    competition = models.ForeignKey(
        Competition,
        on_delete=models.CASCADE,
        related_name="teams",
        verbose_name="Competition",
    )
    stats = models.JSONField(verbose_name="Stats", blank=True, null=True)

    def __str__(self):
        return f"{self.team.name} - {self.season}"

    class Meta:
        verbose_name_plural = "Team Seasons"
        ordering = ["team", "season"]
        constraints = [
            models.UniqueConstraint(
                fields=["team", "competition"], name="unique_team_competition"
            )
        ]
        indexes = [
            models.Index(fields=["team"]),
            models.Index(fields=["competition"]),
        ]
