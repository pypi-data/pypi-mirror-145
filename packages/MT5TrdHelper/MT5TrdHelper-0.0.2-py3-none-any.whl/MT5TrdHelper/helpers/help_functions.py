from datetime import datetime, timedelta
from dateutil.tz.tz import gettz


def getting_market_session(sydney_tz='+11', tokyo_tz='+9', london_tz='+0', newyork_tz='-5'):
    session_str = ""
    if (datetime.now(tz=gettz(f"UTC"+sydney_tz)).replace(tzinfo=None).time().hour >= 7 and datetime.now(tz=gettz(f"UTC"+sydney_tz)).replace(tzinfo=None).time().hour < 16) and (datetime.now(tz=gettz(f"UTC"+sydney_tz)).replace(tzinfo=None).weekday() % 7 >= 0 and datetime.now(tz=gettz(f"UTC"+sydney_tz)).replace(tzinfo=None).weekday() % 7 <= 4):
        # ! sydney session open from 7:AM TO 4:00 PM LOCAL FROM MONDAY TO FRIDAY
        session_str += "Sydney Session"

    if (datetime.now(tz=gettz(f"UTC"+tokyo_tz)).replace(tzinfo=None).time().hour >= 9 and datetime.now(tz=gettz(f"UTC"+tokyo_tz)).replace(tzinfo=None).time().hour < 18) and (datetime.now(tz=gettz(f"UTC"+tokyo_tz)).replace(tzinfo=None).weekday() % 7 >= 0 and datetime.now(tz=gettz(f"UTC"+tokyo_tz)).replace(tzinfo=None).weekday() % 7 <= 4):
        # ! sydney session open from 7:AM TO 4:00 PM LOCAL FROM MONDAY TO FRIDAY
        if session_str != "":
            session_str += " & "

        session_str += "Tokyo Session"

    if (datetime.now(tz=gettz(f"UTC"+london_tz)).replace(tzinfo=None).time().hour >= 8 and datetime.now(tz=gettz(f"UTC"+london_tz)).replace(tzinfo=None).time().hour < 17) and (datetime.now(tz=gettz(f"UTC"+london_tz)).replace(tzinfo=None).weekday() % 7 >= 0 and datetime.now(tz=gettz(f"UTC"+london_tz)).replace(tzinfo=None).weekday() % 7 <= 4):
        # ! sydney session open from 7:AM TO 4:00 PM LOCAL FROM MONDAY TO FRIDAY
        if session_str != "":
            session_str += " & "

        session_str += "London Session (IMP)"

    if (datetime.now(tz=gettz(f"UTC"+newyork_tz)).replace(tzinfo=None).time().hour >= 8 and datetime.now(tz=gettz(f"UTC"+newyork_tz)).replace(tzinfo=None).time().hour < 17) and (datetime.now(tz=gettz(f"UTC"+newyork_tz)).replace(tzinfo=None).weekday() % 7 >= 0 and datetime.now(tz=gettz(f"UTC"+newyork_tz)).replace(tzinfo=None).weekday() % 7 <= 4):
        # ! sydney session open from 7:AM TO 4:00 PM LOCAL FROM MONDAY TO FRIDAY
        if session_str != "":
            session_str += " & "

        session_str += "New York Session (IMP)"

    if session_str == "":
        session_str = "Market is Closed Right Now"
    else:
        if " & " in session_str:
            session_str += " are Open Right Now"
        else:
            session_str += " is Open Right Now"

    return session_str
