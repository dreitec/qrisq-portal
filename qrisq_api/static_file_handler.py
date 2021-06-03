from django.views.static import serve


def static_file_server(request, path, document_root=None, show_indexes=False):
    """
    Customize the response of serving static files.

    Note:
        This should only ever be used in development, and never in production.
    """
    response = serve(request, path, document_root, show_indexes)
    response['Accept-Ranges'] = 'bytes'
    return response