"""
Unit tests for SarvamClient extraction and formatting.
"""

import json
from generator.sarvam_client import SarvamClient

def test_extract_json_direct():
    sample = '{"lesson_id": "1.3", "title": "Test"}'
    data = SarvamClient.extract_json(sample)
    assert data["lesson_id"] == "1.3"
    assert data["title"] == "Test"

def test_extract_json_from_markdown_fences():
    sample = """Here is the generated lesson:
```json
{
  "lesson_id": "1.3",
  "title": "Running Your First Python Program",
  "items": []
}
```
Hope this helps!"""
    data = SarvamClient.extract_json(sample)
    assert data["lesson_id"] == "1.3"
    assert data["title"] == "Running Your First Python Program"

def test_extract_json_embedded_braces():
    sample = """Some preamble text before
{"lesson_id": "1.4", "items": [1, 2, 3]}
and trailing remarks."""
    data = SarvamClient.extract_json(sample)
    assert data["lesson_id"] == "1.4"
    assert len(data["items"]) == 3
