import os
import re
import requests

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
]

RULES = {
    "fenliu": "https://raw.githubusercontent.com/fmz200/wool_scripts/main/QuantumultX/filter/fenliu.list",
    "MyBlockAds": "https://raw.githubusercontent.com/limbopro/Adblock4limbo/main/Surge/rule/Adblock4limbo_surge.list",
    "MyRejectRule": "https://raw.githubusercontent.com/dler-io/Rules/main/Surge/Surge%203/Provider/Reject.list",
    "Block": "https://raw.githubusercontent.com/SouthAlley/z/main/Surge/G.list",
}

HEADER = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
TYPES = "Surge"

def download_and_save_file(url, target_path):
    try:
        response = requests.get(url, headers=HEADER)
        response.raise_for_status()
        with open(target_path, "w", encoding='utf8') as f:
            for line in response.text.splitlines():
                for pattern, replacement in REPLACEMENTS:
                    line = re.sub(pattern, replacement, line)
                f.write(line + '\n')
        print(f"文件处理完成：{target_path}")
    except Exception as e:
        print(f"处理文件时出现错误：{url}, 错误：{e}")

if __name__ == '__main__':
    for rule_name, rule_url in RULES.items():
        target_path = os.path.join(TYPES, f"{rule_name}.list")
        download_and_save_file(rule_url, target_path)
