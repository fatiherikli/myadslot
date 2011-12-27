from django.contrib.auth.decorators import  REDIRECT_FIELD_NAME, user_passes_test

def login_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated(),
        redirect_field_name=redirect_field_name,
        login_url = "/auth/login"
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

