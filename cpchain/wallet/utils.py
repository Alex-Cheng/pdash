import urllib.parse
import time
from datetime import datetime as dt
from cpchain.crypto import ECCipher, Encoder


def build_url(url, values):
    if values:
        if 'timestamp' not in values:
            values['timestamp'] = str(time.time())
    else:
        values = dict(timestamp=str(time.time()))
    data = urllib.parse.urlencode(values)
    new_url = url + "?" + data
    return new_url

def eth_addr_to_string(eth_addr):
    string_addr = eth_addr[2:]
    string_addr = string_addr.lower()
    return string_addr

def get_address_from_public_key_object(pub_key_string):
    pub_key = get_public_key(pub_key_string)
    return ECCipher.get_address_from_public_key(pub_key)

def get_public_key(public_key_string):
    pub_key_bytes = Encoder.hex_to_bytes(public_key_string)
    return ECCipher.create_public_key(pub_key_bytes)

def formatTimestamp(timestamp):
    months = [
        ["Jan.", "January"],
        ["Feb.", "February"],
        ["Mar.", "March"],
        ["Apr.", "April"],
        ["May", "May"],
        ["Jun.", "June"],
        ["Jul.", "July"],
        ["Aug.", "August"],
        ["Sept.", "September"],
        ["Oct.", "October"],
        ["Nov.", "November"],
        ["Dec.", "December"],
    ]
    return months[timestamp.month - 1][0] + ' ' + timestamp.strftime('%d, %Y')

def to_datetime(created):
    return dt.strptime(created, '%Y-%m-%dT%H:%M:%SZ')
