import numpy as np
from pathlib import Path
import html

def generate_wordmark():
    OUT_PATH = Path('/Users/yashitarora/yashitarora/wordmark.svg')

    # Wordmark settings
    TEXT = "YASHIT ARORA"
    # Geometric ASCII representation of the text
    # Using a monospace-friendly construction
    # For a truly "premium" look, I'll use an SVG with a terminal-like font and a subtle glow.

    BG = "#0d1117"
    FRAME = "#30363d"
    INK = "#c9d1d9"
    ACCENT = "#39d353" # Terminal Green
    TITLE_C = "#7d8590"

    W = 600
    H = 120
    PAD = 20

    # SVG Construction
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace">',
        f'<rect width="{W}" height="{H}" rx="12" fill="{BG}"/>',
        f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{FRAME}"/>',
        f'<line x1="0" y1="30" x2="{W}" y2="30" stroke="{FRAME}"/>',
        f'<text x="{W/2}" y="20" fill="{TITLE_C}" font-size="12" text-anchor="middle">yashitarora@github: ~$ ./wordmark.sh</text>'
    ]

    # Main Wordmark text
    text_x = W / 2
    text_y = H / 2 + 10

    # Glow effect - refined for professional look
    parts.append(f'<filter id="glow" x="-20%" y="-20%" width="140%" height="140%">')
    parts.append(f'  <feGaussianBlur stdDeviation="3" result="blur"/>')
    parts.append(f'  <feComposite in="SourceGraphic" in2="blur" operator="over"/>')
    parts.append(f'</filter>')

    # The Wordmark - Larger, bolder, and better spaced
    parts.append(f'<text x="{text_x}" y="{text_y}" fill="{INK}" font-size="48" font-weight="800" text-anchor="middle" filter="url(#glow)" style="letter-spacing: 6px; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;">')
    parts.append(f'  {TEXT}')
    parts.append(f'</text>')

    # Terminal accent (underscore cursor) - adjusted for 48px font
    char_width = 24
    text_width = len(TEXT) * char_width
    cursor_x = text_x + (text_width / 2) + 8

    parts.append(f'<rect x="{cursor_x}" y="{text_y - 32}" width="14" height="35" fill="{ACCENT}">')
    parts.append(f'  <animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite" />')
    parts.append(f'</rect>')

    parts.append('</svg>')

    OUT_PATH.write_text(''.join(parts), encoding='utf-8')
    print(f"Successfully created {OUT_PATH}")

if __name__ == "__main__":
    generate_wordmark()
