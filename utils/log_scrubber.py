import re


def scrub_log(log):
    """
    Scrubs sensitive information from a log string.

    Uses regular expressions to identify patterns that may correspond to sensitive information,
    such as API keys, IP addresses, email addresses, and passwords.
    When it finds a match, it replaces the sensitive information with asterisks (***).

    Args:
        log (str): The log string to be scrubbed.

    Returns:
        str: The scrubbed log string.
    """
    # Patterns for different types of sensitive information
    patterns = [
        r"[a-zA-Z0-9]{20,}",  # API keys
        r"[a-zA-Z0-9]{32}",  # MD5 hash
        r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b",  # IP addresses
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",  # Email addresses
        r"(?i)password\s*=\s*.+",  # Passwords
        r"(?i)username\s*=\s*.+",  # Usernames
        r"(?i)user\s*=\s*.+",  # Usernames
        r"(?i)login\s*=\s*.+",  # Logins
        r"(?i)apikey\s*=\s*.+",  # API Keys
        r"(?i)secret\s*=\s*.+",  # Secrets
        r"(?i)token\s*=\s*.+",  # Tokens
        # Add more patterns here as needed
    ]

    scrubbed_log = log
    for pattern in patterns:
        scrubbed_log = re.sub(pattern, "***", scrubbed_log, flags=re.IGNORECASE)

    return scrubbed_log
