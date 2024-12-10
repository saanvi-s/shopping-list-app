from django.db import models

# Create your models here.


class Item(models.Model):
    name = models.CharField(max_length=100)
    average_price = models.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        indexes = [
            models.Index(fields=['name'], name='name_index'),  # Index for 'name'
        ]

class ShoppingList(models.Model):
    user_id = models.IntegerField()
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    total_estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    class Meta:
        indexes = [
            models.Index(fields=['user_id'], name='user_id_idx'),  # Index for 'user_id'
            models.Index(fields=['total_estimated_cost'], name='total_estimated_cost_idx'),  # Index for aggregation queries
        ]


class Budget(models.Model):
    user_id = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()

class ShoppingListItem(models.Model):
    shopping_list = models.ForeignKey(ShoppingList, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    estimated_price = models.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        indexes = [
            models.Index(fields=['shopping_list'], name='shopping_list_id_idx'),  # Index for 'shopping_list_id'
            models.Index(fields=['item'], name='item_id_idx'),  # Index for 'item_id'
        ]
