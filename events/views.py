from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Event, Location, EventSessionItem, Comment, Bookmark
from .forms import EventForm, EventImageForm, LocationForm, EventSessionForm


def event_list(request):
    events = Event.objects.all()
    return render(request, 'events/event_list.html', {'events': events})


def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    event_sessions = event.sessions.filter(event=event).order_by('start_time')
    comments = event.comment_set.all().order_by('-created_at')
    participants = event.participants.all()

    if request.method == 'POST':
        comment = Comment.objects.create(
            user=request.user,
            event=event,
            text=request.POST.get('comment')
        )
        return redirect('event_detail', event_id=event.id)

    context = {'event': event, 'event_sessions': event_sessions,
               'comments': comments, 'participants': participants}
    return render(request, 'events/event_detail.html', context)


@login_required(login_url='accounts/login')
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            new_event = form.save(commit=False)
            new_event.creator = request.user
            new_event.save()
            return redirect('event_detail', event_id=new_event.id)
    else:
        form = EventForm()

    return render(request, 'events/create_event.html', {'form': form})


@login_required(login_url='accounts/login')
def create_location(request):
    if request.method == 'POST':
        location_form = LocationForm(request.POST)
        if location_form.is_valid():
            location = location_form.save(commit=False)
            location.user = request.user
            location.save()
            return redirect('create_event')
    else:
        location_form = LocationForm()

    return render(request, 'events/create_location.html', {'location_form': location_form})


@login_required(login_url='accounts/login')
def create_session_item(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.method == 'POST':
        event_session_form = EventSessionForm(request.POST)
        if event_session_form.is_valid():
            session = event_session_form.save(commit=False)
            session.event = event
            session.save()
            return redirect('event_detail', event_id=event.id)
    else:
        form = EventSessionForm()
    return render(request, 'events/create_session.html', {'form': form, 'event': event})


@login_required(login_url='accounts/login')
def edit_session_item(request, event_id, session_id):
    event_session = get_object_or_404(EventSessionItem, id=session_id)

    if not request.user.is_authenticated or request.user != event_session.event.creator:
        return render(request, 'error.html', {'error_message': 'Unauthorized access'})

    if request.method == 'POST':
        form = EventSessionForm(request.POST, instance=event_session)
        if form.is_valid():
            form.save()
            return redirect('event_detail', event_id=event_id)
    else:
        form = EventSessionForm(instance=event_session)

    return render(request, 'events/edit_session.html', {'form': form, 'event_session': event_session})


@login_required(login_url='accounts/login')
def edit_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    if request.user != event.creator:
        return redirect('event_detail', event_id=event_id)

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_detail', event_id=event_id)
    else:
        form = EventForm(instance=event)

    return render(request, 'events/edit_event.html', {'form': form, 'event': event})


@login_required(login_url='accounts/login')
def delete_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        event.delete()
        return redirect('event_list')

    return render(request, 'events/delete_event.html', {'event': event})


@login_required(login_url='accounts/login')
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)

    if request.user != comment.user:
        return HttpResponse('You are not allowed to remove this comment')

    if request.method == 'POST':
        comment.delete()
        return redirect('event_detail', comment.event.id)

    return render(request, 'events/delete_comment.html', {'comment': comment})


@login_required(login_url='accounts/login')
def register_to_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    if request.user not in event.participants.all():
        event.participants.add(request.user)

    return redirect('event_detail', event_id=event.id)


@login_required(login_url='accounts/login')
def bookmark_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    bookmark, created = Bookmark.objects.get_or_create(
        user=request.user, event=event)

    if not created:
        # If the bookmark already exists, remove it
        bookmark.delete()

    return redirect('event_detail', event_id=event.id)


@login_required(login_url='accounts/login')
def bookmarked_events(request):
    bookmarks = Bookmark.objects.filter(user=request.user)
    return render(request, 'events/bookmarked_events.html', {'bookmarks': bookmarks})
