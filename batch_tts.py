import asyncio
import re
from pathlib import Path

import edge_tts

# ====== 配置区 ======
INPUT_DIR = Path(r".\txts")
OUTPUT_DIR = Path(r".\mp3")

# 推荐中文女声（自然、清晰）
VOICE = "zh-CN-YunxiaNeural"   # 女声
RATE = "-10%"                   # 语速：慢一点更适合儿童（可改：-5%、-15%）
VOLUME = "+5%"                  # 音量：不额外放大（可改：+5%）

# 每段间隔（防止句子太紧），单位 ms
INSERT_SILENCE_MS = 250
# ====================

def normalize_text(s: str) -> str:
    s = s.replace("\r\n", "\n").replace("\r", "\n").strip()
    # 把过长空白压一压
    s = re.sub(r"[ \t]+", " ", s)
    # 段落间加一点停顿：把空行转成一个明确的短停顿
    # edge-tts 支持 SSML，这里用 break 来插入静音
    parts = [p.strip() for p in re.split(r"\n\s*\n", s) if p.strip()]
    ssml_parts = []
    for p in parts:
        # 行内换行转成句间停顿
        p = p.replace("\n", "。")
        ssml_parts.append(p)
    # 用 SSML 包起来，并在段落之间加 break
    joiner = f'<break time="{INSERT_SILENCE_MS}ms"/>'
    body = joiner.join(ssml_parts)
    ssml = f'<speak version="1.0" xml:lang="zh-CN">{body}</speak>'
    return ssml

async def synthesize_one(txt_path: Path, out_mp3: Path):
    text = txt_path.read_text(encoding="utf-8", errors="ignore").strip()

    communicate = edge_tts.Communicate(
        text,
        voice=VOICE,
        rate=RATE,
        volume=VOLUME,
    )
    await communicate.save(str(out_mp3))

async def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    txt_files = sorted(INPUT_DIR.glob("*.txt"))
    if not txt_files:
        raise SystemExit(f"没找到 txt：{INPUT_DIR}")

    for i, txt_path in enumerate(txt_files, 1):
        out_mp3 = OUTPUT_DIR / (txt_path.stem + ".mp3")
        print(f"[{i}/{len(txt_files)}] 生成: {out_mp3.name}")
        await synthesize_one(txt_path, out_mp3)

    print("完成。输出目录：", OUTPUT_DIR)

if __name__ == "__main__":
    asyncio.run(main())
