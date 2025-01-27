class InitializeSessionReportsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'reports' not in request.session:
            request.session['reports'] = []
        response = self.get_response(request)
        return response
