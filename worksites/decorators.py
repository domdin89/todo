from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import AccessToken
from accounts.models import Profile

INVALID_TOKEN_MESSAGE = 'Invalid token'

def check_and_decode_token(token):
    try:
        decoded_token = AccessToken(token)
        profile_id = decoded_token['profile_id']
        return profile_id
    except TokenError:
        raise InvalidToken(INVALID_TOKEN_MESSAGE)

def validate_token(view_func):
    def wrapper(request, *args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        token = auth_header.split(' ')[1] if auth_header.startswith('Bearer ') else ''
        
        try:
            profile_id = check_and_decode_token(token)
            profile = Profile.objects.get(id=profile_id)
            if profile:
                request.profile_id = profile_id  # Store the profile_id in the request object for later use
            else:
                return Response({'message': 'Utente non presente'}, status=status.HTTP_401_UNAUTHORIZED)
        except InvalidToken:
            return Response({'message': INVALID_TOKEN_MESSAGE}, status=status.HTTP_401_UNAUTHORIZED)
        
        return view_func(request, *args, **kwargs)
    
    return wrapper