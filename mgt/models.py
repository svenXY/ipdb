from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
import re

# Create your models here.

def is_valid_ipv6(ip):
    """Validates IPv6 addresses.
    """
    pattern = re.compile(r"""
        ^
        \s*                         # Leading whitespace
        (?!.*::.*::)                # Only a single whildcard allowed
        (?:(?!:)|:(?=:))            # Colon iff it would be part of a wildcard
        (?:                         # Repeat 6 times:
            [0-9a-f]{0,4}           #   A group of at most four hexadecimal digits
            (?:(?<=::)|(?<!::):)    #   Colon unless preceeded by wildcard
        ){6}                        #
        (?:                         # Either
            [0-9a-f]{0,4}           #   Another group
            (?:(?<=::)|(?<!::):)    #   Colon unless preceeded by wildcard
            [0-9a-f]{0,4}           #   Last group
            (?: (?<=::)             #   Colon iff preceeded by exacly one colon
             |  (?<!:)              #
             |  (?<=:) (?<!::) :    #
             )                      # OR
         |                          #   A v4 address with NO leading zeros 
            (?:25[0-4]|2[0-4]\d|1\d\d|[1-9]?\d)
            (?: \.
                (?:25[0-4]|2[0-4]\d|1\d\d|[1-9]?\d)
            ){3}
        )
        \s*                         # Trailing whitespace
        $
    """, re.VERBOSE | re.IGNORECASE | re.DOTALL)
    return pattern.match(ip) is not None


def validate_ipv6_addr(value):
    if not is_valid_ipv6(value):
        raise ValidationError(u'%s is not a valid IPv6 address' % value)

STATUS_CHOICES = ( 
    ('active', 'Aktiv'),
    ('inactive', 'Inaktiv'),
    ('planned', 'Geplant'),
    ('unknown', 'Unbekannt'),
    ('reserved', 'Reserviert'),
    ('blocked', 'Blockiert'),
)


class Netgroup(models.Model):
    name = models.CharField('Name', max_length=200)
    description = models.CharField('Beschreibung', max_length=200)

    def __unicode__(self):
        return self.name

class Network(models.Model):
    name = models.IPAddressField(
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
    parent = models.ForeignKey(
        'Network', null=True, blank=True,
        verbose_name='Parent' )
    vlan = models.ForeignKey(
        'Vlan', null=True, blank=True)
    def_net_size= models.IntegerField(
         'default net size', validators=[MaxValueValidator(128)], blank=True)
    def_alloc_size= models.IntegerField(
         'default allocation size', validators=[MaxValueValidator(128)], blank=True)

    def __unicode__(self):
        return '/'.join([self.name, str(self.cidr)])

class Range(models.Model):
    parent = models.ForeignKey(
        Network, verbose_name='Parent' )
    description = models.CharField(
        'Beschreibung', max_length=200)
    comment = models.CharField(
        'Kommentar', max_length=200, blank=True)
    start_ip = models.IPAddressField(
        'Start IP', help_text="Please use the following format: <em>xxx.xxx.xxx.xxx</em>.")
    stop_ip = models.IPAddressField(
        'Stop IP', help_text="Please use the following format: <em>xxx.xxx.xxx.xxx</em>.")

    def __unicode__(self):
        return '-'.join([self.start_ip, self.stop_ip])

class IpAddress(models.Model):
    network = models.ForeignKey(Network, verbose_name='Netz ID')
    range = models.ForeignKey(Range, verbose_name='Range', blank=True, null=True)
    name = models.CharField('Name', max_length=50)
    host = models.CharField('Host Name', max_length=50)
    interface = models.CharField('Interface', max_length=10)
    config = models.CharField('Config Info', max_length=200, blank=True)
    purpose = models.CharField('Zweck', max_length=200, blank=True)
    status = models.CharField('Status', choices=STATUS_CHOICES, max_length=20)

    class Meta:
        abstract = True
        
    
class Ip4Address(IpAddress):
    address = models.IpAddressField(
        'IPv4 Adresse', 
        help_text="Please use the following format: <em>xxx.xxx.xxx.xxx</em>.")

    def __unicode__(self):
        return '/'.join([self.address, str(self.cidr)])

class Ip6Address(IpAddress):
    address = models.CharField(
        'IPv6 Adresse', 
        max_length=46,
        help_text="Please enter a valid IPv6 address",
        validators=[validate_ipv6_addr])

    def __unicode__(self):
        return '/'.join([self.address, str(self.cidr)])

