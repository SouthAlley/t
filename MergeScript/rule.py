import os
import re
import requests

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
    "fenliu": {
        "url": "https://raw.githubusercontent.com/fmz200/wool_scripts/main/QuantumultX/filter/fenliu.list",
    },
    "MyBlockAds": {
        "url": "https://raw.githubusercontent.com/limbopro/Adblock4limbo/main/Surge/rule/Adblock4limbo_surge.list",
    },
    "MyRejectRule": {
        "url": "https://raw.githubusercontent.com/dler-io/Rules/main/Surge/Surge%203/Provider/Reject.list",
    },
    "Block": {
        "url": "https://raw.githubusercontent.com/SouthAlley/z/main/Surge/G.list",
    },
    "CorrectionRule": {
        "fenliuxiuzheng": "https://raw.githubusercontent.com/fmz200/wool_scripts/main/QuantumultX/filter/fenliuxiuzheng.list",
        "MyCorrectionRule": "https://raw.githubusercontent.com/GiveYou32Likes/Profile/main/QuantumultX/Rule/CorrectionRule.list",
    },
}

HEADER = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
TYPES = "Surge"

def download_and_save_file(url, target_path):
    try:
        response = requests.get(url, headers=HEADER)
        response.raise_for_status()  # 抛出异常如果请求失败
        with open(target_path, "wb") as f:
            f.write(response.content)
        print(f"文件下载完成：{target_path}")
    except requests.exceptions.RequestException as e:
        print(f"下载文件失败：{url}, 错误：{e}")
    except Exception as e:
        print(f"下载文件时出现未知错误：{url}, 错误：{e}")

def apply_replacements(lines):
    return [apply_replacements_to_line(line) for line in lines]

def apply_replacements_to_line(line):
    for pattern, replacement in replacements:
        line = re.sub(pattern, replacement, line)
    return line

def load_and_process_files(rules):
    for key, value in rules.items():
        if isinstance(value, dict):
            rule_name = key
            rule_url = value.get("url")
            if rule_url:
                try:
                    response = requests.get(rule_url, headers=HEADER)
                    response.raise_for_status()  # 抛出异常如果请求失败
                    lines = response.text.splitlines()

                    # 应用替换规则
                    modified_lines = apply_replacements(lines)

                    # 保存修改后的内容
                    target_path = os.path.join(TYPES, f"{rule_name}.list")
                    with open(target_path, 'w', encoding='utf8') as file:
                        file.write('\n'.join(modified_lines))

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
