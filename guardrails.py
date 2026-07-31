import re

# Text patterns that suggest someone is trying to hijack the AI
INJECTION_PATTERNS = [
    r"ignore (all )?(previous|above) instructions",
    r"you are now",
    r"system prompt",
    r"disregard (the )?(above|previous)",
    r"new instructions?:",
    r"act as (if|a)",
    r"</?(system|instructions|prompt)>",
]

def scan_for_injection(text: str) -> dict:
    """Checks a chunk of retrieved document text for injection attempts."""
    findings = []
    lowered = text.lower()
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, lowered):
            findings.append(pattern)
    return {"safe": len(findings) == 0, "flagged_patterns": findings}

def sanitize_chunk(text: str) -> str:
    """Wraps retrieved text in tags so Claude treats it as reference data,
    not as commands to follow."""
    return f"<untrusted_document_content>\n{text}\n</untrusted_document_content>"
