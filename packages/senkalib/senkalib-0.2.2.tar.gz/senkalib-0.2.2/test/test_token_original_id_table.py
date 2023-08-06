import csv
import os
from pathlib import Path
import unittest
from decimal import Decimal
from unittest.mock import patch
import requests

from senkalib.token_original_id_table import TokenOriginalIdTable

class TestTokenOriginalIdTable(unittest.TestCase):
    TOKEN_ORIGINAL_IDS_URL = 'https://raw.githubusercontent.com/ca3-caaip/token_original_id/master/token_original_id.csv'
    def test_get_all_meta_data(self):
        with patch.object(requests, 'get', new=TestTokenOriginalIdTable.mock_get):
            with patch.object(csv, 'DictReader', new=TestTokenOriginalIdTable.mock_DictReader):
                token_original_id_table = TokenOriginalIdTable(TestTokenOriginalIdTable.TOKEN_ORIGINAL_IDS_URL)
                metadata = token_original_id_table.get_all_meta_data('osmosis', 'ibc/27394FB092D2ECCD56123C74F36E4C1F926001CEADA9CA97EA622B25F41E5EB2')
                assert metadata['symbol_uuid'] == 'e7816a15-ce91-0aa8-0508-21d0d19f3aa8'
                assert metadata['symbol'] == 'atom'
                assert metadata['description'] == 'native token for cosmos'
                assert metadata['chain'] == 'osmosis'
                assert metadata['original_id'] == 'ibc/27394FB092D2ECCD56123C74F36E4C1F926001CEADA9CA97EA622B25F41E5EB2'

    def test_get_symbol_uuid(self):
        with patch.object(requests, 'get', new=TestTokenOriginalIdTable.mock_get):
            with patch.object(csv, 'DictReader', new=TestTokenOriginalIdTable.mock_DictReader):
                token_original_id_table = TokenOriginalIdTable(TestTokenOriginalIdTable.TOKEN_ORIGINAL_IDS_URL)
                symbol_uuid = token_original_id_table.get_symbol_uuid('osmosis', 'ibc/27394FB092D2ECCD56123C74F36E4C1F926001CEADA9CA97EA622B25F41E5EB2')
                assert symbol_uuid == 'e7816a15-ce91-0aa8-0508-21d0d19f3aa8'

    def test_get_symbol(self):
        with patch.object(requests, 'get', new=TestTokenOriginalIdTable.mock_get):
            with patch.object(csv, 'DictReader', new=TestTokenOriginalIdTable.mock_DictReader):
                token_original_id_table = TokenOriginalIdTable(TestTokenOriginalIdTable.TOKEN_ORIGINAL_IDS_URL)
                symbol = token_original_id_table.get_symbol('osmosis', 'ibc/27394FB092D2ECCD56123C74F36E4C1F926001CEADA9CA97EA622B25F41E5EB2')
                assert symbol == 'atom'

    def test_get_description(self):
        with patch.object(requests, 'get', new=TestTokenOriginalIdTable.mock_get):
            with patch.object(csv, 'DictReader', new=TestTokenOriginalIdTable.mock_DictReader):
                token_original_id_table = TokenOriginalIdTable(TestTokenOriginalIdTable.TOKEN_ORIGINAL_IDS_URL)
                description = token_original_id_table.get_description('osmosis', 'ibc/27394FB092D2ECCD56123C74F36E4C1F926001CEADA9CA97EA622B25F41E5EB2')
                assert description == 'native token for cosmos'

    def test_get_chain(self):
        with patch.object(requests, 'get', new=TestTokenOriginalIdTable.mock_get):
            with patch.object(csv, 'DictReader', new=TestTokenOriginalIdTable.mock_DictReader):
                token_original_id_table = TokenOriginalIdTable(TestTokenOriginalIdTable.TOKEN_ORIGINAL_IDS_URL)
                chain = token_original_id_table.get_chain('osmosis', 'ibc/27394FB092D2ECCD56123C74F36E4C1F926001CEADA9CA97EA622B25F41E5EB2')
                assert chain == 'osmosis'

    class TestContent:
        @classmethod
        def decode(cls):
            return ""

    @classmethod
    def mock_get(cls, url: str):
        cls.content = TestTokenOriginalIdTable.TestContent
        return cls
    @classmethod
    def mock_DictReader(cls, src):
        token_original_id_table = [
            {'symbol_uuid': 'e7816a15-ce91-0aa8-0508-21d0d19f3aa8', 'symbol': 'atom', 'description': 'native token for cosmos', 'chain': 'osmosis', 'original_id': 'ibc/27394FB092D2ECCD56123C74F36E4C1F926001CEADA9CA97EA622B25F41E5EB2'},
            {'symbol_uuid': 'e7816a15-ce91-0aa8-0508-21d0d19f3aa8', 'symbol': 'atom', 'description': 'native token for cosmos', 'chain': 'bsc', 'original_id': '0x0Eb3a705fc54725037CC9e008bDede697f62F335'},
            {'symbol_uuid': 'e7816a15-ce91-0aa8-0508-21d0d19f3aa8', 'symbol': 'atom', 'description': 'native token for cosmos', 'chain': 'cosmos', 'original_id': ''},
            {'symbol_uuid': '3a2570c5-15c4-2860-52a8-bff14f27a236', 'symbol': 'juno', 'description': 'native token for juno', 'chain': 'osmosis', 'original_id': 'ibc/46B44899322F3CD854D2D46DEEF881958467CDD4B3B10086DA49296BBED94BED'},
            {'symbol_uuid': 'd7fdee9c-13cf-afd3-e793-33d56c10fc12', 'symbol': 'luna', 'description': 'native token for terra', 'chain': 'osmosis', 'original_id': 'ibc/0EF15DF2F02480ADE0BB6E85D9EBB5DAEA2836D3860E9F97F9AADE4F57A31AA0'},
            {'symbol_uuid': '432374c6-5e69-eb86-10d9-8c49176aeb1b', 'symbol': 'ust', 'description': 'doller peg token on terra', 'chain': 'osmosis', 'original_id': 'ibc/BE1BB42D4BE3C30D50B68D7C41DB4DFCE9678E8EF8C539F6E6A9345048894FCC'},
            {'symbol_uuid': 'c0c8e177-53c3-c408-d8bd-067a2ef41ea7', 'symbol': 'osmo', 'description': 'native token for osmosis', 'chain': 'osmosis', 'original_id': ''},
            {'symbol_uuid': 'c6e75d14-e2e0-8d5e-72bb-5cee05a8820a', 'symbol': 'umee', 'description': 'Umee is a cross chain DeFi hub that interconnects between blockchains', 'chain': 'osmosis', 'original_id': 'ibc/67795E528DF67C5606FC20F824EA39A6EF55BA133F4DC79C90A8C47A0901E17C'},
            {'symbol_uuid': '0449e895-da15-a096-7300-00c666088b39', 'symbol': 'scrt', 'description': 'Native token for secret network', 'chain': 'osmosis', 'original_id': 'ibc/0954E1C28EB7AF5B72D24F3BC2B47BBB2FDF91BDDFD57B74B99E133AED40972A'},
            {'symbol_uuid': 'b5a385b2-4599-24be-adb9-0797c565e906', 'symbol': 'cro', 'description': 'native token for crypto.org', 'chain': 'osmosis', 'original_id': 'ibc/E6931F78057F7CC5DA0FD6CEF82FF39373A6E0452BF1FD76910B93292CF356C1'},
            {'symbol_uuid': '58311b55-9ccc-a50c-8ad7-d77e5798b345', 'symbol': 'xprt', 'description': 'native token for Persistence', 'chain': 'osmosis', 'original_id': 'ibc/A0CC0CF735BFB30E730C70019D4218A1244FF383503FF7579C9201AB93CA9293'},
            {'symbol_uuid': '377b9a23-1cb1-e4b5-4f03-910e3e438d34', 'symbol': 'akt', 'description': 'native token for akash', 'chain': 'osmosis', 'original_id': 'ibc/1480B8FD20AD5FCAE81EA87584D269547DD4D436843C1D20F15E00EB64743EF4'},
            {'symbol_uuid': 'f12c88a1-b54d-d867-9d8f-78fa8960de4a', 'symbol': 'regen', 'description': 'native token for regen network', 'chain': 'osmosis', 'original_id': 'ibc/1DCC8A6CB5689018431323953344A9F6CC4D0BFB261E88C9F7777372C10CD076'},
            {'symbol_uuid': '85f9ab60-60c7-9a98-bbb3-bba925452953', 'symbol': 'dvpn', 'description': 'native token for sentinel', 'chain': 'osmosis', 'original_id': 'ibc/9712DBB13B9631EDFA9BF61B55F1B2D290B2ADB67E3A4EB3A875F3B6081B3B84'},
            {'symbol_uuid': '8ad58d58-f143-3b82-f011-e43eb6c14cfb', 'symbol': 'iris', 'description': 'native token for irisnet', 'chain': 'osmosis', 'original_id': 'ibc/7C4D60AA95E5A7558B0A364860979CA34B7FF8AAF255B87AF9E879374470CEC0'}
        ]
        return token_original_id_table


if __name__ == '__main__':
  unittest.main()