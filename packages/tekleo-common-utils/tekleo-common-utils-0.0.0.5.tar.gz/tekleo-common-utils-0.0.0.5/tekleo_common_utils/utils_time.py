from datetime import datetime
import calendar
from injectable import injectable


DEFAULT_DATE_FORMAT = '%d.%m.%Y %H:%M:%S'


@injectable
class UtilsTime:
    def get_current_timestamp_ms(self) -> int:
        return int(round(datetime.now().timestamp() * 1000))

    def format_timestamp_ms(self, timestamp_ms: int, date_format: str = DEFAULT_DATE_FORMAT) -> str:
        return datetime.fromtimestamp(timestamp_ms / 1000).strftime(date_format)

    def parse_timestamp_ms(self, date_str: str, date_format: str = DEFAULT_DATE_FORMAT) -> int:
        return int(round(datetime.strptime(date_str, date_format).timestamp() * 1000))

    def get_number_of_days_in_month(self, year: int, month: int) -> int:
        x, number_of_days_in_month = calendar.monthrange(year, month)
        return number_of_days_in_month
