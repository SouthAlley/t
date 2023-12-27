import os
import re
import time
import requests
from concurrent.futures import ThreadPoolExecutor

# 正则表达式替换规则
replacements = [
    (r', ', ','),
    (r'([^,]*,[^,]*),.*', r'\1'),
    (r'ip-cidr,', 'IP-CIDR,'),
    (r'(?i)host,', 'DOMAIN,'),
    (r'(?i)host-wildcard,[^,]*', ''),
    (r'(?i)ip6-cidr,', 'IP-CIDR6,'),
    (r'(?i)host-keyword,', 'DOMAIN-KEYWORD,'),
    (r'(?i)host-suffix,', 'DOMAIN-SUFFIX,'),
    (r'(IP-CIDR[6]{0,1},[^,]*)', r'\1,no-resolve'),
    (r'//.*', ''),
]

RULES = {
    "CorrectionRule": {"https://raw.githubusercontent.com/fmz200/wool_scripts/main/QuantumultX/filter/fenliuxiuzheng.list",
    },
    "RejectRule": {
        "fenliu": "https://raw.githubusercontent.com/fmz200/wool_scripts/main/QuantumultX/filter/fenliu.list",
        "MyBlockAds": "https://raw.githubusercontent.com/limbopro/Adblock4limbo/main/Surge/rule/Adblock4limbo_surge.list",
        "MyRejectRule": "https://raw.githubusercontent.com/dler-io/Rules/main/Surge/Surge%203/Provider/Reject.list",
        "Block": "https://raw.githubusercontent.com/SouthAlley/z/main/Surge/G.list",
    }
}

HEADER = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
TYPES = "Surge"
file_paths = [os.path.join(TYPES, folder) for folder in RULES.keys()]

def download_and_save_file(url, target_path):
    try:
        response = requests.get(url, headers=HEADER)
        response.raise_for_status()  # 抛出异常如果请求失败
        with open(target_path, "wb") as f:
            f.write(response.content)
    except requests.exceptions.RequestException as e:
        print(f"下载文件失败：{url}, 错误：{e}")

def apply_replacements(lines):
    return [apply_replacements_to_line(line) for line in lines]

def apply_replacements_to_line(line):
    for pattern, replacement in replacements:
        line = re.sub(pattern, replacement, line)
    return line

def load_files(rules, folder):
    target_directory = os.path.join(TYPES, folder)
    os.makedirs(target_directory, exist_ok=True)

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(download_and_save_file, rule_url, os.path.join(target_directory, f"{rule_name}.list")) for rule_name, rule_url in rules.items()]
        for future in futures:
            future.result()

    # 读取并应用替换规则
    for rule_name in rules.keys():
        path = os.path.join(target_directory, f"{rule_name}.list")
        try:
            with open(path, 'r', encoding='utf8') as file:
                lines = [line.strip() for line in file.readlines()]
            
            # 应用替换规则
            modified_lines = apply_replacements(lines)

            # 保存修改后的内容
            with open(path, 'w', encoding='utf8') as file:
                file.write('\n'.join(modified_lines))

            print(f"文件处理完成：{path}")
        except Exception as e:
            print(f"处理文件时出现错误：{path}, 错误：{e}")

if __name__ == '__main__':
    for folder, rules in RULES.items():
        load_files(rules, folder)
    
    for path in file_paths:
        # 创建文件夹，如果文件夹不存在
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"创建目录成功：{path}")
        
        # 在这里添加自定义逻辑，比如其他文件操作或处理
        # ...

        print(f"处理完成：{path}")
