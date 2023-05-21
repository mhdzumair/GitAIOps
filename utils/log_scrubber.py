import re


def scrub_log(log):
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
