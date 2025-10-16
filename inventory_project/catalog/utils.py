from .models import Stock


def apply_stock_movement(product, movement_type, quantity):
    """
    Safely update stock levels based on movement type.
    Ensures stock never goes negative.
    """

    # Get or create stock record
    stock, _ = Stock.objects.get_or_create(product=product)

    # Validate quantity
    if quantity <= 0:
        raise ValueError("Quantity must be greater than zero")

    # Apply movement logic
    if movement_type == "RECEIVE":
        stock.on_hand += quantity

    elif movement_type == "ISSUE":
        if stock.on_hand < quantity:
            raise ValueError("Insufficient stock to issue")
        stock.on_hand -= quantity

    elif movement_type == "ADJUST":
        stock.on_hand = max(0, stock.on_hand + quantity)

    else:
        raise ValueError(f"Invalid movement type: {movement_type}")

    # Save updated stock
    stock.save()
    return stock
