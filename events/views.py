from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .models import Event, Location, EventSessionItem
from .forms import EventForm, LocationForm, EventSessionForm


def event_list(request):
    events = Event.objects.all()
    return render(request, 'events/event_list.html', {'events': events})


def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    event_sessions = event.sessions.filter(event=event).order_by('start_time')
    context = {'event': event, 'event_sessions': event_sessions}
    return render(request, 'events/event_detail.html', context)


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


def edit_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    # Handle form submission for editing an event
    if request.method == 'POST':
        # Process the form data (assuming you have a form for editing events)
        # ...

        # Redirect to the edited event's detail page
        return redirect('event_detail', event_id=event.id)

    # Render the form for editing the event
    return render(request, 'events/edit_event.html', {'event': event})


def delete_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    # Handle form submission for deleting an event
    if request.method == 'POST':
        # Delete the event
        event.delete()

        # Redirect to the event list page or another appropriate page
        return redirect('event_list')

    # Render the confirmation page for deleting the event
    return render(request, 'events/delete_event.html', {'event': event})
