from django import forms
from .models import PassRequest
from datetime import date


class PassRequestForm(forms.ModelForm):
    class Meta:
        model = PassRequest
        fields = ['name', 'email', 'phone', 'temple', 'persons', 'visit_date', 'id_proof']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'temple': forms.Select(attrs={'class': 'form-control'}),
            'persons': forms.Select(attrs={'class': 'form-control'}),
            'visit_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'min': date.today().isoformat()
            }),
            'id_proof': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_visit_date(self):
        visit_date = self.cleaned_data.get('visit_date')
        temple = self.cleaned_data.get('temple')

        if visit_date < date.today():
            raise forms.ValidationError("Visit date cannot be in the past!")

        if PassRequest.objects.filter(temple=temple, visit_date=visit_date).exists():
            raise forms.ValidationError("This temple is already fully booked for the selected date.")

        return visit_date