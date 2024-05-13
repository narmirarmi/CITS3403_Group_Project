from flask import render_template
from flask_login import login_required
from app.login.routes import unauthorized_callback

def configure_routes(app):
    app.register_error_handler(401, unauthorized_callback)

    @app.route('/')
    @login_required
    def home():
        return render_template('index.html')

    # Define a 401 error handler
    @app.errorhandler(401)
    def page_not_found(e):
        return render_template('404.html'), 401

    # Define a 404 error handler
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404
    
    # Define a 403 error handler
    @app.errorhandler(403)
    def page_not_found(e):
        return render_template('404.html'), 403

    @app.errorhandler(Exception)
    def handle_exception(e):
        # Handle other exceptions
        return render_template('error.html', error=str(e)), 500
