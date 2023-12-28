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

def append_del_to_my_block_ads(del_path, my_block_ads_path):
    try:
        with open(del_path, 'r', encoding='utf8') as del_file:
            del_content = del_file.read()

        with open(my_block_ads_path, 'a', encoding='utf8') as my_block_ads_file:
            my_block_ads_file.write('\n' + del_content)

        print(f"内容成功追加到 {my_block_ads_path}")
    except Exception as e:
        print(f"追加内容时出现错误：{e}")

def remove_delrule_from_my_block_ads(delrule_path, my_block_ads_path):
    try:
        with open(delrule_path, 'r', encoding='utf8') as delrule_file:
            delrule_content = delrule_file.read()

        with open(my_block_ads_path, 'r', encoding='utf8') as my_block_ads_file:
            lines = my_block_ads_file.readlines()

        filtered_lines = [line for line in lines if delrule_content not in line]

        with open(my_block_ads_path, 'w', encoding='utf8') as my_block_ads_file:
            my_block_ads_file.writelines(filtered_lines)

        print(f"成功从 {my_block_ads_path} 中删除与 {delrule_path} 匹配的行")
    except Exception as e:
        print(f"删除匹配内容时出现错误：{e}")

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

    # 调用追加内容函数
    del_file_path = 'del.ini'
    append_del_to_my_block_ads(del_file_path, os.path.join(TYPES, 'MyBlockAds.list'))

    # 调用删除匹配内容函数
    delrule_file_path = 'delrule.ini'
    remove_delrule_from_my_block_ads(delrule_file_path, os.path.join(TYPES, 'MyBlockAds.list'))
