from rest_framework import viewsets, mixins
from rest_framework.generics import get_object_or_404
from cride.circles.models import Circle, Membership
from cride.circles.serializers.memberships import MembershipModelSerializer

class MembershipViewSet(mixins.ListModelMixin,
                        viewsets.GenericViewSet
                        ):

    serializer_class = MembershipModelSerializer

    def dispatch(self, request, *args, **kwargs):
        slug_name = kwargs.get('slug_name')
        self.circle = get_object_or_404(Circle, slug_name=slug_name)
        return super(MembershipViewSet, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Membership.objects.filter(
            circle=self.circle,
            is_active=True
        )