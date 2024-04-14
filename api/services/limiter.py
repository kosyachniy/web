def get_ip(request):
    """Get IP address"""
    return request.state.ip


def get_user(request):
    """Get user ID"""
    return request.state.user or request.state.token


def get_uniq(request):
    """Get unique requester"""
    return get_ip(request) or get_user(request)
