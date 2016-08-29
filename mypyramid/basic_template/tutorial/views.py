# -*- coding: utf-8 -*-
############################################################
from pyramid.response import Response


def resource_view(context, request):
    rtitle = getattr(context, 'title', 'No name')
    leaves = list(context.keys())
    if leaves:
        output = "Resource\'s title: %s, leaves: %s" % (rtitle,
                                                        leaves)
    else:
        output = "Resource\'s title: %s" % rtitle
    return Response(output)
