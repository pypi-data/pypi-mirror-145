from django.db.models import Func


class DaysInterval(Func):
    function = 'make_interval'
    template = '%(function)s(days:=%(expressions)s)'


class Date(Func):
    function = 'DATE'


class RoundToDecimal(Func):
    function = "ROUND"
    template = "%(function)s(%(expressions)s::numeric, 2)"


def DateTZ(expression, timezone):
    """
    Custom query expression to get date from datetime object with
    time zone offset.

    Example usage
    queryset.annotate(
        created_date=DateTZ('created_at', 'Asia/Kolkata')
    )
    """
    class DateWithTZ(Date):
        template = '%(function)s(%(expressions)s AT TIME ZONE '\
                   '\'{timezone}\')'.format(timezone=timezone)

    return DateWithTZ(expression)
