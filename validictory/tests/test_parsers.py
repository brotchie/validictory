from unittest import TestCase
from datetime import datetime

import validictory

class TestParsers(TestCase):
    def test_parser(self):
        schema = {
          "type": "object",
          "properties": {
            "birthday": {
              "type": "string",
              "format": "date"
            }
          }
        }

        def parse_date(validator, fieldname, value, format_option):
            return datetime.strptime(value, "%Y-%m-%d")

        x = {"birthday": "2015-01-01"}
        validictory.validate(x, schema, format_parsers={'date': parse_date})

        self.assertEqual(x['birthday'], datetime(2015, 1, 1))
