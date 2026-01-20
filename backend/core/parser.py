import re
import uuid
from datetime import datetime
from email import message_from_string
from email.header import decode_header
from typing import Dict, List, Optional, Any
from urllib.parse import urlparse


def parse_email(raw_email: str) -> Dict[str, Any]:
    """
    Parse an RFC 822 formatted email string into structured data.

    Args:
        raw_email (str): The raw email content as a string.

    Returns:
        Dict[str, Any]: Parsed email data or error information.
    """
    try:
        msg = message_from_string(raw_email)
    except Exception as e:
        return {
            "error": {
                "type": "PARSING_ERROR",
                "message": f"Failed to parse email: {str(e)}"
            }
        }

    # Generate UUID
    email_id = str(uuid.uuid4())

    # Parse headers
    headers = {}
    headers['from'] = _decode_header(msg.get('From', ''))
    headers['reply_to'] = _decode_header(msg.get('Reply-To')) if msg.get('Reply-To') else None
    headers['subject'] = _decode_header(msg.get('Subject', ''))

    # Received headers - collect all
    received = []
    for header in msg.get_all('Received', []):
        received.append(_decode_header(header))
    headers['received'] = received

    # Parse body
    plain_text, html = _extract_body(msg)

    # Extract URLs
    urls = _extract_urls(plain_text or '', html or '')

    # Metadata
    metadata = {
        "parsed_at": datetime.now().isoformat()
    }

    return {
        "email_id": email_id,
        "headers": headers,
        "body": {
            "plain_text": plain_text,
            "html": html
        },
        "urls": urls,
        "metadata": metadata
    }


def _decode_header(header: Optional[str]) -> str:
    """Decode email header to string."""
    if not header:
        return ''
    decoded_parts = decode_header(header)
    result = ''
    for part, encoding in decoded_parts:
        if isinstance(part, bytes):
            result += part.decode(encoding or 'utf-8', errors='ignore')
        else:
            result += str(part)
    return result


def _extract_body(msg) -> tuple[Optional[str], Optional[str]]:
    """Extract plain text and HTML body from email message."""
    plain_text = None
    html = None

    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == 'text/plain' and not plain_text:
                plain_text = part.get_payload(decode=True).decode('utf-8', errors='ignore')
            elif content_type == 'text/html' and not html:
                html = part.get_payload(decode=True).decode('utf-8', errors='ignore')
    else:
        content_type = msg.get_content_type()
        payload = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
        if content_type == 'text/plain':
            plain_text = payload
        elif content_type == 'text/html':
            html = payload
        else:
            # Fallback, assume plain text
            plain_text = payload

    return plain_text, html


def _extract_urls(plain_text: str, html: str) -> List[Dict[str, str]]:
    """Extract URLs from text using regex."""
    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    urls_found = set()

    # Find in plain text
    for match in re.finditer(url_pattern, plain_text):
        urls_found.add(match.group(0))

    # Find in HTML
    for match in re.finditer(url_pattern, html):
        urls_found.add(match.group(0))

    urls = []
    for url in urls_found:
        domain = urlparse(url).netloc
        if domain:
            urls.append({"url": url, "domain": domain})

    return urls