import os
import re
import time
import requests
from concurrent.futures import ThreadPoolExecutor
import tempfile
import shutil

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

def apply_temp_file_to_original(temp_file_path, original_file_path):
    shutil.move(temp_file_path, original_file_path)

def load_files(rules, folder):
    target_directory = os.path.join(TYPES, folder)
    os.makedirs(target_directory, exist_ok=True)

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(download_and_save_file, url, os.path.join(target_directory, f"{rule_name}.list")) for rule_name, url in rules.items()]

        for future in futures:
            future.result()
        print(f"新文件已下载至：{target_directory}")

def apply_replacements_to_files_in_directory(directory):
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        if os.path.isfile(file_path):
            temp_file_path = apply_replacements_to_temp_file(file_path)
            apply_temp_file_to_original(temp_file_path, file_path)

if __name__ == '__main__':
    for folder, rules in RULES.items():
        load_files(rules, folder)

    for path in file_paths:
        os.makedirs(path, exist_ok=True)

        # 对每个文件应用正则表达式替换规则
        apply_replacements_to_files_in_directory(path)

        print(f"文件夹 {path} 中的正则替换规则已应用")
