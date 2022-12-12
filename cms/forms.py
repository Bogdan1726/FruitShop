from django import forms
from cms.models import Declaration


class DeclarationForm(forms.ModelForm):
    max_upload_size = 20971520  # 20MB
    error_messages = {
        'error_file': 'Размер файла не должен превышать 20MB',
    }

    class Meta:
        model = Declaration
        exclude = ('date',)

        widgets = {
            'file': forms.FileInput(attrs={'type': 'file',
                                           'onchange': "file_valid(this)"}),
        }

    def clean_file(self):
        if self.cleaned_data:
            file = self.cleaned_data['file']
            if file.size > self.max_upload_size:
                raise forms.ValidationError(message=self.error_messages['error_file'])
            return file
