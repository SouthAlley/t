import os
import requests
import re
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
        "Block": "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/BanAD.list"
    },
    "StreamingRule": {
        "Netflix": "https://raw.githubusercontent.com/Jard1n/VPN_Tool/main/Surge/Rule/PayPal.list",
        "Disney": "https://raw.githubusercontent.com/Jard1n/VPN_Tool/main/Surge/Rule/OpenAI.list",
        # 根据需要添加更多的流媒体规则
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
        print(f"下载成功: {target_path}")


def apply_replacements(line):
    for pattern, replacement in replacements:
        line = re.sub(pattern, replacement, line)
    return line


def load_files(rules, folder):
    target_directory = os.path.join(TYPES, folder)
    os.makedirs(target_directory, exist_ok=True)

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(download_and_save_file, rule_url, os.path.join(target_directory, f"{rule_name}.list"))
                   for rule_name, rule_url in rules.items()]

    print(f"新文件已下载至：{target_directory}")


if __name__ == '__main__':
    for folder, rules in RULES.items():
        load_files(rules, folder)
