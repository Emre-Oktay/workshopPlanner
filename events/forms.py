from django import forms
from .models import Event, Tag, Location


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['city', 'district', 'street', 'building_number', 'floor']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update(
                {'class': 'form-control'})


class EventForm(forms.ModelForm):
    location = forms.ModelChoiceField(queryset=Location.objects.all())

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=False,
    )

    # Field for creating new tags
    new_tags = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False,
        help_text='Enter new tags separated by commas',
    )

    class Meta:
        model = Event
        fields = ['title', 'description', 'date',
                  'location', 'category', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'date': forms.DateTimeInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        tags = list(cleaned_data.get('tags', []))  # Convert to list
        new_tags = cleaned_data.get('new_tags', '')

        # Combine existing tags and new tags
        tag_names = [tag.name.lower() for tag in tags] + [tag.strip()
                                                          for tag in new_tags.split(',') if tag.strip()]

        # Remove duplicates
        tag_names = list(set(tag_names))

        # Create Tag objects for new tags
        new_tags_objs = [Tag.objects.get_or_create(
            name=name)[0] for name in tag_names if name]

        # Set the cleaned data with the combined tags
        cleaned_data['tags'] = tags + new_tags_objs

        return cleaned_data
