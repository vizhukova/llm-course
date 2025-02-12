import openpyxl

def extract_data_from_excel(file_path, sheet_name=None):
    workbook = openpyxl.load_workbook(file_path, data_only=True)
    
    if sheet_name:
        sheet = workbook[sheet_name]
    else:
        sheet = workbook.active  # First sheet by default
    
    data = []
    headers = [cell.value for cell in sheet[1]]  # First row as headers
    
    for row in sheet.iter_rows(min_row=2, values_only=True):
        row_data = {headers[i]: row[i] for i in range(len(headers))}
        data.append(row_data)
    
    workbook.close()
    return data

def main():
    file_path = "./content/random_data.xlsx"
    extracted_data = extract_data_from_excel(file_path)
    for entry in extracted_data:
        print(entry)

if __name__ == "__main__":
    main() 