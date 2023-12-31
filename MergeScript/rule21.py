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
    "fenliu": "https://raw.githubusercontent.com/fmz200/wool_scripts/main/QuantumultX/filter/fenliu.list",
    "MyBlockAds": "https://raw.githubusercontent.com/RuCu6/QuanX/main/Rules/MyBlockAds.list",
    "MyRejectRule": "https://raw.githubusercontent.com/dler-io/Rules/main/Surge/Surge%203/Provider/Reject.list",
    "Block": "https://raw.githubusercontent.com/SouthAlley/z/main/Surge/G.list",
}

HEADER = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
TYPES = "Surge"

def download_and_save_file(url, target_path):
    try:
        response = requests.get(url, headers=HEADER)
        response.raise_for_status()
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

if __name__ == '__main__':
    for rule_name, rule_url in RULES.items():
        try:
            response = requests.get(rule_url, headers=HEADER)
            response.raise_for_status()
            lines = response.text.splitlines()

            modified_lines = apply_replacements(lines)

            target_path = os.path.join(TYPES, f"{rule_name}.list")
            with open(target_path, 'w', encoding='utf8') as file:
                file.write('\n'.join(modified_lines))

            print(f"文件处理完成：{target_path}")
        except requests.exceptions.RequestException as e:
            print(f"处理文件时出现错误：{rule_url}, 错误：{e}")
        except Exception as e:
            print(f"处理文件时出现未知错误：{rule_url}, 错误：{e}")
