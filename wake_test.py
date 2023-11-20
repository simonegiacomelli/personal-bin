import unittest

from wake import text_to_props


class TestTextToProps(unittest.TestCase):
    def test_text_to_props_with_properties(self):
        text = "property1=value1\nproperty2=value2"
        expected_result = {"property1": "value1", "property2": "value2"}
        self.assertEqual(text_to_props(text), expected_result)

    def test_text_to_props_with_blank_lines(self):
        text = "\nproperty1=value1\n\nproperty2=value2\n"
        expected_result = {"property1": "value1", "property2": "value2"}
        self.assertEqual(text_to_props(text), expected_result)


if __name__ == '__main__':
    unittest.main()
