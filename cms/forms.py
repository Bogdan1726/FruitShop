from django import forms


class DeclarationForm(forms.Form):
    file = forms.FileField(
        widget=forms.FileInput(),
    )
