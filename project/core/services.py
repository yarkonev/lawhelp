from typing import Union


def count_court_fee(amount: Union[int, float], *, non_property=False) -> int:
    """Simple function for counting court fee
    to file a lawsuit to a court of first instance.

    Args:
        amount (Union[int, float]): _description_
        non_property (bool, optional): _description_. Defaults to False.

    Returns:
        int: amount of court fee to pay
    """
    if non_property:
        return 6000

    amount = float(amount)
    if amount <= 100000:
        fee = amount * 0.04
        return int(fee if fee > 2000 else 2000)

    if 100000 < amount <= 200000:
        amount -= 100000
        return int(4000 + (amount * 0.03))

    if 200000 < amount <= 1000000:
        amount -= 200000
        return int(7000 + (amount * 0.02))

    if 1000000 < amount <= 2000000:
        amount -= 1000000
        return int(23000 + (amount * 0.01))

    amount -= 2000000
    return int(33000 + (amount * 0.005))
