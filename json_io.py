import json, os

def import_json(json_data:json):
    """Attempts to load a JSON file, and return as a dictionary."""
    try:
        is_file = os.path.isfile(json_data)
        if is_file == True:
            file_object = open(json_data)
            dict_from_json = json.load(file_object)
            file_object.close()
            return dict_from_json
        else:
            raise Exception("The file you attempted to load does not exist.")
    except OSError:
        print("OS Error during import_json(json_data) function.")

def export_json(dict_data:dict, file_path = '', file_name = 'data', extention = '.json', auto_rename=True, overwrite=True):
    """Attempts to save a JSON file from the provided dictionary."""
    full_file_name = str(file_name + extention)
    try:
        if overwrite == False:
            is_file = os.path.isfile(str(file_path + full_file_name))
            if is_file == True:
                if auto_rename == True:
                    is_still_file = True
                    count = 0
                    while is_still_file != False:
                        full_file_name = str(file_name + f"_{count}" + extention)
                        if os.path.isfile(str(file_path + full_file_name)) == False:
                            is_still_file = False
                            pass
                        else:
                            count += 1
                        if count > 1000:
                            raise Exception("The JSON file you attepted to export to already exists, & failed to rename.")
                else:
                    raise Exception("The JSON file you attepted to export to already exists")
        file_object = open(str(file_path + full_file_name), 'w+')
        json.dump(dict_data, file_object, indent = 4)
        file_object.close()
        print(f"JSON dump successful to '{str(file_path + full_file_name)}'")
    except OSError:
        print("OS Error during export_json(dict_data) function.")