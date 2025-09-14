import os
import re
import pytest

def test_final_report_file_content():
    path = os.path.join(os.path.dirname(__file__), '../notebooks/final_research_report.md')
    from assertpy import assert_that
    assert_that(os.path.exists(path), description="final_research_report.md should exist").is_true()
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    # Should not contain the raw prompt template or instructions
    assert_that(content, description="Report should not contain raw prompt instructions").does_not_contain('<Task>')
    assert_that(content, description="Report should not contain agent instructions").does_not_contain('Your job is to use tools')
    # Should contain synthesized report structure
    assert_that(content, description="Report should start with expected header").starts_with('# Final Research Report')
    assert_that(content, description="Report should contain research brief section").contains('## Research Brief')
    assert_that(content, description="Report should contain findings section").contains('## Findings')

def test_final_report_blank_lines():
    path = os.path.join(os.path.dirname(__file__), '../notebooks/final_research_report.md')
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    # Check for exactly one blank line before and after headings
    headings = re.findall(r'(^#+ .+$)', content, re.MULTILINE)
    for heading in headings:
        idx = content.index(heading)
        before = content[:idx]
        after = content[idx+len(heading):]
    from assertpy import assert_that
    assert_that(before.endswith('\n\n') or idx == 0, description=f"No blank line before heading: {heading}").is_true()
    assert_that(after.startswith('\n'), description=f"No blank line after heading: {heading}").is_true()

def test_final_report_trailing_newline():
    path = os.path.join(os.path.dirname(__file__), '../notebooks/final_research_report.md')
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    from assertpy import assert_that
    assert_that(content.endswith('\n'), description="Report should end with a single newline").is_true()
