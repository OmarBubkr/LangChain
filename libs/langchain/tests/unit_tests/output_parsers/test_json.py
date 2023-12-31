import pytest

from langchain.output_parsers.json import parse_json_markdown

GOOD_JSON = """```json
{
    "foo": "bar"
}
```"""

JSON_WITH_NEW_LINES = """

```json
{
    "foo": "bar"
}
```

"""

JSON_WITH_NEW_LINES_INSIDE = """```json
{

    "foo": "bar"

}
```"""

JSON_WITH_NEW_LINES_EVERYWHERE = """

```json

{

    "foo": "bar"

}

```

"""

TICKS_WITH_NEW_LINES_EVERYWHERE = """

```

{

    "foo": "bar"

}

```

"""

JSON_WITH_MARKDOWN_CODE_BLOCK = """```json
{
    "foo": "```bar```"
}
```"""

JSON_WITH_MARKDOWN_CODE_BLOCK_AND_NEWLINES = """```json
{
    "action": "Final Answer",
    "action_input": "```bar\n<div id="1" class=\"value\">\n\ttext\n</div>```"
}
```"""

JSON_WITH_UNESCAPED_QUOTES_IN_NESTED_JSON = """```json
{
    "action": "Final Answer",
    "action_input": "{"foo": "bar", "bar": "foo"}"
}
```"""

JSON_WITH_ESCAPED_QUOTES_IN_NESTED_JSON = """```json
{
    "action": "Final Answer",
    "action_input": "{\"foo\": \"bar\", \"bar\": \"foo\"}"
}
```"""

JSON_WITH_PYTHON_DICT = """```json
{
    "action": "Final Answer",
    "action_input": {"foo": "bar", "bar": "foo"}
}
```"""

JSON_WITH_ESCAPED_DOUBLE_QUOTES_IN_NESTED_JSON = """```json
{
    "action": "Final Answer",
    "action_input": "{\\"foo\\": \\"bar\\", \\"bar\\": \\"foo\\"}"
}
```"""

NO_TICKS = """{
    "foo": "bar"
}"""

NO_TICKS_WHITE_SPACE = """
{
    "foo": "bar"
}
"""

TEXT_BEFORE = """Thought: I need to use the search tool

Action:
```
{
  "foo": "bar"
}
```"""

TEXT_AFTER = """```
{
  "foo": "bar"
}
```
This should do the trick"""

TEXT_BEFORE_AND_AFTER = """Action: Testing

```
{
  "foo": "bar"
}
```
This should do the trick"""

TEST_CASES = [
    GOOD_JSON,
    JSON_WITH_NEW_LINES,
    JSON_WITH_NEW_LINES_INSIDE,
    JSON_WITH_NEW_LINES_EVERYWHERE,
    TICKS_WITH_NEW_LINES_EVERYWHERE,
    NO_TICKS,
    NO_TICKS_WHITE_SPACE,
    TEXT_BEFORE,
    TEXT_AFTER,
]


@pytest.mark.parametrize("json_string", TEST_CASES)
def test_parse_json(json_string: str) -> None:
    parsed = parse_json_markdown(json_string)
    assert parsed == {"foo": "bar"}


def test_parse_json_with_code_blocks() -> None:
    parsed = parse_json_markdown(JSON_WITH_MARKDOWN_CODE_BLOCK)
    assert parsed == {"foo": "```bar```"}

    parsed = parse_json_markdown(JSON_WITH_MARKDOWN_CODE_BLOCK_AND_NEWLINES)

    assert parsed == {
        "action": "Final Answer",
        "action_input": '```bar\n<div id="1" class="value">\n\ttext\n</div>```',
    }


TEST_CASES_ESCAPED_QUOTES = [
    JSON_WITH_UNESCAPED_QUOTES_IN_NESTED_JSON,
    JSON_WITH_ESCAPED_QUOTES_IN_NESTED_JSON,
    JSON_WITH_ESCAPED_DOUBLE_QUOTES_IN_NESTED_JSON,
]


@pytest.mark.parametrize("json_string", TEST_CASES_ESCAPED_QUOTES)
def test_parse_nested_json_with_escaped_quotes(json_string: str) -> None:
    parsed = parse_json_markdown(json_string)
    assert parsed == {
        "action": "Final Answer",
        "action_input": '{"foo": "bar", "bar": "foo"}',
    }


def test_parse_json_with_python_dict() -> None:
    parsed = parse_json_markdown(JSON_WITH_PYTHON_DICT)
    assert parsed == {
        "action": "Final Answer",
        "action_input": {"foo": "bar", "bar": "foo"},
    }
