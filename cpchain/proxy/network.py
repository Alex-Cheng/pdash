import logging
import time
import operator

from random import randint

import socket

from twisted.internet import reactor, protocol, defer

import msgpack

from cpchain.proxy.account import sign_proxy_data, derive_proxy_data

logger = logging.getLogger(__name__)

def entropy(length):
    return "".join(chr(randint(0, 255)) for _ in range(length))

def generate_tid():
    return entropy(20)


class PeerProtocol(protocol.DatagramProtocol):
    def __init__(self, peer_ip=None, peer_id=None, peer_info=None, timeout=5):
        self.peer_ip = peer_ip
        self.peer_id = peer_id
        self.peer_info = peer_info
        self.timeout = timeout

        self.peers = {}
        self.peers_lat = {}
        self.request = {}

    def tranaction_timeout(self, tid):
        self.request[tid][0].callback((False, tid))
        del self.request[tid]

    def send_msg(self, msg, addr):
        try:
            if msg['type']:
                logger.debug('send %s to %s' %  (str(msg['type']), str(addr)))
        except:
            logger.debug("send wrong message %s to %s" % (str(msg), str(addr)))
            return

        tid = msg['tid']
        data = msgpack.packb(msg, use_bin_type=True)
        future = time.time() + self.timeout
        while time.time() < future:
            try:
                self.transport.write(data, addr)
                break
            except socket.error as e:
                if e.errno in (11, 10055):
                    time.sleep(0.001)
                else:
                    raise socket.error(e)

        if msg['type'] == 'response':
            return

        # for request only
        d = defer.Deferred()
        timeout = reactor.callLater(self.timeout,
                                    self.tranaction_timeout, tid)
        self.request[tid] = (d, timeout)
        d.addBoth(self.dummy_callback)
        return d

    def dummy_callback(self, result):
        return result

    def datagramReceived(self, data, addr):
        msg = msgpack.unpackb(data, raw=False)

        try:
            if msg['type']:
                logger.debug('receive %s from %s' %  (str(msg['type']), str(addr)))
        except:
            logger.debug("receive wrong message %s from %s" % (str(msg), str(addr)))
            return

        if msg['type'] == 'bootstrap':
            tid = msg['tid']
            sign_tid = msg['sign_tid']

            if tid != derive_proxy_data(sign_tid):
                error = 'wrong signature'
                logger.debug(error)
                response = {
                    'type': 'response',
                    'tid': tid,
                    'data': error
                }

            else:
                peer_ip = (msg['peer_ip'] or addr[0], addr[1])
                peer_id = msg['peer_id']
                peer_info = msg['peer_info']

                peer = {
                    'addr': peer_ip,
                    'peer_info': peer_info,
                    'ts': time.time()
                }

                self.peers[peer_id] = peer
                self.peers_lat[peer_id] = 0  # initialize
                logger.debug("add peer %s" % str(peer['addr']))

                response = {
                    'type': 'response',
                    'tid': tid,
                    'data': "bootstrap"
                }

            self.send_msg(response, addr)

        elif msg['type'] == 'ping':
            tid = msg['tid']

            response = {
                'type': 'response',
                'tid': tid,
                'data': 'pong'
            }
            self.send_msg(response, addr)

        elif msg['type'] == 'pick_peer':
            tid = msg['tid']

            if self.peers_lat:
                peer_id = min(self.peers_lat.items(), key=operator.itemgetter(1))[0]
                peer = self.peers[peer_id]
                pick_peer = peer_id
            else:
                pick_peer = None

            response = {
                'type': 'response',
                'tid': tid,
                'data': pick_peer
            }

            self.send_msg(response, addr)

        elif msg['type'] == 'get_peer':
            tid = msg['tid']
            peer_id = msg['peer_id']

            pick_peer = None
            if peer_id in self.peers:
                peer = self.peers[peer_id]
                pick_peer = (peer['addr'][0], peer['peer_info'])

            response = {
                'type': 'response',
                'tid': tid,
                'data': pick_peer
            }

            self.send_msg(response, addr)

        elif msg['type'] == 'response':
            tid = msg['tid']
            data = msg['data']
            self.accept_response(tid, data)

    def accept_response(self, tid, data):
        d, timeout = self.request[tid]
        timeout.cancel()
        d.callback((True, data))
        del self.request[tid]

    def pick_peer(self, addr):
        msg = {
            'type': 'pick_peer',
            'tid': generate_tid()
        }

        return self.send_msg(msg, addr)

    def get_peer(self, peer_id, addr):
        msg = {
            'type': 'get_peer',
            'peer_id': peer_id,
            'tid': generate_tid()
        }

        return self.send_msg(msg, addr)


    def bootstrap(self, addr):
        if self.transport is None:
            return reactor.callLater(1, self.bootstrap)

        tid = generate_tid()
        msg = {
            'type': 'bootstrap',
            'tid': tid,
            'peer_ip': self.peer_ip,
            'peer_id': self.peer_id,
            'peer_info': self.peer_info,
            'sign_tid': sign_proxy_data(tid)
            }

        return self.send_msg(msg, addr)


    def ping(self, addr):
        msg = {
            'type': 'ping',
            'tid': generate_tid()
            }

        return self.send_msg(msg, addr)


    def refresh_peers(self):
        now = time.time()
        expired_peers = []

        def refresh(result, peer_id, last):
            success, _ = result

            if success:
                now = time.time()
                self.peers[peer_id]['ts'] = now
                lat = now - last
                self.peers_lat[peer_id] = lat
            return result

        for peer_id in self.peers:
            peer = self.peers[peer_id]
            ts = peer['ts']
            if now - ts > 10:
                expired_peers.append(peer_id)
                logger.debug('retire peer %s' %  str(peer['addr']))
            else:
                addr = peer['addr']
                self.ping(addr).addCallback(refresh, peer_id, time.time())

        for peer in expired_peers:
            self.peers.pop(peer)
