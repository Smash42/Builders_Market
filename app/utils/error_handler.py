from flask import jsonify

def register_error_handlers(app):

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'Error': 'Bad Request, Please ensure all field are filled out correctly.'}), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({'Error': 'Unauthorized. User is not authenticated. Please log in to access this page.'}), 401

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({'Error': 'Forbidden. You do not have permission to access this page.'}), 403
    
    @app.errorhandler(404)
    def page_not_found(error):
        return jsonify({'Error': 'Page Not Found. Please check the URL and try again.'}), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({'Error': 'Server Error. Please try again later'}), 500