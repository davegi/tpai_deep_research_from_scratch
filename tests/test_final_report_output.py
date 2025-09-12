import os
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
