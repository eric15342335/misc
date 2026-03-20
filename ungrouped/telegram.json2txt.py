import json
import sys
from pathlib import Path

MEDIA = {
    "sticker": "[Sticker]",
    "animation": "[GIF]",
    "voice_message": "[Voice]",
    "video_file": "[Video]",
    "audio_file": "[Audio]",
    "video_message": "[VideoNote]",
}


def text(raw):
    if isinstance(raw, str):
        return raw.replace("\n", " ")
    return "".join(p if isinstance(p, str) else p.get("text", "") for p in raw).replace("\n", " ")


def fmt(msg):
    if msg.get("type") != "message":
        return None
    ts = msg["date"][:16].replace("T", " ")
    sender = msg.get("from") or msg.get("actor") or "Unknown"
    parts = [f"[{ts}] {sender}:"]
    if rid := msg.get("reply_to_message_id"):
        parts.append(f"[reply:{rid}]")
    if mt := msg.get("media_type"):
        parts.append(MEDIA.get(mt, f"[{mt}]"))
    if "photo" in msg:
        parts.append("[Photo]")
    if body := text(msg.get("text", "")):
        parts.append(body)
    return " ".join(parts)


src = Path(sys.argv[1] if len(sys.argv) > 1 else "result.json")
dst = Path(sys.argv[2] if len(sys.argv) > 2 else src.with_suffix(".txt"))

data = json.loads(src.read_text(encoding="utf-8"))
lines = list(filter(None, map(fmt, data["messages"])))
dst.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"{len(lines)} messages -> {dst}")
