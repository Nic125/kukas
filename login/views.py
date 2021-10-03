import json
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt, csrf_protect
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.exceptions import ObjectDoesNotExist


@ensure_csrf_cookie
def set_csrf_token(request):
    """
    This will be `/api/set-csrf-cookie/` on `urls.py`
    """
    return JsonResponse({"details": "CSRF cookie set"})

@csrf_exempt
@require_POST
def user_register(request):
    user_data = JSONParser().parse(request)

    if User.objects.filter(email=user_data['email']).exists():
        return HttpResponse('Ya existe una cuenta con es email')
    elif User.objects.filter(username=user_data['username']).exists():
        return HttpResponse('Nombre de usuario no dispoble')
    else:
        new_user = User(
            username=user_data['username'],
            email=user_data['email']
        )
        new_user.set_password(user_data['password'])
        new_user.is_active = False
        new_user.save()

        current_site = get_current_site(request)
        mail_subject = 'Activa tu cuenta.'
        message = render_to_string('acc_active_email.html', {
            'user': new_user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
            'token': default_token_generator.make_token(new_user),
        })
        to_email = user_data['email']
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        return HttpResponse('Por favor confirme su email para completar el registro')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


@csrf_exempt

def user_login(request):
    """
    This will be `/api/login/` on `urls.py`
    """
    data = json.loads(request.body)
    if User.objects.filter(email=data.get('email')).exists():
        user_username = User.objects.get(email=data.get('email'))
        username = user_username
        password = data.get('password')
        if username is None or password is None:
            return JsonResponse({
                "errors": {
                    "__all__": "Please enter both username and password"
                }
            }, status=400)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            data = {
                'username': user.username,
                'email': user.email,
                'id': user.id,
                'is_staff': user.is_staff
            }

            return JsonResponse({"detail": data})
    else:

        return JsonResponse(
            {"detail": "Credenciales inválidas"},
            status=400,
        )


def get_user(request):
    if request.user.is_authenticated:
        current_user = request.user
        data = {
            'username': current_user.username,
            'email': current_user.email,
            'id': current_user.id,
            'is_staff': current_user.is_staff
        }
        return JsonResponse({"detail": data})
    else:
        return JsonResponse({"detail": "not login"})

# @csrf_exempt
def logout_view(request):
    logout(request)

# @csrf_exempt
def user_unsubscribe(request):

    if request.method == 'POST':
        user_id = request.GET['user_id']
        user_sel = User.objects.get(id=user_id)
        user_sel.delete()
        return JsonResponse("Usuario dado de baja", safe=False)

@csrf_exempt
def user_change_password(request):

    if request.method == 'POST':
        data = JSONParser().parse(request)
        if data['change'] == 'pass':

            user_sel = User.objects.get(id=data['id'])
            user = authenticate(username=data['username'], password=data['pass'])

            if user is not None:
                user_sel.set_password(data['new_pass'])
                user_sel.save()
                return JsonResponse("Contraseña actualizada!", safe=False)
            else:
                return JsonResponse("Contraseña actual incorrecta", safe=False)

        elif data['change'] == 'email':

            if User.objects.filter(email=data['email']).exists():
                return JsonResponse("El correo electrónico ya existe, por favor elige otro", safe=False)
            else:
                user = User.objects.get(id=data['id'])
                user.email = data['email']
                user.save()
                return JsonResponse("Correo electrónico actualizado!", safe=False)

        elif data['change'] == 'username':

            if User.objects.filter(username=data['new_username']).exists():
                return JsonResponse("El nombre de usuario ya existe, por favor elige otro", safe=False)
            else:
                user = User.objects.get(id=data['id'])
                user.username = data['new_username']
                user.save()
                return JsonResponse("Nombre de usuario actualizado!", safe=False)

