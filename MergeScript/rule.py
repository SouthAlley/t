import os
import re
import time
import requests
from concurrent.futures import ThreadPoolExecutor
import subprocess

def process_file(file_path):
    subprocess.run(['sed', '-i', 's/, /,/g', file_path])
    subprocess.run(['awk', '{sub("host-wildcard.*$", ""); print}', file_path], stdout=open('tmpfile', 'w'))
    subprocess.run(['mv', 'tmpfile', file_path])
    subprocess.run(['sed', '-i', '-e', 's/host,/DOMAIN,/gi', file_path])
    subprocess.run(['sed', '-i', '-e', 's/host-suffix,/DOMAIN-SUFFIX,/gi', file_path])
    subprocess.run(['sed', '-i', '-e', 's/host-keyword,/DOMAIN-KEYWORD,/gi', file_path])
    subprocess.run(['sed', '-i', 's/ip-cidr,/IP-CIDR,/gi', file_path])
    subprocess.run(['sed', '-i', 's/ip6-cidr,/IP-CIDR6,/gi', file_path])
    subprocess.run(['sed', '-i', 's/user-agent,/USER-AGENT,/g', file_path])
    subprocess.run(['sed', '-i', 's/\([^,]*,[^,]*\),.*/\\1/g', file_path])
    subprocess.run(['sed', '-i', '/IP-CIDR/ {/no-resolve/! s/$/,no-resolve/}; /IP-CIDR6/ {/no-resolve/! s/$/,no-resolve/}', file_path])
    subprocess.run(['sed', '-i', 's/;/# /g', file_path])

# 在 apply_replacements 函数中添加参数 replacements
def apply_replacements(line, replacements):
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

        # 在这里定义替换规则
        replacements = [
            # 你的替换规则格式应该是 (pattern, replacement)
            (r'原始模式', r'替换后的内容'),
            # 添加其他替换规则
        ]

        # 应用替换规则
        modified_lines = [apply_replacements(line, replacements) for line in lines]

        # 保存修改后的内容
        with open(path, 'w', encoding='utf8') as file:
            file.write('\n'.join(modified_lines))

    print(f"新文件已下载并替换至：{target_directory}")

RULES = {
    # 你的规则定义
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

if __name__ == '__main__':
    for folder, rules in RULES.items():
        load_files(rules, folder)
    for path in file_paths:
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"创建目录 {path} 成功")

        # 在这里添加自定义逻辑，比如其他文件操作或处理
        # ...

        process_file(path)

        print(f"处理 {path} 完成")
