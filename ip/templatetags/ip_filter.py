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

from django import template

register = template.Library()

def last_part(ip, with_dot=False):
    "Returns the last part of an IP address"
    if ':' in ip:
        delim = ':'
    else:
        delim = '.'
    if with_dot:
        dot = delim
    else:
        dot = ''
    last = ip.split(delim)[-1]
    return ''.join([dot, last])

register.filter('last_part', last_part)

def uqdn(fqdn):
    "Returns the short name of a host"
    return (fqdn.split('.'))[0]

register.filter('uqdn', uqdn)

def breadcrumb(ancestors, delimiter='/'):
    "Returns a breadcrumb of ancestor-IDs"
    return delimiter.join([str(a.id) for a in ancestors])

register.filter('breadcrumb', breadcrumb)
