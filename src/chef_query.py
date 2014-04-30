#!/usr/bin/env python
# vim: set expandtab:

###
# Copyright (c) 2012, Jim Richardson <weaselkeeper@gmail.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###


"""

License: GPL V2 See LICENSE file
Author: Jim Richardson
email: weaselkeeper@gmail.com

"""
PROJECTNAME = 'chef_query'
import os
import sys
import ConfigParser
import logging
import ssl
import socket

# Setup logging
logging.basicConfig(level=logging.WARN,
                    format='%(asctime)s %(levelname)s - %(message)s',
                    datefmt='%y.%m.%d %H:%M:%S')

# Setup logging to console.
console = logging.StreamHandler(sys.stderr)
console.setLevel(logging.WARN)
logging.getLogger(PROJECTNAME).addHandler(console)
log = logging.getLogger(PROJECTNAME)


def run(_args):
    """ Do, whatever it is, we do. """
    # parse config
    get_config(args)
    ssl_host = _args.HOST
    ssl_cert = _args.CERT
    ssl_clientuser = _args.CLIENT
    conn = ssl_conn(ssl_host, ssl_cert, ssl_clientuser)
    log.debug(_args)

    log.debug('leaving run now')
    return


def ssl_conn(ssl_host, ssl_cert, ssl_clientuser):
    """ Make an ssl connection, and return it to calling function """
    log.debug('in ssl_conn with %s', ssl_host)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssl_sock = ssl.wrap_socket(sock, ca_certs='/etc/ssl/certs/ca-certificates.crt', cert_reqs=ssl.CERT_REQUIRED)
    ssl_sock.connect((ssl_host, 443))
    print repr(ssl_sock.getpeername())
    print ssl_sock.cipher()
    return ssl_sock


def get_options():
    """ Parse the command line options"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Someproject does something')
    parser.add_argument('-n', '--dry-run', action='store_true',
                        help='Dry run, do not actually perform action',
                        default=False)
    parser.add_argument('-d', '--debug', action='store_true',
                        help='Enable debugging during execution.',
                        default=None)
    parser.add_argument('-r', '--readable', action='store_true', default=False,
                        help='Display output in human readable formant.')
    parser.add_argument('-c', '--config', action='store', default=None,
                        help='Specify a path to an alternate config file')

    _args = parser.parse_args()
    _args.usage = PROJECTNAME + ".py [options]"

    return _args


def get_config(_args):
    """ Now parse the config file.  Get any and all info from config file."""
    log.debug('Now in get_config')
    parser = ConfigParser.SafeConfigParser()
    configfile = os.path.join('/etc', PROJECTNAME, PROJECTNAME + '.conf')
    if _args.config:
        _config = _args.config
    else:
        if os.path.isfile(configfile):
            _config = configfile
        else:
            log.warn('No config file found at %s', configfile)
            sys.exit(1)
    log.debug("Using config file from %s", _config)
    parser.read(_config)
    try:
        _args.HOST = parser.get('SSL', 'HOST')
        _args.CERT = parser.get('SSL', 'CERT')
        _args.CLIENT = parser.get('SSL', 'CLIENT')
    except (ConfigParser.NoOptionError, ConfigParser.NoSectionError) as error:
        log.warn("something failed in config read, python says %s" , error)
        sys.exit(1)

    log.debug('leaving get_config')
    return

# Here we start if called directly (the usual case.)
if __name__ == "__main__":
    # This is where we will begin when called from CLI. No need for argparse
    # unless being called interactively, so import it here
    args = get_options()

    if args.debug:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.WARN)

        # and now we can do, whatever it is, we do.
    sys.exit(run(args))
