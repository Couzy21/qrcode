import json
import os

from django.core.cache import cache
from django.shortcuts import render
from django.utils.crypto import get_random_string

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
