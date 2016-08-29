# -*- coding: utf-8 -*-
############################################################
from pyramid.response import Response


msg1 = "<p>Resource\'s title: <strong>{title}</strong></p>"

def resource_view(context, request):
    rtitle = getattr(context, 'title', 'No name')
    leaves = ', '.join(context.keys())
    if leaves:
        out = msg1 + "<p>leaves: {leaves}</p>"
        output = out.format(title=rtitle, leaves=leaves)
    else:
        output = msg1.format(title=rtitle)
    return Response(output)
