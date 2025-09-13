import os
import re
import pytest

def test_final_report_file_content():
    path = os.path.join(os.path.dirname(__file__), '../notebooks/final_research_report.md')
    assert os.path.exists(path), "final_research_report.md does not exist!"
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    # Should not contain the raw prompt template or instructions
    assert '<Task>' not in content, "Report contains raw prompt instructions!"
    assert 'Your job is to use tools' not in content, "Report contains agent instructions!"
    # Should contain synthesized report structure
    assert content.startswith('# Final Research Report'), "Report does not start with expected header!"
    assert '## Research Brief' in content, "Report missing research brief section!"
    assert '## Findings' in content, "Report missing findings section!"

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
        assert before.endswith('\n\n') or idx == 0, f"No blank line before heading: {heading}"
        assert after.startswith('\n'), f"No blank line after heading: {heading}"

def test_final_report_trailing_newline():
    path = os.path.join(os.path.dirname(__file__), '../notebooks/final_research_report.md')
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    assert content.endswith('\n'), "Report does not end with a single newline!"
