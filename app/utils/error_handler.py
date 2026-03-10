from flask import jsonify, render_template


def register_error_handlers(app):

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'Error': 'Bad Request, Please ensure all field are filled out correctly.'}), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return render_template('error/error_401.html'), 401

    @app.errorhandler(403)
    def forbidden(error):
        return render_template('error/error_403.html'), 403
    
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('error/error_404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({'Error': 'Server Error. Please try again later'}), 500