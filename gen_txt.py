import os
import re

OUT_DIR = "./txts/"

def clean_filename(title):
    """
    清理非法文件名字符
    """
    # 去除非法字符
    title = re.sub(r'[\\/:*?"<>|]', '', title)
    # 去除前后空格
    title = title.strip()
    # 限制长度（防止过长）
    return title[:100]

def main():
    print("请粘贴你的文本内容（第一行将作为标题）：")
    print("结束输入请按 Ctrl+Z (Windows) 或 Ctrl+D (Mac/Linux)\n")

    # 读取多行输入
    content = ""
    try:
        while True:
            line = input()
            content += line + "\n"
    except EOFError:
        pass

    if not content.strip():
        print("未输入任何内容。")
        return

    lines = content.strip().split("\n")
    title = lines[0]
    body = "\n".join(lines[1:]) if len(lines) > 1 else ""

    filename = OUT_DIR + clean_filename(title) + ".txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(body)

    print(f"\n文件已生成：{filename}")
    print("文件保存在当前程序所在目录。")

if __name__ == "__main__":
    main()