from rest_framework import viewsets, mixins
from rest_framework.generics import get_object_or_404
from cride.circles.models import Circle, Membership
from cride.circles.serializers.memberships import MembershipModelSerializer
from rest_framework.permissions import IsAuthenticated
from cride.circles.permissions.memberships import IsActiveCircleMember

class MembershipViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet
                        ):

    serializer_class = MembershipModelSerializer

    def dispatch(self, request, *args, **kwargs):
        slug_name = kwargs.get('slug_name')
        self.circle = get_object_or_404(Circle, slug_name=slug_name)
        return super(MembershipViewSet, self).dispatch(request, *args, **kwargs)

    def get_permissions(self):
        permission = [IsAuthenticated, IsActiveCircleMember]
        return [p() for p in permission]

    def get_queryset(self):
        return Membership.objects.filter(
            circle=self.circle,
            is_active=True
        )

    def get_object(self):
        return get_object_or_404(
            Membership,
            user__username=self.kwargs.get('pk'),
            circle=self.circle,
            is_active=True
        )

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()