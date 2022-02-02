import graphene
from .schema_nodes import MeetingNode, ScheduleNode, UserNode
from .models import UserMeeting, UserSchedule
from .mutations import (CreateScheduleMutation, UpdateScheduleMutation, DeleteScheduleMutation, CreateMeetingMutation,
                        UpdateMeetingMutation, DeleteMeetingMutation)
from graphene_django.filter import DjangoFilterConnectionField
from django.contrib.auth.models import User
from datetime import datetime


class Query(graphene.ObjectType):
    schedule = DjangoFilterConnectionField(ScheduleNode)
    meeting = DjangoFilterConnectionField(MeetingNode)
    all_users = DjangoFilterConnectionField(UserNode)
    get_available_time_for_user = graphene.List(ScheduleNode, user_id=graphene.Int())

    def resolve_schedule(root, info, **kwargs):
        return UserSchedule.objects.all()

    def resolve_meeting(root, info, **kwargs):
        return UserMeeting.objects.all()

    def resolve_all_users(root, info, **kwargs):
        return User.objects.all()

    def resolve_get_available_time_for_user(root, info, **kwargs):
        user_id = kwargs.get('user_id', None)
        return UserSchedule.objects.filter(id=user_id, start_time__gte=datetime.now())


class Mutation(graphene.ObjectType):
    create_schedule = CreateScheduleMutation.Field()
    update_schedule = UpdateScheduleMutation.Field()
    delete_schedule = DeleteScheduleMutation.Field()

    create_meeting = CreateMeetingMutation.Field()
    update_meeting = UpdateMeetingMutation.Field()
    delete_meeting = DeleteMeetingMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
