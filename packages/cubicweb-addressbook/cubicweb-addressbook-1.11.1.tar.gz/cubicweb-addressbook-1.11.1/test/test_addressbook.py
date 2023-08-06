import unittest
from cubicweb.devtools.testlib import AutomaticWebTest


class AddressbookAutomaticWebTest(AutomaticWebTest):

    def to_test_etypes(self):
        return set(('PhoneNumber', 'PostalAddress'))

    def list_startup_views(self):
        return ()


del AutomaticWebTest

if __name__ == '__main__':
    unittest.main()
