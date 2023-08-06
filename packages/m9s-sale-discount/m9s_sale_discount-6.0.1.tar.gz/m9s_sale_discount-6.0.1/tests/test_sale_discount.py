# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import doctest
import unittest

from trytond.tests.test_tryton import (
    ModuleTestCase, doctest_checker, doctest_teardown)
from trytond.tests.test_tryton import suite as test_suite


class SaleDiscountTestCase(ModuleTestCase):
    'Test Sale Discount module'
    module = 'sale_discount'
    #extras = [
    #    'gift_card',
    #    'sale_promotion',
    #    'sale_shipment_cost',
    #    'purchase_shipment_cost,'
    #    ]


def suite():
    suite = test_suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            SaleDiscountTestCase))
    suite.addTests(doctest.DocFileSuite(
            'scenario_sale_discount.rst',
            tearDown=doctest_teardown, encoding='utf-8',
            checker=doctest_checker,
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE))
    suite.addTests(doctest.DocFileSuite(
            'scenario_sale_promotion.rst',
            tearDown=doctest_teardown, encoding='utf-8',
            checker=doctest_checker,
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE))
    return suite
