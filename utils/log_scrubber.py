import regex as re

# List of regex patterns
regex_patterns = [
    r"[a-zA-Z0-9]{20,}",  # API keys
    r"[a-zA-Z0-9]{32}",  # MD5 hash
    r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b",  # IP addresses
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",  # Email addresses
    r"(?i)username\s*[:=]\s*.+",  # Usernames
    r"(?i)user\s*[:=]\s*.+",  # Usernames
    r"(?i)login\s*[:=]\s*.+",  # Logins
    r"(?i)apikey\s*[:=]\s*.+",  # API Keys
    r"(?i)secret\s*[:=]\s*.+",  # Secrets
    r"(?i)token\s*[:=]\s*.+",  # Tokens
    r"(?i)password\s*[:=]\s*.+",  # Passwords
    r"\b(?:mongodb|postgresql|mysql|mssql):\/\/[a-z0-9]+:[a-z0-9]+@[a-z0-9.]+:[0-9]+\/[a-z0-9]+\b",  # Database credentials
    r"\b(?:api|secret)_?(?:key|id)?\s*=\s*[a-z0-9]{20,}\b",  # API keys/secrets for other services
    r"\baccess_?token\s*=\s*[a-z0-9]{20,}\b",  # Access tokens
    # Add more patterns here as needed
]

# Compile the patterns
patterns = [re.compile(pattern, re.IGNORECASE) for pattern in regex_patterns]


def scrub_log(log: str) -> str:
    """
    Scrubs sensitive data from a log string.

    This function takes a log string as input and returns a scrubbed version of the log,
    where sensitive data such as API keys, MD5 hashes, IP addresses, email addresses,
    passwords, usernames, logins, API keys, secrets, and tokens are replaced with "***".

    Args:
        log (str): The log string to be scrubbed.

    Returns:
        str: The scrubbed log string.
    """
    scrubbed_log = log
    for pattern in patterns:
        scrubbed_log = pattern.sub("***", scrubbed_log)
    return scrubbed_log
