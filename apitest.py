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


def run_case(path):
    run_cmd = "hrun {} --failfast --log-level info".format(path)
    os.system(run_cmd)


import smtplib
from email.mime.text import MIMEText
from email.header import Header


def sent_mails():
    MAIL_HOST = "smtp.office365.com"
    SMTP_PORT = 587
    mail_user = "qa"
    mail_password = "test"

    try:
        server = smtplib.SMTP(MAIL_HOST, SMTP_PORT)
        server.starttls()

        server.login(mail_user, mail_password)
        me = mail_user

        msg = MIMEText("hello", 'text', 'utf-8')
        msg['From'] = me
        msg['To'] = "ming"
        msg['Subject'] = Header("hello", 'utf-8')
        server.sendmail(me, "ming", msg.as_string())
        server.close()
        print("pass")
        return True

    except Exception:
        print("fail")
        return False


# rewrite_file()

if __name__ == "__main__":

    check_folder(json_dir)
    extract_har(har_dir)
    source_json = [x for x in os.listdir(har_dir) if x.endswith('json')]
    if source_json:
        for source in source_json:
            rewrite_file(os.path.join(har_dir, source), os.path.join(json_dir, source))

    if is_json_exist:
        json_file = [x for x in os.listdir(json_dir) if x.endswith('json')]

        for source in json_file:
            run_case(os.path.join(json_dir, source))

    sent_mails()


