from bs4 import BeautifulSoup

def parse_html_text(html_text):
    """Receives a text with <b>, <i> and <u> tags and returns a list of dictionaries
    with each part of the text indicating if it is bold, italics or underline"""
    soup = BeautifulSoup(html_text, 'html.parser')
    result = []

    def extract_text(tag, bold=False, italic=False, underline=False):
        for element in tag.children:
            if isinstance(element, str):  # Plain text
                result.append({
                    'text': element,
                    'bold': bold,
                    'italic': italic,
                    'underline': underline
                })
            elif element.name in ['b', 'strong']:
                extract_text(element, bold=True, italic=italic, underline=underline)
            elif element.name in ['i', 'em']:
                extract_text(element, bold=bold, italic=True, underline=underline)
            elif element.name in ['u']:
                extract_text(element, bold=bold, italic=italic, underline=True)
            else:
                extract_text(element, bold=bold, italic=italic, underline=underline)

    extract_text(soup)
    return result


if __name__ == '__main__':
    for text in "<u><b>data</b></u>", "data", "<b>data</b>", "<u>data</u>", :
        # print(text, parse_markdown_back_to_runs(text))
        print(text, parse_html_text(text))

