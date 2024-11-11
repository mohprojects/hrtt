from django import forms
from django.core.validators import MaxLengthValidator, MinLengthValidator


from app.models.organizations import Organizations
from app.models.projects import Projects
from app.models.implementers import Implementers
from app.models.users import Users
        
class ProjectsSearchIndexForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(ProjectsSearchIndexForm, self).clean()
        return cleaned_data

    class Meta:
        model = Projects
        fields = ()


class ProjectsCreateForm(forms.ModelForm):
    name = forms.CharField(
        label='Project Title',
        min_length=1,
        max_length=191,
        required=True,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "",
            }
        ))
    financing_agent = forms.MultipleChoiceField(
        choices= (('', '--select--'),) ,
        initial="",
        label="Financing Agent Name",
        required=True,
        validators=[],
        widget=forms.SelectMultiple(
            attrs={
                "id": "id_financing_agent",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )
    
    implementer = forms.MultipleChoiceField(
        choices= (('', '--select--'),),
        initial="",
        label="Implementer Name",
        required=True,
        validators=[],
        widget=forms.SelectMultiple(
            attrs={
                "id": "id_project_implementer",
                 "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )
    funding_source =forms.MultipleChoiceField(
        choices= (('', '--select--'),),
        initial="",
        label="Funding Source",
        required=False,
        validators=[],
        widget=forms.SelectMultiple(
            attrs={
                "id": "id_project_funding_source",
                 "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )
    

    organization_id = forms.ChoiceField(
        choices= (('', '--select--'),),
        initial="",
        label="Organization",
        required=True,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "search-input-select-organization-id",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ))
   
    start_time =forms.DateField(
        label="Start date",
        required=True,
        validators=[],
        # input_formats=['%Y-%m-%d %H:%M'],
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )
    
    deadline = forms.DateField(
        label="End date",
        required=True,
        validators=[],
        # input_formats=['%Y-%m-%d %H:%M'],
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )
    def clean_name(self):
        data = self.cleaned_data["name"]
        # try:
        #     item = Projects.objects.get(project_name=data)
        # except ( NameError, ValueError, OverflowError, Projects.DoesNotExist):
        #     item = None
        # if item is not None:
        #     raise forms.ValidationError(
        #         u'Project Title: "%s" is already in use.' % data)
        return data
    
    def clean_financing_agent(self):
        data = self.cleaned_data['financing_agent']
        return data
    
    def clean_implementer(self):
        data = self.cleaned_data['implementer']
        return data
    
    def clean_funding_source(self):
        data = self.cleaned_data['funding_source']
        return data


    def clean_organization_id(self):
        data = self.cleaned_data["organization_id"]
        return data
   
    
    
    def clean_start_time(self):
        data = self.cleaned_data['start_time']
        return data
    
    def clean_deadline(self):
        data = self.cleaned_data["deadline"]
        if data is None:
            return None
        return str(data)

    def clean(self):
        cleaned_data = super(ProjectsCreateForm, self).clean()
        return cleaned_data

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super(ProjectsCreateForm, self).__init__(*args, **kwargs)

        ORGANIZATIONS= (('', '--select--'),)
        organizations = Organizations.objects.all()
        for item in organizations:
            ORGANIZATIONS=ORGANIZATIONS+ \
                ((item.organization_id, item.organization_name),)
            
        if user.user_role == Users.TYPE_ACTIVITY_MANAGER:
            ORGANIZATIONSID= (('', '--select--'),)
            organizations_activity_manager = organizations.filter(organization_id = user.organization_id)
            for item in organizations_activity_manager:
                ORGANIZATIONSID=ORGANIZATIONSID+ \
                    ((item.organization_id, item.organization_name),)
            self.fields['organization_id'] = forms.ChoiceField(
                choices=ORGANIZATIONSID[1:],
                initial='',
                label='Organization',
                required=True,
                validators=[],
                widget=forms.Select(
                    attrs={
                        'id': 'search-input-select-organization-id',
                        'class': 'form-control',
                        'style': 'width:100%;',
                        'placeholder': '--select--',
                    }
                ))
        else:    

            self.fields['organization_id'] = forms.ChoiceField(
                choices=ORGANIZATIONS[1:],
                initial='',
                label='Organization',
                required=True,
                validators=[],
                widget=forms.Select(
                    attrs={
                        'id': 'search-input-select-organization-id',
                        'class': 'form-control',
                        'style': 'width:100%;',
                        'placeholder': '--select--',
                    }
                ))
        self.fields['funding_source'] = forms.MultipleChoiceField(
        choices= ORGANIZATIONS[1:],
        initial="",
        label="Funding Source",
        required=False,
        validators=[],
        widget=forms.SelectMultiple(
            attrs={
                "id": "id_project_funding_source",
                 "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),)
        
        
        FUNDINGSOURCES = (('', '--select--'),)
        fundingsources = organizations.filter(organization_category__icontains=Organizations.STATUS_FINANCING)
        for item in fundingsources:
                        FUNDINGSOURCES = FUNDINGSOURCES + \
                            ((item.organization_id, item.organization_name),)
        self.fields['financing_agent'] = forms.MultipleChoiceField(
        choices= FUNDINGSOURCES[1:]  ,
        initial="",
        label="Financing Agent Name",
        required=True,
        validators=[],
        widget=forms.SelectMultiple(
            attrs={
                "id": "id_financing_agent",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),)


        IMPLEMENTERS_ = (('', '--select--'),)
        for item in organizations:
             IMPLEMENTERS_ = IMPLEMENTERS_ + \
                    ((item.organization_id, item.organization_name),)
        implementers = Implementers.objects.all()
        for item in implementers:
            IMPLEMENTERS_=IMPLEMENTERS_ + \
                    (("impl_"+ str(item.implementer_id), item.implementer_name),)   
            
        self.fields['implementer'] = forms.MultipleChoiceField(
            choices= IMPLEMENTERS_ [1:],
            initial="",
            label="Implementer Name",
            required=True,
            validators=[],
            widget=forms.SelectMultiple(
                attrs={
                    "id": "id_project_implementer",
                    "class": "form-control",
                    "style": "width:100%;",
                    "placeholder": "",
                }
            ),)
        


    class Meta:
        model = Projects
        fields = (
            'name',
            'financing_agent',
            'implementer',
            'funding_source',
            'organization_id',
            'start_time',
            'deadline',
        )


class ProjectsUpdateForm(forms.ModelForm):
    name = forms.CharField(
        label='Project Title',
        min_length=1,
        max_length=191,
        required=True,
        validators=[MinLengthValidator(1), MaxLengthValidator(191)],
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "",
            }
        ))
    financing_agent = forms.MultipleChoiceField(
        choices= (('', '--select--'),),
        initial="",
        label="Financing Agent Name",
        required=True,
        validators=[],
        widget=forms.SelectMultiple(
            attrs={
                "id": "id_financing_agent",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )
    
    implementer = forms.MultipleChoiceField(
        choices= (('', '--select--'),) ,
        initial="",
        label="Implementer Name",
        required=True,
        validators=[],
        widget=forms.SelectMultiple(
            attrs={
                "id": "id_project_implementer",
                 "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )
    funding_source = forms.MultipleChoiceField(
        choices= (('', '--select--'),),
        initial="",
        label="Funding Source",
        required=False,
        validators=[],
        widget=forms.SelectMultiple(
            attrs={
                "id": "id_project_funding_source",
               "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )
    organization_id = forms.ChoiceField(
        choices=(('', '--select--'),),
        initial="",
        label="Organization",
        required=True,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "search-input-select-organization-id",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ))
  
    start_time =forms.DateField(
        label="Start date",
        required=True,
        validators=[],
        # input_formats=['%Y-%m-%d %H:%M'],
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )
    
    deadline = forms.DateField(
        label="End date",
        required=True,
        validators=[],
        # input_formats=['%Y-%m-%d %H:%M'],
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
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

    def clean_name(self):
        data = self.cleaned_data["name"]
        return data
    
    def clean_financing_agent(self):
        data = self.cleaned_data['financing_agent']
        return data
    
    def clean_implementer(self):
        data = self.cleaned_data['implementer']
        return data
    
    def clean_funding_source(self):
        data = self.cleaned_data['funding_source']
        return data

    def clean_organization_id(self):
        data = self.cleaned_data["organization_id"]
        return data
    
    def clean_start_time(self):
        data = self.cleaned_data['start_time']
        return data
    
    def clean_deadline(self):
        data = self.cleaned_data["deadline"]
        if data is None:
            return None
        return str(data)
    
    def clean_assign_to(self):
        data = self.cleaned_data["assign_to"]
        return data

    def clean(self):
        cleaned_data = super(ProjectsUpdateForm, self).clean()
        return cleaned_data

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super(ProjectsUpdateForm, self).__init__(*args, **kwargs)

        ORGANIZATIONS= (('', '--select--'),)
        organizations = Organizations.objects.all()
        for item in organizations:
            ORGANIZATIONS=ORGANIZATIONS+ \
                ((item.organization_id, item.organization_name),)
            
        if user.user_role == Users.TYPE_ACTIVITY_MANAGER:
            ORGANIZATIONSID= (('', '--select--'),)
            organizations_activity_manager = organizations.filter(organization_id = user.organization_id)
            for item in organizations_activity_manager:
                ORGANIZATIONSID=ORGANIZATIONSID+ \
                    ((item.organization_id, item.organization_name),)
            self.fields['organization_id'] = forms.ChoiceField(
                choices=ORGANIZATIONSID[1:],
                initial='',
                label='Organization',
                required=True,
                validators=[],
                widget=forms.Select(
                    attrs={
                        'id': 'search-input-select-organization-id',
                        'class': 'form-control',
                        'style': 'width:100%;',
                        'placeholder': '--select--',
                    }
                ))
        else:    

            self.fields['organization_id'] = forms.ChoiceField(
                choices=ORGANIZATIONS[1:],
                initial='',
                label='Organization',
                required=True,
                validators=[],
                widget=forms.Select(
                    attrs={
                        'id': 'search-input-select-organization-id',
                        'class': 'form-control',
                        'style': 'width:100%;',
                        'placeholder': '--select--',
                    }
                ))
        self.fields['funding_source'] = forms.MultipleChoiceField(
        choices= ORGANIZATIONS[1:],
        initial="",
        label="Funding Source",
        required=False,
        validators=[],
        widget=forms.SelectMultiple(
            attrs={
                "id": "id_project_funding_source",
                 "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),)
        
        
        FUNDINGSOURCES = (('', '--select--'),)
        fundingsources = organizations.filter(organization_category__icontains=Organizations.STATUS_FINANCING)
        for item in fundingsources:
                        FUNDINGSOURCES = FUNDINGSOURCES + \
                            ((item.organization_id, item.organization_name),)
        self.fields['financing_agent'] = forms.MultipleChoiceField(
        choices= FUNDINGSOURCES[1:]  ,
        initial="",
        label="Financing Agent Name",
        required=True,
        validators=[],
        widget=forms.SelectMultiple(
            attrs={
                "id": "id_financing_agent",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),)


        IMPLEMENTERS_ = (('', '--select--'),)
        for item in organizations:
             IMPLEMENTERS_ = IMPLEMENTERS_ + \
                    ((item.organization_id, item.organization_name),)
        implementers = Implementers.objects.all()
        for item in implementers:
            IMPLEMENTERS_=IMPLEMENTERS_ + \
                    (("impl_"+ str(item.implementer_id), item.implementer_name),)
            
        self.fields['implementer'] = forms.MultipleChoiceField(
            choices= IMPLEMENTERS_ [1:],
            initial="",
            label="Implementer Name",
            required=True,
            validators=[],
            widget=forms.SelectMultiple(
                attrs={
                    "id": "id_project_implementer",
                    "class": "form-control",
                    "style": "width:100%;",
                    "placeholder": "",
                }
            ),)
        
        REPORTERS = (("0", "NONE"),)
        reporters = Users.objects.filter(organization_id = user.organization_id, user_role = Users.TYPE_DATA_REPORTER)
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
        model = Projects
        fields = (
            'name',
            'financing_agent',
            'implementer',
            'funding_source',
            'organization_id',
            'start_time',
            'deadline',
            'assign_to'
        )


class ProjectsViewForm(forms.ModelForm):
    name = forms.CharField(
        label='Project Title',
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
        ))
    
    financing_agent = forms.MultipleChoiceField(
        choices= (('', '--select--'),),
        initial="",
        label="Financing Agent Name",
        required=True,
        validators=[],
        widget=forms.SelectMultiple(
            attrs={
                "id": "id_financing_agent",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )
    
    implementer = forms.MultipleChoiceField(
        choices= (('', '--select--'),),
        initial="",
        label="Implementer Name",
        required=True,
        validators=[],
        widget=forms.SelectMultiple(
            attrs={
                "id": "id_project_implementer",
                 "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
                "readonly": True
            }
        ),
    )
    funding_source = forms.MultipleChoiceField(
        choices= (('', '--select--'),),
        initial="",
        label="Funding Source",
        required=False,
        validators=[],
        widget=forms.SelectMultiple(
            attrs={
                "id": "id_project_funding_source",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),
    )

    organization_id = forms.ChoiceField(
        choices=(('', '--select--'),),
        initial="",
        label="Organization",
        required=True,
        validators=[],
        widget=forms.Select(
            attrs={
                "id": "search-input-select-organization-id",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
                "readonly": True,
                "disabled": True,
            }
        ))
  
    start_time =forms.DateField(
        label="Start date",
        required=True,
        validators=[],
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
                "readonly": True,
                "disabled": True,
            }
        ),
    )
    
    deadline = forms.DateField(
        label="End date",
        required=True,
        validators=[],
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
                "readonly": True,
                "disabled": True,
            }
        ),
    )

    def clean_name(self):
        data = self.cleaned_data["name"]
        return data
    
    def clean_financing_agent(self):
        data = self.cleaned_data['financing_agent']
        return data
    
    def clean_implementer(self):
        data = self.cleaned_data['implementer']
        return data
    
    def clean_funding_source(self):
        data = self.cleaned_data['funding_source']
        return data

    def clean_organization_id(self):
        data = self.cleaned_data["organization_id"]
        return data
    
    def clean_start_time(self):
        data = self.cleaned_data['start_time']
        return data
    
    def clean_deadline(self):
        data = self.cleaned_data["deadline"]
        if data is None:
            return None
        return str(data)

    def clean(self):
        cleaned_data = super(ProjectsViewForm, self).clean()
        return cleaned_data

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super(ProjectsViewForm, self).__init__(*args, **kwargs)
        ORGANIZATIONS= (('', '--select--'),)
        organizations = Organizations.objects.all()
        for item in organizations:
            ORGANIZATIONS=ORGANIZATIONS+ \
                ((item.organization_id, item.organization_name),)
            
        if user.user_role == Users.TYPE_ACTIVITY_MANAGER:
            ORGANIZATIONSID= (('', '--select--'),)
            organizations_activity_manager = organizations.filter(organization_id = user.organization_id)
            for item in organizations_activity_manager:
                ORGANIZATIONSID=ORGANIZATIONSID+ \
                    ((item.organization_id, item.organization_name),)
            self.fields['organization_id'] = forms.ChoiceField(
                choices=ORGANIZATIONSID[1:],
                initial='',
                label='Organization',
                required=True,
                validators=[],
                widget=forms.Select(
                    attrs={
                        'id': 'search-input-select-organization-id',
                        'class': 'form-control',
                        'style': 'width:100%;',
                        'placeholder': '--select--',
                    }
                ))
        else:    

            self.fields['organization_id'] = forms.ChoiceField(
                choices=ORGANIZATIONS[1:],
                initial='',
                label='Organization',
                required=True,
                validators=[],
                widget=forms.Select(
                    attrs={
                        'id': 'search-input-select-organization-id',
                        'class': 'form-control',
                        'style': 'width:100%;',
                        'placeholder': '--select--',
                    }
                ))
        self.fields['funding_source'] = forms.MultipleChoiceField(
        choices= ORGANIZATIONS[1:],
        initial="",
        label="Funding Source",
        required=False,
        validators=[],
        widget=forms.SelectMultiple(
            attrs={
                "id": "id_project_funding_source",
                 "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),)
        
        
        FUNDINGSOURCES = (('', '--select--'),)
        fundingsources = organizations.filter(organization_category__icontains=Organizations.STATUS_FINANCING)
        for item in fundingsources:
                        FUNDINGSOURCES = FUNDINGSOURCES + \
                            ((item.organization_id, item.organization_name),)
        self.fields['financing_agent'] = forms.MultipleChoiceField(
        choices= FUNDINGSOURCES[1:]  ,
        initial="",
        label="Financing Agent Name",
        required=True,
        validators=[],
        widget=forms.SelectMultiple(
            attrs={
                "id": "id_financing_agent",
                "class": "form-control",
                "style": "width:100%;",
                "placeholder": "",
            }
        ),)


        IMPLEMENTERS_ = (('', '--select--'),)
        for item in organizations:
             IMPLEMENTERS_ = IMPLEMENTERS_ + \
                    ((item.organization_id, item.organization_name),)
        implementers = Implementers.objects.all()
        for item in implementers:
            IMPLEMENTERS_=IMPLEMENTERS_ + \
                    (("impl_"+ str(item.implementer_id), item.implementer_name),)
            
        self.fields['implementer'] = forms.MultipleChoiceField(
            choices= IMPLEMENTERS_ [1:],
            initial="",
            label="Implementer Name",
            required=True,
            validators=[],
            widget=forms.SelectMultiple(
                attrs={
                    "id": "id_project_implementer",
                    "class": "form-control",
                    "style": "width:100%;",
                    "placeholder": "",
                }
            ),)
    class Meta:
        model = Projects
        fields = (
            'name',
            'financing_agent',
            'implementer',
            'funding_source',
            'organization_id',
            'start_time',
            'deadline',
        )
