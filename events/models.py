from django.db import models

from users.models import User


class Location(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    building_number = models.CharField(max_length=255)
    floor = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.city}, {self.district}"


class Event(models.Model):
    DRAFTED = 'drafted'
    PUBLISHED = 'published'
    ARCHIVED = 'archived'

    STATUS_CHOICES = [
        (DRAFTED, 'Drafted'),
        (PUBLISHED, 'Published'),
        (ARCHIVED, 'Archived'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name='events')
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='events_created')
    collaborators = models.ManyToManyField(
        User, related_name='events_collaborated', blank=True)
    participants = models.ManyToManyField(
        User, related_name='events_participated', blank=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=DRAFTED)
    tags = models.ManyToManyField('Tag', related_name='events', blank=True)
    category = models.ForeignKey(
        'Category', on_delete=models.CASCADE, related_name='events')
    invited_users = models.ManyToManyField(
        User,
        through='Invitation',
        through_fields=('event', 'user'),
        related_name='events_invited',
        blank=True
    )
    comments = models.ManyToManyField(
        'Comment', related_name='event_comments', blank=True)
    schedule_items = models.ManyToManyField(
        'EventSessionItem', related_name='event_schedule', blank=True)
    main_image = models.ImageField(upload_to='event_images/', blank=True)

    def __str__(self):
        return self.title


class EventSessionItem(models.Model):
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name='sessions')
    start_time = models.TimeField()
    end_time = models.TimeField()
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.start_time} - {self.end_time} - {self.title}"


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'


class Invitation(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    invited_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='invitations_sent_by')
    is_accepted = models.BooleanField(default=False)


class Comment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"


class EventImage(models.Model):
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name='images')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='event_images/')


class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['user', 'event']
