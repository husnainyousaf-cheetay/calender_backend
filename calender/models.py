from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Q

from .enums import INTERVAL_CHOICES, FIFTEEN_MINUTES


class BaseModel(models.Model):
    start_time = models.DateTimeField(null=False, blank=False)
    end_time = models.DateTimeField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserMeeting(BaseModel):
    user = models.ForeignKey(User, related_name='user_meeting', on_delete=models.PROTECT)
    guest = models.ForeignKey(User, related_name='guest_user', on_delete=models.PROTECT, null=True)
    guest_email = models.EmailField(null=True)
    title = models.CharField(max_length=500)

    def __str__(self) -> str:
        return self.user.first_name + " " + str(self.id)

    @property
    def duration(self) -> int:
        return int((self.end_time - self.start_time).total_seconds()/60)

    def save(self, *args, **kwargs):
        meeting_overlap = UserMeeting.objects.filter(user=self.user).filter(
            Q(start_time__lte=self.start_time, end_time__gt=self.start_time) |
            Q(start_time__lt=self.end_time, end_time__gte=self.end_time) |
            Q(start_time__gte=self.start_time, end_time__lte=self.end_time)).exists()
        if meeting_overlap:
            raise ValidationError("Already Meeting In same time range")

        schedule_mismatch = UserSchedule.objects.filter(user=self.user).filter(
            Q(start_time__lte=self.start_time, end_time__gt=self.start_time) |
            Q(start_time__lt=self.end_time, end_time__gte=self.end_time) |
            Q(start_time__gte=self.start_time, end_time__lte=self.end_time)).exists()
        if schedule_mismatch:
            raise ValidationError("User not available in the time range")
        # super(UserMeeting, self).save(*args, **kwargs)


class UserSchedule(BaseModel):
    user = models.ForeignKey(User, related_name='user_schedule', on_delete=models.PROTECT)
    end_time = models.DateTimeField(null=False, blank=False)
    interval = models.IntegerField(choices=INTERVAL_CHOICES, default=FIFTEEN_MINUTES, null=False)

    def __str__(self) -> str:
        return self.user.first_name + " " + str(self.id)

    def save(self, *args, **kwargs):
        over_lapping = UserSchedule.objects.filter(user=self.user).filter(
            Q(start_time__lte=self.start_time, end_time__gt=self.start_time) |
            Q(start_time__lt=self.end_time, end_time__gte=self.end_time) |
            Q(start_time__gte=self.start_time, end_time__lte=self.end_time),
            ).exists()
        if over_lapping:
            raise ValidationError("OverLapping Schedule")
