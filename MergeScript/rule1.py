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
    "fenliu": "https://raw.githubusercontent.com/fmz200/wool_scripts/main/QuantumultX/filter/fenliu.list",
    "MyBlockAds": "https://raw.githubusercontent.com/limbopro/Adblock4limbo/main/Surge/rule/Adblock4limbo_surge.list",
    "MyRejectRule": "https://raw.githubusercontent.com/dler-io/Rules/main/Surge/Surge%203/Provider/Reject.list",
    "fenliuxiuzheng": "https://raw.githubusercontent.com/fmz200/wool_scripts/main/QuantumultX/filter/fenliuxiuzheng.list",
    "Block": "https://raw.githubusercontent.com/SouthAlley/z/main/Surge/G.list",
    "CorrectionRule": {
        "fenliuxiuzheng": "https://raw.githubusercontent.com/fmz200/wool_scripts/main/QuantumultX/filter/fenliuxiuzheng.list",
        "MyCorrectionRule": "https://raw.githubusercontent.com/GiveYou32Likes/Profile/main/QuantumultX/Rule/CorrectionRule.list",
    },
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

def process_string_rule(rule, folder):
    # 这里假设字符串规则是直接的URL，你可以根据实际情况进行修改
    target_path = os.path.join(TYPES, folder, f"{folder}.list")

    try:
        response = requests.get(rule, headers=HEADER)
        response.raise_for_status()  # 如果请求失败则抛出异常

        # 获取字符串内容并应用替换规则
        content = apply_replacements_to_line(response.text)

        # 保存修改后的内容
        with open(target_path, "w", encoding="utf8") as f:
            f.write(content)

        print(f"处理完成：{target_path}")
    except requests.exceptions.RequestException as e:
        print(f"处理字符串规则失败：{rule}, 错误：{e}")

def load_files(rules, folder):
    target_directory = os.path.join(TYPES, folder)
    os.makedirs(target_directory, exist_ok=True)

    with ThreadPoolExecutor() as executor:
        for rule_name, rule_value in rules.items():
            if isinstance(rule_value, str):
                # 如果值是字符串，直接下载并保存文件
                executor.submit(download_and_save_file, rule_value, os.path.join(target_directory, f"{rule_name}.list"))
                # 处理字符串规则
                process_string_rule(rule_value, folder)
            elif isinstance(rule_value, dict):
                # 如果值是字典，递归调用 load_files 处理子规则
                load_files(rule_value, os.path.join(folder, rule_name))

    # 其余部分保持不变
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
        if isinstance(rules, str):
            # 如果值是字符串，直接下载并保存文件
            download_and_save_file(rules, os.path.join(TYPES, f"{folder}.list"))
            # 处理字符串规则
            process_string_rule(rules, folder)
        elif isinstance(rules, dict):
            # 如果值是字典，递归调用 load_files 处理子规则
            load_files(rules, folder)

    for path in file_paths:
        # 创建文件夹，如果文件夹不存在
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"创建目录成功：{path}")

        # 在这里添加自定义逻辑，比如其他文件操作或处理
        # ...

        print(f"处理完成：{path}")
