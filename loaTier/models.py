from django.db import models
# class clientInfo(models.Model):
#     """A typical class defining a model, derived from the Model class."""

class Tier(models.Model):
    """A typical class defining a model, derived from the Model class."""
    # Fields
    rname = models.TextField()
    tier1 = models.TextField()
    tier2 = models.TextField()
    tier3 = models.TextField()
    tier4 = models.TextField()
    tier5 = models.TextField()
    tierout = models.TextField()

    @property
    def pk(self):
        return self.id
