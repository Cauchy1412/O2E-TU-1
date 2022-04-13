from django.db import models
from .user import User
from .paper import Paper
from .interpretation import Interpretation
from .notation import Notation

# updating types
PUB_PAP = 0  # published a new paper
PUB_INTER = 1  # published a new interpretation on paper
PUB_NOTAT = 2  # published a new notation on paper
FWD_INTER = 3  # foward an interpretation

UPDATING_TYPE_CHOICES = (
    (PUB_PAP, 'Publish Paper'),
    (PUB_INTER, 'Publish Interpretation'),
    (PUB_NOTAT, 'Publish Notation'),
    (FWD_INTER, 'Foward Interpretation'),
)

class Updating(models.Model):

    updating_type = models.IntegerField(choices=UPDATING_TYPE_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updates')

    # optionals
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE, related_name='+', blank=True)
    interpretation = models.ForeignKey(Interpretation, on_delete=models.CASCADE, related_name='+', blank=True)
    notation = models.ForeignKey(Notation, on_delete=models.CASCADE, related_name='+', blank=True)
