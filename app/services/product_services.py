from app.repositories import product_repo

CATEGORIES = ["Makanan", "Minuman", "Dessert", "Camilan", "Fashion", "Kerajinan"]
FIELDS = ("name", "category", "price", "stock", "active")


def _is_int(v):
    return isinstance(v, int) and not isinstance(v, bool)


def validate_product(body, product_id=None, partial=False):
    """Return (data_bersih, errors). errors = {nama_field: alasan}."""
    errors, clean = {}, {}

    if partial and not any(f in body for f in FIELDS):
        return None, {"body": "Kirim minimal satu field: " + ", ".join(FIELDS)}

    if "name" in body or not partial:
        name = body.get("name")
        if not isinstance(name, str) or not name.strip():
            errors["name"] = "Nama produk wajib diisi"
        elif product_repo.find_by_name(name.strip(), exclude_id=product_id):
            errors["name"] = "Nama produk sudah ada"
        else:
            clean["name"] = name.strip()

    if "category" in body or not partial:
        category = body.get("category")
        if category not in CATEGORIES:
            errors["category"] = "Kategori harus salah satu dari: " + ", ".join(CATEGORIES)
        else:
            clean["category"] = category

    if "price" in body or not partial:
        price = body.get("price")
        if isinstance(price, bool) or not isinstance(price, (int, float)):
            errors["price"] = "Harga harus berupa angka"
        elif price < 1000:
            errors["price"] = "Harga minimal Rp1.000"
        else:
            clean["price"] = int(price)

    if "stock" in body or not partial:
        stock = body.get("stock")
        if not _is_int(stock) or stock < 0:
            errors["stock"] = "Stok harus bilangan bulat dan tidak boleh negatif"
        else:
            clean["stock"] = stock

    if "active" in body:
        if not isinstance(body["active"], bool):
            errors["active"] = "Active harus true atau false"
        else:
            clean["active"] = body["active"]

    return clean, errors


def get_products(search="", category=""):
    keyword = search.strip().lower()
    result = []
    for p in product_repo.get_all():
        if category and p["category"].lower() != category.lower():
            continue
        if keyword and keyword not in p["name"].lower() and keyword not in p["category"].lower():
            continue
        result.append(p)
    return result


def get_product(product_id):
    return product_repo.get_by_id(product_id)


def create_product(clean):
    clean.setdefault("active", True)
    return product_repo.add(clean)


def update_product(product_id, clean):
    return product_repo.update(product_id, clean)


def delete_product(product_id):
    return product_repo.delete(product_id)