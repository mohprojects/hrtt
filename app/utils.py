import base64
import datetime
import json
import os
import re
import time
from django.utils.crypto import get_random_string
import pytz

from PIL import Image

from django.utils import dateparse
from django.utils import timezone

from app import settings
from app.models.currency_rates import Currency_Rates


class Utils(object):
    @staticmethod
    def get_app_domain():
        if settings.IS_LOCAL:
            domain = settings.APP_DOMAIN_LOCAL
        else:
            domain = settings.APP_DOMAIN_PROD
        return domain

    @staticmethod
    def get_backend_domain():
        if settings.IS_LOCAL:
            domain = settings.BACKEND_DOMAIN_LOCAL
        else:
            domain = settings.BACKEND_DOMAIN_PROD
        return domain

    @staticmethod
    def get_frontend_domain():
        if settings.IS_LOCAL:
            domain = settings.FRONTEND_DOMAIN_LOCAL
        else:
            domain = settings.FRONTEND_DOMAIN_PROD
        return domain

    @staticmethod
    def get_office_domain():
        if settings.IS_LOCAL:
            domain = settings.OFFICE_DOMAIN_LOCAL
        else:
            domain = settings.OFFICE_DOMAIN_PROD
        return domain

    @staticmethod
    def get_random_basic_string(length):
        return get_random_string(
            length,
            allowed_chars="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
        )

    @staticmethod
    def format_device_date(value):
        index1 = -1
        index2 = -1
        index = -1
        counter = 0
        for c in value:
            index = index + 1
            # print(c)
            if c == "/":
                counter = counter + 1
                if counter == 1:
                    index1 = index
                if counter == 2:
                    index2 = index

        # print(index1)
        # print(index2)

        date = value[0:index1]
        # print('Date: %s', date)
        month = value[index1 + 1 : index2]
        # print('Month: %s', month)
        year = value[index2 + 1 : len(value)]
        # print('Year: %s', year)

        if int(date) < 10:
            str_date = "0" + date
        else:
            str_date = "" + date
        if int(month) < 10:
            str_month = "0" + month
        else:
            str_month = "" + month
        if int(year) < 10:
            str_year = "000" + year
        elif int(year) < 100:
            str_year = "00" + year
        elif int(year) < 1000:
            str_year = "0" + year
        else:
            str_year = "" + year

        value = str_year + "-" + str_month + "-" + str_date
        print(value)
        return value

    @staticmethod
    def format_device_time(value):
        index1 = -1
        index2 = -1
        index = -1
        counter = 0
        for c in value:
            index = index + 1
            # print(c)
            if c == ":":
                counter = counter + 1
                if counter == 1:
                    index1 = index
                if counter == 2:
                    index2 = index

        # print(index1)
        # print(index2)

        hours = value[0:index1]
        # print('Hours: %s', hours)
        minutes = value[index1 + 1 : index2]
        # print('Minutes: %s', minutes)
        seconds = value[index2 + 1 : len(value)]
        # print('Seconds: %s', seconds)

        if int(hours) < 10:
            str_hours = "0" + hours
        else:
            str_hours = "" + hours
        if int(minutes) < 10:
            str_minutes = "0" + minutes
        else:
            str_minutes = "" + minutes
        if int(seconds) < 10:
            str_seconds = "0" + seconds
        else:
            str_seconds = "" + seconds

        value = str_hours + ":" + str_minutes + ":" + str_seconds
        print(value)
        return value

    @staticmethod
    def convert_string_to_datetime(value):
        value = datetime.datetime.strptime(
            value, settings.APP_CONSTANT_INPUT_DATETIME_FORMAT
        )
        return value
    
    @staticmethod
    def convert_string_to_date(value):
        value = datetime.datetime.strptime(
            value, settings.APP_CONSTANT_INPUT_DATE_FORMAT
        ).date()
        return value

    @staticmethod
    def get_epochtime_ms():
        return round(datetime.datetime.utcnow().timestamp() * 1000)

    @staticmethod
    def get_current_datetime_utc():
        if settings.TIME_IN_SECONDS:
            return round(datetime.datetime.utcnow().timestamp())
        return datetime.datetime.now(tz=timezone.utc).strftime(
            settings.APP_CONSTANT_INPUT_DATETIME_FORMAT
        )

    @staticmethod
    def get_midnight_datetime_utc():
        now = datetime.datetime.utcnow()
        if settings.TIME_IN_SECONDS:
            return round(
                now.replace(hour=0, minute=0, second=0, microsecond=0).timestamp()
            )
        return now.replace(hour=0, minute=0, second=0, microsecond=0)

    @staticmethod
    def get_before_datetime_utc(before):
        return (
            datetime.datetime.now(tz=timezone.utc) - datetime.timedelta(minutes=before)
        ).strftime(settings.APP_CONSTANT_INPUT_DATETIME_FORMAT)

    @staticmethod
    def get_convert_datetime(value, tz_from, tz_to):
        if settings.TIME_IN_SECONDS:
            if int(value) == 0:
                return "N/A"
            value = datetime.datetime.fromtimestamp(value).strftime(
                settings.APP_CONSTANT_INPUT_DATETIME_FORMAT
            )
        else:
            value = datetime.datetime.strftime(
                value, settings.APP_CONSTANT_INPUT_DATETIME_FORMAT
            )
        value = dateparse.parse_datetime(value)
        utc_dt = pytz.timezone(tz_from).localize(value)
        display_dt = utc_dt.astimezone(pytz.timezone(tz_to))
        return datetime.datetime.strftime(
            display_dt, settings.APP_CONSTANT_DISPLAY_DATETIME_FORMAT
        )

    @staticmethod
    def get_convert_datetime_in_milliseconds(value, tz_from, tz_to):
        value = datetime.datetime.strftime(
            value, settings.APP_CONSTANT_INPUT_DATETIME_FORMAT
        )
        value = dateparse.parse_datetime(value)
        utc_dt = pytz.timezone(tz_from).localize(value)
        display_dt = utc_dt.astimezone(pytz.timezone(tz_to))
        display_dt = datetime.datetime.strftime(
            display_dt, settings.APP_CONSTANT_DISPLAY_DATETIME_FORMAT
        )
        d = datetime.datetime.strptime(
            display_dt, settings.APP_CONSTANT_DISPLAY_DATETIME_FORMAT
        )
        return int(time.mktime(d.timetuple()))

    @staticmethod
    def get_convert_datetime_other(value, tz_from, tz_to):
        if settings.TIME_IN_SECONDS:
            value = datetime.datetime.fromtimestamp(value).strftime(
                settings.APP_CONSTANT_INPUT_DATETIME_FORMAT
            )
        else:
            value = datetime.datetime.strftime(
                value, settings.APP_CONSTANT_INPUT_DATETIME_FORMAT
            )
        value = dateparse.parse_datetime(value)
        utc_dt = pytz.timezone(tz_from).localize(value)
        display_dt = utc_dt.astimezone(pytz.timezone(tz_to))
        return datetime.datetime.strftime(
            display_dt, settings.APP_CONSTANT_DISPLAY_DATETIME_FORMAT_OTHER
        )

    # refer http://strftime.org/
    @staticmethod
    def get_string_date(value):
        value = datetime.datetime.strptime(value, "%Y-%m-%d").strftime("%Y-%m-%d")
        return value

    @staticmethod
    def get_format_input_date(value):
        value = datetime.datetime.strptime(value, "%Y-%m-%d").strftime("%Y-%m-%d")
        
        return value

    @staticmethod
    def get_format_display_date(value):
        value = datetime.datetime.strptime(value, "%Y-%m-%d").strftime("%d %b %Y")
        return value

    @staticmethod
    def pretty_date(time=False):
        """
        Get a datetime object or a int() Epoch timestamp and return a
        pretty string like 'an hour ago', 'Yesterday', '3 months ago',
        'just now', etc
        """
        now = datetime.datetime.now()
        if type(time) is int:
            diff = now - datetime.datetime.fromtimestamp(time)
        elif isinstance(time, datetime.datetime):
            diff = now - time
        elif not time:
            diff = now - now
        else:
            diff = now - now
        second_diff = diff.seconds
        day_diff = diff.days

        if day_diff < 0:
            return ""

        if day_diff == 0:
            if second_diff < 10:
                return "just now"
            if second_diff < 60:
                return str(int(round(second_diff, 0))) + " seconds ago"
            if second_diff < 120:
                return "a minute ago"
            if second_diff < 3600:
                return str(int(round(second_diff / 60, 0))) + " minutes ago"
            if second_diff < 7200:
                return "an hour ago"
            if second_diff < 86400:
                return str(int(round(second_diff / 3600, 0))) + " hours ago"
        if day_diff == 1:
            return "Yesterday"
        if day_diff < 7:
            return str(int(round(day_diff, 0))) + " days ago"
        if day_diff < 31:
            return str(int(round(day_diff / 7, 0))) + " weeks ago"
        if day_diff < 365:
            return str(int(round(day_diff / 30, 0))) + " months ago"
        return str(int(round(day_diff / 365, 0))) + " years ago"

    @staticmethod
    def bytes_2_human_readable(number_of_bytes):
        if number_of_bytes < 0:
            raise ValueError("!!! number_of_bytes can't be smaller than 0 !!!")

        step_to_greater_unit = 1024.0

        number_of_bytes = float(number_of_bytes)
        unit = "bytes"

        if (number_of_bytes / step_to_greater_unit) >= 1:
            number_of_bytes /= step_to_greater_unit
            unit = "KB"

        if (number_of_bytes / step_to_greater_unit) >= 1:
            number_of_bytes /= step_to_greater_unit
            unit = "MB"

        if (number_of_bytes / step_to_greater_unit) >= 1:
            number_of_bytes /= step_to_greater_unit
            unit = "GB"

        if (number_of_bytes / step_to_greater_unit) >= 1:
            number_of_bytes /= step_to_greater_unit
            unit = "TB"

        precision = 1
        number_of_bytes = round(number_of_bytes, precision)

        return str(number_of_bytes) + " " + unit

    @staticmethod
    def save_file_by_bytes(file_data_in_bytes, file_path):
        f = open(file_path, "wb")
        f.write(file_data_in_bytes)
        f.close()

    @staticmethod
    def save_image_base64(image_data, file_path):
        format, file_string = image_data.split(";base64,")
        # print("format", format)
        format.split("/")[-1]
        # print("file_string", file_string)
        # print("ext", ext)
        file_bytes = base64.b64decode(file_string)
        # print("file_bytes", file_bytes)
        f = open(file_path, "wb")
        f.write(file_bytes)
        f.close()

    @staticmethod
    def save_image_from_file_path(file_path):
        try:
            image = Image.open(file_path)
            if not image:
                return None
            filename = str(Utils.get_epochtime_ms()) + ".png"
            file_path = settings.MEDIA_ROOT + "/temp/" + filename
            image.file.seek(0)
            pil_image = Image.open(image.file)
            pil_image.save(file_path, "PNG")
            return filename
        except Exception:
            return None

    @staticmethod
    def readimage(path):
        os.stat(path).st_size / 2
        with open(path, "rb") as f:
            return bytearray(f.read())

    @staticmethod
    def delete_file(path):
        """Deletes file from filesystem."""
        if os.path.isfile(path):
            os.remove(path)

    @staticmethod
    def get_ip_address(request):
        # request.environ['REMOTE_ADDR']
        # request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        return request.environ["REMOTE_ADDR"]

    @staticmethod
    def get_browser_details_from_request(request):
        return (
            "Browser:"
            + request.user_agent.browser.family
            + " "
            + request.user_agent.browser.version_string
            + " Device:"
            + request.user_agent.device.family
            + " OS:"
            + request.user_agent.os.family
            + " "
            + request.user_agent.os.version_string
        )

    @staticmethod
    def hex_to_rgb(value):
        value = value.lstrip("#")
        lv = len(value)
        return tuple(int(value[i : i + lv / 3], 16) for i in range(0, lv, lv / 3))

    @staticmethod
    def rgb_to_hex(rgb):
        return "#%02x%02x%02x" % rgb

    @staticmethod
    def is_json(data):
        try:
            json.loads(data)
        except ValueError:
            return False
        return True

    @staticmethod
    def is_json_or_xml(data):
        # Remove tabs, spaces, and new lines when reading
        data = re.sub(r"\s+", "", data)
        if re.match(r"^({|[).+(}|])$", data):
            return 1
        if re.match(r"^<.+>$", data):
            return 2
        return 0

    @staticmethod
    def last_day_of_month(date):
        if date.month == 12:
            return date.replace(day=31)
        return date.replace(month=date.month + 1, day=1) - datetime.timedelta(days=1)

    @staticmethod
    def get_day(index):
        if index == str(0):
            return "Sun"
        if index == str(1):
            return "Mon"
        if index == str(2):
            return "Tue"
        if index == str(3):
            return "Wed"
        if index == str(4):
            return "Thu"
        if index == str(5):
            return "Fri"
        if index == str(6):
            return "Sat"
        return ""

    @staticmethod
    def get_days_array(index, last_day_date):
        days = {}
        days[0] = Utils.get_day(index)
        index = Utils.get_next_day_index(index)
        days[1] = Utils.get_day(index)
        index = Utils.get_next_day_index(index)
        days[2] = Utils.get_day(index)
        index = Utils.get_next_day_index(index)
        days[3] = Utils.get_day(index)
        index = Utils.get_next_day_index(index)
        days[4] = Utils.get_day(index)
        index = Utils.get_next_day_index(index)
        days[5] = Utils.get_day(index)
        index = Utils.get_next_day_index(index)
        days[6] = Utils.get_day(index)
        index = Utils.get_next_day_index(index)
        days[7] = Utils.get_day(index)
        index = Utils.get_next_day_index(index)
        days[8] = Utils.get_day(index)
        index = Utils.get_next_day_index(index)
        days[9] = Utils.get_day(index)
        index = Utils.get_next_day_index(index)
        days[10] = Utils.get_day(index)
        index = Utils.get_next_day_index(index)
        days[11] = Utils.get_day(index)
        index = Utils.get_next_day_index(index)
        days[12] = Utils.get_day(index)
        index = Utils.get_next_day_index(index)
        days[13] = Utils.get_day(index)
        index = Utils.get_next_day_index(index)
        days[14] = Utils.get_day(index)
        index = Utils.get_next_day_index(index)
        days[15] = Utils.get_day(index)
        index = Utils.get_next_day_index(index)
        days[16] = Utils.get_day(index)
        index = Utils.get_next_day_index(index)
        days[17] = Utils.get_day(index)
        index = Utils.get_next_day_index(index)
        days[18] = Utils.get_day(index)
        index = Utils.get_next_day_index(index)
        days[19] = Utils.get_day(index)
        index = Utils.get_next_day_index(index)
        days[20] = Utils.get_day(index)
        index = Utils.get_next_day_index(index)
        days[21] = Utils.get_day(index)
        index = Utils.get_next_day_index(index)
        days[22] = Utils.get_day(index)
        index = Utils.get_next_day_index(index)
        days[23] = Utils.get_day(index)
        index = Utils.get_next_day_index(index)
        days[24] = Utils.get_day(index)
        index = Utils.get_next_day_index(index)
        days[25] = Utils.get_day(index)
        index = Utils.get_next_day_index(index)
        days[26] = Utils.get_day(index)

        index = Utils.get_next_day_index(index)
        if int(last_day_date) >= 28:
            days[27] = Utils.get_day(index)
        else:
            days[27] = ""

        index = Utils.get_next_day_index(index)
        if int(last_day_date) >= 29:
            days[28] = Utils.get_day(index)
        else:
            days[28] = ""

        index = Utils.get_next_day_index(index)
        if int(last_day_date) >= 30:
            days[29] = Utils.get_day(index)
        else:
            days[29] = ""

        index = Utils.get_next_day_index(index)
        if int(last_day_date) >= 31:
            days[30] = Utils.get_day(index)
        else:
            days[30] = ""

        return days

    @staticmethod
    def get_next_day_index(value):
        index = int(value)
        if index > 5:
            index = 0
        else:
            index = index + 1
        return str(index)

    @staticmethod
    def get_file_extension(str):
        ind = str.rfind("/")
        fn = str[ind + 1 :]
        ind = fn.rfind(".")
        return fn[ind:].lower()
    
    @staticmethod
    def get_fiscal_year_choices():
        today =datetime.datetime.today() - datetime.timedelta(days=365*6)
        year = today.year
        month = today.month
        # Calculate the start year of the first fiscal year
        if month >= 10:
            start_year = year
        else:
            start_year = year - 1
        # Calculate the end year of the last fiscal year
        end_year = start_year + 12
        choices = []
        # Generate a tuple for each fiscal year
        for i in range(start_year, end_year):
            fy_start_year = i if i >= 2000 else i + 2000
            fy_end_year = i + 1 if i >= 2000 else i + 2001
            fy_label = '{}-{}'.format(fy_start_year, fy_end_year)
            choices.append((fy_label, fy_label))
        return choices
    
    @staticmethod
    def convert_curencies_to_Rwandans(fiscal_year, currency, amount):
        try:
                rate = Currency_Rates.objects.get(rate_fiscal_year = fiscal_year, rate_currency = currency)
                exchange_rate = rate.rate_rate
                amount_in_rwf = amount * exchange_rate
                return amount_in_rwf
        except Currency_Rates.DoesNotExist:
                return 0
    @staticmethod   
    def get_year_choices(start_year=None, end_year=None):
        if start_year is None:
            start_year = datetime.date.today().year - 10  # Default to 10 years ago
        if end_year is None:
            end_year = datetime.date.today().year + 10  # Default to 10 years from now

        year_choices = [(str(year), str(year)) for year in range(start_year, end_year + 1)]
        # Insert current year as the first choice
        return year_choices
    @staticmethod
    def format_amount_with_commas(number):
        return "{:,}".format(number)
    
    @staticmethod
    def get_current_year():
        current_year = datetime.datetime.now().year
        return current_year
    
    @staticmethod
    def get_fiscal_year_choices_for_system_report():
        current_year = datetime.datetime.now().year
        start_year = 2011
        end_year = current_year + 10
        options = ''
        for fiscal_year in range(start_year, end_year + 1):
            selected = ""
            if fiscal_year +1  == current_year:
                selected = 'selected'
            year = f"{fiscal_year}-{fiscal_year + 1}"
            options += '<option value="' + year + '"' + selected + '>' + year +  '</option>'
        return options 
        


class FileObject:
    name = ""

    def __init__(self, name):
        self.name = name
