from django.db import models
from django.utils.text import slugify

from .team import Team
from .competition import Competition


class Match(models.Model):
    id = models.IntegerField(primary_key=True)  # ID aus der API
    competition = models.ForeignKey(
        Competition,
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
