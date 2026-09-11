from PIL import Image, ImageEnhance, ImageOps, ImageFilter
import cv2, numpy as np, html
from pathlib import Path

# Configuration
SRC_PATH = Path('/Users/yashitarora/github_profile_assets/Yashit_GitHub_Profile_Final/yashit-photo.jpg')
OUT_PATH = Path('/Users/yashitarora/yashitarora/portrait.svg')
PREVIEW_PATH = Path('/Users/yashitarora/yashitarora/scripts/portrait-preview.png')

def generate_portrait():
    if not SRC_PATH.exists():
        print(f"Source photo not found at {SRC_PATH}")
        return

    # 1. Load and Preprocess
    im = Image.open(SRC_PATH).convert('RGB')
    arr = np.array(im)
    h, w = arr.shape[:2]

    # Tight crop around the person.
    # Based on the provided script, these coordinates were tuned for the photo.
    x1, y1, x2, y2 = 185, 360, 425, 805
    crop = arr[y1:min(y2, h), x1:min(x2, w)].copy()
    ch, cw = crop.shape[:2]

    # 2. Subject Isolation (GrabCut)
    mask = np.zeros((ch, cw), np.uint8)
    rect = (22, 18, max(1, cw-44), max(1, ch-28))
    bgd = np.zeros((1, 65), np.float64); fgd = np.zeros((1, 65), np.float64)
    cv2.grabCut(crop, mask, rect, bgd, fgd, 7, cv2.GC_INIT_WITH_RECT)
    keep = np.where((mask == 2) | (mask == 0), 0, 255).astype(np.uint8)

    # Cleanup and feathering
    k = np.ones((5, 5), np.uint8)
    keep = cv2.morphologyEx(keep, cv2.MORPH_OPEN, k)
    keep = cv2.morphologyEx(keep, cv2.MORPH_CLOSE, k)
    keep = cv2.GaussianBlur(keep, (0, 0), 1.1)

    # 3. Contrast Enhancement
    gray = cv2.cvtColor(crop, cv2.COLOR_RGB2GRAY)
    alpha = keep.astype(np.float32) / 255.0
    canvas = np.full_like(gray, 250, dtype=np.float32)

    # Use CLAHE for local contrast enhancement (essential for facial features)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray).astype(np.float32)

    # Composite subject on near-white canvas to eliminate background in ASCII
    composed = enhanced * alpha + canvas * (1 - alpha)
    composed = np.clip(composed, 0, 255).astype(np.uint8)

    # 4. ASCII Conversion
    COLS, ROWS = 100, 53
    # Dense ASCII ramp for high detail
    RAMP = '@#W$S%?*+;:,.'
    # Note: Reversing it for dark-on-light or light-on-dark.
    # For terminal look (light text on dark bg), we want bright areas = dense chars.
    RAMP = " .'`:-=+*#%@"

    small = Image.fromarray(composed, 'L').resize((COLS, ROWS), Image.Resampling.LANCZOS)
    px = np.asarray(small).astype(np.float32) / 255.0

    # Contrast curve to push shadows and highlights
    px = np.power(px, 1.3)

    rows = []
    for y in range(ROWS):
        line = ''
        for x in range(COLS):
            lum = px[y, x]
            if lum >= 0.75: # Background threshold
                ch = ' '
            else:
                # Map luminance to RAMP
                idx = int((1 - lum) * (len(RAMP) - 1) + 0.5)
                ch = RAMP[max(0, min(len(RAMP) - 1, idx))]
            line += ch
        rows.append(line)

    # 5. SVG Generation
    # Visual style: Terminal Window
    W = COLS * 8 + 40
    H = ROWS * 15 + 90
    PAD = 20
    INK = '#c9d1d9'
    BG = '#0d1117'
    FRAME = '#30363d'
    TITLE_C = '#7d8590'

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace">',
        f'<rect width="{W}" height="{H}" rx="12" fill="{BG}"/>',
        f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{FRAME}"/>',
        f'<line x1="0" y1="30" x2="{W}" y2="30" stroke="{FRAME}"/>',
        f'<text x="{W/2}" y="20" fill="{TITLE_C}" font-size="12" text-anchor="middle">yashitarora@github: ~$ ./portrait.sh</text>'
    ]

    # Draw the ASCII art
    # We remove textLength="800" and instead calculate a centering offset
    # Character width is approx 8px for font-size 12.9
    char_w = 8.0
    content_w = COLS * char_w
    offset_x = (W - content_w) / 2

    for ry, line in enumerate(rows):
        y = 40 + ry * 15 + 11
        rowy = 40 + ry * 15
        safe = html.escape(line)
        # Remove textLength and lengthAdjust to preserve natural character aspect ratio
        text = f'<text xml:space="preserve" x="{offset_x}" y="{y}" fill="{INK}" font-size="12.9">{safe}</text>'

        # Simple reveal animation
        delay = ry * 0.03
        parts.append(f'<clipPath id="r{ry}"><rect x="{offset_x}" y="{rowy}" width="{content_w}" height="15"><animate attributeName="width" from="0" to="{content_w}" begin="{delay:.3f}s" dur="0.2s" fill="freeze"/></rect></clipPath>')
        parts.append(f'<g clip-path="url(#r{ry})">{text}</g>')

    parts.append(f'<line x1="0" y1="{H-38}" x2="{W}" y2="{H-38}" stroke="{FRAME}"/>')
    parts.append(f'<text x="{PAD}" y="{H-16}" fill="{TITLE_C}" font-size="13">yashitarora@github:~$ whoami <tspan fill="{INK}">Yashit Arora</tspan></text>')
    parts.append('</svg>')

    OUT_PATH.write_text(''.join(parts), encoding='utf-8')
    print(f"Successfully created {OUT_PATH}")

if __name__ == "__main__":
    generate_portrait()
