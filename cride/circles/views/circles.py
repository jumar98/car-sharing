from rest_framework import viewsets
from cride.circles.models import Circle
from cride.circles.serializers import CircleModelSerializer

class CircleViewSet(viewsets.ModelViewSet):

    queryset = Circle.objects.all()
    serializer_class = Circle