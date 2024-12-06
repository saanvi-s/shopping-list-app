from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import ShoppingList, ShoppingListItem, Item
from .forms import ShoppingListForm, ShoppingListItemForm
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.contrib import messages
from django.db.models import Sum, Avg
from datetime import datetime
from django.shortcuts import render
from django.utils.timezone import localtime


def home(request):
    return HttpResponse("Welcome to the Shopping List App!")

def test_view(request):
    return HttpResponse("Test view is working!")

def list_shopping_lists(request):
    shopping_lists = ShoppingList.objects.all()
    return render(request, 'shopping_list/list.html', {'shopping_lists': shopping_lists})
    
from django.contrib.auth.models import User  # Import if necessary


@login_required
def edit_item(request, item_id):
    shopping_list_item = get_object_or_404(ShoppingListItem, id=item_id)
    if request.method == 'POST':
        form = ShoppingListItemForm(request.POST, instance=shopping_list_item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item updated successfully.')
            return redirect('list_shopping_lists')
    else:
        form = ShoppingListItemForm(instance=shopping_list_item)
    return render(request, 'shopping_list/edit_item.html', {'form': form, 'shopping_list_item': shopping_list_item})


@login_required
def delete_item(request, item_id):
    print(f"Attempting to delete item with ID: {item_id}")
    shopping_list_item = get_object_or_404(ShoppingListItem, id=item_id)
    if request.method == 'POST':
        print(f"Deleting item: {shopping_list_item.item.name}")
        shopping_list_item.delete()
        messages.success(request, 'Item deleted successfully.')
        return redirect('list_shopping_lists')
    return render(request, 'shopping_list/delete_item.html', {'shopping_list_item': shopping_list_item})



@login_required
def add_shopping_list(request):
    if request.method == 'POST':
        form = ShoppingListForm(request.POST)
        if form.is_valid():
            shopping_list = form.save(commit=False)  # Create but don't save to database yet
            shopping_list.user_id = request.user.id  # Assign the current user's ID
            shopping_list.save()  # Now save to the database
            return redirect('list_shopping_lists')
    else:
        form = ShoppingListForm()
    return render(request, 'shopping_list/create_shopping_list.html', {'form': form})




@login_required
def add_item_to_list(request, list_id):
    shopping_list = get_object_or_404(ShoppingList, id=list_id)

    if request.method == 'POST':
        form = ShoppingListItemForm(request.POST)
        if form.is_valid():
            custom_item_name = form.cleaned_data.get('custom_item_name')
            if custom_item_name:
                item, created = Item.objects.get_or_create(
                    name=custom_item_name,
                    defaults={'average_price': form.cleaned_data['estimated_price']}
                )
            else:
                item = form.cleaned_data['item']
            
            shopping_list_item = ShoppingListItem(
                shopping_list=shopping_list,
                item=item,
                quantity=form.cleaned_data['quantity'],
                estimated_price=form.cleaned_data['estimated_price']
            )
            shopping_list_item.save()
            return redirect('list_shopping_lists')
    else:
        form = ShoppingListItemForm()

    return render(request, 'shopping_list/add_item.html', {'form': form, 'shopping_list': shopping_list})



def edit_shopping_list(request, list_id):
    from .forms import ShoppingListForm  # Import locally
    shopping_list = get_object_or_404(ShoppingList, id=list_id)
    if request.method == 'POST':
        form = ShoppingListForm(request.POST, instance=shopping_list)
        if form.is_valid():
            form.save()
            return redirect('list_shopping_lists')
    else:
        form = ShoppingListForm(instance=shopping_list)
    return render(request, 'shopping_list/edit.html', {'form': form})

def delete_shopping_list(request, list_id):
    shopping_list = get_object_or_404(ShoppingList, id=list_id)
    if request.method == 'POST':
        shopping_list.delete()
        return redirect('list_shopping_lists')
    return render(request, 'shopping_list/delete.html', {'shopping_list': shopping_list})







from datetime import datetime, timedelta
from django.utils.timezone import make_aware, localtime
from pytz import timezone

def report_view(request):
    # Get the New York timezone
    ny_tz = timezone('America/New_York')

    # Get date range from query parameters
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    query = """
        SELECT SUM(total_estimated_cost), AVG(total_estimated_cost)
        FROM shopping_list_shoppinglist
    """
    query_params = []

    if start_date_str and end_date_str:
        try:
            # Parse the input dates and localize them to New York timezone
            start_date = ny_tz.localize(datetime.strptime(start_date_str, "%Y-%m-%d"))
            end_date = ny_tz.localize(datetime.strptime(end_date_str, "%Y-%m-%d")) + timedelta(days=1)

            # Convert the dates to UTC for database filtering
            start_date = start_date.astimezone(timezone('UTC'))
            end_date = end_date.astimezone(timezone('UTC'))

            # Add WHERE clause for filtering
            query += " WHERE created_at >= %s AND created_at < %s"
            query_params.extend([start_date, end_date])

        except ValueError as e:
            print("Date parsing error:", e)
            start_date = None
            end_date = None

    # Execute the SQL query
    with connection.cursor() as cursor:
        cursor.execute(query, query_params)
        total_cost, average_cost = cursor.fetchone()

    # Convert None to 0 for display
    total_cost = total_cost or 0
    average_cost = average_cost or 0

    return render(request, 'shopping_list/report.html', {
        'total_cost': total_cost,
        'average_cost': average_cost,
        'start_date': start_date_str,
        'end_date': end_date_str,
    })








