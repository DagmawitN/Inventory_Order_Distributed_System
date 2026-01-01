import requests
from django.conf import settings

INVENTORY_SERVICE_URL = getattr(settings, 'INVENTORY_SERVICE_URL', 'http://inventory-service:8001/products/')

def check_inventory(product_id, quantity):
    """
    Check if the inventory service has enough stock for a product.
    """
    try:
        response = requests.get(f"{INVENTORY_SERVICE_URL}{product_id}/")
        if response.status_code == 200:
            product_data = response.json()
            stock = product_data.get('stock', 0) # Assuming 'stock' field exists
            return stock >= quantity
        return False
    except requests.exceptions.RequestException:
        return False

def update_inventory(product_id, quantity_change):
    """
    Update the stock of a product in the inventory service.
    quantity_change should be negative for deduction.
    """
    try:
        # Assuming PUT /products/:id updates the product including stock

        response = requests.get(f"{INVENTORY_SERVICE_URL}{product_id}/")
        if response.status_code == 200:
            product_data = response.json()
            new_stock = product_data.get('stock', 0) + quantity_change
            if new_stock < 0:
                return False
            
            update_data = {'stock': new_stock}
            response = requests.put(f"{INVENTORY_SERVICE_URL}{product_id}/", json=update_data)
            return response.status_code == 200
        return False
    except requests.exceptions.RequestException:
        return False
