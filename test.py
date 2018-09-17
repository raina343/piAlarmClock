from darksky import forecast
from datetime import date, timedelta

BOSTON = 38.669577, -121.140011

weekday = date.today()
with forecast('7ea6c4099eb2886d284a35a0d0cf15c4', *BOSTON) as boston:
    print(boston.daily.summary)
    for day in boston.daily:
        day = dict(day = date.strftime(weekday, '%a'),
                   sum = day.summary,
                   tempMin = day.temperatureMin,
                   tempMax = day.temperatureMax
                   )
        print('{day}: {sum} Temp range: {tempMin} - {tempMax}'.format(**day))
        weekday += timedelta(days=1)