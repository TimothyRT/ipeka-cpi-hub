import gdown

import os
import pathlib
import requests
import shutil


def download_drive_folder(link: str, directory: str):
    print(f">> Downloading from {link}")
    try:
        shutil.rmtree(directory)
    except:
        pass
    finally:
        output_list = gdown.download_folder(link)
        possible_folder = pathlib.Path(str(output_list[0]))
        while True:
            if possible_folder.parent.name != "api-employee-photos":
                possible_folder = pathlib.Path(possible_folder.parent)
            else:
                break
        folder = possible_folder
        shutil.move(folder, directory)
        
        
def download_gsheet(link: str, directory: str, file_name: str, file_extension: str):
    try:
        shutil.rmtree(directory)
    except:
        pass
    else:
        os.mkdir(directory)
    finally:        
        # Parse URL
        _link: list[str] = link.split("/")
        if "spreadsheets" not in _link:
            return {
                "ok": False,
                "details": "Not a Google Sheets link!"
            }
        
        id = ""
        for i in range(len(_link)):
            if _link[i] == "spreadsheets":
                try:
                    id = _link[i + 2]
                except IndexError:
                    return {
                        "ok": False,
                        "details": "Link is seemingly broken."
                    }
        
        if not id:
            return {
                "ok": False,
                "details": "Link is seemingly broken."
            }
        else:
            excel_response = requests.get("https://docs.google.com/spreadsheets/d/" + id + "/export?format=" + file_extension)
            if excel_response.ok and excel_response.status_code == 200:
                with open(os.path.join(directory, f"{file_name}.{file_extension}"), mode="wb") as file:
                    file.write(excel_response.content)
                return {
                    'ok': True,
                    'details': "Item succesfully downloaded!"
                }
            else:
                return {
                    'ok': False,
                    'details': f"Request failed with status code {excel_response.status_code}."
                }


if __name__ == "__main__":
    download_drive_folder(
        link="https://drive.google.com/drive/folders/1ZiiYq3aQudiNY6jyh7Uf0L1RyDKY8i-h",
        directory="static/images/downloaded/employees"
    )
    
    # download_gsheet(
    #     link="https://docs.google.com/spreadsheets/d/1EWSXZHYrLl0wyzE4vsFdNru61rrgyN8pNDCwvTgFeo8",
    #     directory="static/gsheet",
    #     file_name="employee",
    #     file_extension="xlsx"
    # )
