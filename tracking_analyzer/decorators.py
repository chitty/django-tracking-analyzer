from tracking_analyzer.models import Tracker


def log_action(func):
    """
    Wraps any view function to log the user action
    :param func:
    :return:
    """

    def wrap(request, *args, **kwargs):
        # Check user tracking permission status before logging the information.
        # We can't track if we don't have permission.
        Tracker.objects.create_from_request(request, func.__name__)
        return func(request, *args, **kwargs)

    return wrap
