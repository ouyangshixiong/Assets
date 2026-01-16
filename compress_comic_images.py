import os
from io import BytesIO

from PIL import Image


SRC_DIR = "comic-1"
DST_DIR = "comic-1-compressed"
TARGET_SIZE = 300 * 1024
MIN_QUALITY = 40
QUALITY_STEP = 5


def ensure_dst_dir():
    if not os.path.exists(DST_DIR):
        os.makedirs(DST_DIR, exist_ok=True)


def compress_image(path):
    name = os.path.basename(path)
    base, _ = os.path.splitext(name)
    dst_path = os.path.join(DST_DIR, base + ".jpg")

    with Image.open(path) as img:
        if img.mode not in ("RGB", "L"):
            img = img.convert("RGB")

        quality = 90
        buffer = BytesIO()
        img.save(buffer, format="JPEG", quality=quality, optimize=True)
        data = buffer.getvalue()

        while len(data) > TARGET_SIZE and quality > MIN_QUALITY:
            quality -= QUALITY_STEP
            buffer = BytesIO()
            img.save(buffer, format="JPEG", quality=quality, optimize=True)
            data = buffer.getvalue()

    with open(path, "rb") as f:
        original_size = len(f.read())

    with open(dst_path, "wb") as f:
        f.write(data)

    compressed_size = len(data)
    print(f"{name}: {original_size // 1024}KB -> {compressed_size // 1024}KB (quality={quality})")


def main():
    ensure_dst_dir()
    if not os.path.isdir(SRC_DIR):
        raise SystemExit(f"Source directory not found: {SRC_DIR}")

    for entry in os.listdir(SRC_DIR):
        path = os.path.join(SRC_DIR, entry)
        if not os.path.isfile(path):
            continue
        lower = entry.lower()
        if not (lower.endswith(".png") or lower.endswith(".jpg") or lower.endswith(".jpeg")):
            continue
        compress_image(path)


if __name__ == "__main__":
    main()

