def convert_file_to_list(filename):
    analysis_file = open(filename, "r")
    processed_data = []
    for entry in analysis_file.readlines():
        if entry[0] not in ("\n", "#"):
            processed_data.append(entry.split())
    return processed_data

def aggregate_data_lists(filenames):
    data = []
    for f in filenames:
        data.extend(convert_file_to_list(f))
    return data
