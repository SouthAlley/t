import os
import re
import time
import requests
from concurrent.futures import ThreadPoolExecutor
import subprocess


def process_file(file_path):
    # 使用 Sed 和 Awk 命令进行处理
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

RULES = {
    "CorrectionRule": {
        "fenliuxiuzheng": "https://raw.githubusercontent.com/fmz200/wool_scripts/main/QuantumultX/filter/fenliuxiuzheng.list",
        "MyCorrectionRule": "https://raw.githubusercontent.com/GiveYou32Likes/Profile/main/QuantumultX/Rule/CorrectionRule.list",
    },
    "RejectRule": {
        "fenliu": "https://raw.githubusercontent.com/fmz200/wool_scripts/main/QuantumultX/filter/fenliu.list",
        "MyBlockAds": "https://raw.githubusercontent.com/limbopro/Adblock4limbo/main/Surge/rule/Adblock4limbo_surge.list",
        "MyRejectRule": "https://raw.githubusercontent.com/dler-io/Rules/main/Surge/Surge%203/Provider/Reject.list",
        "Block": "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/BanAD.list"
    },
    "StreamingRule": {
        "Netflix": "https://raw.githubusercontent.com/Jard1n/VPN_Tool/main/Surge/Rule/PayPal.list",
        "Disney": "https://raw.githubusercontent.com/Jard1n/VPN_Tool/main/Surge/Rule/OpenAI.list",
        "YouTube": "https://raw.githubusercontent.com/Jard1n/VPN_Tool/main/Surge/Rule/TikTok.list",
        "Spotify": "https://raw.githubusercontent.com/Jard1n/VPN_Tool/main/Surge/Rule/ProxyMedia.list",
        "AppleTV": "https://raw.githubusercontent.com/Jard1n/VPN_Tool/main/Surge/Rule/Twitter.list",
        "Netfli": "https://raw.githubusercontent.com/Jard1n/VPN_Tool/main/Surge/Rule/Telegram.list",
        "Disne": "https://raw.githubusercontent.com/Jard1n/VPN_Tool/main/Surge/Rule/Game.list",
        "YouTub": "https://raw.githubusercontent.com/Jard1n/VPN_Tool/main/Surge/Rule/Microsoft.list",
        "Spotif": "https://raw.githubusercontent.com/Jard1n/VPN_Tool/main/Surge/Rule/Google.list",
        "AppleT": "https://raw.githubusercontent.com/Jard1n/VPN_Tool/main/Surge/Rule/AppleProxy.list",
        "Spoti": "https://raw.githubusercontent.com/Jard1n/VPN_Tool/main/Surge/Rule/Apple.list",
        "Apple": "https://raw.githubusercontent.com/Jard1n/VPN_Tool/main/Surge/Rule/Proxy.list",
        "Appl": "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/BilibiliHMT.list",
        "App": "https://raw.githubusercontent.com/ConnersHua/RuleGo/master/Surge/Ruleset/Extra/Streaming/Video/bilibili.list",
        
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

        # 处理文件
        process_file(path)

        print(f"处理 {path} 完成")
