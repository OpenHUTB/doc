"""
Extract code blocks from markdown files
"""
import re
from typing import TextIO, Callable
import os


class RunMethods:
    """Functions that receive a block of code and "run" it somehow"""

    EXECUTE = lambda block: exec(block)


def run_code_from_markdown_blocks(
    blocks: list[str], method: Callable[[str], None] = RunMethods.EXECUTE
) -> None:
    """Executes code from extracted blocks (use output from `get_code_from_markdown`)"""
    for block in blocks:
        method(block)


def get_code_from_markdown(lines: list[str], *, language: str = "python") -> list[str]:
    """Outputs extracted code blocks from a list of strings of markdown text"""
    regex = re.compile(
        r"(?P<start>^```(?P<block_language>(\w|-)+)\n)(?P<code>.*?\n)(?P<end>```)",
        re.DOTALL | re.MULTILINE,
    )
    blocks = [
        (match.group("block_language"), match.group("code"))
        for match in regex.finditer("".join(lines))
    ]
    return [block for block_language, block in blocks if block_language == language]


def get_code_from_markdown_file(markdown_file: TextIO, **kwargs) -> list[str]:
    """Calls `get_code_from_markdown` after getting lines from the open file"""
    lines = [line for line in markdown_file]
    return get_code_from_markdown(lines, **kwargs)


def get_code_from_markdown_filename(markdown_filename: str, **kwargs) -> list[str]:
    """Calls `get_code_from_markdown_file` after opening file using the given filename"""
    with open(markdown_filename, "r") as f:
        return get_code_from_markdown_file(f, **kwargs)
