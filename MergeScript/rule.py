import os
import re
import shutil
import time
import requests
from concurrent.futures import ThreadPoolExecutor

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
]

RULES = {
        "fenliu": "https://raw.githubusercontent.com/fmz200/wool_scripts/main/QuantumultX/filter/fenliu.list",
        "Hijacking": "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Hijacking/Hijacking.list",
        "MyBlockAds": "https://raw.githubusercontent.com/RuCu6/QuanX/main/Rules/MyBlockAds.list",
}

HEADER = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
TYPES = "Surge"
file_paths = [TYPES + "/" + rule for rule in RULES.keys()]

def download_and_save_file(url, target_path):
    response = requests.get(url, headers=HEADER)
    if response.status_code == 200:
        with open(target_path, "wb") as f:
            f.write(response.content)
        time.sleep(1)

def apply_replacements(line):
    for pattern, replacement in replacements:
        line = re.sub(pattern, replacement, line)
    return line

def load_files(rules, folder):
    target_directory = os.path.join(TYPES, folder)
    os.makedirs(target_directory, exist_ok=True)

    with ThreadPoolExecutor() as executor:
        futures = []
        for rule_name, rule_url in rules.items():
            target_path = os.path.join(target_directory, f"{rule_name}.list")
            futures.append(executor.submit(download_and_save_file, rule_url, target_path))
        
        for future in futures:
            future.result()
        print(f"新文件已下载至：{target_directory}")

if __name__ == '__main__':
    for folder, rules in RULES.items():
        load_files(rules, folder)
    for path in file_paths:
        # 创建文件夹，如果文件夹不存在
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"创建目录 {path} 成功")
            
        # 下面是替换规则的代码
        for file_name in os.listdir(path):
            file_path = os.path.join(path, file_name)
            if os.path.isfile(file_path):
                with open(file_path, 'r', encoding='utf8') as in_f:
                    lines = [apply_replacements(line.strip()) for line in in_f.readlines()]
                with open(file_path, 'w', encoding='utf8') as out_f:
                    out_f.writelines(line + '\n' for line in lines)
                print(f"{file_name} 文件替换")
