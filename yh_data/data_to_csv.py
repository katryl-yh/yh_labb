import pandas as pd
from pathlib import Path

# Get the parent folder of the current script
parent_folder = Path(__file__).resolve().parent  

# Load the updated Excel file
file_path = parent_folder / "v7_YrkesCo.xlsx"
xls = pd.ExcelFile(file_path)

# Export each sheet as a CSV file in the parent folder
for sheet_name in xls.sheet_names:
    df = pd.read_excel(xls, sheet_name=sheet_name)
    output_file = parent_folder / f"{sheet_name}.csv"
    
    # Save CSV without BOM (Use encoding="utf-8" instead of "utf-8-sig")
    df.to_csv(output_file, index=False, encoding="utf-8")

print(f"CSV files have been saved in {parent_folder}")
