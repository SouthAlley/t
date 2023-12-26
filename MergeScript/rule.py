import os
import re
import time
import requests
from concurrent.futures import ThreadPoolExecutor

# 正则表达式替换规则
replacements = [
    (r', ', ','),
    (r'([^,]*,[^,]*),.*', r'\1'),
    (r'(host-keyword,|HOST-KEYWORD,)', 'DOMAIN-KEYWORD,'),
    (r'(host-suffix,|HOST-SUFFIX,)', 'DOMAIN-SUFFIX,'),
    (r'ip-cidr,', 'IP-CIDR,'),
    (r'(host,|HOST,)', 'DOMAIN,'),
    (r'(IP6-CIDR,|ip6-cidr,)', 'IP-CIDR6,'),
    (r'(IP-CIDR[6]{0,1},[^,]*)', r'\1,no-resolve'),
    (r'//.*', ''),
]

RULES = {
    "CorrectionRule": {
        "fenliuxiuzheng": "https://raw.githubusercontent.com/fmz200/wool_scripts/main/QuantumultX/filter/fenliuxiuzheng.list",
        "MyCorrectionRule": "https://raw.githubusercontent.com/GiveYou32Likes/Profile/main/QuantumultX/Rule/CorrectionRule.list",
    },
    "RejectRule": {
        "fenliu": "https://raw.githubusercontent.com/fmz200/wool_scripts/main/QuantumultX/filter/fenliu.list",
        "MyBlockAds": "https://raw.githubusercontent.com/limbopro/Adblock4limbo/main/Surge/rule/Adblock4limbo_surge.list",
        "MyRejectRule": "https://raw.githubusercontent.com/dler-io/Rules/main/Surge/Surge%203/Provider/Reject.list",
        "Block": "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/BanAD.list",
    }
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
    
    # 读取并应用替换规则
    for path in [os.path.join(target_directory, f"{rule_name}.list") for rule_name in rules.keys()]:
        with open(path, 'r', encoding='utf8') as file:
            lines = [line.strip() for line in file.readlines()]

        # 应用替换规则
        modified_lines = [apply_replacements(line) for line in lines]

        # 保存修改后的内容
        with open(path, 'w', encoding='utf8') as file:
            file.write('\n'.join(modified_lines))

    print(f"新文件已下载并替换至：{target_directory}")

if __name__ == '__main__':
    for folder, rules in RULES.items():
        load_files(rules, folder)
    for path in file_paths:
        # 创建文件夹，如果文件夹不存在
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"创建目录 {path} 成功")
            
        # 在这里添加自定义逻辑，比如其他文件操作或处理
        # ...

        print(f"处理 {path} 完成")

