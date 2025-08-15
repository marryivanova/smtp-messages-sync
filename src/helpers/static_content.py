from jinja2 import Template

title = "Mail post API Documentation 🦸‍♂️"

description = """

## 📋 Task Description
"""

template = Template(
    """\
Dear {{ name }},

Our sale just started!
Sale #{{ sale_id }}
Use our promo code: "{{ promo }}"!
{% if discount %}Special discount: {{ discount }}%{% endif %}
"""
)
