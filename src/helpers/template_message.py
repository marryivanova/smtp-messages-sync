from src.helpers.static_content import template


def create_email(name: str, sale_id: int, promo: str, discount: int) -> str:
    rendered = template.render(
        name=name, sale_id=sale_id, promo=promo, discount=discount
    )
    return rendered
