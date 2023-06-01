import json
import os

from django.core.cache import cache
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from .models import User, UserProfile


import qrcode
import qrcodegen

# Create your views here.


qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4,
)


def home(request):
    context = {}
    if request.method == "POST":
        name = request.POST.get('name')
        details = request.POST.get('details')
        context.update({
            "name": name,
            "details": details
        })
        data = json.dumps(context)

        qr.add_data(data)
        qr.make(fit=True)
        image = qr.make_image(fill_color="black", back_color="white")
        img_name = get_random_string(8)+".png"
        context.update({'qr_name': img_name})
        qr_path = os.path.join(qrcodegen.settings.BASE_DIR,
                               'static/images', img_name)
        qr_code_count = cache.get('qr_code_count', 0)
        qr_code_count += 1
        cache.set('qr_code_count', qr_code_count)
        context.update({'qr_code_count': qr_code_count})
        image.save(qr_path)
        print(context)
        return render(request, "qr/generate.html", context=context)
    else:
        error_message = 'Invalid details'
    return render(request, "qr/home.html", )


def login(request):
    cart = json.loads(request.COOKIES.get('cart', '{}'))
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember-me')
        user = authenticate(request, username=email, password=password)
        print(user)
        if user is not None:
            response = HttpResponse()
            response.delete_cookie('register')  # delete the cart cookie
            login(request, user)
            response = HttpResponse()
            # set a cookie that lasts for 30 days
            response.set_cookie('cart', json.dumps(cart),
                                max_age=3600 * 24 * 30)
            if remember_me:
                request.session.set_expiry(1209600)  # 2 weeks
            else:
                # session expires when user closes browser
                request.session.set_expiry(0)
            return redirect('qr:home')
        else:
            error_message = 'Invalid email or password'
    else:
        error_message = None

    return render(request, "qr/login.html", {'error_message': error_message})


def signup(request):
    if request.user.is_authenticated:
        return redirect('qr:home')

    # form submission
    f_name = request.POST.get('name')
    e_mail = request.POST.get('email')
    password = request.POST.get('password')

    data = {"f_name": f_name,
            "e_mail": e_mail}
    if e_mail:
        user = User.objects.create_user(
            username=e_mail,
            password=password,  # set a default password here or let the user set it later
            email=e_mail,
            name=f_name,
        )
        user.save()
        user_profile = UserProfile.objects.create(
            user=user,
            email=e_mail,

        )
        user_profile.save()
    return render(request, "qr/signup.html")
