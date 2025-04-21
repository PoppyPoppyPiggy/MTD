def categorize_strategy(strategy):
    if strategy == 'mtd':
        return "MTD"
    elif strategy == 'mtd+honey':
        return "MTD+Honeypot"
    elif strategy == 'mtd+honey+decoy':
        return "MTD+Honeypot+Decoy"
    return "Unknown"
