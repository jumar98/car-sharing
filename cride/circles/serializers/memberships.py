from rest_framework import serializers
from cride.circles.models.memberships import Membership
from cride.circles.models.invitations import Invitation
from cride.users.serializers import UserModelSerializer
from django.utils import timezone

class MembershipModelSerializer(serializers.ModelSerializer):

    joined_at = serializers.DateTimeField(source='created', read_only=True)
    user = UserModelSerializer(read_only=True)
    invited_by = serializers.StringRelatedField()

    class Meta:

        model = Membership
        fields = (
            'user',
            'is_admin', 'is_active',
            'used_invitation', 'remaining_invitation',
            'invited_by', 'rides_taken', 'rides_offered',
            'joined_at'
        )
        read_only_fields = (
            'user',
            'used_invitation',
            'invited_by',
            'rides_taken', 'rides_offered'
        )

class AddMemberSerializer(serializers.Serializer):

    invitation_code = serializers.CharField(min_length=8)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_user(self, data):
        circle = self.context['circle']
        user = data
        query = Membership.objects.filter(circle=circle, user=user)
        if query.exists():
            raise serializers.ValidationError('User is already a register member.')

    def validate_invitation_code(self, data):
        try:
            invitation = Invitation.objects.get(
                    code=data,
                    circle=self.context['circle'],
                    used=False
                )
        except Invitation.DoesNotExists:
            raise serializers.ValidationError('Invalid invitation code')

    def validate(self, data):
        circle = self.context['circle']
        if circle.is_limited and circle.members.count() >= circle.members_limit:
            raise serializers.ValidationError('Circle is in its invitations limit')
        return data

    def create(self, data):
        circle = self.context['circle']
        invitation = self.context['invitation']
        user = data['user']
        now = timezone.now()

        member = Membership.objects.create(
            user=user,
            profile=user.profile,
            cicle=circle,
            invited_by=invitation.issued_by
        )

        invitation.used_by = user
        invitation.used = True
        invitation.used_at = now
        invitation.save()

        issuer = Membership.objects.get(
            user=invitation.issued_by,
            circle=circle
        )
        issuer.used_invitation +=1
        issuer.remaining_invitation -= 1

        return member