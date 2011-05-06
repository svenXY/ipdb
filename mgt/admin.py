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

from mgt.models import Netgroup, Network, Range, Vlan, Ip4Address, Ip6Address
from django.contrib import admin

class RangeAdmin(admin.ModelAdmin):
    list_display = ['start_ip', 'stop_ip', 'parent', 'description' ]

class RangeInline(admin.TabularInline):
    model = Range
    extra = 0
    #list_display = ['start_ip', 'stop_ip', 'parent', 'description' ]

class VlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'vlan_id' ]

class Ip4AddressAdmin(admin.ModelAdmin):
    list_display = ['address', 'name', 'host', 'interface', 'status', 'purpose' ]

class Ip4AddressInline(admin.TabularInline):
    model = Ip4Address
    extra = 0
    #list_display = ['address', 'name', 'host', 'interface', 'status', 'purpose' ]

class Ip6AddressAdmin(admin.ModelAdmin):
    list_display = ['address', 'name', 'host', 'interface', 'status', 'purpose' ]

class Ip6AddressInline(admin.TabularInline):
    model = Ip6Address
    extra = 0
    #list_display = ['address', 'name', 'host', 'interface', 'status', 'purpose' ]

class NetworkAdmin(admin.ModelAdmin):
    list_display = ['name','cidr', 'type', 'description', 'parent' ]
    inlines = [RangeInline, Ip4AddressInline, Ip6AddressInline]

class NetworkInline(admin.TabularInline):
    model = Network
    extra = 0
    #list_display = ['name','cidr', 'type', 'description', 'parent' ]

class NetgroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'description' ]
    inlines = [NetworkInline]

admin.site.register(Netgroup, NetgroupAdmin)
admin.site.register(Network, NetworkAdmin)
admin.site.register(Range, RangeAdmin)
admin.site.register(Vlan, VlanAdmin)
admin.site.register(Ip4Address, Ip4AddressAdmin)
admin.site.register(Ip6Address, Ip6AddressAdmin)


