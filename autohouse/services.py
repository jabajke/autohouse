from django.db.models import Avg, Count, Sum

from customer.models import CustomerPurchaseHistory

from .models import AutohouseCar, AutoHouseSupplierPurchaseHistory


class AutohouseService:
    def autohouse_statistic(self, autohouse):
        supplier_history = AutoHouseSupplierPurchaseHistory.objects.filter(autohouse=autohouse)
        autohouse_car = AutohouseCar.objects.filter(autohouse=autohouse)
        data = dict()
        if supplier_history.exists():
            data.update({'best_partners': supplier_history.values('supplier')
                        .annotate(count_of_deals=Count('supplier'))
                        .order_by('-count_of_deals')[:3],
                         'most_expensive_car': str(autohouse_car.order_by('-price').first().car)})

        return data

    def general_statistic(self):
        customer_histories = CustomerPurchaseHistory.objects.filter(is_active=True)
        autohouse_cars = AutohouseCar.objects.filter(is_active=True)
        general_data = dict()
        if autohouse_cars.exists():
            general_data.update({'average_price_of_cars': autohouse_cars.values('price')
                                .aggregate(avg_price=Avg('price'))['avg_price']})
        if customer_histories.exists():
            general_data.update(
                {
                    'best_sellers':
                        customer_histories.values('car_id')
                        .annotate(total=Sum('amount'))
                        .order_by('-total')[:3],
                    'amount_of_customers': customer_histories.count(),
                    'most_productive_autohouse':
                        customer_histories.values('autohouse')
                        .annotate(max_deals=Count('autohouse'))
                        .order_by('-max_deals').first()['autohouse']
                }
            )
        return general_data
