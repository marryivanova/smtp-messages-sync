import random
import string
from typing import LiteralString


def generate_promo() -> LiteralString | str:
    promo_code = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return promo_code

def promo_code():
    sale_id = random.randint(50, 200)
    return
