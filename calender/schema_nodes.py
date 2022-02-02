import graphene
from django.contrib.auth.models import User
from graphene_django.types import DjangoObjectType
from .models import UserMeeting, UserSchedule


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        interfaces = (graphene.relay.Node,)
        filter_fields = {'id': ['exact']}


class ScheduleNode(DjangoObjectType):
    class Meta:
        model = UserSchedule
        interfaces = (graphene.relay.Node,)
        filter_fields = {'user_id': ['exact']}


class MeetingNode(DjangoObjectType):
    duration = graphene.Int()
    guest = UserNode
    user = UserNode

    def resolve_duration(self, resolve_info):
        return self.duration

    def resolve_guest(self, resolve_info):
        return self.guest

    def resolve_user(self, resolve_info):
        return self.user

    class Meta:
        model = UserMeeting
        interfaces = (graphene.relay.Node,)
        filter_fields = {'id': ['exact']}
