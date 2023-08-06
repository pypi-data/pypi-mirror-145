from platform import platform
import unittest
from senkalib.caaj_journal import CaajJournal
from decimal import Decimal

class TestCaajJounal(unittest.TestCase):
  def test_init(self):
    executed_at = '2022-01-12 11:11:11'
    chain = 'chain'
    platform = 'platform'
    application = 'application'
    transaction_id = '0x36512c7e09e3570dfc53176252678ee9617660550d36f4da797afba6fc55bba6'
    trade_uuid = 'bbbbbbddddddd'
    type = 'deposit'
    amount = Decimal('0.005147')
    token_symbol = 'juno'
    token_original_id = 'ibc/46B44899322F3CD854D2D46DEEF881958467CDD4B3B10086DA49296BBED94BED'
    token_symbol_uuid = '3a2570c5-15c4-2860-52a8-bff14f27a236'
    caaj_from = '0x111111111111111111111'
    caaj_to = '0x222222222222222222222'
    comment = 'hello world'

    cj = CaajJournal(executed_at, chain, platform, application, transaction_id, trade_uuid,
      type, amount, token_symbol, token_original_id, token_symbol_uuid, caaj_from, caaj_to, comment)
    assert cj.executed_at == '2022-01-12 11:11:11'
    assert cj.chain == 'chain'
    assert cj.platform == 'platform'
    assert cj.application == 'application'
    assert cj.transaction_id == '0x36512c7e09e3570dfc53176252678ee9617660550d36f4da797afba6fc55bba6'
    assert cj.trade_uuid == 'bbbbbbddddddd'
    assert cj.type == 'deposit'
    assert cj.amount == Decimal('0.005147')
    assert cj.token_symbol == 'juno'
    assert cj.token_original_id == 'ibc/46B44899322F3CD854D2D46DEEF881958467CDD4B3B10086DA49296BBED94BED'
    assert cj.token_symbol_uuid == '3a2570c5-15c4-2860-52a8-bff14f27a236'
    assert cj.caaj_from == '0x111111111111111111111'
    assert cj.caaj_to == '0x222222222222222222222'
    assert cj.comment == 'hello world'

if __name__ == '__main__':
  unittest.main()