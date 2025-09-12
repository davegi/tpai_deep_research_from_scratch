#!/usr/bin/env python
"""Generate the final_research_report.md used by tests.

This script mirrors the notebook logic but runs deterministically so CI/tests
can regenerate the artifact after template or MockLLM changes.
"""
import re
import asyncio
from datetime import date
from research_agent_framework.prompts import renderer
from research_agent_framework.llm.client import MockLLM, LLMConfig


def sanitize(text: str) -> str:
    # Remove angle-bracketed instruction fragments like <Task>...</>
    out = re.sub(r"<[^>]+>", "", text)
    out = re.sub(r"\n{3,}", "\n\n", out)
    return out.strip()


def main():
    report_metadata = {
        'date': date.today().isoformat(),
        'research_brief': 'Find the best coffee shops in SF with no cover charge, open now, highest ratings in SOMA.',
        'findings': [
            'Blue Bottle Coffee: 4.7 stars, open now, free WiFi, no cover charge.',
            'Sightglass Coffee: 4.6 stars, open now, SOMA location, no cover charge.',
            'Verve Coffee: 4.5 stars, open now, SOMA, no cover charge.'
        ],
        'sources': []
    }

    prompt = renderer.render_template('final_report_generation_prompt.j2', report_metadata)
    print('--- Rendered prompt preview ---')
    print(prompt)
    print('--- End preview ---')

    sanitized = sanitize(prompt)
    print('--- Sanitized prompt preview ---')
    print(sanitized)
    print('--- End sanitized preview ---')

    llm = MockLLM(LLMConfig(api_key='test', model='mock-model'))
    final = asyncio.run(llm.generate(sanitized))

    # The MockLLM returns a canonical echo for most prompts: "mock response for: {prompt}"
    # Some tests expect the file to start with the report header. If MockLLM returned
    # an echoed prompt, strip that prefix so the artifact contains the rendered report.
    if isinstance(final, str) and final.startswith('mock response for:'):
        # remove the prefix and any leading whitespace/newlines
        final = final[len('mock response for:'):].lstrip()

    # Ensure file ends with a single newline and headings have surrounding blank lines
    final = re.sub(r"\n{3,}", "\n\n", final).strip() + "\n"

    out_path = 'notebooks/final_research_report.md'
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(final)

    print(f'Wrote {out_path}')


if __name__ == '__main__':
    main()
