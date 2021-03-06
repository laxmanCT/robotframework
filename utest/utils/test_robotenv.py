import unittest
import os

from robot.utils.asserts import assert_equals, assert_not_none, assert_none, assert_true
from robot.utils import (get_env_var, set_env_var, del_env_var, get_env_vars,
                         decode_from_system, encode_to_system)

TEST_VAR = 'TeST_EnV_vAR'
TEST_VAL = 'original value'
NON_ASCII_VAR = u'\xe4iti'
NON_ASCII_VAL = u'is\xe4'


class TestRobotEnv(unittest.TestCase):

    def setUp(self):
        os.environ[TEST_VAR] = TEST_VAL

    def tearDown(self):
        if TEST_VAR in os.environ:
            del os.environ[TEST_VAR]

    def test_get_env_var(self):
        assert_not_none(get_env_var('PATH'))
        assert_equals(get_env_var(TEST_VAR), TEST_VAL)
        assert_none(get_env_var('NoNeXiStInG'))
        assert_equals(get_env_var('NoNeXiStInG', 'default'), 'default')

    def test_set_env_var(self):
        set_env_var(TEST_VAR, 'new value')
        assert_equals(os.getenv(TEST_VAR), 'new value')

    def test_del_env_var(self):
        old = del_env_var(TEST_VAR)
        assert_none(os.getenv(TEST_VAR))
        assert_equals(old, TEST_VAL)
        assert_none(del_env_var(TEST_VAR))

    def test_get_set_del_non_ascii_vars(self):
        set_env_var(NON_ASCII_VAR, NON_ASCII_VAL)
        for k, v in os.environ.items():
            assert_true(isinstance(k, str) and isinstance(v, str))
        assert_equals(get_env_var(NON_ASCII_VAR), NON_ASCII_VAL)
        assert_equals(del_env_var(NON_ASCII_VAR), NON_ASCII_VAL)
        assert_none(get_env_var(NON_ASCII_VAR))

    def test_get_env_vars(self):
        set_env_var(NON_ASCII_VAR, NON_ASCII_VAL)
        vars = get_env_vars()
        assert_true('PATH' in vars)
        assert_equals(vars[self._upper_on_windows(TEST_VAR)], TEST_VAL)
        assert_equals(vars[self._upper_on_windows(NON_ASCII_VAR)], NON_ASCII_VAL)
        for k, v in vars.items():
            assert_true(isinstance(k, unicode) and isinstance(v, unicode))

    def _upper_on_windows(self, name):
        return name if os.sep == '/' else name.upper()


if __name__ == '__main__':
    unittest.main()
