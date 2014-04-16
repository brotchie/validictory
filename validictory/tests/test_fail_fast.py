from unittest import TestCase

import validictory


class TestFailFast(TestCase):

    def test_multi_error(self):
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"}
            },
        }
        data = {"name": 2, "age": "fourty-two"}

        # ensure it raises an error
        self.assertRaises(validictory.ValidationError, validictory.validate,
                          data, schema, fail_fast=True)

        # ensure it raises a MultiError
        self.assertRaises(validictory.MultipleValidationError, validictory.validate,
                          data, schema, fail_fast=False)

        # ensure that the MultiError has 2 errors
        try:
            validictory.validate(data, schema, fail_fast=False)
        except validictory.MultipleValidationError as mve:
            assert len(mve.errors) == 2

    def test_multi_error_in_list(self):
        schema = {
            "type": "object",
            "properties": {
                "words": {"type": "array", "items": {"type": "string"}},
            },
        }
        data = {"words": ["word", 32, 2.1, True]}

        # ensure it raises an error
        self.assertRaises(validictory.ValidationError, validictory.validate,
                          data, schema, fail_fast=True)

        # ensure it raises a MultiError
        self.assertRaises(validictory.MultipleValidationError, validictory.validate,
                          data, schema, fail_fast=False)

        # ensure that the MultiError has 3 errors since 3 of the items were bad
        try:
            validictory.validate(data, schema, fail_fast=False)
        except validictory.MultipleValidationError as mve:
            assert len(mve.errors) == 3
