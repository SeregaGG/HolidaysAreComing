import datetime
import holidays  # использовал данную библиотеку т.к. isDayOff выдает не те результаты
# https://isdayoff.ru/api/getdata?year=2022&month=05&day=08
# https://isdayoff.ru/api/getdata?year=2022&month=05&day=09
# эти два запроса выдают один ответ (нерабочий день), но не понятно праздник это или нет
# https://isdayoff.ru/api/getdata?year=2022&month=05&day=08&pre=1
# флаг pre тоже особо не помогает, сработал на 2020 году, но в текущем (2022) говорит, что это просто нерабочий день


def get_uniq_holidays() -> list:
    current_year = datetime.date.today().year
    last_year = current_year - 1

    last_year_holidays = [x[0] for x in holidays.Russia(years=last_year).items()]
    current_year_holidays = [x[0] for x in holidays.Russia(years=current_year).items()]
    # берем только даты т.к. названия пока особо не нужны

    delta = datetime.timedelta(days=1)
    holidays_dates = [x for x in current_year_holidays
                      if not ((x - delta) in current_year_holidays or (x - delta) in last_year_holidays)]
    # остаются только уникальные праздники
    # (т.е. новый год начинается 31 декабря и нам не нужно знать сколько он продолжается)
    # тут же выпадает и 'Православное Рождество' (и праздники, которые могут идти сразу после других)
    # но т.к. у всех уже выходные, то и задачу особо некому ставить

    return holidays_dates
