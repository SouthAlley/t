import os
import re
import requests

REPLACEMENTS = [
    (r', ', ','),
    # ... (其他替换规则)
]

RULES = {
    "fenliu": "https://raw.githubusercontent.com/fmz200/wool_scripts/main/QuantumultX/filter/fenliu.list",
    # ... (其他规则)
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
