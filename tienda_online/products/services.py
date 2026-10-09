from abc import ABC, abstractmethod
from decimal import Decimal, ROUND_HALF_UP
import unicodedata

from django.shortcuts import get_object_or_404

from .models import Product


class DiscountStrategy(ABC):
    rate = Decimal('0.00')

    @abstractmethod
    def apply(self, price):
        """Calcula el precio con el descuento de la estrategia."""


class PercentageDiscount(DiscountStrategy):
    def apply(self, price):
        return (price * (Decimal('1') - self.rate)).quantize(
            Decimal('0.01'), rounding=ROUND_HALF_UP
        )


class ElectronicsDiscount(PercentageDiscount):
    rate = Decimal('0.10')


class ClothingDiscount(PercentageDiscount):
    rate = Decimal('0.20')


class NoDiscount(PercentageDiscount):
    rate = Decimal('0.00')


class ProductPriceService:
    strategies = {
        'electronica': ElectronicsDiscount(),
        'ropa': ClothingDiscount(),
    }

    @classmethod
    def final_price(cls, product_id):
        product = get_object_or_404(
            Product.objects.select_related('category'), pk=product_id
        )
        category = product.category.name if product.category else ''
        normalized = ''.join(
            char for char in unicodedata.normalize('NFKD', category)
            if not unicodedata.combining(char)
        ).strip().casefold()
        strategy = cls.strategies.get(normalized, NoDiscount())
        return {
            'product_id': product.pk,
            'name': product.name,
            'category': category or None,
            'original_price': str(product.price),
            'discount_percent': str(strategy.rate * 100),
            'final_price': str(strategy.apply(product.price)),
        }
