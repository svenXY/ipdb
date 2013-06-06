# -*- coding: utf-8 -*-
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from mptt.models import MPTTModel, TreeForeignKey
from ipaddress import ip_address, ip_network

STATUS_CHOICES = ( 
    ('active', 'Aktiv'),
    ('inactive', 'Inaktiv'),
    ('planned', 'Geplant'),
    ('unknown', 'Unbekannt'),
    ('reserved', 'Reserviert'),
    ('blocked', 'Blockiert'),
)

IFACE_CHOICES = tuple([ (i,i) for i in range(11)])


class Netgroup(models.Model):
    name = models.CharField('Name', max_length=200)
    parent = models.ManyToManyField('self', null=True, blank=True)
    description = models.CharField('Beschreibung', max_length=200)

    def __unicode__(self):
        return self.name
    created = models.DateField(auto_now=True, null=True)
    modified = models.DateField(auto_now=True, null=True)


class Network(MPTTModel):
    name = models.GenericIPAddressField(
        'Netzwerk ID', help_text="Please use the following format: <em>xxx.xxx.xxx.xxx</em>.")
    cidr = models.IntegerField(
        'CIDR Maske', validators=[MaxValueValidator(128)])
    type = models.CharField(
        'Typ', max_length=20, choices=(('subnet','Netzwerk'),('netblock','Netzblock')),
        help_text="Block - ordnet nur; Netz - enthält Adressen")
    description = models.CharField(
        'Beschreibung', max_length=200)
    comment = models.CharField(
        'Kommentar', max_length=200, blank=True)
    parent = TreeForeignKey('self', null=True, blank=True,
                               related_name='subnets',
                                limit_choices_to = { 'type':'netblock'})
    netgroup = models.ManyToManyField(Netgroup, null=True, blank=True,
        verbose_name='Net Group' )
    vlan = models.ForeignKey(
        'Vlan', null=True, blank=True)
    def_net_size= models.IntegerField(
         'default net size', validators=[MaxValueValidator(128)], blank=True, null=True)
    def_alloc_size= models.IntegerField(
         'default allocation size', validators=[MaxValueValidator(128)], blank=True, null=True)

    def __unicode__(self):
        return '/'.join([self.name, str(self.cidr)])

    def clean(self):
        # make sure the network/netblock is contained in its parent
        if self.parent:
            try:
                for a_net in ip_network(
                                    unicode(self.parent)
                                ).address_exclude(
                                    ip_network(
                                        unicode(
                                            '/'.join(
                                                        [self.name, str(self.cidr)]
                                                    )
                                        )
                                    )
                                ):
                    pass
            except ValueError, e:
                raise ValidationError(e)
    created = models.DateField(auto_now=True, null=True)
    modified = models.DateField(auto_now=True, null=True)


class Range(models.Model):
    parent = models.ForeignKey(Network, limit_choices_to = {'type':'subnet'})
    description = models.CharField(
        'Beschreibung', max_length=200)
    comment = models.CharField(
        'Kommentar', max_length=200, blank=True)
    start_ip = models.GenericIPAddressField(
        'Start IP', help_text="Please use a valid IPv4 or IPv6 format.")
    stop_ip = models.GenericIPAddressField(
        'Stop IP', help_text="Please use a valid IPv4 or IPv6 format.")

    def __unicode__(self):
        return '-'.join([self.start_ip, self.stop_ip])

    def get_next_known(self):
        '''Return the next known address in this range as IpAddress object.
           Known means that is is in the DB, but with states like unknown,
           reserved, blocked
        '''
        q = IpAddress.objects.filter(
            range__id=self.pk).filter(
                status__in=[
                    'unknown', 
                    'reserved', 
                    'blocked']
            ).order_by('address')
        return q[0]

    def get_next_free(self):
        '''Return the next free address in this range as String '''
        used_addresses = IpAddress.objects.filter(
            range__id=self.pk).order_by('address')
        addr_list = [ o.address for o in used_addresses ]
        net = ip_network(self.parent)
        start = ip_address(self.start_ip)
        stop = ip_address(self.stop_ip)
        for x in net.hosts():
            if x < start: continue
            if str(x) in addr_list:
                continue
            if x > stop: break
            return str(x)
        return 'No more free addresses avaliable!'

    def clean(self):
        '''Validate start and stop addresses as valid addresses of the network'''
        net = ip_network(self.parent)
        start = ip_address(self.start_ip)
        stop = ip_address(self.stop_ip)
        if start not in net:
            raise ValidationError('Start IP not in net')
        elif stop not in net:
            raise ValidationError('Stop IP not in net')
        elif self.stop_ip < self.start_ip:
            raise ValidationError('Order of start/stop IP is wrong')
    created = models.DateField(auto_now=True, null=True)
    modified = models.DateField(auto_now=True, null=True)


class Vlan(models.Model):
    vlan_id = models.IntegerField()
    name = models.CharField(
        'Vlan Name', max_length=200)

    def __unicode__(self):
        return "%s (%d)" % (self.name, self.vlan_id)
    created = models.DateField(auto_now=True, null=True)
    modified = models.DateField(auto_now=True, null=True)


class Host(models.Model):
    name = models.CharField(
        'Hostname', max_length=200)
    created = models.DateField(auto_now=True, null=True)
    modified = models.DateField(auto_now=True, null=True)

    def __unicode__(self):
        return self.name


class IpAddress(models.Model):
    range = models.ForeignKey(Range)
    address = models.GenericIPAddressField('IP Addresse') 
    interface = models.IntegerField('Interface Nummer', choices=IFACE_CHOICES,
                                    help_text='# of the interface (0-n)',
                                    blank = True,
                                    null=True)
    base_interface = models.BooleanField('Basis-Interface?', default=False)
    global_interface = models.BooleanField('Global generieren?', default=False)
    name = models.CharField('Interface Name', help_text='DNS-Name up to denic.de', max_length=50, blank=True)
    host = models.ManyToManyField(Host, verbose_name='hostname', 
                                  help_text='FQDN de(r|s) Hosts, der das Interface bekommt', 
                                  blank=True)
    purpose = models.CharField('Zweck', max_length=200, blank=True)
    status = models.CharField('Status', choices=STATUS_CHOICES, max_length=20)
    config = models.CharField('Config Info', max_length=200, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    modified = models.DateTimeField(auto_now=True, null=True)

    def __unicode__(self):
        return self.address
    
    def clean(self):
        # make sure the address is within the selected range
        if self.address:
            if ip_address(unicode(self.address)) < ip_address(unicode(self.range.start_ip)):
                raise ValidationError('Address is below chosen range')
            elif ip_address(unicode(self.address)) > ip_address(unicode(self.range.stop_ip)):
                raise ValidationError('Address is above chosen range')

