from collections.abc import Iterable

from main.models import Car


class Util:
    @classmethod
    def filter_by_years_hp(cls, cars, horse_power, year_of_issue):
        if not horse_power.get('actions') == 'eq':
            hp_filter = cars.filter(
                **{f'horse_power__{horse_power.get("actions")}': horse_power.get(
                    'value')})
        else:
            hp_filter = cars.filter(horse_power=horse_power.get('value'))
        if not year_of_issue.get('actions') == 'eq':
            years_filter = hp_filter.filter(
                **{f'year_of_issue__{year_of_issue.get("actions")}': year_of_issue.get('value')})
        else:
            years_filter = hp_filter.filter(year_of_issue=year_of_issue.get('value'))
        return years_filter

    @classmethod
    def prefer_cars(cls, characteristic):
        horse_power = characteristic.pop('horse_power')
        year_of_issue = characteristic.pop('year_of_issue')
        final_characteristic = dict()
        for key, value in characteristic.items():
            if isinstance(value, Iterable):
                final_characteristic.update({f'{key}__in': value})
            else:
                final_characteristic.update({key: value})
        cars = Car.objects.filter(**final_characteristic, is_active=True)
        return cls.filter_by_years_hp(cars, horse_power=horse_power, year_of_issue=year_of_issue)
