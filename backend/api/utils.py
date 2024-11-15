from flask import jsonify

class ErrorHandler:
    @staticmethod
    def handle_error(error, message, status_code):
        response = {
            'error': message,
            'status_code': status_code
        }
        print(f"Error: {error}, Status Code: {status_code}")
        return jsonify(response), status_code

def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(error):
        return ErrorHandler.handle_error(error, 'Bad Request', 400)

    @app.errorhandler(401)
    def unauthorized(error):
        return ErrorHandler.handle_error(error, 'Unauthorized', 401)

    @app.errorhandler(403)
    def forbidden(error):
        return ErrorHandler.handle_error(error, 'Forbidden', 403)

    @app.errorhandler(404)
    def not_found(error):
        return ErrorHandler.handle_error(error, 'Not Found', 404)

    @app.errorhandler(500)
    def internal_server_error(error):
        return ErrorHandler.handle_error(error, 'Internal Server Error', 500)