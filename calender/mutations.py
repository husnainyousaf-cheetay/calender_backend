import graphene
from graphene_django.types import ErrorType
from graphql_relay.node.node import from_global_id

from graphene.relay import ClientIDMutation
from django.contrib.auth.models import User

from .models import *


def get_id(g_id):
    return int(from_global_id(g_id)[1])


class ScheduleInputBase:
    user = graphene.ID(required=False)
    start_time = graphene.DateTime(required=True)
    end_time = graphene.DateTime(required=True)
    interval = graphene.Int(required=True)


class MeetingInputBase:
    user = graphene.ID(required=False)
    guest = graphene.ID(required=False)
    guest_email = graphene.String(required=False)
    start_time = graphene.DateTime(required=True)
    end_time = graphene.DateTime(required=True)
    title = graphene.String(required=True)


class CreateScheduleMutation(ClientIDMutation):
    class Input(ScheduleInputBase):
        pass

    ok = graphene.Boolean()
    errors = graphene.List(ErrorType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        try:
            user = User.objects.get(id=get_id(input.get('user')))
            start_time = input.get('start_time')
            end_time = input.get('end_time')
            interval = input.get('interval')
            schedule = UserSchedule(
                user=user,
                start_time = start_time,
                end_time = end_time,
                interval = interval)
            schedule.full_clean()
            schedule.save()
            return CreateScheduleMutation(errors=None, ok=True)
        except Exception as e:
            errors = [ErrorType(field=type(e), messages=[str(e)])]
            return CreateScheduleMutation(errors=errors, ok=False)


class UpdateScheduleMutation(ClientIDMutation):
    class Input(ScheduleInputBase):
        schedule_id = graphene.String()

    ok = graphene.Boolean()
    errors = graphene.List(ErrorType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        try:
            schedule = UserSchedule.objects.get(id=get_id(input.get('schedule_id')))
            schedule.start_time = input.get('start_time')
            schedule.end_time = input.get('end_time')
            schedule.interval = input.get('interval')
            schedule.save()
            return UpdateScheduleMutation(errors=None, ok=True)
        except Exception as e:
            errors = [ErrorType(field=type(e), messages=[str(e)])]
            return UpdateScheduleMutation(errors=errors, ok=False)


class DeleteScheduleMutation(ClientIDMutation):
    class Input(ScheduleInputBase):
        schedule_id = graphene.String()

    ok = graphene.Boolean()
    errors = graphene.List(ErrorType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        try:
            UserSchedule.objects.filter(id=get_id(input.get('schedule_id'))).delete()
            return DeleteScheduleMutation(errors=None, ok=True)
        except Exception as e:
            errors = [ErrorType(field=type(e), messages=[str(e)])]
            return DeleteScheduleMutation(errors=errors, ok=False)


class CreateMeetingMutation(ClientIDMutation):
    class Input(MeetingInputBase):
        pass

    ok = graphene.Boolean()
    errors = graphene.List(ErrorType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        try:
            user = User.objects.get(id=input.get('user'))
            guest = User.objects.get(id=input.get('guest'))
            guest_email = input.get('guest_email')
            start_time = input.get('start_time')
            end_time = input.get('end_time')
            title = input.get('title')
            meeting = UserMeeting(user=user, guest=guest, start_time=start_time, end_time=end_time,
                                  title=title, guest_email=guest_email)
            meeting.full_clean()
            meeting.save()
            return CreateMeetingMutation(errors=None, ok=True)
        except Exception as e:
            errors = [ErrorType(field=type(e), messages=[str(e)])]
            return CreateMeetingMutation(errors=errors, ok=False)


class UpdateMeetingMutation(ClientIDMutation):
    class Input(MeetingInputBase):
        meeting_id = graphene.String()

    ok = graphene.Boolean()
    errors = graphene.List(ErrorType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        try:
            meeting = UserMeeting.objects.get(id=get_id(input.get('meeting_id')))
            meeting.start_time = input.get('start_time')
            meeting.end_time = input.get('end_time')
            meeting.user = input.get('user')
            meeting.guest = input.get('guest')
            meeting.save()
            return UpdateMeetingMutation(errors=None, ok=True)
        except Exception as e:
            errors = [ErrorType(field=type(e), messages=[str(e)])]
            return UpdateMeetingMutation(errors=errors, ok=False)


class DeleteMeetingMutation(ClientIDMutation):
    class Input(MeetingInputBase):
        meeting_id = graphene.String()

    ok = graphene.Boolean()
    errors = graphene.List(ErrorType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        try:
            UserMeeting.objects.filter(id=get_id(input.get('meeting_id'))).delete()
            return DeleteScheduleMutation(errors=None, ok=True)
        except Exception as e:
            errors = [ErrorType(field=type(e), messages=[str(e)])]
            return DeleteScheduleMutation(errors=errors, ok=False)
