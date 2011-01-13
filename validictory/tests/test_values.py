"""
    Tests that test the value of individual items
"""

from unittest import TestCase

import validictory


class TestEnum(TestCase):
    schema = {"enum":["test", True, 123, ["???"]]}

    def test_enum_pass(self):
        data = ["test", True, 123, ["???"]]
        try:
            for item in data:
                validictory.validate(item, self.schema)
        except ValueError, e:
            self.fail("Unexpected failure: %s" % e)

    def test_enum_fail(self):
        data = "unknown"

        self.assertRaises(ValueError, validictory.validate, data, self.schema)


class TestPattern(TestCase):

    # match simplified regular expression for an e-mail address
    schema = {"pattern":
              "^[A-Za-z0-9][A-Za-z0-9\.]*@([A-Za-z0-9]+\.)+[A-Za-z0-9]+$"}

    def test_pattern_pass(self):
        data = "my.email01@gmail.com"

        try:
            validictory.validate(data, self.schema)
        except ValueError, e:
            self.fail("Unexpected failure: %s" % e)

    def test_pattern_pass_nonstring(self):
        data = 123

        try:
            validictory.validate(data, self.schema)
        except ValueError, e:
            self.fail("Unexpected failure: %s" % e)

    def test_pattern_fail(self):
        data = "whatever"

        self.assertRaises(ValueError, validictory.validate, data, self.schema)

class TestFormat(TestCase):

    schema_datetime =    {"format": "date-time"}
    schema_date =        {"format": "date"}
    schema_time =        {"format": "time"}
    schema_utcmillisec = {"format": "utc-millisec"}

    def test_format_datetime_pass(self):
        data = "2011-01-13T10:56:53Z"

        try:
            validictory.validate(data, self.schema_datetime)
        except ValueError, e:
            self.fail("Unexpected failure: %s" % e)

    def test_format_date_pass(self):
        data = "2011-01-13"

        try:
            validictory.validate(data, self.schema_date)
        except ValueError, e:
            self.fail("Unexpected failure: %s" % e)

    def test_format_time_pass(self):
        data = "10:56:53"

        try:
            validictory.validate(data, self.schema_time)
        except ValueError, e:
            self.fail("Unexpected failure: %s" % e)

    def test_format_utcmillisec_pass(self):
        data = 1294915735

        try:
            validictory.validate(data, self.schema_utcmillisec)
        except ValueError, e:
            self.fail("Unexpected failure: %s" % e)


    def test_format_datetime_nonexisting_day_fail(self):
        data = "2013-13-13T00:00:00Z"

        self.assertRaises(ValueError, validictory.validate, data, self.schema_datetime)

    def test_format_datetime_feb29_fail(self):
        data = "2011-02-29T00:00:00Z"

        self.assertRaises(ValueError, validictory.validate, data, self.schema_datetime)

    def test_format_datetime_notutc_fail(self):
        data = "2011-01-13T10:56:53+01:00"

        self.assertRaises(ValueError, validictory.validate, data, self.schema_datetime)

    def test_format_datetime_fail(self):
        data = "whatever"
        self.assertRaises(ValueError, validictory.validate, data, self.schema_datetime)

    def test_format_date_fail(self):
        data = "whatever"
        self.assertRaises(ValueError, validictory.validate, data, self.schema_date)

    def test_format_time_fail(self):
        data = "whatever"
        self.assertRaises(ValueError, validictory.validate, data, self.schema_time)

    def test_format_utcmillisec_fail(self):
        data = "whatever"
        self.assertRaises(ValueError, validictory.validate, data, self.schema_utcmillisec)

    def test_format_utcmillisec_negative_fail(self):
        data = -1
        self.assertRaises(ValueError, validictory.validate, data, self.schema_utcmillisec)


class TestUniqueItems(TestCase):

    schema = {"uniqueItems": True}
    schema_false = {"uniqueItems": False}

    def test_uniqueitems_pass(self):
        data = [1,2,3]

        try:
            validictory.validate(data, self.schema)
        except ValueError, e:
            self.fail("Unexpected failure: %s" % e)

    def test_uniqueitems_pass_string(self):
        data = ['1', '2', '3']

        try:
            validictory.validate(data, self.schema)
        except ValueError, e:
            self.fail("Unexpected failure: %s" % e)

    def test_uniqueitems_pass_nested_array(self):
        '''
        uniqueItems only applies for the array it was specified on and not to
        all datastructures nested within.
        '''
        data = [[1, [5, 5]], [2, [5, 5]]]

        try:
            validictory.validate(data, self.schema)
        except ValueError, e:
            self.fail("Unexpected failure: %s" % e)

    def test_uniqueitems_pass_different_types(self):
        data = [1, "1"]

        try:
            validictory.validate(data, self.schema)
        except ValueError, e:
            self.fail("Unexpected failure: %s" % e)

    def test_uniqueitems_false_pass(self):
        data = [1, 1, 1]

        try:
            validictory.validate(data, self.schema_false)
        except ValueError, e:
            self.fail("Unexpected failure: %s" % e)

    def test_uniqueitems_fail(self):
        data = [1, 1, 1]

        self.assertRaises(ValueError, validictory.validate, data, self.schema)

    def test_uniqueitems_fail_nested_arrays(self):
        data = [[1,2,3], [1,2,3]]

        self.assertRaises(ValueError, validictory.validate, data, self.schema)

    def test_uniqueitems_fail_nested_objects(self):
        data = [{'one': 1, 'two': 2}, {'one': 1, 'two': 2}]

        self.assertRaises(ValueError, validictory.validate, data, self.schema)

    def test_uniqueitems_fail_null(self):
        data = [None, None]

        self.assertRaises(ValueError, validictory.validate, data, self.schema)


class TestMaximum(TestCase):
    props = {
        "prop01": { "type":"number", "maximum":10 },
        "prop02": { "type":"integer", "maximum":20 }
    }
    schema = {"type": "object", "properties":props}

    def test_maximum_pass(self):
        #Test less than
        data1 = { "prop01": 5, "prop02": 10 }
        #Test equal
        data2 = { "prop01": 10, "prop02": 20 }

        try:
            validictory.validate(data1, self.schema)
            validictory.validate(data2, self.schema)
        except ValueError, e:
            self.fail("Unexpected failure: %s" % e)

    def test_maximum_fail(self):
        #Test number
        data1 = { "prop01": 11, "prop02": 19 }
        #Test integer
        data2 = { "prop01": 9, "prop02": 21 }

        self.assertRaises(ValueError, validictory.validate, data1, self.schema)
        self.assertRaises(ValueError, validictory.validate, data2, self.schema)


class TestMinimum(TestCase):
    props = {
        "prop01": { "type":"number", "minimum":10 },
        "prop02": { "type":"integer", "minimum":20 }
    }
    schema = {"type": "object", "properties":props}

    def test_minimum_pass(self):
        #Test greater than
        data1 = { "prop01": 21, "prop02": 21 }
        #Test equal
        data2 = { "prop01": 10, "prop02": 20 }

        try:
            validictory.validate(data1, self.schema)
            validictory.validate(data2, self.schema)
        except ValueError, e:
            self.fail("Unexpected failure: %s" % e)

    def test_minumum_fail(self):
        #Test number
        data1 = { "prop01": 9, "prop02": 21 }
        #Test integer
        data2 = { "prop01": 10, "prop02": 19 }

        self.assertRaises(ValueError, validictory.validate, data1, self.schema)
        self.assertRaises(ValueError, validictory.validate, data2, self.schema)


class TestMinLength(TestCase):
    schema = { "minLength": 4 }

    def test_minLength_pass(self):
        # str-equal, str-gt, list-equal, list-gt
        data = ['test', 'string', [1,2,3,4], [0,0,0,0,0]]

        try:
            for item in data:
                validictory.validate(item, self.schema)
        except ValueError, e:
            self.fail("Unexpected failure: %s" % e)

    def test_minLength_pass_nonstring(self):
        #test when data is not a string
        data1 = 123

        try:
            validictory.validate(data1, self.schema)
        except ValueError, e:
            self.fail("Unexpected failure: %s" % e)

    def test_minLength_fail(self):
        #test equal
        data = ["car", [1,2,3]]

        for item in data:
            self.assertRaises(ValueError, validictory.validate, data,
                              self.schema)


class TestMaxLength(TestCase):
    schema = { "maxLength": 4 }

    def test_maxLength_pass(self):
        # str-equal, str-lt, list-equal, list-lt
        data = ["test", "car", [1,2,3,4], [0,0,0]]
        try:
            for item in data:
                validictory.validate(item, self.schema)
        except ValueError, e:
            self.fail("Unexpected failure: %s" % e)

    def test_maxLength_pass_nonstring(self):
        # test when data is not a string
        data1 = 12345

        try:
            validictory.validate(data1, self.schema)
        except ValueError, e:
            self.fail("Unexpected failure: %s" % e)

    def test_maxLength_fail(self):
        data = ["string", [1,2,3,4,5]]
        for item in data:
            self.assertRaises(ValueError, validictory.validate, item,
                              self.schema)


class TestBlank(TestCase):

    def test_blank_default(self):
        try:
            validictory.validate("test", {})
        except ValueError, e:
            self.fail("Unexpected failure: %s" % e)

        self.assertRaises(ValueError, validictory.validate, "", {})

    def test_blank_false(self):
        schema = {"blank":False}
        try:
            validictory.validate("test", schema)
        except ValueError, e:
            self.fail("Unexpected failure: %s" % e)

        self.assertRaises(ValueError, validictory.validate, "", schema)

    def test_blank_true(self):
        try:
            validictory.validate("", {"blank":True})
            validictory.validate("test", {"blank":True})
        except ValueError, e:
            self.fail("Unexpected failure: %s" % e)