import re
import os  # Add this line
import requests
from git import Repo

# 正则表达式替换规则
replacements = [
    (r'\s+', ''),
    (r',no-resolve', ''),
    (r',(?:DIRECT$|direct$|REJECT$|reject$|PROXY$|proxy$)', ''),
    (r'-suffix', '-SUFFIX'),
    (r'-keyword', '-KEYWORD'),
    (r'ip-cidr', 'IP-CIDR'),
    (r'^(?:host|HOST)', 'DOMAIN'),
    (r'IP6-CIDR', 'IP-CIDR6'),
    (r'//.*', ''),
]

# 获取远程规则内容
remote_url = "https://raw.githubusercontent.com/fmz200/wool_scripts/main/QuantumultX/filter/fenliuxiuzheng.list"
remote_content = requests.get(remote_url).text

# 应用替换规则
for pattern, replacement in replacements:
    remote_content = re.sub(pattern, replacement, remote_content)

# 推送到本地仓库
local_path = "t"
repo = Repo(os.path.join("/github/workspace", local_path))

with open(os.path.join(local_path, "fenliuxiuzheng_modified.list"), "w") as file:
    file.write(remote_content)

repo.index.add([os.path.join(local_path, "fenliuxiuzheng_modified.list")])
repo.index.commit("Apply regex replacements to fenliuxiuzheng.list")
repo.remote().push()
