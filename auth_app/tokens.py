from rest_framework_simplejwt.tokens import AccessToken

def generate_tokens(user):
    access_token = AccessToken.for_user(user)
    return {
        'access_token': str(access_token),
        'refresh_token': str(access_token),
    }
