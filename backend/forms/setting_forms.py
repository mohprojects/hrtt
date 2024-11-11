from django import forms


class SettingExcelImportForm(forms.ModelForm):
    excel_file = forms.FileField(
        label="Excel File",
        required=True,
        validators=[],
        widget=forms.FileInput(
            attrs={
                "class": "form-control",
                "accept": ".csv, application/vnd.ms-excel, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            }
        ),
    )

    def clean_excel_file(self):
        excel_file = self.cleaned_data["excel_file"]
        return excel_file

    def clean(self):
        cleaned_data = super(SettingExcelImportForm, self).clean()
        return cleaned_data

    class Meta:
        fields = ()


class SettingJsonImportForm(forms.ModelForm):
    json_file = forms.FileField(
        label="Json File",
        required=False,
        validators=[],
        widget=forms.FileInput(
            attrs={
                "class": "form-control",
                "accept": ".json",
            }
        ),
    )

    def clean_json_file(self):
        json_file = self.cleaned_data["json_file"]
        return json_file

    def clean(self):
        cleaned_data = super(SettingJsonImportForm, self).clean()
        return cleaned_data

    class Meta:
        fields = ()
