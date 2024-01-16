from django import forms
from .models import *

class FormControl(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field, forms.BooleanField):
                field.widget.attrs.update({'class': 'form-control'})

class ShortnerForm(forms.ModelForm):
    class Meta:
        model = ShortURL
        fields = ['original_url', 'short_part', 'expiration_date']

    def clean_short_part(self):
        short_part = self.cleaned_data['short_part']
        if ShortURL.objects.filter(short_part=short_part).exists():
            raise forms.ValidationError('This short URL is already in use. Please choose another.')
        return short_part
