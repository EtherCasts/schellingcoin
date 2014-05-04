from sniffer.api import runnable

#
# Custom configuration for sniffer to use unittest.discover
# http://pypi.python.org/pypi/sniffer/
#

@runnable
def execute_discover(*args):
    import unittest
    suite = unittest.defaultTestLoader.discover(start_dir='test')
    result = unittest.TextTestRunner().run(suite)
    return result.wasSuccessful()
