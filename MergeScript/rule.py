import os
import re
import requests

# 正则表达式替换规则
replacements = [
    # ... （保持不变）
]

RULES = {
    "fenliu": "https://raw.githubusercontent.com/fmz200/wool_scripts/main/QuantumultX/filter/fenliu.list",
    "MyBlockAds": "https://raw.githubusercontent.com/limbopro/Adblock4limbo/main/Surge/rule/Adblock4limbo_surge.list",
    "MyRejectRule": "https://raw.githubusercontent.com/dler-io/Rules/main/Surge/Surge%203/Provider/Reject.list",
    "Block": "https://raw.githubusercontent.com/SouthAlley/z/main/Surge/G.list",
    
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
        if isinstance(value, str):
            # 处理单个文件
            rule_name = key
            rule_url = value
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

                print(f"文件处理完成：{target_path}")
            except requests.exceptions.RequestException as e:
                print(f"处理文件时出现错误：{rule_url}, 错误：{e}")
            except Exception as e:
                print(f"处理文件时出现未知错误：{rule_url}, 错误：{e}")
        elif isinstance(value, dict):
            # 递归处理嵌套字典
            load_and_process_files(value)

if __name__ == '__main__':
    for folder, rules in RULES.items():
        load_and_process_files(rules)
