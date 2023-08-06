##############################################################################
#
# Copyright (c) 2010 ViFiB SARL and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################

import argparse
import os
import subprocess
import sys
try:
  import configparser
except ImportError:
  import ConfigParser as configparser

def generateCertificate(certificate_file, key_file, common_name):
  if os.path.lexists(certificate_file):
    raise ValueError("Certificate %r exists, will not overwrite." %
      certificate_file)
  if os.path.lexists(key_file):
    raise ValueError("Key %r exists, will not overwrite." %
      key_file)

  print('Generating certificate for %r (key: %r, certficate: %r)\n' % (
    common_name, key_file, certificate_file))
  subj = '/CN=%s' % common_name
  subprocess.check_call(
    ["openssl", "req", "-x509", "-nodes", "-days", "36500",
    "-subj", subj, "-newkey", "rsa:1024", "-keyout", key_file, "-out",
    certificate_file])
  if certificate_file != '-':
    with open(certificate_file, 'r') as f:
      print(f.read())
  print("\nDon't forget to add the certificate to the "
          "signature-certificate-list in your SlapOS configuration file.")


def run(args=None):
  parser = argparse.ArgumentParser()
  parser.add_argument('--cert-file', default='-',
    help='Path of certificate to generate (by default, only print on stdout)')
  parser.add_argument('key_file',
    help='Key file to generate.')
  parser.add_argument('common_name',
    help='Common name to use in the generated certificate.')
  args = parser.parse_args(args)

  generateCertificate(args.cert_file, args.key_file, args.common_name)
