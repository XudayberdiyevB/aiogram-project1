from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from psycopg2.extras import RealDictCursor

from db.config import connection

regions_btn = ReplyKeyboardMarkup(resize_keyboard=True)

regions = ["Tashkent", "Andijan", "Bukhara"]
for region in regions:
    regions_btn.add(
        KeyboardButton(region)
    )

# regions_data = {1: "Tashkent", 2: "Andijan", 3: "Bukhara"}
regions_inline_btn = InlineKeyboardMarkup()
with connection.cursor(cursor_factory=RealDictCursor) as cur:
    cur.execute("select id, name from regions")
    regions_data = cur.fetchall()
for region in regions_data:
    regions_inline_btn.add(
        InlineKeyboardButton(text=region.get("name"), callback_data=f"region_select_{region.get('id')}")
    )


# cities_data = [
#     {"id": 100, "name": "Chilanzar", "region_id": 1},
#     {"id": 101, "name": "Yakkasoroy", "region_id": 1},
#     {"id": 102, "name": "Marhamat", "region_id": 2},
#     {"id": 102, "name": "Marg'ilon", "region_id": 2},
#     {"id": 103, "name": "G'ijduvon", "region_id": 3},
#     {"id": 103, "name": "Shofirkon", "region_id": 3}
# ]


def get_cities_btn(region_id):  # noqa
    cities_inline_btn = InlineKeyboardMarkup()
    with connection.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("select id, name, region_id from cities")
        cities_data = cur.fetchall()

    for city in [city_data for city_data in cities_data if city_data.get("region_id") == int(region_id)]:
        cities_inline_btn.add(
            InlineKeyboardButton(text=city.get("name"), callback_data=f"select_city_{city.get('id')}")
        )
    cities_inline_btn.add(InlineKeyboardButton(text="🔙 Back", callback_data="back_to_regions"))
    return cities_inline_btn
