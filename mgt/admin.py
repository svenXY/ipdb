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

from mgt.models import Netgroup, Network, Range, Vlan, IpAddress, Host
from django.contrib import admin
from mptt.admin import MPTTModelAdmin


class VlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'vlan_id' ]

class IpAddressAdmin(admin.ModelAdmin):
    fields = ['address', 'range', 'name', 'host', 'interface', 'status', 'purpose' ]

class IpAddressInline(admin.TabularInline):
    model = IpAddress
    extra = 0
    fields = ['address', 'range', 'name', 'host', 'interface', 'status', 'purpose' ]

class RangeAdmin(admin.ModelAdmin):
    list_display = ['start_ip', 'stop_ip', 'parent', 'description' ]
    inlines = [IpAddressInline]

class RangeInline(admin.TabularInline):
    model = Range
    extra = 0
    #list_display = ['start_ip', 'stop_ip', 'parent', 'description' ]

class NetworkAdmin(MPTTModelAdmin):
    list_display = ['name','cidr', 'type', 'description', 'parent' ]
    inlines = [RangeInline]

class NetworkInline(admin.TabularInline):
    model = Network
    extra = 0
    #list_display = ['name','cidr', 'type', 'description', 'parent' ]

class NetgroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'description' ]

class HostAdmin(admin.ModelAdmin):
    pass
    #inlines = [IpAddressInline]

admin.site.register(Netgroup, NetgroupAdmin)
#admin.site.register(Netgroup, MPTTModelAdmin)
admin.site.register(Network, NetworkAdmin)
#admin.site.register(Network, MPTTModelAdmin)
admin.site.register(Range, RangeAdmin)
admin.site.register(Vlan, VlanAdmin)
admin.site.register(IpAddress, IpAddressAdmin)
admin.site.register(Host, HostAdmin)


