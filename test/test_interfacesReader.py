# -*- coding: utf-8 -*-
import os
import unittest
from ..debinterface import InterfacesReader


INF_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "interfaces.txt")
INF2_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "interfaces2.txt")
INF3_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "interfaces3.txt")

class TestInterfacesReader(unittest.TestCase):
    def test_parse_interfaces_count(self):
        """Should have 8 adapters"""

        nb_adapters = 8
        reader = InterfacesReader(INF_PATH)
        adapters = reader.parse_interfaces()
        self.assertEqual(len(adapters), nb_adapters)

    def test_parse_interfaces1(self):
        """All adapters should validate and not raise ValueError"""
        reader = InterfacesReader(INF_PATH)
        for adapter in reader.parse_interfaces():
            adapter.validateAll()

    def test_parse_interfaces1_comments(self):
        """All adapters should validate and not raise ValueError"""
        reader = InterfacesReader(INF_PATH)
        adapters, comments = reader.parse_interfaces(read_comments=True)
        for adapter in adapters:
            adapter.validateAll()
        expected_comment = ('# Used by ifup(8) and ifdown(8). See the interfaces(5) manpage or\n'
                            '# /usr/share/doc/ifupdown/examples for more information.\n')
        self.assertEqual(expected_comment, comments)

    def test_parse_interfaces2(self):
        """All adapters should validate and not raise ValueError"""
        reader = InterfacesReader(INF2_PATH)
        for adapter in reader.parse_interfaces():
            adapter.validateAll()

    def test_parse_interfaces2_comments(self):
        """All adapters should validate and not raise ValueError"""
        reader = InterfacesReader(INF2_PATH)
        adapters, comments = reader.parse_interfaces(read_comments=True)
        for adapter in adapters:
            adapter.validateAll()
        self.assertEqual('# The primary network interface\n', comments)

    def test_dnsnameservers_not_unknown(self):
        """All adapters should validate"""
        reader = InterfacesReader(INF_PATH)
        eth1 = next(
            (x for x in reader.parse_interfaces() if x.attributes['name'] == "eth1"),
            None
        )
        self.assertNotEqual(eth1, None)
        self.assertEqual(eth1.attributes["dns-nameservers"], "8.8.8.8")

    def test_interfaces2(self):
        """All adapters should validate"""
        reader = InterfacesReader(INF2_PATH)
        adapters = reader.parse_interfaces()
        self.assertEqual(len(adapters), 2)
        for adapter in adapters:
            adapter.validateAll()
        self.assertEqual(adapters[0].attributes, {
            'addrFam': 'inet',
            'broadcast': '192.168.0.255',
            'name': 'eth0',
            'auto': True,
            'bridge-opts': {},
            'up': ['ethtool -s eth0 wol g'],
            'gateway': '192.168.0.254',
            'down': [],
            'source': 'static',
            'netmask': '255.255.255.0',
            'address': '192.168.0.250',
            'pre-up': [],
            'post-down': [],
            'post-up': [],
            'pre-down': []
        })

    def test_multiDns_read(self):
        """All adapters should validate"""
        reader = InterfacesReader(INF2_PATH)
        adapters = reader.parse_interfaces()
        self.assertEqual(len(adapters), 2)
        for adapter in adapters:
            adapter.validateAll()
        self.assertEqual(adapters[1].attributes, {
            'addrFam': 'inet',
            'name': 'eth2',
            'source': 'static',
            'bridge-opts': {},
            'dns-nameservers': ['8.8.8.8', '8.8.4.4', '4.2.2.2'],
            'netmask': '255.255.255.0',
            'address': '10.1.20.10',
            'up': [],
            'down': [],
            'pre-up': [],
            'pre-down': [],
            'post-up': [],
            'post-down': []
        })

    def test_read_comments_no_space(self):
        """Comments at the top of file should all be returned."""
        reader = InterfacesReader(INF_PATH)
        adapters, comments = reader.parse_interfaces(read_comments=True)
        expected = ('# Used by ifup(8) and ifdown(8). See the interfaces(5) manpage or\n'
                    '# /usr/share/doc/ifupdown/examples for more information.\n')
        self.assertEqual(expected, comments)

    def test_read_comments_space(self):
        """Comments at the top of file should all be returned."""
        reader = InterfacesReader(INF3_PATH)
        adapters, comments = reader.parse_interfaces(read_comments=True)
        expected = ('# This is a comment block\n'
                    '# That contains a space after it\n'
                    '# before starting parsing any interfaces information.\n')
        self.assertEqual(expected, comments)
        self.assertEqual(adapters[0].attributes, {'addrFam': 'inet',
                                                  'auto': True,
                                                  'bridge-opts': {},
                                                  'down': [],
                                                  'name': 'lo',
                                                  'post-down': [],
                                                  'post-up': [],
                                                  'pre-down': [],
                                                  'pre-up': [],
                                                  'source': 'loopback',
                                                  'up': []})
