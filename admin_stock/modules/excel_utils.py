import pandas as pd
from pathlib import Path

def export_to_excel(items):
    df = pd.DataFrame(items)
    download_dir = Path.home() / 'Downloads'
    file_path = download_dir / "inventory_export.xlsx"
    df.to_excel(file_path, index=False)
    print(f"Data exported to {file_path}")
