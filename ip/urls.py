#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Name			:	
# Description	:	
# Author		: Sven Hergenhahn
#
# $Id$
# 
###################################################

from django.conf.urls import patterns, url
from .views import *

urlpatterns = patterns('ip.views', 
    url(r'^$', 'index'), 
    url(r'^range/(?P<range>\d+)/$', 'range'), 
    url(r'^range/(?P<range>\d+)/add/$', 'ip_add'), 
    #url(r'^ip/$', 'ip'), 
    url(r'^ip/(?P<pk>\d+)$', IpDetailView.as_view(), name='ip_detail'), 
    url(r'^ip/(?P<ip_id>\d+)/edit$', 'ip_edit'), 
    url(r'^ip/(?P<ip_id>\d+)/del$', 'ip_delete'), 
    url(r'^host/(?P<pk>\d+)$', HostDetailView.as_view(), name='host_detail'), 
    url(r'^host/(?P<pk>\d+)/edit$', HostUpdateView.as_view(), name='host_edit'), 
    url(r'^host/(?P<pk>\d+)/del$', HostDeleteView.as_view(), name='host_delete'), 
)
