from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(
    404)  # we want these handlers to work for the entire app, that is why we have 'app_errorhandlers' instead of just 'errorhandlers'
def error_404(error):
    return render_template('errors/404.html'), 404


@errors.app_errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403
    # in flask you can return a second value i.e. status code, default is 200


@errors.app_errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500
