from django.http import JsonResponse

from core.models import Ping


def health(request):
    Ping.objects.create()
    return JsonResponse({"status": "ok", "pings": Ping.objects.count()})
