# Compatibily code in case that pyOpenSSL is not installed.

import functools, tempfile
from subprocess import Popen, PIPE, STDOUT

_tmpfile = functools.partial(tempfile.NamedTemporaryFile, prefix=__name__+'-')

class Error(Exception): pass

FILETYPE_PEM = 1

class X509(object):
  pass

def dump_publickey(type, pkey):
  assert type == FILETYPE_PEM, type
  pkey.seek(0, 0)
  r = pkey.read()
  if not r.startswith(b'-----BEGIN PUBLIC KEY-----'):
    p = Popen(("openssl", "rsa", "-in", pkey.name, "-pubout"),
              stdout=PIPE, stderr=PIPE)
    r, err = p.communicate()
    if p.poll():
      raise Error(err)
  return r

def load_privatekey(type, buffer):
  assert type == FILETYPE_PEM, type
  r = _tmpfile()
  r.write(buffer.encode())
  r.flush()
  return r

def load_certificate(type, buffer):
  # extract public key since we only use it to verify signatures
  assert type == FILETYPE_PEM, type
  r = _tmpfile()
  p = Popen(("openssl", "x509", "-pubkey", "-noout"),
            stdin=PIPE, stdout=r, stderr=PIPE)
  err = p.communicate(buffer.encode())[1]
  if p.poll():
    raise Error(err)
  cert = X509()
  cert.get_pubkey = lambda: r
  return cert

def sign(pkey, data, digest):
  p = Popen(("openssl", digest, "-sign", pkey.name),
            stdin=PIPE, stdout=PIPE, stderr=PIPE)
  out, err = p.communicate(data)
  if p.poll():
    raise Error(err)
  return out

def verify(cert, signature, data, digest):
  with _tmpfile() as f:
    f.write(signature)
    f.flush()
    p = Popen(("openssl", digest, "-verify", cert.get_pubkey().name,
               "-signature", f.name), stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    err = p.communicate(data)[0]
  if p.poll():
    raise Error(err)
