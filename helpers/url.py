def back(request):
    return request.META.get("HTTP_REFERER")
