from user.models import UserLog


class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def middleware(self, method, url, user):
        try:
            user_log = UserLog.objects.get(method=method, url=url, user=user)
            user_log.count += 1
            user_log.save()
        except:
            UserLog.objects.create(method=method, url=url, user=user)

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated:
            self.middleware(request.method, request.path, request.user)
        return response

