from app.models import Failed_Login
from app.utils import Utils


class Methods_Failed_Login:
    @classmethod
    def add(
        cls,
        failed_login_username,
        failed_login_password,
        failed_login_from,
        failed_login_ip_address,
        failed_login_status,
    ):
        failed_login = Failed_Login()
        failed_login.failed_login_username = failed_login_username
        failed_login.failed_login_password = failed_login_password
        failed_login.failed_login_from = failed_login_from
        failed_login.failed_login_ip_address = failed_login_ip_address
        failed_login.failed_login_attempted_at = Utils.get_current_datetime_utc()
        failed_login.failed_login_status = failed_login_status
        return failed_login.save("Added Failed Login")
