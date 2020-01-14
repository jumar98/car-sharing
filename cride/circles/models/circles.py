
from django.db import models
from cride.utils.models import CSharingModel
import csv

class Circle(CSharingModel):

    name = models.CharField('circle name', max_length=140)
    slug_name = models.SlugField(unique=True, max_length=50)
    about = models.TextField('circle description')
    picture = models.ImageField(upload_to='circles/pictures', blank=True, null=True)
    rides_offered = models.PositiveIntegerField(default=0)
    rides_taken = models.PositiveIntegerField(default=0)
    is_verified = models.BooleanField(
        'verified circle',
        default=False,
        help_text='Verified circles that are known as official communities.' 
    )
    is_public = models.BooleanField(
        default=True,
        help_text='Public circles are listed in the main page to join it for everyone.'
    )
    is_limited = models.BooleanField(
        'limited',
        default=False,
        help_text='Limited circles can grow up to a fixed number of members.'
    )
    members_limit = models.PositiveIntegerField(
        default=0,
        help_text='If circle is limited, this will be the limit of members in the circle.'
    )

    def __str__(self):
        return self.name

    class Meta(CSharingModel.Meta):

        ordering = ['-rides_taken', '-rides_offered']

    def fill_circles(self):
        with open('circles.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            line_count = 0
            for row in csv_reader:
                Circle.objects.create(**row)