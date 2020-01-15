import json
import os
import re
import shutil

har_dir = '/Users/anderson/Documents/har_file'
json_dir = '/Users/anderson/Documents/json_file'


def check_folder(folder):
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.makedirs(folder)


def is_json_exist(path):
    if os.path.isfile(path) and path.endswith('json'):
        print("{file} exist".format(file=path))
        return True

    else:
        print("{file} does't exist".format(file=path))
        return False


def extract_har(source_path):
    if os.path.isdir(source_path):
        for d in os.listdir(source_path):
            if d.endswith("har"):
                cmd = "har2case {} ".format(os.path.join(source_path, d))
                print(cmd)
                os.system(cmd)

    if not os.listdir(source_path):
        print("no file exist, please check your source")


def rewrite_file(source_file, target_file):
    with open(source_file, 'r') as load_f:
        load_dict = json.load(load_f)

        load_dict["config"]["base_url"] = "http://mobilefirst.englishtown.cn"
        load_dict["config"]["verify"] = False
        value = {"userName": "stest70631", "password": "1"}
        (load_dict["config"]["variables"]).update(value)

        if "name" in load_dict["teststeps"][0]:
            load_dict["teststeps"][0]["extract"] = [
                {"token": "content.serviceResponse.token", "sessionId": "content.serviceResponse.sessionId"}]

        if "userName" and "password" in load_dict["teststeps"][0]["request"]["json"][
            "serviceRequest"]:
            load_dict["teststeps"][0]["request"]["json"]["serviceRequest"]["userName"] = "$userName"
            load_dict["teststeps"][0]["request"]["json"]["serviceRequest"]["password"] = "$password"

    for i in range(len(load_dict["teststeps"])):
        if "url" in load_dict["teststeps"][i]["request"]:
            load_dict["teststeps"][i]["request"]["url"] = re.sub("[a-zA-z]+://.*.(com|cn)", "",
                                                                 load_dict["teststeps"][i]["request"]["url"])

    str = json.dumps(load_dict)
    obj = re.compile(r'"sessionId": "(\w+)"')
    ret = obj.findall(str)
    for i in ret:
        str = str.replace(i, "$sessionId")

    obj = re.compile(r'"token": "(\w+)"')
    ret = obj.findall(str)
    for i in ret:
        str = str.replace(i, "$token")

    str = json.loads(str)

    with open(target_file, "w") as dump_f:
        json.dump(str, dump_f, indent=4)

import json

import yaml


class YAML():
    # Write YAML file
    def write_yml(self, save_path, data):
        with open(save_path, 'w', encoding='utf8') as outfile:
            try:
                yaml.safe_dump(data, outfile, default_flow_style=False, allow_unicode=True)
            except yaml.YAMLError as exc:
                print(exc)

                # Read YAML file

    def read_yml(self, load_path):
        with open(load_path, 'r') as stream:
            try:
                data_loaded = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
        return data_loaded




def add_checkpoint(target_file):
    file_path = "/Users/anderson/Documents/api.yml"
    yaml_file = YAML().read_yml(file_path)["oneapp"]

    json_file = open(target_file, "r")
    print(json_file)

    name_list = []
    for i, ele in enumerate(json_file["teststeps"]):
        name_list.append(ele["name"])

    for key in yaml_file.keys():
        if yaml_file[key]["api"] in name_list:
            index = name_list.index(yaml_file[key]["api"])

            if len(yaml_file[key]["eq"]):
                for checks in yaml_file[key]["eq"]:
                    (json_file["teststeps"][index]["validate"]).append({"eq": checks})

    json_file = json.dumps(json_file, indent=4)

    print(json_file)
    json_file.close()



def run_case(path):
    run_cmd = "hrun {} --failfast --log-level info".format(path)
    os.system(run_cmd)





# rewrite_file()

if __name__ == "__main__":

    check_folder(json_dir)
    extract_har(har_dir)
    source_json = [x for x in os.listdir(har_dir) if x.endswith('json')]
    if len(source_json):
        for source in source_json:
            rewrite_file(os.path.join(har_dir, source), os.path.join(json_dir, source))
        add_checkpoint(os.path.join(json_dir, source_json[0]))

    if is_json_exist:
        json_file = [x for x in os.listdir(json_dir) if x.endswith('json')]

        for source in json_file:
            run_case(os.path.join(json_dir, source))

    # sent_mails()

