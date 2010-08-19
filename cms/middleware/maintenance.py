# -*- coding: utf-8 -*-
import os
from django.conf import settings
from django.views.generic.simple import direct_to_template

class UnderConstructionMiddleware(object):
    """
    Middleware for development usage. Checks requested user's IP against
    the list provided in settings.py, CMS_UNDER_CONSTRUCTION_ALLOWED_IPS tuple.
    
    If user's IP is not included in the tuple, middleware checks the extension
    of requested files to aviod disabling media. Then the 'under construction'
    template is rendered.
    
    List of allowed media file extensions is defined in
    CMS_UNDER_CONSTRUCTION_ALLOWED_EXT tuple.
    
    """
    def process_request(self, request):
        if settings.CMS_UNDER_CONSTRUCTION_ALLOWED_IPS:
            if not request.META['REMOTE_ADDR'] in settings.CMS_UNDER_CONSTRUCTION_ALLOWED_IPS:
                extension = os.path.splitext(request.path)[1]
                if not extension in settings.CMS_UNDER_CONSTRUCTION_ALLOWED_EXT:
                    return direct_to_template(request, settings.CMS_UNDER_CONSTRUCTION_TEMPLATE)
            return None
        return None
