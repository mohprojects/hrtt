from django import forms
from app.models.users import Users


class NotificationsSearchIndexForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(NotificationsSearchIndexForm, self).clean()
        return cleaned_data

    class Meta:
        model = Users
        fields = ()

class NotificationsCreateForm(forms.ModelForm):
    notification = forms.CharField(
        label="Add Notification",
        min_length=1,
        max_length=1000,
        required=True,
         widget=forms.Textarea(
            attrs={
                "id": "id_notification",
                "class": "form-control",
                "placeholder": "",
                "rows": 2,
                "maxlength": 1000,
            }
        ),
    )
    project_id= forms.CharField(
        label="Project_id",
        min_length=1,
        max_length=191,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "",
            }
        ),
    )

    def clean_notification(self):
        data = self.cleaned_data["notification"]
        return data
    
    def clean_project_id(self):
        data = self.cleaned_data["project_id"]
        return data

    def clean(self):
        cleaned_data = super(NotificationsCreateForm, self).clean()
        return cleaned_data

    def __init__(self, *args, **kwargs):
        kwargs.pop("user")
        project_id = kwargs.pop("project_id")
        super(NotificationsCreateForm, self).__init__(*args, **kwargs)
        self.fields['project_id'] = forms.CharField(
            initial=project_id,
            label="Project Idd",
            min_length=1,
            max_length=191,
            required=False,
            widget=forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "",
                    "readonly": True,
                }
            ),
        )
        

    class Meta:
        model = Users
        fields = ("notification","project_id",)
         
  
