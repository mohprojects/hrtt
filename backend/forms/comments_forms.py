from app.models.comments import Comments
from django.db.models import Q
from app.models.users import Users
from django import forms
from django.core.validators import MaxLengthValidator, MinLengthValidator
from tinymce.widgets import TinyMCE


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


class CommentsSearchIndexForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(CommentsSearchIndexForm, self).clean()
        return cleaned_data

    class Meta:
        model = Comments
        fields = ()


class CommentsCreateForm(forms.ModelForm):
    message = forms.CharField(
        label="Add Comment",
        min_length=1,
        max_length=1000,
        required=True,
        initial="Accepted!",
        validators=[MinLengthValidator(1), MaxLengthValidator(1000)],
        widget=forms.Textarea(
            attrs={
                "id": "id_message_comments",
                "class": "form-control",
                "placeholder": "",
                "rows": 5,
                "maxlength": 1000,
            }
        ),
    )

    to = forms.CharField(
        initial="",
        label="To",
        min_length=1,
        max_length=191,
        required=False,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
            }
        ),
    )

    def clean_message(self):
        data = self.cleaned_data["message"]
        return data
    
    def clean_to(self):
        data = self.cleaned_data["to"]
        return data

    def clean(self):
        cleaned_data = super(CommentsCreateForm, self).clean()
        return cleaned_data

    def __init__(self, *args, **kwargs):
        kwargs.pop("user")
        super(CommentsCreateForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Comments
        fields = ("message",)


class CommentsUpdateForm(forms.ModelForm):
    message = forms.CharField(
        label="Message",
        min_length=1,
        max_length=191,
        required=True,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.Textarea(
            attrs={
                "id": "id_message_comments",
                "class": "form-control",
                "placeholder": "",
                "rows": 2,
                "maxlength": 1000,
            }
        ),
    )

    to = forms.CharField(
        initial="",
        label="To",
        min_length=1,
        max_length=191,
        required=False,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
            }
        ),
    )

    def clean_message(self):
        data = self.cleaned_data["message"]
        return data
    
    def clean_to(self):
        data = self.cleaned_data["to"]
        return data

    def clean(self):
        cleaned_data = super(CommentsUpdateForm, self).clean()
        return cleaned_data

    def __init__(self, *args, **kwargs):
        kwargs.pop("user")
        super(CommentsUpdateForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Comments
        fields = ("message",)


class CommentsViewForm(forms.ModelForm):
    message = forms.CharField(
        label="Message",
        min_length=1,
        max_length=191,
        required=True,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.Textarea(
            attrs={
                "id": "id_message_comments",
                "class": "form-control",
                "placeholder": "",
                "rows": 2,
                "maxlength": 1000,
                "readonly": True,
                "disabled": True,
            }
        ),
    )

    to = forms.CharField(
        initial="",
        label="To",
        min_length=1,
        max_length=191,
        required=False,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
            }
        ),
    )

    def clean_message(self):
        data = self.cleaned_data["message"]
        return data

    def clean(self):
        cleaned_data = super(CommentsViewForm, self).clean()
        return cleaned_data

    def __init__(self, *args, **kwargs):
        kwargs.pop("user")
        super(CommentsViewForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Comments
        fields = ("message",)

class CommentsCreateHtmlForm(forms.ModelForm):
    message = forms.CharField(
        label="Add Comment",
        required=True,
        widget=TinyMCEWidget(
            attrs={
                "required": False,
                "id": "id_message_comments",
                "rows": 6,
                "cols": 110,
            }
        ),
    )

    def clean_message(self):
        data = self.cleaned_data["message"]
        return data
    
    def clean_to(self):
        data = self.cleaned_data["to"]
        return data

    def clean(self):
        cleaned_data = super(CommentsCreateHtmlForm, self).clean()
        return cleaned_data

    def __init__(self, *args, **kwargs):
        kwargs.pop("user")
        super(CommentsCreateHtmlForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Comments
        fields = ("message",)


class CommentsAssignForm(forms.ModelForm):
    message = forms.CharField(
        label="Add Comment",
        initial="Work on this project!",
        min_length=1,
        max_length=1000,
        required=False,
        validators=[MinLengthValidator(1), MaxLengthValidator(1000)],
        widget=forms.Textarea(
            attrs={
                "id": "id_message_comments_assign",
                "class": "form-control",
                "placeholder": "",
                "rows": 5,
                "maxlength": 1000,
            }
        ),
    )

    assign_to = forms.ChoiceField(
        choices=(("", "--select--"),),
        initial="",
        label="Assign To",
        required=True,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "search-input-select-assign-to",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )

    def clean_message(self):
        data = self.cleaned_data["message"]
        return data

    def clean_assign_to(self):
        data = self.cleaned_data["assign_to"]
        return data

    def clean(self):
        cleaned_data = super(CommentsAssignForm, self).clean()
        return cleaned_data

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super(CommentsAssignForm, self).__init__(*args, **kwargs)

        REPORTERS = (("0", "NONE"),)
        reporters = Users.objects.filter(Q(organization_id = user.organization_id) & Q(user_role = Users.TYPE_DATA_REPORTER))
        for item in reporters:
           REPORTERS = REPORTERS + ((item.user_id, item.user_name),)
        self.fields["assign_to"] = forms.ChoiceField(
            choices=REPORTERS,
            initial="",
            label="Assign To",
            required=False,
            validators=[],
            widget=forms.Select(
                attrs={
                    "id": "search-input-select-assign-to",
                    "class": "form-control",
                    "style": "width:100%;",
                    "placeholder": "--select--",
                }
            ),
        )

    class Meta:
        model = Comments
        fields = ("message",)

    
