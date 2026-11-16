import re
from datetime import datetime

# 页面中的全局变量写法：{{ 变量名 }}
VARIABLE_PATTERN = re.compile(r'\{\{\s*([A-Za-z0-9_]+)\s*\}\}')


def on_config(config, **kwargs):
    year = str(datetime.now().year)
    config.copyright = config.copyright.format(year=year)


def replace_variables(markdown, variables):
    """把 Markdown 中的 {{ 变量名 }} 替换为 mkdocs.yml 中定义的值。

    代码块（``` / ~~~ 围起来的部分）保持原样，避免文档里的
    GitHub Actions 表达式等被误替换。
    """
    lines = []
    in_code_block = False
    for line in markdown.splitlines(keepends=True):
        if line.lstrip().startswith(('```', '~~~')):
            in_code_block = not in_code_block
            lines.append(line)
            continue
        if not in_code_block:
            line = VARIABLE_PATTERN.sub(
                lambda match: str(variables.get(match.group(1), match.group(0))),
                line)
        lines.append(line)
    return ''.join(lines)


def on_page_markdown(markdown, config, **kwargs):
    variables = config.get('extra', {}).get('variables', {})
    if variables:
        markdown = replace_variables(markdown, variables)
    return markdown
