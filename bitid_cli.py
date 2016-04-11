#!/usr/bin/env python

import json
import sys, getopt
import pybitid.bitid as bitid

def main(argv):
    message = {'valid_address':'',
               'valid_uri':'',
               'valid_signature':'',
               'callback': '',
               'nonce':'',
               'address':'',
               'uri':'',
               'qrcode':'',
               'signature':''}
    try:
        opts, args = getopt.getopt(argv, "c:n:a:u:s:", ["callback=","nonce=","address=","uri=","signature="])
    except getopt.GetoptError:
        print ('To generate a bitid auth request')
        print ('bitid -c (--callback) -n (--nonce)')
        print ('To verify a bitid auth request:')
        print ('bitid -a (--address) -u (--uri) -s (--signature) -c (--callback)')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-n':
            message['nonce'] = arg
            print ('nonce', message['nonce'])
        if opt == '-c':
            message['callback'] = arg
        if opt == '-a':
            message['address'] = arg
        if opt == '-u':
            message['uri'] = arg
        if opt == '-s':
            message['signature'] = arg

        if message['address'] != '':
            message['valid_address'] = str( bitid.address_valid( message['address'] ) )

        if message['callback'] != '':
            if message['uri'] != '':
                message['valid_uri'] = str( bitid.uri_valid( message['uri'], message['callback'] ) )

                if message['address'] != '' and message['signature'] != '':
                    valid_signature = bitid.signature_valid( message['address'], message['signature'], message['uri'], message['callback'] )
                    message['valid_signature'] = str( valid_signature )
            else:
                if message['nonce'] == '':
                    print ('generating nonce')
                    message['nonce'] = bitid.generate_nonce()
                print (message['nonce'])
                message['uri'] = bitid.build_uri( message['callback'], message['nonce'] )
                message['qrcode'] = bitid.qrcode( message['uri'] )

    return json.dumps(message)
  

if __name__ == "__main__":
    retval = main(sys.argv[1:])
    print (retval)
