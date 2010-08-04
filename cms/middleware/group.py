from django.conf import settings
from django.http import HttpResponseForbidden
from django.template import RequestContext,Template,loader,TemplateDoesNotExist
from django.utils.importlib import import_module

def render_to_403(*args, **kwargs):       
    """       
    Returns a HttpResponseForbidden whose content is filled with the result of calling       
    django.template.loader.render_to_string() with the passed arguments.       
    """      
    if not isinstance(args,list):           
        args = []           
        args.append('403.html')                
  
    httpresponse_kwargs = {'mimetype': kwargs.pop('mimetype', None)}            
    response = HttpResponseForbidden(loader.render_to_string(*args, **kwargs), **httpresponse_kwargs)                
    return response

class GroupsRequiredMiddleware(object):
    """
    Checks if currently logged user is permitted to display particular pages.
    
    If the user does not pass group test, 403 Forbidden page is rendered.
    
    """
    def process_request(self, request):
        if not request.user.is_staff:
            if not request.user.is_anonymous():
                if request.current_page:
                    if request.current_page.login_required:                
                        if request.user.is_authenticated():
                            for group in request.user.groups.all():
                                if request.current_page:
                                    if group in request.current_page.groups_required.all():
                                        return None
                                    else:
                                        return render_to_403(context_instance=RequestContext(request))
                        else:
                            if request.current_page:
                                if request.current_page.login_required:
                                    return render_to_403(context_instance=RequestContext(request))
                                else:
                                    return None
            else:
                try:
                    if request.current_page:
                        if request.current_page.login_required:
                            return render_to_403(context_instance=RequestContext(request))
                        else:
                            return None
                except:
                    return render_to_403(context_instance=RequestContext(request))
        return None
    
    


