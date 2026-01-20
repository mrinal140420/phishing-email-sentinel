from bs4 import BeautifulSoup
from typing import Dict, Any


def sanitize_html(html: str) -> Dict[str, Any]:
    """
    Sanitize HTML content by removing scripts and dangerous elements.

    Args:
        html (str): Raw HTML string.

    Returns:
        Dict[str, Any]: Sanitized HTML or error.
    """
    if not html:
        return {"sanitized_html": ""}

    try:
        soup = BeautifulSoup(html, 'html.parser')

        # Remove dangerous tags
        dangerous_tags = ['script', 'iframe', 'object', 'embed', 'form', 'input']
        for tag in dangerous_tags:
            for elem in soup.find_all(tag):
                elem.decompose()

        # Remove dangerous attributes
        dangerous_attrs = ['onclick', 'onload', 'onerror', 'onmouseover', 'javascript']
        for elem in soup.find_all(True):
            for attr in dangerous_attrs:
                if attr in elem.attrs:
                    del elem.attrs[attr]

        sanitized = str(soup)
        return {"sanitized_html": sanitized}
    except Exception as e:
        return {
            "error": {
                "type": "SANITIZATION_ERROR",
                "message": f"Failed to sanitize HTML: {str(e)}"
            }
        }