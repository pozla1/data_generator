import json


# Returns data loaded from given json file.
def load_from_json(filename):
    with open(filename, "r") as file:
        return json.load(file)


# Writes given data to given json file.
def write_to_json(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent="\t")


# Appends given data to given file.
def append_to_file(filename, data):
    with open(filename, "a") as file:
        file.write(str(data) + "\n")


# Returns an array of dictionaries from given xls file.
def xls_to_array_of_dicts(filename):
    import xlrd
    workbook = xlrd.open_workbook(filename)
    worksheet = workbook.sheet_by_index(0)
    header = []
    for column in range(worksheet.ncols):
        header.append(worksheet.cell_value(0, column))
    data = []
    for row in range(1, worksheet.nrows):
        element = {}
        for column in range(worksheet.ncols):
            element[header[column]] = worksheet.cell_value(row, column)
        data.append(element)
    return data
