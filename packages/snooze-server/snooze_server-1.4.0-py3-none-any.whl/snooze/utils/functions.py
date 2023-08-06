#
# Copyright 2018-2020 Florian Dematraz <florian.dematraz@snoozeweb.net>
# Copyright 2018-2020 Guillaume Ludinard <guillaume.ludi@gmail.com>
# Copyright 2020-2021 Japannext Co., Ltd. <https://www.japannext.co.jp/>
# SPDX-License-Identifier: AFL-3.0
#

#!/usr/bin/python3.6
import os
import hashlib
from pathlib import Path

def dig(dic, *lst):
    """
    Input: Dict, List
    Output: Any

    Like a Dict[value], but recursive
    """
    if len(lst) > 0:
        try:
            if lst[0].isnumeric():
                return dig(dic[int(lst[0])], *lst[1:])
            else:
                return dig(dic[lst[0]], *lst[1:])
        except:
            return None
    else:
        return dic

def ensure_kv(dic, value, *lst):
    """
    Input: Dict, Value, List
    Output: Any

    Set value at dic[*lst]
    """
    element = dic
    for i, raw_key in enumerate(lst):
        key = raw_key
        if raw_key.isnumeric():
            key = int(raw_key)
        try:
            if key not in element:
                if i == len(lst) - 1:
                    element[key] = value
                    return dic
                else:
                    element[key] = {}
            element = element[key]
        except:
            return dic
    return dic

def sanitize(d, str_from = '.', str_to = '_'):
    new_d = {}
    if isinstance(d, dict):
        for k, v in d.items():
            new_d[k.replace(str_from, str_to)] = sanitize(v)
        return new_d
    else:
        return d

flatten = lambda x: [z for y in x for z in (flatten(y) if hasattr(y, '__iter__') and not isinstance(y, str) else (y,))]

def to_tuple(l):
    return tuple(to_tuple(x) for x in l) if type(l) is list else l

CA_BUNDLE_PATHS = [
    '/etc/ssl/certs/ca-certificates.crt', # Debian / Ubuntu / Gentoo
    '/etc/pki/tls/certs/ca-bundle.crt', # RHEL 6
    '/etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem', # RHEL 7
    '/etc/ssl/ca-bundle.pem', # OpenSUSE
    '/etc/pki/tls/cacert.pem', # OpenELEC
    '/etc/ssl/cert.pem', # Alpine Linux
]

def ca_bundle():
    '''Returns Linux CA bundle path'''
    if os.environ.get('SSL_CERT_FILE'):
        return os.environ.get('SSL_CERT_FILE')
    elif os.environ.get('REQUESTS_CA_BUNDLE'):
        return os.environ.get('REQUESTS_CA_BUNDLE')
    else:
        for ca_path in CA_BUNDLE_PATHS:
            if Path(ca_path).exists():
                return ca_path

def ensure_hash(record):
    if not 'hash' in record:
        if 'raw' in record:
            record['hash'] = hashlib.md5(record['raw']).hexdigest()
        else:
            record['hash'] = hashlib.md5(repr(sorted(record.items())).encode('utf-8')).hexdigest()
