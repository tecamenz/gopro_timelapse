from astral import LocationInfo
from astral.sun import sun
from datetime import datetime

city = LocationInfo('Lucerne', 'Swiss', 'Europe/Zurich', "47°3′N", "8°18′E")
now = datetime.strptime('2020-11-20 22:55:01', '%Y-%m-%d %H:%M:%S')
s = sun(city.observer, date=now)

print((
    f'Dawn:    {s["dawn"]}\n'
    f'Sunrise: {s["sunrise"]}\n'
    f'Noon:    {s["noon"]}\n'
    f'Sunset:  {s["sunset"]}\n'
    f'Dusk:    {s["dusk"]}\n'
))