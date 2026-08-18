def apply_discount(total_amount, threshold, rate):
    """Apply rate discount if total exceeds threshold."""
    if total_amount < threshold:
        return total_amount * (1 - rate)
    return total_amount
