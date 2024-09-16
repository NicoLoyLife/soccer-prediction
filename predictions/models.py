from django.db import models
from django.utils.text import slugify
from django.core.files import File
from django.core.validators import MinValueValidator, MaxValueValidator
import requests
from io import BytesIO
from django.db.models import Q
from django.utils import timezone


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


class Competition(models.Model):
    id = models.IntegerField(primary_key=True)  # ID von der API
    tsapi_id = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="TSAPI ID"
    )  # Optionales API-spezifisches ID-Feld
    name = models.CharField(
        max_length=255, verbose_name="Competition Name"
    )  # Wettbewerbstitel
    league = models.ForeignKey(
        "League",
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
        "Competition",
        on_delete=models.CASCADE,
        related_name="teams",
        verbose_name="Competition",
    )
    stats = models.JSONField(verbose_name="Stats", blank=True, null=True)

    def __str__(self):
        return f"{self.team.name} - {self.season}"

    def get_next_match(self):
        """
        Diese Methode gibt das nächste Match des Teams zurück.
        """
        next_match = (
            Match.objects.filter(
                Q(hometeam=self.team) | Q(awayteam=self.team),
                date_unix__gte=int(timezone.now().timestamp()),
                competition=self.competition,
            )
            .select_related("hometeam", "awayteam", "competition")
            .order_by("date_unix")
            .first()
        )

        return next_match

    def get_previous_match(self):
        """
        Diese Methode gibt das vorherige Match des Teams zurück.
        """
        previous_match = (
            Match.objects.filter(
                Q(hometeam=self.team) | Q(awayteam=self.team),
                date_unix__lt=int(timezone.now().timestamp()),
                competition=self.competition,
            )
            .select_related("hometeam", "awayteam", "competition")
            .order_by("-date_unix")
            .first()
        )

        return previous_match

    def get_all_matches(self):
        """
        Diese Methode gibt alle Matches des Teams zurück, optional gefiltert nach einer spezifischen Competition.
        """
        matches = (
            Match.objects.filter(
                Q(hometeam=self.team) | Q(awayteam=self.team),
                competition=self.competition,
            )
            .select_related("hometeam", "awayteam", "competition")
            .order_by("date_unix")
        )
        return matches

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


class Match(models.Model):
    id = models.IntegerField(primary_key=True)  # ID aus der API
    competition = models.ForeignKey(
        "Competition",
        on_delete=models.CASCADE,
        related_name="matches",
        verbose_name="Competition",
    )
    hometeam = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="home_matches",
        verbose_name="Home Team",
    )
    awayteam = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="away_matches",
        verbose_name="Away Team",
    )
    date_unix = models.IntegerField(null=True, blank=True, verbose_name="Date Unix")
    season = models.CharField(max_length=255, verbose_name="Season")
    status = models.CharField(
        max_length=255, verbose_name="Status", null=True, blank=True
    )
    game_week = models.IntegerField(null=True, blank=True, verbose_name="Game Week")

    # Match result fields
    home_goals = models.IntegerField(null=True, blank=True, verbose_name="Home Goals")
    away_goals = models.IntegerField(null=True, blank=True, verbose_name="Away Goals")
    total_goals = models.IntegerField(null=True, blank=True, verbose_name="Total Goals")

    # Match statistics in JSON (consolidated stats)
    match_stats = models.JSONField(null=True, blank=True, verbose_name="Match Stats")
    team_a_stats = models.JSONField(null=True, blank=True, verbose_name="Team A Stats")
    team_b_stats = models.JSONField(null=True, blank=True, verbose_name="Team B Stats")

    # Odds (consolidated in JSON)
    odds = models.JSONField(null=True, blank=True, verbose_name="Odds Data")

    # Attendance and stadium information
    attendance = models.IntegerField(null=True, blank=True, verbose_name="Attendance")
    stadium_name = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Stadium Name"
    )
    stadium_location = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Stadium Location"
    )

    slug = models.SlugField(unique=True, blank=True, null=True, max_length=255)

    def __str__(self):
        return f"{self.hometeam.name} vs {self.awayteam.name} - {self.season}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(
                f"{self.hometeam.name} vs {self.awayteam.name} {self.date_unix}"
            )
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Matches"
        ordering = ["date_unix"]
        indexes = [
            models.Index(fields=["competition"]),
            models.Index(fields=["hometeam"]),
            models.Index(fields=["awayteam"]),
            models.Index(fields=["season"]),
        ]


class MatchFeatures(models.Model):
    match = models.OneToOneField(
        Match, on_delete=models.CASCADE, related_name="features", verbose_name="Match"
    )

    # Played matches
    hmpo = models.IntegerField(
        null=True, blank=True, verbose_name="Home Matches Played Overall"
    )
    hmph = models.IntegerField(
        null=True, blank=True, verbose_name="Home Matches Played Home"
    )
    ampo = models.IntegerField(
        null=True, blank=True, verbose_name="Away Matches Played Overall"
    )
    ampa = models.IntegerField(
        null=True, blank=True, verbose_name="Away Matches Played Away"
    )
    h2hmp = models.IntegerField(
        null=True, blank=True, verbose_name="H2H Matches Played"
    )

    # Goals and averages
    hga = models.FloatField(null=True, blank=True, verbose_name="Home Goals Average")
    aga = models.FloatField(null=True, blank=True, verbose_name="Away Goals Average")
    hgaa = models.FloatField(
        null=True, blank=True, verbose_name="Home Goals Against Average"
    )
    agaa = models.FloatField(
        null=True, blank=True, verbose_name="Away Goals Against Average"
    )
    hxga = models.FloatField(
        null=True, blank=True, verbose_name="Home Expected Goals Average"
    )
    axga = models.FloatField(
        null=True, blank=True, verbose_name="Away Expected Goals Average"
    )
    hxgaa = models.FloatField(
        null=True, blank=True, verbose_name="Home Expected Goals Against Average"
    )
    axgaa = models.FloatField(
        null=True, blank=True, verbose_name="Away Expected Goals Against Average"
    )

    # Possession
    hpa = models.FloatField(
        null=True, blank=True, verbose_name="Home Possession Average"
    )
    apa = models.FloatField(
        null=True, blank=True, verbose_name="Away Possession Average"
    )

    # Wins, draws, and losses
    hw = models.FloatField(null=True, blank=True, verbose_name="Home Wins")
    aw = models.FloatField(null=True, blank=True, verbose_name="Away Wins")
    hd = models.FloatField(null=True, blank=True, verbose_name="Home Draws")
    ad = models.FloatField(null=True, blank=True, verbose_name="Away Draws")
    hl = models.FloatField(null=True, blank=True, verbose_name="Home Losses")
    al = models.FloatField(null=True, blank=True, verbose_name="Away Losses")

    # Shots
    hsota = models.FloatField(
        null=True, blank=True, verbose_name="Home Shots on Target Average"
    )
    asota = models.FloatField(
        null=True, blank=True, verbose_name="Away Shots on Target Average"
    )
    hsoffta = models.FloatField(
        null=True, blank=True, verbose_name="Home Shots off Target Average"
    )
    asoffta = models.FloatField(
        null=True, blank=True, verbose_name="Away Shots off Target Average"
    )

    # Goals in last 5 matches
    agl5h = models.FloatField(
        null=True, blank=True, verbose_name="Average Goals Last 5 Matches Home"
    )
    agl5a = models.FloatField(
        null=True, blank=True, verbose_name="Average Goals Last 5 Matches Away"
    )

    # Head-to-head (H2H) stats
    agh2h = models.FloatField(
        null=True, blank=True, verbose_name="Average Goals in H2H Matches"
    )
    bttsh2h = models.FloatField(
        null=True, blank=True, verbose_name="BTTS in H2H Matches"
    )
    ach2h = models.FloatField(
        null=True, blank=True, verbose_name="Average Corners in H2H Matches"
    )

    # Team form (recent performance)
    tfhw = models.FloatField(null=True, blank=True, verbose_name="Teamform Home Wins")
    tfhd = models.FloatField(null=True, blank=True, verbose_name="Teamform Home Draws")
    tfhl = models.FloatField(null=True, blank=True, verbose_name="Teamform Home Losses")
    tfaw = models.FloatField(null=True, blank=True, verbose_name="Teamform Away Wins")
    tfad = models.FloatField(null=True, blank=True, verbose_name="Teamform Away Draws")
    tfal = models.FloatField(null=True, blank=True, verbose_name="Teamform Away Losses")

    def __str__(self):
        return f"{self.match.hometeam.name} vs {self.match.awayteam.name} - {self.match.season}"

    class Meta:
        verbose_name_plural = "Match Features"
        ordering = ["match"]
        indexes = [
            models.Index(fields=["match"]),
        ]
