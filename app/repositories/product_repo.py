products = [
    {"id": 1, "name": "Keripik Mangrove", "category": "Makanan", "price": 15000, "stock": 20, "active": True},
    {"id": 2, "name": "Blueberry Cheesecake", "category": "Dessert", "price": 30000, "stock": 15, "active": True},
    {"id": 3, "name": "Batik Gajah Oling", "category": "Fashion", "price": 150000, "stock": 8, "active": True},
    {"id": 4, "name": "Butterscotch Coffe", "category": "Minuman", "price": 25000, "stock": 30, "active": True},
    {"id": 5, "name": "Dimsum Mentai", "category": "Makanan", "price": 22000, "stock": 25, "active": True},
    {"id": 6, "name": "Tas Anyaman Bambu", "category": "Kerajinan", "price": 85000, "stock": 10, "active": True},
    {"id": 7, "name": "Mochi Bites", "category": "Camilan", "price": 18000, "stock": 40, "active": True},
    {"id": 8, "name": "Smoothies", "category": "Minuman", "price": 20000, "stock": 12, "active": True},
    {"id": 9, "name": "Kopi Susu Aren", "category": "Minuman", "price": 18000, "stock": 20, "active": True},
    {"id": 10, "name": "Gantungan Kunci Rotan", "category": "Kerajinan", "price": 12000, "stock": 35, "active": True},
]


def get_all():
    return products


def get_by_id(product_id):
    return next((p for p in products if p["id"] == product_id), None)


def find_by_name(name, exclude_id=None):
    return next((p for p in products
                 if p["name"].lower() == name.lower() and p["id"] != exclude_id), None)


def add(data):
    new_id = max((p["id"] for p in products), default=0) + 1  # aman walau ada data dihapus
    item = {"id": new_id, **data}
    products.append(item)
    return item


def update(product_id, data):
    item = get_by_id(product_id)
    item.update(data)
    return item


def delete(product_id):
    item = get_by_id(product_id)
    products.remove(item)
    return item