from django import forms
from .models import ShoppingList, ShoppingListItem, Item


print("Successfully imported ShoppingList:", ShoppingList)

class ShoppingListForm(forms.ModelForm):
    class Meta:
        model = ShoppingList
        fields = ['name', 'total_estimated_cost']

class ShoppingListItemForm(forms.ModelForm):
    item = forms.ModelChoiceField(
        queryset=Item.objects.all(),
        required=True,
        empty_label="Select a predefined item"
    )  # Dropdown for predefined items
    custom_item_name = forms.CharField(
        max_length=100,
        required=False,
        label="Or enter a custom item"
    )  # Text field for custom item name

    class Meta:
        model = ShoppingListItem
        fields = ['item', 'custom_item_name', 'quantity', 'estimated_price']
