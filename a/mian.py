import subprocess
import os

def run_script(script_name, input_file=None, output_file=None):
    command = ["python", script_name]
    if input_file:
        command.append(input_file)
    if output_file:
        command.append(output_file)
    subprocess.run(command, check=True)

def main():
    # 1. 下载和替换规则
    run_script("down-replace.py")

    # 2. 去除特殊字符
    run_script("nospecial.py")

    # 3. 处理反向规则
    run_script("reverse.py")
    run_script("process-rev.py")
    run_script("unreverse.py")

    # 4. 处理相同后缀
    run_script("process-same-suffix-nosuff.py")

    # 5. 关键字去重
    run_script("keyworddd.py")

    # 6. 处理删除规则
    if os.path.exists("del.ini"):
        run_script("del-file.py")

if __name__ == "__main__":
    main()
