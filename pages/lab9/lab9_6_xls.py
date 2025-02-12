import pandas as pd

def extract_data_from_excel(file_path, sheet_name=None):
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    return df

def main():
    file_path = "./content/random_data.xlsx"  
    extracted_data = extract_data_from_excel(file_path)
    print(extracted_data)

if __name__ == "__main__":
    main() 