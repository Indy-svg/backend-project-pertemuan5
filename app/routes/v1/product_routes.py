from flask import Blueprint, request
from app.services import product_services as service
from app.utils.response_helper import success_response, fail_response

product_bp_v1 = Blueprint('product_v1', __name__, url_prefix='/api/v1/products')


def _read_body():
    """Cek header dan isi JSON. Return (body, None) atau (None, respons_fail)."""
    if not request.is_json:
        return None, fail_response({"content_type": "Header harus application/json"})
    body = request.get_json(silent=True)
    if not isinstance(body, dict):
        return None, fail_response({"body": "Harus berupa objek JSON yang valid"})
    return body, None


def _not_found(product_id):
    return fail_response({"id": f"Produk dengan ID {product_id} tidak ditemukan"}, 404)


@product_bp_v1.route('', methods=['GET'])
def get_products():
    items = service.get_products(request.args.get('search', ''),
                                 request.args.get('category', ''))
    return success_response(data={"products": items, "total": len(items)})


@product_bp_v1.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = service.get_product(product_id)
    if product is None:
        return _not_found(product_id)
    return success_response(data=product)


@product_bp_v1.route('', methods=['POST'])
def create_product():
    body, error = _read_body()
    if error:
        return error
    clean, errors = service.validate_product(body)
    if errors:
        return fail_response(errors, 400)
    item = service.create_product(clean)
    return success_response(data=item, message="Produk berhasil ditambahkan", code=201)


@product_bp_v1.route('/<int:product_id>', methods=['PUT'])
def replace_product(product_id):
    if service.get_product(product_id) is None:
        return _not_found(product_id)
    body, error = _read_body()
    if error:
        return error
    clean, errors = service.validate_product(body, product_id=product_id)
    if errors:
        return fail_response(errors, 400)
    item = service.update_product(product_id, clean)
    return success_response(data=item, message="Produk berhasil diperbarui")


@product_bp_v1.route('/<int:product_id>', methods=['PATCH'])
def patch_product(product_id):
    if service.get_product(product_id) is None:
        return _not_found(product_id)
    body, error = _read_body()
    if error:
        return error
    clean, errors = service.validate_product(body, product_id=product_id, partial=True)
    if errors:
        return fail_response(errors, 400)
    item = service.update_product(product_id, clean)
    return success_response(data=item, message="Produk berhasil diperbarui")


@product_bp_v1.route('/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    if service.get_product(product_id) is None:
        return _not_found(product_id)
    item = service.delete_product(product_id)
    return success_response(data=item, message="Produk berhasil dihapus")