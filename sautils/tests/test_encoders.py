from datetime import datetime
from datetime import timedelta
import json
import unittest

from sautils.encoders import DateTimeEncoder


class TestDefault(unittest.TestCase):

    def test_is_datetime(self):
        """Ensure that if a datetime object is passed, the stringified version
        of that datetime is returned.
        """

        a_datetime = datetime(1, 1, 1)

        actual = json.dumps(a_datetime, cls=DateTimeEncoder)

        self.assertEqual(json.dumps(str(a_datetime)), actual)

    def test_is_timedelta(self):
        """Ensure that if a timedelta object is passed, the stringified version
        of that timedelta is returned.
        """

        a_timedelta = timedelta(1, 1)

        actual = json.dumps(a_timedelta, cls=DateTimeEncoder)

        self.assertEqual(json.dumps(str(a_timedelta)), actual)

    def test_not_datetime_or_timedelta(self):
        """Ensure that if an object other than datetime or timedelta is passed,
        a TypeError is raised.
        """

        an_object = 'name'

        encoder = DateTimeEncoder()

        self.assertRaises(TypeError, encoder.default, an_object)

