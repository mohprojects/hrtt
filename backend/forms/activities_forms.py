from django import forms
from django.core.validators import MaxLengthValidator, MinLengthValidator
from app.models.activities import Activities
from app.models.projects import Projects
from app.models.levels import Levels
from app.utils import Utils
#from app.data import (FUNCTIONS,SUBFUNCTIONS,PROGRAMS,SUBPROGRAMS,LOCATION)

current_fiscal_year = f"{Utils.get_current_year()}-{Utils.get_current_year()+1}"
class ActivitiesSearchIndexForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(ActivitiesSearchIndexForm, self).clean()
        return cleaned_data

    class Meta:
        model = Activities
        fields = ()

class ActivitiesCreateForm(forms.ModelForm):
    name = forms.CharField(
        label="Activity",
        min_length=1,
        max_length=191,
        required=True,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
            }
        ),
    )

    location = forms.ChoiceField(
        choices=(("0", "--Select--"),),
        initial="",
        label="Location",
        required=True,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
                "id": "id_activity_location",
            }
        ),
    )

    functions = forms.ChoiceField(
        choices=(("0", "--Select--"),),
        initial="",
        label="Function",
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
                "id": "id_activity_functions",
            }
        ),
    )
    sub_functions = forms.ChoiceField(
        choices=(("0", "--Select--"),),
        initial="",
        label="Sub Function",
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "id": "id_activity_sub_functions",
            }
        ),
    )
    domain = forms.ChoiceField(
        choices=(("0", "--Select--"),),
        initial="",
        label="Domain",
        required=True,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
                "id": "id_activity_domain",
            }
        ),
    )

    sub_domain = forms.ChoiceField(
        choices=(("0", "--Select--"),),
        initial="",
        label="Sub Domain",
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
                "id": "id_activity_sub_domain",
            }
        ),
    )

    fiscal_year = forms.ChoiceField(
        choices=Utils.get_fiscal_year_choices(),
        initial= current_fiscal_year,
        label="Fiscal Year",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "id_fiscal_year",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
        )

  

    def clean_name(self):
        data = self.cleaned_data["name"]
        return data

    def clean_location(self):
        data = self.cleaned_data["location"]
        return data

    def clean_functions(self):
        data = self.cleaned_data["functions"]
        return data

    def clean_sub_functions(self):
        data = self.cleaned_data["sub_functions"]
        return data

    def clean_domain(self):
        data = self.cleaned_data["domain"]
        return data
    
    def clean_sub_domain(self):
        data = self.cleaned_data["sub_domain"]
        return data
    
    def clean_fiscal_year(self):
        data = self.cleaned_data["fiscal_year"]
        return data

    def clean(self):
        cleaned_data = super(ActivitiesCreateForm, self).clean()
        return cleaned_data

    def __init__(self, *args, **kwargs):
        kwargs.pop("user")
        super(ActivitiesCreateForm, self).__init__(*args, **kwargs)

        LOCATION = (("0", "--Select--"),) 
        locations = Levels.objects.filter(level_key ='location', level_parent = 0).order_by("level_id")
        for item in locations:
                    LOCATION = LOCATION + \
                        ((str(item.level_id), str(item.level_code) + ': ' + str(item.level_name)),)
                    
        self.fields['location'] = forms.ChoiceField(
        choices=LOCATION,
        initial="",
        label="Location",
        required=True,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
                "id": "id_activity_location",
            }
        ),) 

        PROGRAMS = (("0", "--Select--"),) 
        programs = Levels.objects.filter(level_key ='domain', level_parent = 0).order_by("level_id")
        for item in programs:
                    PROGRAMS  = PROGRAMS + \
                    ((str(item.level_id), str(item.level_code) + ': ' + str(item.level_name)),) 
        self.fields['domain'] = forms.ChoiceField(
        choices=PROGRAMS,
        initial="",
        label="Domain",
        required=True,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
                "id": "id_activity_domain",
            }
        ),)

        SUBPROGRAMS = (("0", "NONE"),) 
        sub_programs = Levels.objects.filter(level_key ='sub-domain').order_by("level_id")
        for item in sub_programs:
                    SUBPROGRAMS  = SUBPROGRAMS + \
                        ((str(item.level_id), str(item.level_code) + ': ' + str(item.level_name)),)
                    
        self.fields['sub_domain'] = forms.ChoiceField(
        choices=SUBPROGRAMS,
        initial="",
        label="Sub Domain",
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
                "id": "id_activity_sub_domain",
            }
        ),)

        FUNCTIONS = (("0", "--Select--"),) 
        functions = Levels.objects.filter(level_key = 'function').order_by("level_id")
        for item in functions:
                    FUNCTIONS  = FUNCTIONS  + \
                        ((str(item.level_id), str(item.level_code) + ': ' + str(item.level_name)),)
                    
        self.fields['functions'] = forms.ChoiceField(
        choices=FUNCTIONS,
        initial="",
        label="Function",
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
                "id": "id_activity_functions",
            }
        ),)

        SUBFUNCTIONS = (("0", "NONE"),) 
        sub_functions = Levels.objects.filter(level_key ='sub-function').order_by("level_id")
        for item in sub_functions:
                    SUBFUNCTIONS  = SUBFUNCTIONS + \
                        ((str(item.level_id), str(item.level_code) + ': ' + str(item.level_name)),)
                    
        self.fields['sub_functions'] = forms.ChoiceField(
        choices=SUBFUNCTIONS,
        initial="",
        label="Sub Function",
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
                "id": "id_activity_sub_functions",
            }
        ),)

       

    class Meta:
        model = Activities
        fields = (
            "name",
            "location",
            "functions",
            "sub_functions",
            "domain",
            "sub_domain",
            "fiscal_year",
        )


class ActivitiesUpdateForm(forms.ModelForm):

    name = forms.CharField(
        label="Activity",
        min_length=1,
        max_length=191,
        required=True,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
            }
        ),
    )

    location = forms.ChoiceField(
        choices=(("0", "--Select--"),),
        initial="",
        label="Location",
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
                "id": "id_activity_location",
            }
        ),
    )

    functions = forms.ChoiceField(
        choices=(("0", "--Select--"),),
        initial="",
        label="Function",
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
                "id": "id_activity_functions",
            }
        ),
    )
    sub_functions = forms.ChoiceField(
        choices=(("0", "--Select--"),),
        initial="",
        label="Sub Function",
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "id": "id_activity_sub_functions",
            }
        ),
    )
    domain = forms.ChoiceField(
        choices=(("0", "--Select--"),),
        initial="",
        label="Domain",
        required=True,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
                "id": "id_activity_domain",
            }
        ),
    )

    sub_domain = forms.ChoiceField(
        choices=(("0", "--Select--"),),
        initial="",
        label="Sub Domain",
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
                "id": "id_activity_sub_domain",
            }
        ),
    )
    fiscal_year = forms.ChoiceField(
        choices=Utils.get_fiscal_year_choices(),
        initial="",
        label="Fiscal Year",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "id_fiscal_year",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
        )

    def clean_name(self):
        data = self.cleaned_data["name"]
        return data

    def clean_location(self):
        data = self.cleaned_data["location"]
        return data

    def clean_functions(self):
        data = self.cleaned_data["functions"]
        return data

    def clean_sub_functions(self):
        data = self.cleaned_data["sub_functions"]
        return data

    def clean_domain(self):
        data = self.cleaned_data["domain"]
        return data
    
    def clean_sub_domain(self):
        data = self.cleaned_data["sub_domain"]
        return data
    
    def clean_fiscal_year(self):
        data = self.cleaned_data["fiscal_year"]
        return data
 
    def clean(self):
        cleaned_data = super(ActivitiesUpdateForm, self).clean()
        return cleaned_data

    def __init__(self, *args, **kwargs):
        kwargs.pop("user")
        super(ActivitiesUpdateForm, self).__init__(*args, **kwargs)
        LOCATION = (("0", "--Select--"),) 
        locations = Levels.objects.filter(level_key ='location', level_parent = 0).order_by("level_id")
        for item in locations:
                    LOCATION = LOCATION + \
                        ((str(item.level_id), str(item.level_code) + ': ' + str(item.level_name)),)
                    
        self.fields['location'] = forms.ChoiceField(
        choices=LOCATION,
        initial="",
        label="Location",
        required=True,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
                "id": "id_activity_location",
            }
        ),) 

        PROGRAMS = (("0", "--Select--"),) 
        programs = Levels.objects.filter(level_key ='domain', level_parent = 0).order_by("level_id")
        for item in programs:
                    PROGRAMS  = PROGRAMS + \
                    ((str(item.level_id), str(item.level_code) + ': ' + str(item.level_name)),) 
        self.fields['domain'] = forms.ChoiceField(
        choices=PROGRAMS,
        initial="",
        label="Domain",
        required=True,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
                "id": "id_activity_domain",
            }
        ),)

        SUBPROGRAMS = (("0", "NONE"),) 
        sub_programs = Levels.objects.filter(level_key ='sub-domain').order_by("level_id")
        for item in sub_programs:
                    SUBPROGRAMS  = SUBPROGRAMS + \
                        ((str(item.level_id), str(item.level_code) + ': ' + str(item.level_name)),)
                    
        self.fields['sub_domain'] = forms.ChoiceField(
        choices=SUBPROGRAMS,
        initial="",
        label="Sub Domain",
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
                "id": "id_activity_sub_domain",
            }
        ),)

        FUNCTIONS = (("0", "--Select--"),) 
        functions = Levels.objects.filter(level_key = 'function').order_by("level_id")
        for item in functions:
                    FUNCTIONS  = FUNCTIONS  + \
                        ((str(item.level_id), str(item.level_code) + ': ' + str(item.level_name)),)
                    
        self.fields['functions'] = forms.ChoiceField(
        choices=FUNCTIONS,
        initial="",
        label="Function",
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
                "id": "id_activity_functions",
            }
        ),)

        SUBFUNCTIONS = (("0", "NONE"),) 
        sub_functions = Levels.objects.filter(level_key ='sub-function').order_by("level_id")
        for item in sub_functions:
                    SUBFUNCTIONS  = SUBFUNCTIONS + \
                        ((str(item.level_id), str(item.level_code) + ': ' + str(item.level_name)),)
                    
        self.fields['sub_functions'] = forms.ChoiceField(
        choices=SUBFUNCTIONS,
        initial="",
        label="Sub Function",
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
                "id": "id_activity_sub_functions",
            }
        ),)

       
    
    class Meta:
        model = Activities
        fields = (
            "name",
            "location",
            "functions",
            "sub_functions",
            "domain",
            "sub_domain",
            "fiscal_year",
        )


class ActivitiesViewForm(forms.ModelForm):

    name = forms.CharField(
        label="Activity",
        min_length=1,
        max_length=191,
        required=True,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "readonly": True,
                "disabled": True,
            }
        ),
    )

    location = forms.ChoiceField(
        choices=(("0", "--Select--"),),
        initial="",
        label="Location",
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "id": "id_activity_location",
                "readonly": True,
                "disabled": True,
            }
        ),
    )

    functions = forms.ChoiceField(
        choices=(("0", "--Select--"),),
        initial="",
        label="Function",
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "id": "id_activity_functions",
                "readonly": True,
                "disabled": True,
            }
        ),
    )
    sub_functions = forms.ChoiceField(
        choices=(("0", "--Select--"),),
        initial="",
        label="Sub Function",
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "id": "id_activity_sub_functions",
                "readonly": True,
                "disabled": True,
            }
        ),
    )
    domain = forms.ChoiceField(
        choices=(("0", "--Select--"),),
        initial="",
        label="Domain",
        required=True,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "id": "id_activity_domain",
                "readonly": True,
                "disabled": True,
            }
        ),
    )

    sub_domain = forms.ChoiceField(
        choices=(("0", "--Select--"),),
        initial="",
        label="Sub Domain",
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "id": "id_activity_sub_domain",
                "readonly": True,
                "disabled": True,
            }
        ),
    )

    fiscal_year = forms.ChoiceField(
        choices=Utils.get_fiscal_year_choices(),
        initial="",
        label="Fiscal Year",
        required=False,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "id_fiscal_year",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
        )

    def clean_name(self):
        data = self.cleaned_data["name"]
        return data

    def clean_location(self):
        data = self.cleaned_data["location"]
        return data

    def clean_functions(self):
        data = self.cleaned_data["functions"]
        return data

    def clean_sub_functions(self):
        data = self.cleaned_data["sub_functions"]
        return data

    def clean_domain(self):
        data = self.cleaned_data["domain"]
        return data
    
    def clean_sub_domain(self):
        data = self.cleaned_data["sub_domain"]
        return data
    
    def clean_fiscal_year(self):
        data = self.cleaned_data["fiscal_year"]
        return data

    def clean(self):
        cleaned_data = super(ActivitiesViewForm, self).clean()
        return cleaned_data

    def __init__(self, *args, **kwargs):
        kwargs.pop("user")
        super(ActivitiesViewForm, self).__init__(*args, **kwargs)
        LOCATION = (("0", "--Select--"),) 
        locations = Levels.objects.filter(level_key ='location', level_parent = 0).order_by("level_id")
        for item in locations:
                    LOCATION = LOCATION + \
                        ((str(item.level_id), str(item.level_code) + ': ' + str(item.level_name)),)
                    
        self.fields['location'] = forms.ChoiceField(
        choices=LOCATION,
        initial="",
        label="Location",
        required=True,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
                "id": "id_activity_location",
            }
        ),) 

        PROGRAMS = (("0", "--Select--"),) 
        programs = Levels.objects.filter(level_key ='domain', level_parent = 0).order_by("level_id")
        for item in programs:
                    PROGRAMS  = PROGRAMS + \
                    ((str(item.level_id), str(item.level_code) + ': ' + str(item.level_name)),) 
        self.fields['domain'] = forms.ChoiceField(
        choices=PROGRAMS,
        initial="",
        label="Domain",
        required=True,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
                "id": "id_activity_domain",
            }
        ),)

        SUBPROGRAMS = (("0", "NONE"),) 
        sub_programs = Levels.objects.filter(level_key ='sub-domain').order_by("level_id")
        for item in sub_programs:
                    SUBPROGRAMS  = SUBPROGRAMS + \
                        ((str(item.level_id), str(item.level_code) + ': ' + str(item.level_name)),)
                    
        self.fields['sub_domain'] = forms.ChoiceField(
        choices=SUBPROGRAMS,
        initial="",
        label="Sub Domain",
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
                "id": "id_activity_sub_domain",
            }
        ),)

        FUNCTIONS = (("0", "--Select--"),) 
        functions = Levels.objects.filter(level_key = 'function').order_by("level_id")
        for item in functions:
                    FUNCTIONS  = FUNCTIONS  + \
                        ((str(item.level_id), str(item.level_code) + ': ' + str(item.level_name)),)
                    
        self.fields['functions'] = forms.ChoiceField(
        choices=FUNCTIONS,
        initial="",
        label="Function",
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
                "id": "id_activity_functions",
            }
        ),)

        SUBFUNCTIONS = (("0", "NONE"),) 
        sub_functions = Levels.objects.filter(level_key ='sub-function').order_by("level_id")
        for item in sub_functions:
                    SUBFUNCTIONS  = SUBFUNCTIONS + \
                        ((str(item.level_id), str(item.level_code) + ': ' + str(item.level_name)),)
                    
        self.fields['sub_functions'] = forms.ChoiceField(
        choices=SUBFUNCTIONS,
        initial="",
        label="Sub Function",
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "",
                "style": "width:100%;",
                "id": "id_activity_sub_functions",
            }
        ),)


    class Meta:
        model = Activities
        fields = (
            "name",
            "location",
            "functions",
            "sub_functions",
            "domain",
            "sub_domain",
            "fiscal_year",
        )
