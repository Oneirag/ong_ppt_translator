from unittest import TestCase

from ong_ppt_translator.process_runs import parse_html_text


class Test(TestCase):
    def test_parse_markdown_back_to_runs(self):
        for (text, expectation) in [
            (
                    "data in <b>bold</b> and <b>again</b>",
                    [
                        {'text': 'data in ', 'bold': False, 'italic': False, 'underline': False},
                        {'text': 'bold', 'bold': True, 'italic': False, 'underline': False},
                        {'text': ' and ', 'bold': False, 'italic': False, 'underline': False},
                        {'text': 'again', 'bold': True, 'italic': False, 'underline': False},
                    ]
            ),
            (
                    "data",
                    [{'text': 'data', 'bold': False, 'italic': False, 'underline': False}]
            ),
            (
                    "<b>data</b>",
                    [{'text': 'data', 'bold': True, 'italic': False, 'underline': False}]
            ),
            (
                    "<b><i>data</i></b>",
                    [{'text': 'data', 'bold': True, 'italic': True, 'underline': False}]
            ),
            (
                    "<b><i><u>data</u></i></b>",
                    [{'text': 'data', 'bold': True, 'italic': True, 'underline': True}]
            ),

        ]:
            with self.subTest(text=text):
                parsed = parse_html_text(text)
                self.assertEqual(parsed, expectation,
                                 f"Failed to process {text}")
                pass
