# views.py
from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import ShortURL
from .forms import ShortnerForm
import qrcode
from .models import decode_base62
from io import BytesIO
import base64
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

@method_decorator(login_required, name='dispatch')
class URLShortenerView(View):
    template_name = 'shortner/url_shortener.html'

    def get(self, request, short_part=None):
        if short_part:
            short_url = get_object_or_404(ShortURL, short_part=short_part)
            return redirect(short_url.original_url)
        form = ShortnerForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = ShortnerForm(request.POST)
        if form.is_valid():
            short_url = form.save()
            short_url.added_by = request.user
            short_url.save()
            # Generate QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(short_url.original_url)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")


            buffer = BytesIO()
            img.save(buffer, format="PNG")
            qr_image_bytes = buffer.getvalue()

            # Convert the bytes to a base64-encoded string
            qr_image_base64 = base64.b64encode(qr_image_bytes).decode('utf-8')
            short_url.qr = qr_image_base64
            short_url.save()

            # short_url.qr.save(short_url.short_part+'.png', img, save=True)

            return render(request, 'shortner/url_shortened.html', {'short_url': short_url})
        return render(request, self.template_name, {'form': form})


@method_decorator(login_required, name='dispatch')
class ShortURLEditView(UpdateView):
    model = ShortURL
    form_class = ShortnerForm
    template_name = 'shortner/url_shortener.html'
    success_url = reverse_lazy('shortner:url_list')   


@method_decorator(login_required, name='dispatch')
class ShortURLDeleteView(DeleteView):
    model = ShortURL
    template_name = 'shortner/url_confirm_delete.html'
    success_url = reverse_lazy('shortner:url_list')   


@method_decorator(login_required, name='dispatch')
class ShortURLListView(ListView):
    model = ShortURL
    template_name = 'shortner/url_list.html'
    
    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(added_by=self.request.user).filter(deleted_at=None)