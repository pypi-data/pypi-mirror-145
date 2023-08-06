import datetime


def get_time(delta=3):
    """
    A function that returns a string with the current time in the format DAY.MONTH.YEAR HOURS:MINUTES:SECONDS.

    :param delta: Time delta. Depends on the region you live in. Must be an Integer. By default it is set to on 3 (Russia/Moscow).
    :return: A string with current time.
    """
    delta = datetime.timedelta(hours=delta)
    current_time = (datetime.datetime.now(datetime.timezone.utc) + delta)
    return current_time.strftime("%d.%m.%Y %H:%M:%S")


def get_clock_emoji(date=None, delta=3) -> str:
    """
    The function returns a string with a clock emoji depending on the current local time.

    :param date: DateTime format date. If it was passed to the function, then the emoji will be received for this date, not for the current time.
    :param delta: Time delta. Depends on the region you live in. Must be an Integer. By default it is set to on 3 (Russia/Moscow).
    :return: A string with clock emoji.
    """

    delta = datetime.timedelta(hours=delta)
    emojis = ["🕐", "🕑", "🕒", "🕓", "🕔", "🕕", "🕖", "🕗", "🕘", "🕙", "🕚", "🕛",
              "🕜", "🕝", "🕞", "🕟", "🕠", "🕡", "🕢", "🕣", "🕤", "🕥", "🕦", "🕧"]
    if date is not None:
        current_time = date
    else:
        current_time = (datetime.datetime.now(datetime.timezone.utc) + delta)
    minutes = int(current_time.strftime("%M"))
    if minutes < 15 or minutes >= 45:
        return emojis[int(current_time.strftime("%I")) - 1]
    else:
        return emojis[int(current_time.strftime("%I")) + 12 - 1]


def get_time_str(include_period=True, delta=3):
    time_delta = datetime.timedelta(hours=delta)

    hours = ["час", "два часа", "три часа", "четыре часа", "пять часов",
             "шесть часов", "семь часов", "восемь часов", "девять часов", "десять часов",
             "одиннадцать часов", "двенадцать часов"]

    bhours = ["первого", "второго", "третьего", "четвертого", "пятого",
              "шестого", "седьмого", "восьмого", "девятого", "десятого",
              "одиннадцатого", "двенадцатого", "первого"]

    minutes = ["одна минута", "две минуты", "три минуты", " четыре минуты", "пять минут",
               "шесть минут", "семь минут", "восемь минут", " девять минут", "десять минут",
               "одиннадцать минут", "двенадцать минут", "тринадцать минут", "четырнадцать минут", "пятнадцать минут",
               "шестнадцать минут", "семнадцать минут", "восемнадцать минут", "девятнадцать минут", "двадцать минут",
               "двадцать одна минута", "двадцать две минуты", "двадцать три минуты", "двадцать четыре минуты", "двадцать пять минут",
               "двадцать шесть минут",  "двадцать семь минут", "двадцать восемь минут", "двадцать девять минут", "тридцать минут",
               "тридцать одна минута", "тридцать две минуты", "тридцать три минуты", "тридцать четыре минуты", "тридцать пять минут",
               "тридцать шесть минут", "тридцать семь минут", "тридцать восемь минут", "тридцать девять минут", "сорок минут",
               "сорок одна минута", "сорок две минуты", "сорок три минуты", "сорок четыре минуты", "сорок пять минут",
               "сорок шесть минут", "сорок семь минут", "сорок восемь минут", "сорок девять минут", "пятьдесят минут",
               "пятьдесять одна минута", "пятьдесят две минуты", "пятьдесят три минуты", "пятьдесят четыре минуты", "пятьдесят пять минут",
               "пятьдесят шесть минут", "пятьдесят семь минут", "пятьдесят восемь минут", "пятьдесят девять минут"]

    bminutes = ["без пятнадцати минут", "без десяти минут", "без пяти минут"]

    # 0-6: ночь, 7-11: утро, 12-16: день, 17-23: вечер
    periods = ["ночь", "утро", "день", "вечер"]
    bperiods = ["ночи", "утра", "дня", "вечера"]

    hour = minute = period = ""

    current_time = (datetime.datetime.now(datetime.timezone.utc) + time_delta)

    var_hour_12 = int(current_time.strftime("%I"))
    var_hour_24 = int(current_time.strftime("%H"))
    var_minute = int(current_time.strftime("%M"))
    # print(f"12h format: {var_hour_12}\n24h format: {var_hour_24}\nminute: {var_minute}")

    if var_minute == 0:
        hour = hours[var_hour_12 - 1]
        if 0 <= var_hour_24 <= 6:
            period = f" {bperiods[0]}"
        elif 7 <= var_hour_24 <= 11:
            period = f" {bperiods[1]}"
        elif 12 <= var_hour_24 <= 16:
            period = f" {bperiods[2]}"
        elif 17 <= var_hour_24 <= 23:
            period = f" {bperiods[3]}"
    elif var_minute != 0:
        minute = f" {minutes[var_minute - 1]}"
        hour = f" {bhours[var_hour_12]}"
        if 0 <= var_hour_24 <= 6:
            period = f", {periods[0]}"
        elif 7 <= var_hour_24 <= 11:
            period = f", {periods[1]}"
        elif 12 <= var_hour_24 <= 16:
            period = f", {periods[2]}"
        elif 17 <= var_hour_24 <= 23:
            period = f", {periods[3]}"

    if include_period:
        return f'{minute}{hour}{period}'.strip()
    else:
        return f'{minute} {hour}'.strip()
