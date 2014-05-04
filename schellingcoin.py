#!/usr/bin/env python

import hashlib
import operator
import sys

if sys.version_info < (3, 4):
   import sha3

def hash_sender_value(sender, value):
    s = hashlib.sha3_512()
    s.update(str(sender))
    s.update(str(value))
    return s.hexdigest()

def median(mylist):
    length = len(mylist)
    if not length % 2:
        return (mylist[length / 2][1] + mylist[length / 2 - 1][1]) / 2.0
    return mylist[length / 2][1]


class Submission(object):

    def __init__(self, sender, hash):
        self.sender = sender
        self.hash = hash
        self.value = None

    def is_complete(self):
        return self.hash is not None and self.value is not None

    def is_valid(self):
        return self.hash == hash_sender_value(self.sender, self.value)


class SchellingCoin(object):

    def __init__(self, block=0):
        self.block = block
        self.submissions = {}

    def increment_block(self):
        self.block += 1

    def can_submit_hash(self):
        return self.block % 2 == 0

    def can_submit_proof(self):
        return self.block % 2 == 1

    def submit_hash(self, sender, hash):
        if not self.can_submit_hash():
            raise RuntimeError("Can't submit hash this block")

        if sender in self.submissions:
            raise RuntimeError("Already submitted")

        self.submissions[sender] = Submission(sender, hash)

    def submit_proof(self, sender, value):
        if not self.can_submit_proof():
            raise RuntimeError("Can't submit proof this block")

        if sender not in self.submissions:
            raise RuntimeError("No hash submitted")

        submission = self.submissions[sender]
        submission.value = value

    def correctly_sorted_values(self):
        return sorted([(submission.sender, submission.value)
                       for submission in self.submissions.values()
                       if submission.is_valid()],
                key=operator.itemgetter(1))
