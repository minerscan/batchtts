import os
import re

start_number = 81

def extract_number(filename):
    match = re.match(r"(\d+)", filename)
    return int(match.group(1)) if match else None

def main():
    folder = os.path.join(os.getcwd(), "mp3")

    if not os.path.exists(folder):
        print("未找到 mp3 文件夹。")
        return

    files = os.listdir(folder)

    numbered_files = []
    for f in files:
        if f.lower().endswith(".mp3"):
            number = extract_number(f)
            if number is not None:
                numbered_files.append((number, f))

    if not numbered_files:
        print("未找到以数字开头的 mp3 文件。")
        return

    numbered_files.sort()

    # 第一步：临时改名防冲突
    temp_files = []
    for i, (old_number, filename) in enumerate(numbered_files):
        old_path = os.path.join(folder, filename)
        temp_name = f"temp_rename_{i}.tmp"
        temp_path = os.path.join(folder, temp_name)
        os.rename(old_path, temp_path)
        temp_files.append((temp_name, filename))

    # 第二步：正式改名
    for i, (temp_name, old_filename) in enumerate(temp_files):
        new_number = start_number + i
        new_number_str = f"{new_number:03d}"

        new_name = re.sub(r"^\d+", new_number_str, old_filename)

        temp_path = os.path.join(folder, temp_name)
        new_path = os.path.join(folder, new_name)

        os.rename(temp_path, new_path)
        print(f"{old_filename} → {new_name}")

    print("\n全部重命名完成！")

if __name__ == "__main__":
    main()
