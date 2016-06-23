class HerokuRemoteAddr(object):
    """
    This middleware class is required for rate limiting
    """
    def process_request(self, request):
        """
            if 'HTTP_X_FORWARDED_FOR' is set, then the actual address will
            be the last IP in the list
        """
        if (
            'HTTP_X_FORWARDED_FOR' in request.META and
            len(request.META['HTTP_X_FORWARDED_FOR']) > 0):
            
            request.META['REMOTE_ADDR'] = request.META['HTTP_X_FORWARDED_FOR'][-1]
        pass
        # request.META['REMOTE_ADDR'] = # [...]
