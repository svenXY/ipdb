# Create your views here.
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.views import generic
from .models import Network, Range, IpAddress, Host
import forms
from django.shortcuts import get_object_or_404
import socket, struct

def dottedQuadToNum(ip):
    "convert decimal dotted quad string to long integer"
    return struct.unpack('L',socket.inet_aton(ip))[0]


def index(request):
    net_list = Network.objects.all().order_by('id')
    return render_to_response('ip/index.html', {'net_list': net_list,})

def ip_edit(request, ip_id=None):
    if request.POST:
        if ip_id:
            ip_data = get_object_or_404(IpAddress, pk=ip_id)
            form = forms.Ip4AddressForm(instance=ip_data, data=request.POST)
        else:
            form = forms.Ip4AddressForm(data=request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect('/ip/')
    else:
        if ip_id:
            ip_data = get_object_or_404(IpAddress, pk=ip_id)
            form =  forms.Ip4AddressForm(instance=ip_data)
        else:
            form =  forms.Ip4AddressForm()

    return render_to_response('ip/ip.html', {'form':form}, context_instance=RequestContext(request)) 

class IpDetailView(generic.DetailView):
    model = IpAddress

def ip_add(request, range=None):
    if request.POST:
        form = forms.Ip4AddressForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/ip/')
        else:
            return render_to_response('ip/ip.html', {'form':form}, context_instance=RequestContext(request)) 
    elif range:
        form = forms.Ip4AddressForm(initial={ 'range':range })
        return render_to_response('ip/ip.html', {'form':form}, context_instance=RequestContext(request)) 

def ip_delete(request, ip_id=None):
        ip_obj = get_object_or_404(IpAddress, pk=ip_id)
        ip_obj.delete()
        return HttpResponseRedirect('/ip/')

def range(request, range):
    ip_list = IpAddress.objects.filter(range__id=range)
    range_data = Range.objects.filter(pk=range)[0]
    return render_to_response('ip/range.html', {'ip_list': ip_list,
                                                 'range':range_data})

class HostDetailView(generic.DetailView):
    model = Host

class HostUpdateView(generic.UpdateView):
    model = Host

class HostDeleteView(generic.DeleteView):
    model = Host

