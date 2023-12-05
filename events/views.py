from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .models import Event
from .forms import EventForm


def event_list(request):
    events = Event.objects.all()
    return render(request, 'events/event_list.html', {'events': events})


def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    return render(request, 'events/event_detail.html', {'event': event})


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
