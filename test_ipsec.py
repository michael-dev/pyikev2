#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" This module defines test for the IPsec module
"""
import subprocess
import unittest
from ipaddress import ip_address, ip_network

from xfrm import Xfrm, Mode
from crypto import Cipher, Integrity
from message import TrafficSelector, Proposal

__author__ = 'Alejandro Perez <alex@um.es>'


class TestIpsec(unittest.TestCase):
    def setUp(self):
        self.xfrm = Xfrm()
        self.xfrm.flush_policies()
        self.xfrm.flush_sas()

    def test_create_transport_policy(self):
        ike_conf = {
            'protect': [
                {
                    'my_port': 0,
                    'peer_port': 80,
                    'ip_proto': TrafficSelector.IpProtocol.TCP,
                    'ipsec_proto': Proposal.Protocol.AH,
                    'mode': Mode.TRANSPORT
                }
            ]
        }
        self.xfrm.create_policies(ip_address('192.168.1.1'), ip_address('192.168.1.2'), ike_conf)

    def test_create_tunnel_policy(self):
        ike_conf = {
            'protect': [
                {
                    'my_subnet': ip_network('192.168.1.0/24'),
                    'peer_subnet': ip_network('10.0.0.0/8'),
                    'my_port': 0,
                    'peer_port': 80,
                    'ip_proto': TrafficSelector.IpProtocol.TCP,
                    'ipsec_proto': Proposal.Protocol.AH,
                    'mode': Mode.TUNNEL
                }
            ]
        }
        self.xfrm.create_policies(ip_address('192.168.1.1'), ip_address('192.168.1.2'), ike_conf)

    def test_create_transport_ipsec_sa(self):
        self.xfrm.create_sa(ip_address('192.168.1.1'), ip_address('192.168.1.2'),
                            TrafficSelector(TrafficSelector.Type.TS_IPV4_ADDR_RANGE,
                                            TrafficSelector.IpProtocol.TCP, 0, 0,
                                            ip_address('192.168.1.1'),
                                            ip_address('192.168.1.1')),
                            TrafficSelector(TrafficSelector.Type.TS_IPV4_ADDR_RANGE,
                                            TrafficSelector.IpProtocol.TCP, 0, 0,
                                            ip_address('192.168.1.2'),
                                            ip_address('192.168.1.2')),
                            Proposal.Protocol.ESP, b'1234', Cipher.Id.ENCR_AES_CBC, b'1' * 16,
                            Integrity.Id.AUTH_HMAC_MD5_96, b'1' * 16, Mode.TRANSPORT)

    def test_create_tunnel_ipsec_sa(self):
        self.xfrm.create_sa(ip_address('192.168.1.1'), ip_address('192.168.1.2'),
                            TrafficSelector(TrafficSelector.Type.TS_IPV4_ADDR_RANGE,
                                            TrafficSelector.IpProtocol.TCP, 0, 0,
                                            ip_address('192.168.1.1'),
                                            ip_address('192.168.1.1')),
                            TrafficSelector(TrafficSelector.Type.TS_IPV4_ADDR_RANGE,
                                            TrafficSelector.IpProtocol.TCP, 0, 0,
                                            ip_address('192.168.1.2'),
                                            ip_address('192.168.1.2')),
                            Proposal.Protocol.ESP, b'1234', Cipher.Id.ENCR_AES_CBC, b'1' * 16,
                            Integrity.Id.AUTH_HMAC_MD5_96, b'1' * 16, Mode.TUNNEL)

    def tearDown(self):
        self.xfrm.flush_policies()
        self.xfrm.flush_sas()


if __name__ == '__main__':
    unittest.main()
