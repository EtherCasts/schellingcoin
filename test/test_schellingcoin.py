import unittest

import schellingcoin

class SchellingCoinTestCase(unittest.TestCase):

    SENDER = 'alice'
    VALUE = 123
    HASH = schellingcoin.hash_sender_value(SENDER, VALUE)

    def setUp(self):
        self.c = schellingcoin.SchellingCoin()

    def test_submit_hash(self):
        self.c.submit_hash(self.SENDER, self.HASH)
        s = self.c.submissions[self.SENDER]

        self.assertEqual(s.sender, self.SENDER)
        self.assertFalse(s.is_complete())

    def test_submit_proof(self):
        self.c.submit_hash(self.SENDER, self.HASH)
        self.c.increment_block()
        self.c.submit_proof(self.SENDER, self.VALUE)
        s = self.c.submissions[self.SENDER]

        self.assertEqual(s.sender, self.SENDER)
        self.assertEqual(s.value, self.VALUE)
        self.assertTrue(s.is_complete())

    def test_valid_submission(self):
        self.c.submit_hash(self.SENDER, self.HASH)
        self.c.increment_block()
        self.c.submit_proof(self.SENDER, self.VALUE)
        s = self.c.submissions[self.SENDER]

        self.assertEqual(s.sender, self.SENDER)
        self.assertEqual(s.value, self.VALUE)
        self.assertTrue(s.is_valid())

        sorted_values = self.c.correctly_sorted_values()
        self.assertEquals(sorted_values, [(self.SENDER, self.VALUE)])

    def test_invalid_submission(self):
        self.c.submit_hash(self.SENDER, self.HASH)
        self.c.increment_block()
        self.c.submit_proof(self.SENDER, self.VALUE + 1)
        s = self.c.submissions[self.SENDER]

        self.assertEqual(s.sender, self.SENDER)
        self.assertFalse(s.is_valid())

        self.assertEqual(self.c.correctly_sorted_values(), [])

    def test_valid_multiple_submission(self):
        entries = [('alice', 123), ('bob', 300), ('charlie', 122), ('dirk', 50)]

        for sender, value in entries:
            hash = schellingcoin.hash_sender_value(sender, value)
            self.c.submit_hash(sender, hash)

        self.c.increment_block()

        for sender, value in entries:
            self.c.submit_proof(sender, value)

        self.assertEqual(len(self.c.submissions), 4)

        expected_values = [('dirk', 50), ('charlie', 122), ('alice', 123), ('bob', 300)]
        actual_values = self.c.correctly_sorted_values()
        self.assertEquals(expected_values, actual_values)

        self.assertEquals(122.5, schellingcoin.median(expected_values))


