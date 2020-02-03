from rest_framework.permissions import BasePermission
from cride.circles.models.memberships import Membership

class IsActiveCircleMember(BasePermission):

    def has_permission(self, request, view):
        circle = view.circle
        try:
            Membership.objects.get(
                user=request.user,
                circle=view.circle,
                is_active=True
            )
        except Membership.DoesNotExist:
            return False
        return True