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


from mgt.models import Netgroup, Network, Range, IpAddress
from django.forms import ModelForm

class Ip4AddressForm(ModelForm):
    class Meta:
        model=IpAddress
        #fields = [ 'address', 'name', 'host', 'interface', 'status', 'range', 'purpose' ]
