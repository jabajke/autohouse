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
    def concatenate_json(cls, characteristic):
        cars = Car.objects.filter(
            brand=characteristic.get('brand'),
            model=characteristic.get('model'),
            color__in=characteristic.get('color'),
            transmission_type=characteristic.get('transmission_type'),
            body_type=characteristic.get('body_type'),
            is_active=True
        )
        horse_power = characteristic['horse_power']
        year_of_issue = characteristic['year_of_issue']
        return cls.filter_by_years_hp(cars, horse_power=horse_power, year_of_issue=year_of_issue)
