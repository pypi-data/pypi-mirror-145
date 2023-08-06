import os
import json
import yaml
import dhall

class FileParser:
    """
    Parses files dhall, json, and yaml configuration files for oompa
    inputs:
      path (optional): Path to where configuration exists. Defaults to ./
      file (optional): Configuration file name. Defaults to builder.dhall
    """
    def __init__(self, path = os.getcwd(), file = "builder.dhall"):
        self.path = path
        self.file = file
        self.format = "DHALL"


    def set_file(self, file):
        print(f"Using file {file}")
        file_name_len = len(file)
        self.file = file
        if file[file_name_len-6:] == ".dhall":
            self.format = "DHALL"
        elif (file[file_name_len-5:] == ".yaml" or file[file_name_len-4:] == ".yml"):
            self.format = "YAML"
        elif file[file_name_len-5:] == ".json":
            self.format = "JSON"
        else:
            raise ValueError(f"Unacceptable file format {file}. Acceptable formats are: .dhall, .yml, .yaml, .json")

    def set_path(self,path):
        isabs = os.path.isabs(path)
        if isabs:
            self.path = path
        else:
            self.path = os.getcwd() + "/" + path

    def parse_file(self):
        if self.format == "DHALL":
            with open(self.path + "/" + self.file, 'r', encoding='utf-8') as config_file:
                config = dhall.load(config_file)
        elif self.format == "YAML":
            with open(self.path + "/" + self.file, 'r', encoding='utf-8') as config_file:
                config = yaml.safe_load(config_file)
        elif self.format == "JSON":
            with open(self.path + "/" + self.file, 'r', encoding='utf-8') as config_file:
                config = json.load(config_file)
        return config
