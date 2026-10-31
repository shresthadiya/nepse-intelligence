import re


def normalize_text(text: str) -> str:
    """Normalize text for company-name matching."""
    text = (text or "").lower()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return " ".join(text.split())


def get_company_aliases(company):
    """Generate searchable company-name variations."""

    name = normalize_text(company.name)

    aliases = {name}

    # Remove common legal suffixes.
    suffixes = [
        " limited",
        " ltd",
        " company limited",
        " company",
    ]

    for suffix in suffixes:
        if name.endswith(suffix):
            aliases.add(name[:-len(suffix)].strip())

    return aliases


def find_company_matches(text: str, companies: list):
    """
    Identify companies mentioned in news text.

    Returns multiple company matches with confidence scores.
    """

    normalized_text = normalize_text(text)
    original_text = text or ""

    matches = []

    for company in companies:

        confidence = 0.0
        matched_terms = []

        # Match stock symbol using strict word boundaries.
        symbol_pattern = (
            r"(?<![A-Za-z0-9])"
            + re.escape(company.symbol)
            + r"(?![A-Za-z0-9])"
        )

        if re.search(symbol_pattern, original_text, re.IGNORECASE):
            confidence = 0.97
            matched_terms.append(company.symbol)

        # Match company names and aliases.
        for alias in get_company_aliases(company):

            if not alias:
                continue

            pattern = r"\b" + re.escape(alias) + r"\b"

            if re.search(pattern, normalized_text):
                matched_terms.append(alias)

                if alias == normalize_text(company.name):
                    confidence = max(confidence, 0.99)
                else:
                    confidence = max(confidence, 0.93)

        if confidence > 0:

            matches.append({
                "company_id": company.id,
                "company_name": company.name,
                "symbol": company.symbol,
                "confidence": confidence,
                "matched_terms": list(set(matched_terms))
            })

    return matches