import re
from zebra import Zebra

ZEBRA = Zebra()

def get_printers():
    ''' Return a list of available printers, empty if there aren't any
    '''
    return ZEBRA.getqueues()

def get_default_printer():
    ''' Return the queue name for the first Zebra printer found, None
    if no Zebra can be found
    '''
    print "Hello"
    printers = get_printers()
    for p in printers:
        if any(z in p.lower() for z in ('zebra', 'zpl', 'zdesigner')):
            print p
            ZEBRA.setqueue(p)
            return p
    return None
	
print get_default_printer()