# python  .\zebra_print_python37.py --variable_file .\variables_4.txt .\4_units.txt --printer Zebra34

# python  .\zebra_print_python37.py --variable_file .\variables_8.txt .\8_units.txt --printer Zebra34

import re
from zebra import Zebra

ZEBRA = Zebra()


class ZebraPRNPrintException(Exception):
    pass


class MissingVariableException(ZebraPRNPrintException):
    pass


def get_printers():
    ''' Return a list of available printers, empty if there aren't any
    '''
    return ZEBRA.getqueues()


def get_default_printer():
    ''' Return the queue name for the first Zebra printer found, None
    if no Zebra can be found
    '''
    print("Hello")
    printers = get_printers()
    for p in printers:
        if any(z in p.lower() for z in ('zebra', 'zpl', 'zdesigner')):
            print(p)
            ZEBRA.setqueue(p)
            return p
    return None


def parse_prn(prn_text):
    ''' Return a list of variable names in the prn_text input
    '''
    m = re.findall('<([a-zA-Z_0-9]+?)>', prn_text)
    if m is None:
        return []
    return list(set(m))


def read_variables(fin='variables2.txt'):
    ''' Read the variables specified in 'fin' and return a dict
    '''
    d = {}
    with open(fin, 'r') as fh:
        for l in fh:
            if ',' in l:
                d.update((l.strip().split(',', 1),))
    return d


def replace_prn_variables(prn_text, variables):
    ''' Ensure that all required variables for the supplied PRN text
    are in the variables dict, raising MissingVariableException 
    with a list of missing variable names if not
    Otherwise replace all variables and return the new PRN text
    '''
    expected = parse_prn(prn_text)
    missing = []
    for e in expected:
        v = variables.get(e, None)
        if v is None:
            missing.append(e)
        else:
            prn_text = prn_text.replace('<%s>' % e, v)
    if missing:
        raise MissingVariableException(missing)
    return prn_text


def send_prn(prn_text):
    ''' Send prn_text to the printer. Only printable chars are sent

    Silently escape errors
    '''
    try:
        ZEBRA.output(''.join(c for c in prn_text if ord(c) < 128))
    except Exception:
        return None


if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        description='Print a Zebra ZPL PRN file on a local Zebra printer')
    dflt = get_default_printer()
    if dflt is None:
        dflt_str = 'No default printer available'
    else:
        dflt_str = 'Defaults to "%s"' % dflt
    parser.add_argument('file', help='The file containing PRN data to print')
    parser.add_argument('--printer', default=None,
                        help='The Zebra printer to use. %s' % dflt_str)
    parser.add_argument('--variable_file', default='variables.txt',
                        help='The file to read the variable values from. Defaults to %(default)s')
    args = parser.parse_args()

    if args.printer is None:
        if dflt is None:
            printers = get_printers()
            if printers:
                print(
                    'No default printer is available. Please specify a valid printer with the --printer argument.')
                print('Available printers are:')
                print
                print('\n'.join(printers))
            else:
                print('No printers are available on the system')
            sys.exit(1)
    else:
        # printer supplied, try and use it
        printers = get_printers()
        if args.printer not in printers:
            print('Please select a valid printer')
            print('Available printers are:')
            print
            print('\n'.join(printers))
            sys.exit(1)
        else:
            ZEBRA.setqueue(args.printer)

    v = read_variables(args.variable_file)
    with open(args.file, 'r') as fh:
        try:
            t = replace_prn_variables(
                ''.join(c for c in fh.read() if ord(c) < 128), v)
            send_prn(t)

        except MissingVariableException as e:
            print('Some variables specified in the PRN text are not supplied in the "%s" file.' %
                  args.variable_file)
            print('These variables are not supplied:')
            e[0].sort()
            print('\n'.join(e[0]))
