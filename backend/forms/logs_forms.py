from django import forms
from app.models.users import Users


class LogsSearchIndexForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(LogsSearchIndexForm, self).clean()
        return cleaned_data

    class Meta:
        model = Users
        fields = ()
