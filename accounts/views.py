from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status
from django.urls import reverse
from rest_framework_simplejwt.views import TokenRefreshView

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Class-based view per ottenere l'access token e l'URL per il refresh token.
    """

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == status.HTTP_200_OK:
            # Estrai l'access token dal corpo della risposta
            access_token = response.data['access']
            
            # Crea un URL per il refresh token
            refresh_url = reverse('token_refresh')
            refresh_url = request.build_absolute_uri(refresh_url)
            
            return Response({
                'access_token': access_token,
                'refresh_token_url': refresh_url
            })

        return response


class CustomTokenRefreshView(TokenRefreshView):
    """
    Class-based view per il refresh del token JWT.
    """

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == status.HTTP_200_OK:
            # Crea un URL per il refresh token
            refresh_url = reverse('token_refresh')
            refresh_url = request.build_absolute_uri(refresh_url)
            
            return Response({
                'refresh_token_url': refresh_url
            })

        return response