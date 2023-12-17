import os
import requests
import re
from requests.exceptions import RequestException

def download_file_from_comment(file_path):
    try:
        with open(file_path, 'rb') as file:
            content = file.read()

            match = re.search(r'(引用地址：https?://[^\s]*\.js)', content.decode('utf-8'))

            if match:
                full_url = match.group(1)
                download_url = full_url.replace('引用地址：', '')

                response = requests.get(download_url)
                response.raise_for_status()

                # 提取在“Scripts”目录内的相对路径
                relative_path = os.path.relpath(file_path, 'Scripts')

                # 构建在“Scripts”目录内的新文件路径
                new_file_path = os.path.join("Scripts", f"{os.path.splitext(relative_path)[0]}.js")

                with open(new_file_path, 'wb') as new_file:
                    new_file.write(f"// 引用地址：{download_url}\n".encode('utf-8'))
                    new_file.write(response.content)

                print(f"文件 {new_file_path} 下载成功！")
            else:
                print(f"在文件 {file_path} 中未找到引用地址")
    except Exception as e:
        print(f"发生错误：{e}")

# 文件夹路径
folder_path = "Scripts"

# 遍历文件夹及其子文件夹内的所有文件
for root, dirs, files in os.walk(folder_path):
    for filename in files:
        file_path = os.path.join(root, filename)

        if re.search(r'\.js$', filename):
            download_file_from_comment(file_path)
