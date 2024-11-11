# Generated by Django 4.1.7 on 2023-08-17 14:24

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Access_Permissions',
            fields=[
                ('access_permission_name', models.CharField(max_length=100, primary_key=True, serialize=False, unique=True, verbose_name='Access Permission Name')),
                ('access_permission_details', models.CharField(blank=True, max_length=255, verbose_name='Details')),
                ('access_permission_created_at', models.IntegerField(default=0, verbose_name='Created At')),
                ('access_permission_updated_at', models.IntegerField(default=0, verbose_name='Updated At')),
            ],
        ),
        migrations.CreateModel(
            name='Activities',
            fields=[
                ('activity_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Activity Id')),
                ('project_id', models.IntegerField(default=0, verbose_name='Project')),
                ('activity_name', models.CharField(default=None, max_length=300, verbose_name='Name')),
                ('activity_location', models.CharField(default=None, max_length=191, verbose_name='Location')),
                ('activity_functions', models.CharField(default='', max_length=250, verbose_name='Function')),
                ('activity_sub_functions', models.CharField(default='', max_length=250, verbose_name='Sub Function')),
                ('activity_domain', models.CharField(default=None, max_length=191, verbose_name='Domain')),
                ('activity_sub_domain', models.CharField(default='-', max_length=191, verbose_name='Sub Domain')),
                ('activity_fiscal_year', models.CharField(default=None, max_length=191, verbose_name='Fiscal Year')),
                ('activity_created_at', models.IntegerField(default=0, verbose_name='Created At')),
                ('activity_created_by', models.IntegerField(default=0, verbose_name='Created By')),
                ('activity_updated_at', models.IntegerField(default=0, verbose_name='Updated At')),
                ('activity_updated_by', models.IntegerField(default=0, verbose_name='Updated By')),
                ('activity_submitted_at', models.IntegerField(default=0, verbose_name='Submitted At')),
                ('activity_submitted_by', models.IntegerField(default=0, verbose_name='Submitted By')),
                ('activity_accepted_at', models.IntegerField(default=0, verbose_name='Accepted At')),
                ('activity_accepted_by', models.IntegerField(default=0, verbose_name='Accepted By')),
                ('activity_rejected_at', models.IntegerField(default=0, verbose_name='Rejected At')),
                ('activity_rejected_by', models.IntegerField(default=0, verbose_name='Rejected By')),
                ('activity_approved_at', models.IntegerField(default=0, verbose_name='Approved At')),
                ('activity_approved_by', models.IntegerField(default=0, verbose_name='Approved By')),
                ('activity_denied_at', models.IntegerField(default=0, verbose_name='Approved At')),
                ('activity_denied_by', models.IntegerField(default=0, verbose_name='Approved By')),
                ('activity_status', models.IntegerField(default=0, verbose_name='Status')),
            ],
        ),
        migrations.CreateModel(
            name='Activities_Inputs',
            fields=[
                ('activity_input_id', models.AutoField(primary_key=True, serialize=False, verbose_name=' Id')),
                ('activity_id', models.IntegerField(default=0, verbose_name='Activity')),
                ('activity_input_class', models.CharField(default='', max_length=191, verbose_name='Input Class')),
                ('activity_input_sub_class', models.CharField(default='', max_length=191, verbose_name='Input Sub Class')),
                ('activity_input_scheme_class', models.CharField(default='', max_length=250, verbose_name='Financial schemes class')),
                ('activity_input_scheme_sub_class', models.CharField(default='', max_length=250, verbose_name='Financial schemes Sub class')),
                ('activity_input_funder', models.CharField(default='', max_length=191, verbose_name='Funder')),
                ('activity_input_funds_transfer_class', models.CharField(default=None, max_length=191, verbose_name='Funds Transfer Class')),
                ('activity_input_funds_transfer_sub_class', models.CharField(default=None, max_length=191, verbose_name='Funds Transfer Sub Class')),
                ('activity_input_implementer', models.CharField(default='', max_length=191, verbose_name='Implementer')),
                ('activity_input_division', models.CharField(default='', max_length=191, verbose_name='Division')),
                ('activity_input_budget', models.DecimalField(decimal_places=2, default=0.0, max_digits=20, verbose_name='Budget')),
                ('activity_input_budget_currency', models.CharField(default='', max_length=191, verbose_name='Budget Currency')),
                ('activity_input_expenses', models.DecimalField(decimal_places=2, default=0.0, max_digits=20, verbose_name='Expenditure')),
                ('activity_input_expenses_currency', models.CharField(default='', max_length=191, verbose_name='Expenditure Currency')),
                ('activity_input_created_at', models.IntegerField(default=0, verbose_name='Created At')),
                ('activity_input_created_by', models.IntegerField(default=0, verbose_name='Created By')),
                ('activity_input_updated_at', models.IntegerField(default=0, verbose_name='Updated At')),
                ('activity_input_updated_by', models.IntegerField(default=0, verbose_name='Updated By')),
                ('activity_input_budget_accepted_at', models.IntegerField(default=0, verbose_name='Budget Accepted At')),
                ('activity_input_budget_accepted_by', models.IntegerField(default=0, verbose_name='Budget  Accepted By')),
                ('activity_input_expenses_accepted_at', models.IntegerField(default=0, verbose_name='Expenditure Accepted At')),
                ('activity_input_expenses_accepted_by', models.IntegerField(default=0, verbose_name='Expenditure Accepted By')),
                ('activity_input_budget_rejected_at', models.IntegerField(default=0, verbose_name='Budget  Rejected At')),
                ('activity_input_budget_rejected_by', models.IntegerField(default=0, verbose_name='Budget  Rejected By')),
                ('activity_input_expenses_rejected_at', models.IntegerField(default=0, verbose_name='Expenditure Rejected At')),
                ('activity_input_expenses_rejected_by', models.IntegerField(default=0, verbose_name='Expenditure Rejected By')),
                ('activity_input_budget_approved_at', models.IntegerField(default=0, verbose_name='Budget  Approved At')),
                ('activity_input_budget_approved_by', models.IntegerField(default=0, verbose_name='Budget Approved By')),
                ('activity_input_expenses_approved_at', models.IntegerField(default=0, verbose_name='Expenditure Approved At')),
                ('activity_input_expenses_approved_by', models.IntegerField(default=0, verbose_name='Expenditure Approved By')),
                ('activity_input_budget_denied_at', models.IntegerField(default=0, verbose_name='Budget Approved At')),
                ('activity_input_budget_denied_by', models.IntegerField(default=0, verbose_name='Budget Approved By')),
                ('activity_input_expenses_denied_at', models.IntegerField(default=0, verbose_name='Expenditure Approved At')),
                ('activity_input_expenses_denied_by', models.IntegerField(default=0, verbose_name='Expenditure Approved By')),
                ('activity_input_status', models.IntegerField(default=0, verbose_name='Status')),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('comment_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Comment Id')),
                ('comment_model', models.CharField(default='', max_length=191, verbose_name='Model')),
                ('comment_model_id', models.CharField(default='', max_length=191, verbose_name='Model Id')),
                ('comment_parent_id', models.IntegerField(default=0, verbose_name='Parent')),
                ('comment_message', models.TextField(verbose_name='Message')),
                ('comment_section', models.CharField(default='', max_length=191, verbose_name='Section')),
                ('comment_to', models.IntegerField(default=0, verbose_name='To')),
                ('comment_updated_at', models.IntegerField(default=0, verbose_name='Updated At')),
                ('comment_updated_id', models.IntegerField(default=0, verbose_name='Updated Id')),
                ('comment_updated_by', models.CharField(default='', max_length=191, verbose_name='Updated By')),
                ('comment_updated_by_email', models.CharField(default='', max_length=191, verbose_name='Updated By Email')),
                ('comment_updated_by_phone', models.CharField(default='', max_length=191, verbose_name='Updated By Phone')),
            ],
        ),
        migrations.CreateModel(
            name='Currency_Rates',
            fields=[
                ('rate_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Currency Rate Id')),
                ('rate_fiscal_year', models.CharField(default=None, max_length=191, verbose_name='Fiscal Year')),
                ('rate_currency', models.CharField(default=None, max_length=191, verbose_name='Currency')),
                ('rate_rate', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Rate')),
                ('rate_created_at', models.IntegerField(default=0, verbose_name='Created At')),
                ('rate_created_by', models.IntegerField(default=0, verbose_name='Created By')),
                ('rate_updated_at', models.IntegerField(default=0, verbose_name='Updated At')),
                ('rate_updated_by', models.IntegerField(default=0, verbose_name='Updated By')),
            ],
        ),
        migrations.CreateModel(
            name='Failed_Login',
            fields=[
                ('failed_login_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Id')),
                ('failed_login_username', models.CharField(max_length=255, verbose_name='Username')),
                ('failed_login_password', models.CharField(max_length=255, verbose_name='Password')),
                ('failed_login_from', models.CharField(choices=[('backend', 'backend'), ('frontend', 'frontend')], default='frontend', max_length=20, verbose_name='From')),
                ('failed_login_ip_address', models.CharField(max_length=100, verbose_name='Ip Address')),
                ('failed_login_attempted_at', models.IntegerField(default=0, verbose_name='Updated At')),
                ('failed_login_status', models.IntegerField(default=0, verbose_name='Status')),
            ],
            options={
                'db_table': 'failed_login',
            },
        ),
        migrations.CreateModel(
            name='Files',
            fields=[
                ('file_id', models.AutoField(primary_key=True, serialize=False, verbose_name='File Id')),
                ('file_model', models.CharField(max_length=191, verbose_name='Model')),
                ('file_model_id', models.CharField(max_length=191, verbose_name='Model Id')),
                ('file_model_no', models.CharField(default=0, max_length=191, verbose_name='Model No')),
                ('file_name', models.CharField(max_length=191, verbose_name='Name')),
                ('file_size', models.BigIntegerField(default=0, verbose_name='Size')),
                ('file_type', models.CharField(max_length=191, verbose_name='Type')),
                ('file_mime', models.CharField(max_length=191, verbose_name='Mime')),
                ('file_path', models.CharField(max_length=191, verbose_name='Path')),
                ('file_name_ext', models.CharField(max_length=191, verbose_name='Code')),
                ('file_parent_id', models.IntegerField(default=0, verbose_name='Parent Id')),
                ('file_directory_code', models.CharField(default='', max_length=191, verbose_name='Directory Code')),
                ('file_directory_name', models.CharField(default='', max_length=191, verbose_name='Directory Name')),
                ('file_uploaded_response', models.TextField(default='', verbose_name='Uploaded Response')),
                ('file_office_key', models.CharField(default='', max_length=191, verbose_name='Office File Key')),
                ('file_office_name', models.CharField(default='', max_length=191, verbose_name='Office File Name')),
                ('file_office_type', models.CharField(default='', max_length=191, verbose_name='Office File Type')),
                ('file_office_directory_code', models.CharField(default='', max_length=191, verbose_name='Office Directory Code')),
                ('file_office_directory_name', models.CharField(default='', max_length=191, verbose_name='Office Directory Name')),
                ('file_office_uploaded', models.IntegerField(default=0, verbose_name='Office Uploaded')),
                ('file_office_uploaded_response', models.TextField(default='', verbose_name='Office Uploaded Response')),
                ('file_public', models.BooleanField(default=False)),
                ('file_created_at', models.IntegerField(default=0, verbose_name='Created At')),
                ('file_created_id', models.IntegerField(default=0, verbose_name='Created Id')),
                ('file_created_by', models.CharField(max_length=191, verbose_name='Created By')),
                ('file_updated_at', models.IntegerField(default=0, verbose_name='Updated At')),
                ('file_updated_id', models.IntegerField(default=0, verbose_name='Updated Id')),
                ('file_updated_by', models.CharField(max_length=191, verbose_name='Updated By')),
                ('file_deleted_at', models.IntegerField(default=0, verbose_name='Deleted At')),
                ('file_deleted_id', models.IntegerField(default=0, verbose_name='Deleted Id')),
                ('file_deleted_by', models.CharField(default='', max_length=191, verbose_name='Deleted By')),
                ('file_status', models.CharField(default='', max_length=191, verbose_name='Status')),
            ],
        ),
        migrations.CreateModel(
            name='Fundings',
            fields=[
                ('funding_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Funding Id')),
                ('project_id', models.IntegerField(default=0, verbose_name='Project')),
                ('funder_id', models.IntegerField(default=0, verbose_name='Funders')),
                ('funding_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=20, verbose_name='Funded Amount')),
                ('funding_currency', models.CharField(default=None, max_length=191, verbose_name='currency')),
                ('funding_created_at', models.IntegerField(default=0, verbose_name='Created At')),
                ('funding_created_by', models.IntegerField(default=0, verbose_name='Created By')),
                ('funding_updated_at', models.IntegerField(default=0, verbose_name='Updated At')),
                ('funding_updated_by', models.IntegerField(default=0, verbose_name='Updated By')),
            ],
        ),
        migrations.CreateModel(
            name='Gdp_Populations',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='Configurables Id')),
                ('fiscal_year', models.CharField(default=None, max_length=191, verbose_name='Fiscal Year')),
                ('population', models.BigIntegerField(default=0, verbose_name='Total Population')),
                ('budget', models.BigIntegerField(default=0, verbose_name='Total Government Budget')),
                ('expenditure', models.BigIntegerField(default=0, verbose_name='Total Government Expenditure')),
                ('gdp', models.BigIntegerField(default=0, verbose_name='GDP')),
                ('payment_rate', models.DecimalField(decimal_places=1, default=0.0, max_digits=3, verbose_name='Co-Payment Rate')),
                ('created_at', models.IntegerField(default=0, verbose_name='Created At')),
                ('created_by', models.IntegerField(default=0, verbose_name='Created By')),
                ('updated_at', models.IntegerField(default=0, verbose_name='Updated At')),
                ('updated_by', models.IntegerField(default=0, verbose_name='Updated By')),
            ],
        ),
        migrations.CreateModel(
            name='Implementers',
            fields=[
                ('implementer_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Id')),
                ('implementer_name', models.CharField(default='', max_length=191, verbose_name='Implementer Name')),
                ('implementer_created_at', models.IntegerField(default=0, verbose_name='Created At')),
                ('implementer_created_by', models.IntegerField(default=0, verbose_name='Created By')),
                ('implementer_updated_at', models.IntegerField(default=0, verbose_name='Updated At')),
                ('implementer_updated_by', models.IntegerField(default=0, verbose_name='Updated By')),
            ],
        ),
        migrations.CreateModel(
            name='Levels',
            fields=[
                ('level_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Level Id')),
                ('level_key', models.CharField(default=None, max_length=191, verbose_name='Key')),
                ('level_code', models.CharField(default=None, max_length=191, verbose_name='Code')),
                ('level_name', models.CharField(default=None, max_length=191, verbose_name='Name')),
                ('level_parent', models.IntegerField(default=0, verbose_name='Parent')),
                ('level_created_at', models.IntegerField(default=0, verbose_name='Created At')),
                ('level_created_by', models.IntegerField(default=0, verbose_name='Created By')),
                ('level_updated_at', models.IntegerField(default=0, verbose_name='Updated At')),
                ('level_updated_by', models.IntegerField(default=0, verbose_name='Updated By')),
                ('level_status', models.IntegerField(default=4, verbose_name='Status')),
            ],
        ),
        migrations.CreateModel(
            name='MailServerConfig',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='Id')),
                ('host', models.CharField(max_length=191, verbose_name='Host')),
                ('port', models.IntegerField(verbose_name='Port')),
                ('username', models.CharField(max_length=191, verbose_name='User Name')),
                ('password', models.CharField(max_length=191, verbose_name='Password')),
                ('sender', models.CharField(default='', max_length=191, verbose_name='Sender')),
                ('subject_prefix', models.CharField(default='', max_length=191, verbose_name='Subject Prefix')),
                ('tls_enabled', models.BooleanField(default=True, verbose_name='TLS')),
                ('ssl_enabled', models.BooleanField(default=False, verbose_name='SSL')),
                ('created_at', models.IntegerField(default=0, verbose_name='Created At')),
                ('created_by', models.IntegerField(default=0, verbose_name='Created By')),
                ('updated_at', models.IntegerField(default=0, verbose_name='Updated At')),
                ('updated_by', models.IntegerField(default=0, verbose_name='Updated By')),
            ],
        ),
        migrations.CreateModel(
            name='Organizations',
            fields=[
                ('organization_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Organization Id')),
                ('organization_name', models.CharField(default=None, max_length=191, unique=True, verbose_name='Name')),
                ('organization_email', models.EmailField(default='', max_length=100, verbose_name='Email')),
                ('organization_phone_number', models.CharField(blank=True, max_length=13, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+250123456789'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$'), django.core.validators.MinLengthValidator(10), django.core.validators.MaxLengthValidator(15)], verbose_name='Phone Number')),
                ('organization_type', models.CharField(default='', max_length=191, verbose_name='Type')),
                ('organization_sub_type', models.CharField(default='', max_length=191, verbose_name='Sub Type')),
                ('organization_category', models.CharField(default='', max_length=191, verbose_name='Category')),
                ('organization_financial_agent_class', models.CharField(default='', max_length=250, verbose_name='Financial Agency class')),
                ('organization_financial_agent_sub_class', models.CharField(default='', max_length=250, verbose_name='Financial Agency Sub class')),
                ('organization_financial_schemes_name', models.CharField(default='', max_length=250, verbose_name='Financial schemes Name')),
                ('organization_financial_schemes_class', models.CharField(default='', max_length=250, verbose_name='Financial schemes class')),
                ('organization_financial_schemes_sub_class', models.CharField(default='', max_length=250, verbose_name='Financial schemes Sub class')),
                ('organization_financial_sources_class', models.CharField(default='', max_length=250, verbose_name='Financial Sources class')),
                ('organization_financial_sources_sub_class', models.CharField(default='', max_length=250, verbose_name='Financial Sources Sub class')),
                ('organization_healthcare_class', models.CharField(default='', max_length=250, verbose_name='HealthCare Provider Class')),
                ('organization_healthcare_sub_class', models.CharField(default='', max_length=250, verbose_name='HealthCare Provider Sub Class')),
                ('organization_created_at', models.IntegerField(default=0, verbose_name='Created At')),
                ('organization_created_by', models.IntegerField(default=0, verbose_name='Created By')),
                ('organization_updated_at', models.IntegerField(default=0, verbose_name='Updated At')),
                ('organization_updated_by', models.IntegerField(default=0, verbose_name='Updated By')),
                ('organization_status', models.IntegerField(default=5, verbose_name='Status')),
            ],
        ),
        migrations.CreateModel(
            name='Projects',
            fields=[
                ('project_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Project Id')),
                ('organization_id', models.IntegerField(default=0, verbose_name='Organization')),
                ('project_name', models.CharField(default=None, max_length=250, verbose_name='Project Title')),
                ('project_financing_agent', models.CharField(default='', max_length=250, verbose_name='Financing Agent')),
                ('project_implementer', models.CharField(default='', max_length=250, verbose_name='Implementer')),
                ('project_tags', models.CharField(default='', max_length=250, verbose_name='Tags')),
                ('project_start_date', models.DateField(blank=True, null=True)),
                ('project_deadline', models.DateField(blank=True, null=True)),
                ('project_created_at', models.IntegerField(default=0, verbose_name='Created At')),
                ('project_created_by', models.IntegerField(default=0, verbose_name='Created By')),
                ('project_updated_at', models.IntegerField(default=0, verbose_name='Updated At')),
                ('project_updated_by', models.IntegerField(default=0, verbose_name='Updated By')),
                ('project_assigned_at', models.IntegerField(default=0, verbose_name='Assigned At')),
                ('project_assigned_by', models.IntegerField(default=0, verbose_name='Assigned By')),
                ('project_assigned_to', models.IntegerField(default=0, verbose_name='Assigned To')),
                ('project_status', models.IntegerField(default=0, verbose_name='Status')),
            ],
        ),
        migrations.CreateModel(
            name='Reports',
            fields=[
                ('report_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Report Id')),
                ('project_id', models.IntegerField(default=0, verbose_name='Project')),
                ('report_asset_name', models.CharField(default=None, max_length=191, verbose_name='Asset Name')),
                ('report_capital_class', models.CharField(default='', max_length=191, verbose_name='Capital Class')),
                ('report_capital_sub_class', models.CharField(default='', max_length=191, verbose_name='Capital Sub Class')),
                ('report_purchase_value', models.DecimalField(decimal_places=2, default=0.0, max_digits=20, verbose_name='Purchase Value')),
                ('report_purchase_currency', models.CharField(default='', max_length=191, verbose_name='Purchase Value Currrency')),
                ('report_book_value', models.DecimalField(decimal_places=2, default=0.0, max_digits=20, verbose_name='Book Amount')),
                ('report_book_currency', models.CharField(default='', max_length=191, verbose_name='Book Value Currrency')),
                ('report_year_purchased', models.CharField(default='', max_length=191, verbose_name='Year Purchased')),
                ('report_funding_source', models.CharField(default='', max_length=191, verbose_name='Funding Source')),
                ('report_funds_transfer_class', models.TextField(default=None, max_length=191, verbose_name='Funds Transfer Class')),
                ('report_fiscal_year', models.CharField(default=None, max_length=191, verbose_name='Fiscal Year')),
                ('report_created_at', models.IntegerField(default=0, verbose_name='Created At')),
                ('report_created_by', models.IntegerField(default=0, verbose_name='Created By')),
                ('report_updated_at', models.IntegerField(default=0, verbose_name='Updated At')),
                ('report_updated_by', models.IntegerField(default=0, verbose_name='Updated By')),
                ('report_submitted_at', models.IntegerField(default=0, verbose_name='Submitted At')),
                ('report_submitted_by', models.IntegerField(default=0, verbose_name='Submitted By')),
                ('report_accepted_at', models.IntegerField(default=0, verbose_name='Accepted At')),
                ('report_accepted_by', models.IntegerField(default=0, verbose_name='Accepted By')),
                ('report_rejected_at', models.IntegerField(default=0, verbose_name='Rejected At')),
                ('report_rejected_by', models.IntegerField(default=0, verbose_name='Rejected By')),
                ('report_approved_at', models.IntegerField(default=0, verbose_name='Approved At')),
                ('report_approved_by', models.IntegerField(default=0, verbose_name='Approved By')),
                ('report_denied_at', models.IntegerField(default=0, verbose_name='Approved At')),
                ('report_denied_by', models.IntegerField(default=0, verbose_name='Approved By')),
                ('report_status', models.IntegerField(default=0, verbose_name='Status')),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False, verbose_name='User Id')),
                ('user_type', models.CharField(choices=[('', '--select--'), ('super-admin', 'Super Admin'), ('admin', 'Admin'), ('staff', 'Staff'), ('other', 'Other')], default='other', max_length=20, verbose_name='Type')),
                ('user_username', models.CharField(max_length=100, unique=True, verbose_name='Username')),
                ('user_auth_key', models.CharField(max_length=255, verbose_name='Auth key')),
                ('user_password_hash', models.CharField(max_length=255, verbose_name='Password')),
                ('user_password_reset_token', models.CharField(blank=True, max_length=255, verbose_name='Password reset token')),
                ('user_name', models.CharField(max_length=100, verbose_name='Name')),
                ('user_first_name', models.CharField(default='', max_length=50, verbose_name='First Name')),
                ('user_middle_name', models.CharField(default='', max_length=50, verbose_name='Middle Name')),
                ('user_last_name', models.CharField(default='', max_length=50, verbose_name='Last Name')),
                ('user_gender', models.CharField(choices=[('', '--select--'), ('male', 'Male'), ('female', 'Female'), ('other', 'Other')], default='', max_length=6, verbose_name='Gender')),
                ('user_contact_phone_number', models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+250123456789'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$'), django.core.validators.MinLengthValidator(10), django.core.validators.MaxLengthValidator(15)], verbose_name='Phone Number')),
                ('user_contact_email_id', models.EmailField(blank=True, max_length=100, verbose_name='Email id')),
                ('user_profile_photo_file_path', models.CharField(blank=True, max_length=255, verbose_name='Profile photo file path')),
                ('user_role', models.CharField(blank=True, max_length=255, verbose_name='Role')),
                ('organization_id', models.IntegerField(default=0, verbose_name='Organization')),
                ('user_created_at', models.IntegerField(default=0, verbose_name='Created At')),
                ('user_created_by', models.IntegerField(default=0, verbose_name='Created By')),
                ('user_updated_at', models.IntegerField(default=0, verbose_name='Updated At')),
                ('user_updated_by', models.IntegerField(default=0, verbose_name='Updated By')),
                ('user_status', models.IntegerField(default=3, verbose_name='Status')),
            ],
        ),
        migrations.CreateModel(
            name='User_Access_Permissions',
            fields=[
                ('user_access_permission_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Id')),
                ('user_access_permission_updated_at', models.IntegerField(default=0, verbose_name='Updated At')),
                ('user_access_permission_updated_by', models.IntegerField(default=0, verbose_name='Updated By')),
                ('access_permissions_access_permission_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.access_permissions')),
                ('users_user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.users')),
            ],
        ),
    ]
