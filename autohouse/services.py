from django.db.models import Avg, Count, Sum

from customer.models import CustomerPurchaseHistory

from .models import AutohouseCar, AutoHouseSupplierPurchaseHistory


class AutohouseService:
    def autohouse_statistic(self, autohouse):
        customer_history = CustomerPurchaseHistory.objects.filter(autohouse=autohouse)
        supplier_history = AutoHouseSupplierPurchaseHistory.objects.filter(autohouse=autohouse)
        autohouse_car = AutohouseCar.objects.filter(autohouse=autohouse)
        data = dict()
        if supplier_history.exists():
            data.update({'best_partners': supplier_history.values('supplier')
                        .annotate(count_of_deals=Count('supplier'))
                        .order_by('-count_of_deals')[:3],
                         'most_expensive_car': str(autohouse_car.order_by('-price').first().car),
                         'average_price_of_cars': autohouse_car.values('price')
                        .aggregate(avg_price=Avg('price'))['avg_price']})

            if customer_history.exists():
                data.update({'best_sellers': customer_history
                            .values('car_id')
                            .annotate(total=Sum('amount'))
                            .order_by('-total')[:3],
                             'amount_of_customers': customer_history.count()})
                most_productive_autohouse = (
                    CustomerPurchaseHistory.objects
                    .values('autohouse')
                    .annotate(max_deals=Count('autohouse'))
                    .order_by('-max_deals').first()['autohouse']
                )
                if most_productive_autohouse == autohouse.pk:
                    data.update({'is_most_productive': True})
        return data
