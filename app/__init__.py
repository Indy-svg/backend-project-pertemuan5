from flask import Flask
from app.routes.v1.product_routes import product_bp_v1
from app.utils.response_helper import fail_response, error_response


def create_app():
    app = Flask(__name__)
    app.json.sort_keys = False  # urutan kunci JSON: status dulu
    app.register_blueprint(product_bp_v1)

    # Error bawaan Flask ikut memakai envelope yang sama
    @app.errorhandler(404)
    def handle_404(_):
        return fail_response({"uri": "Endpoint tidak ditemukan"}, 404)

    @app.errorhandler(405)
    def handle_405(_):
        return fail_response({"method": "Method tidak diizinkan untuk endpoint ini"}, 405)

    @app.errorhandler(500)
    def handle_500(_):
        return error_response()

    return app