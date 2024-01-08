from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.conf import settings
from django.utils.encoding import force_bytes, force_text
from django.shortcuts import get_object_or_404
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
import requests
from django.contrib import messages
from django.contrib.auth.models import User
from accounts.models import Profile
from accounts.serializers import UserSerializer, ProfileSerializer, UserGetSerializer
from django.http import HttpResponseRedirect


def send_link(request, user, token):
    context = {
        'token': token,
        'url': settings.SITE_URL,
        'user': user
    }
    message_txt = render_to_string('registration-link.txt', context)
    message_html = render_to_string('registration-link.html', context)

    send_mail(
        subject='Fanta20 conferma account',
        message=message_txt,
        html_message=message_html,
        from_email=settings.EMAIL_SENDER,
        recipient_list=[user.email],
        fail_silently=False,
    )

    return Response({'message': 'ok'})

def confirm_account(request):
    token = request.GET.get('token')

    profile = Profile.objects.get(token=token)

    if profile.token == token:
        # Token is valid, confirm the user's account
        profile.user.is_active = True
        profile.user.save()
        # Redirect to some success page or login page
        return redirect('https://fanta20.it/register-success')
    else:
        return redirect('https://fanta20.it/registrazione-fallita')
        # Token is invalid, handle the error or redirect to some error page

@api_view(['POST'])
def register(request):
    user_serializer = UserSerializer(data=request.data)
    if user_serializer.is_valid():
        user = user_serializer.save()

        token = default_token_generator.make_token(user)
        profile_serializer = ProfileSerializer(
            data={'user': user.id, 'name': user.first_name, 'surname': user.last_name, 'token': token, 'email': user.email })
        if profile_serializer.is_valid():
            profile = profile_serializer.save()
            user_serializer = UserGetSerializer(user)
            send_link(request, user, token)

            return Response(user_serializer.data, status=status.HTTP_201_CREATED)
        else:
            user.delete()
            return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def create_tinyurl(request, url):
    if request.method == 'POST':
        api_token = '4UEg0RmH3QcYDpVak9OImrePpnDtNU2Qe6wPU1abikgzPnfehbHFvbNJlcwL'
        url = url
        domain = 'tinyurl.com'

        if not url:
            return Response({'error': 'URL is missing'})

        try:
            # Make a POST request to the TinyURL API
            api_url = f'https://api.tinyurl.com/create?api_token={api_token}'
            headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json'
            }
            data = {
                'url': url,
                'domain': domain
            }
            response = requests.post(api_url, headers=headers, json=data)
            response_data = response.json()

            # Check if the response contains the shortened URL
            if 'data' in response_data and 'tiny_url' in response_data['data']:
                tinyurl = response_data['data']['tiny_url']
                return tinyurl
            else:
                return Response({'error': 'Failed to create TinyURL'})

        except requests.exceptions.RequestException as e:
            return Response({'error': 'Failed to connect to TinyURL service'})

    return Response({'error': 'Invalid request method'})

def recover_password(request):
    return render(request, 'confirm-password.html')

@api_view(['POST'])
def password_reset_request(request):
    email = request.data.get('email')
    profile = get_object_or_404(Profile, email=email)

    token = default_token_generator.make_token(profile.user)
    uid = urlsafe_base64_encode(force_bytes(profile.pk))

    reset_link = f'https://fanta20.it/recover-password?uid={uid}&token={token}'


    shortened_url = create_tinyurl(request, reset_link)
    print(f'short {shortened_url}')

    send_reset_email(profile, shortened_url)

    return Response({
                    'message': 'Password reset link has been sent to your email.',
                    'uid': uid,
                    'token': token,
                     }, status=status.HTTP_200_OK)


@api_view(['POST'])
def password_reset_confirm(request):
    try:
        uidb64 = request.data.get('uidb64')
        token = request.data.get('token')
        uid = force_text(urlsafe_base64_decode(uidb64))
        profile = Profile.objects.get(pk=uid)

        user = profile.user
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return HttpResponseRedirect('https://fanta20.it/reset-password-fail/')

    if default_token_generator.check_token(user, token):
        # Handle the password reset here
        # For example, you can update the user's password and log them in.
        new_password = request.data.get('new_password')

        user.set_password(new_password)

        user.save()
        return HttpResponseRedirect('https://fanta20.it/reset-password-success/')
    else:
        return HttpResponseRedirect('https://fanta20.it/reset-password-fail/')
def send_reset_email(user, reset_link):
    context = {
        'reset_link': reset_link,
    }
    message_txt = render_to_string('password_reset_link.txt', context)
    message_html = render_to_string('password_reset_link.html', context)

    send_mail(
        subject='Password Reset',
        message=message_txt,
        html_message=message_html,
        from_email=settings.EMAIL_SENDER,
        recipient_list=[user.email],
        fail_silently=False,
    )
