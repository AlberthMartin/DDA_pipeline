import json

def generate_metadata(df, filename):

    metadata = {
        "file": filename,
        "rows": len(df),
        "columns": list(df.columns),
        "missing_values": int(df.isna().sum().sum())
    }

    return metadata


def save_metadata(metadata, path):

    with open(path, "w") as f:
        json.dump(metadata, f, indent=4)