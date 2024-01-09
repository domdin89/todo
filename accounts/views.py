from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponseRedirect
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import AccessToken
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.conf import settings
from django.utils.encoding import force_bytes, force_str
from django.shortcuts import get_object_or_404
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
import requests
from django.contrib import messages
from django.contrib.auth.models import User
from accounts.models import Profile
from accounts.serializers import UserSerializer, ProfileSerializer, UserGetSerializer
from django.shortcuts import reverse
from django.utils.safestring import mark_safe
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from datetime import datetime, timedelta
import jwt, os, re, requests



def login_as(request):
    token = request.GET.get('token')
    
    if token:
        return login_with_token(request, token)
    else:
        messages.warning(request, "Token non trovato nell'intestazione")
        return redirect('accounts:login')

def validate_and_extract_token(token):
    try:
        # Decode token using the same secret key used for encoding
        decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return decoded_data
    except:
        return None
    
def login_with_token(request, token):
    
    user_data = validate_and_extract_token(token)
    print(user_data)

    if user_data:
        username = user_data.get('username')
        print(username)
        try:
            user = User.objects.get(username=username)

            if user:
                login(request, user)
                messages.success(request, f'Benvenuto {username}')
                return redirect('iniziative:lista-eventi')
            else:
                messages.warning(request, "Autenticazione fallita")
                return redirect('accounts:login')

        except User.DoesNotExist:
            messages.warning(request, "Utente non trovato")
            return redirect('accounts:login')

    else:
        messages.warning(request, "Token non valido")
        return redirect('accounts:login')


def generate_tokens(data):
    access_token_payload = {
        'username': data['username'],
        'exp': datetime.utcnow() + timedelta(days=1000)
    }

    access_token = jwt.encode(access_token_payload, settings.SECRET_KEY, algorithm='HS256')
    return access_token, access_token_payload


@api_view(['POST'])
def login_api(request):
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            user = authenticate(request, username=User.objects.get(
                email=username), password=password)

        except:
            user = authenticate(request, username=username, password=password)

        if user is not None:
            tokens_data = {
            'username': username,
            }

            access_token, access_token_payload = generate_tokens(tokens_data)
            expires_at = datetime.utcfromtimestamp(int(access_token_payload['exp'].timestamp()))

            if isinstance(access_token, bytes):
                print('here')
                access_token = access_token.decode('utf-8')
        # Store the refresh token
            AccessToken.objects.create(user=user, token=access_token, expires_at=expires_at)

        else:
            return Response({'error': 'Login failed'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = UserGetSerializer(user)

        return Response({'access_token': access_token, "user": serializer.data})



def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']

        if password != password_confirm:
            messages.warning(request, 'Attenzione, le due password non coincidono')
            return render(request, 'accounts/register.html', {'title': 'register'})

        if User.objects.filter(username=username).exists():
            messages.warning(request, 'Attenzione, Username già esistente, hai dimenticato la password? Recuperala')
            return render(request, 'accounts/register.html', {'title': 'register'})

        if User.objects.filter(email=email).exists():
            reset_password_link = '/password-reset/'  # Replace this with your reset password link
            message = f'Attenzione, Email già esistente, hai dimenticato la password? <a href="{reset_password_link}">Recuperala</a>'
            messages.warning(request, mark_safe(message))
            return render(request, 'accounts/register.html', {'title': 'register'})

        else:
            # Create user and profile if all validation checks pass
            try:
                user = User.objects.create(email=email, first_name=first_name, last_name=last_name, username=username)
                user.set_password(password)
                user.save()
            except Exception as e:
                print(e)

            messages.success(
                request, f'Account creato correttamente')
            # message_txt = render_to_string('accounts/user-register.txt')
            # message_html = render_to_string('accounts/user-register.html')
            # send_mail(
            #     'Perfetto! Account {} è stato creato con successo!'.format(
            #         user.username),
            #     message_txt,
            #     f'{settings.EMAIL_SENDGRID}',
            #     # destinatario
            #     [user.email],
            #     html_message=message_html,
            #     fail_silently=False,
            # )
            return HttpResponseRedirect(reverse('accounts:login'))


    return render(request, 'accounts/register.html', {
        'title': 'register',
    })



def login_user(request):
    if request.method == 'POST':
        form = LoginForm()
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = authenticate(request, username=User.objects.get(
                email=username), password=password)

        except:
            user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(
                request, f'Benvenuto {username}')
            return redirect('worksites:worksites-lists')

        else:
            messages.warning(request, "username o password non corretta")

    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {
        'title': 'Login',
        'form': form
    })

def reset_password(request):

    return render(request, 'accounts/recover_password.html', {})

def logout_user(request):
    logout(request)
    messages.success(
        request, 'Utente disconnesso con successo')
    return redirect('accounts:login')

def recover_password(request):
    return render(request, 'confirm-password.html')

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

@api_view(['POST'])
def password_reset_request(request):
    email = request.data.get('email')
    
    # Check if the user exists
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        # If user does not exist, handle it gracefully
        messages.error(request, "Nessun utente trovato con questa email.")
        return render(request, 'accounts/password_reset_request.html', {
            'title': 'Password Reset Request'
        })

    # If user exists, continue with password reset process
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    reset_link = f'{settings.SITE_URL}/password/reset/confirm/{uid}/{token}/'

    shortened_url = create_tinyurl(request, reset_link)
    send_reset_email(user, shortened_url)

    messages.success(request, "Il link per il recupero password è stato inviato via email")

    return render(request, 'accounts/auth/password_reset_done.html', {
        'title': 'Recover Password'
    })

@api_view(['GET'])
def password_reset_confirm(request, uidb64, token):
    context = {
        'uidb64': uidb64,
        'token': token
    }
    return render(request, 'accounts/auth/password_reset_confirm.html', context)


@api_view(['POST'])
def password_reset_new(request):
    try:
        uidb64 = request.data.get('uidb64')
        token = request.data.get('token')
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return HttpResponseRedirect(f'{settings.SITE_URL}/reset-password-fail/')

    if default_token_generator.check_token(user, token):
        # Handle the password reset here
        # For example, you can update the user's password and log them in.
        new_password = request.data.get('new_password2')
        print(f'new password', new_password)

        user.set_password(new_password)

        user.save()

        #return HttpResponseRedirect('https://acf.abruzzocosafare.it/reset-password-success/')
        return HttpResponseRedirect(f'{settings.SITE_URL}/reset-password-done/')
    else:
        return HttpResponseRedirect(f'{settings.SITE_URL}/reset-password-fail/')
    
def send_reset_email(user, reset_link):
    context = {
        'token': 'asdas',
        'reset_link': reset_link,
        'url': settings.SITE_URL,
        'user': user
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

def password_reset_done(request):
    return render(request, 'accounts/auth/password_reset_complete.html')
    