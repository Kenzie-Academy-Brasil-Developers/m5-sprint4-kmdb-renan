from email.policy import default
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class RecomendationChoices(models.Choices):
    MUST_WATCH = "Must Watch"
    SHOULD_WATCH = "Should Watch"
    AVOID_WATCH = "Avoid Watch"
    DEFAULT = "No Opinion"


class Review(models.Model):
    stars = models.PositiveIntegerField(default=10,
                                        validators=[MinValueValidator(1), MaxValueValidator(10)])
    review = models.TextField()
    spoilers = models.BooleanField(default=False)
    recomendation = models.CharField(
        max_length=50,
        choices=RecomendationChoices.choices,
        default=RecomendationChoices.DEFAULT
    )
    movie_id = models.ForeignKey(
        "movies.Movie",
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    critic = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="reviews"
    )
