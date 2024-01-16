from django import forms
from .models import *
from django.forms import DateInput

class FormControl(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field, forms.BooleanField):
                field.widget.attrs.update({'class': 'form-control'})

class ShortnerForm(FormControl, forms.ModelForm):
    class Meta:
        model = ShortURL
        fields = ['original_url', 'short_part', 'expiration_date']
        widgets = {
            'expiration_date': DateInput(attrs={'type': 'date'}),
        }

    def clean_short_part(self):
        cleaned_data = super().clean()
        short_part = cleaned_data.get('short_part')

        if short_part:
            if ShortURL.objects.filter(short_part=short_part).exists():
                raise forms.ValidationError('This short URL is already in use. Please choose another.')

        return short_part
