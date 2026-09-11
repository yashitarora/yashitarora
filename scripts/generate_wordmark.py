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
    # Use a larger font size with a subtle glow effect
    text_x = W / 2
    text_y = H / 2 + 15

    # Glow effect
    parts.append(f'<filter id="glow" x="-20%" y="-20%" width="140%" height="140%">')
    parts.append(f'  <feGaussianBlur stdDeviation="2" result="blur"/>')
    parts.append(f'  <feComposite in="SourceGraphic" in2="blur" operator="over"/>')
    parts.append(f'</filter>')

    # The Wordmark
    parts.append(f'<text x="{text_x}" y="{text_y}" fill="{INK}" font-size="42" font-weight="bold" text-anchor="middle" filter="url(#glow)" style="letter-spacing: 4px;">')
    parts.append(f'  {TEXT}')
    parts.append(f'</text>')

    # Terminal accent (underscore cursor)
    cursor_x = text_x + (len(TEXT) * 15) # Approximate
    # Since we are using text-anchor="middle", we need to calculate the end of the string.
    # A better way is to use a separate element for the cursor.

    # Calculate approx width of "YASHIT ARORA" in 42px monospace
    char_width = 22 # Approx for monospace 42px
    text_width = len(TEXT) * char_width
    cursor_x = text_x + (text_width / 2) + 5

    parts.append(f'<rect x="{cursor_x}" y="{text_y - 25}" width="12" height="30" fill="{ACCENT}">')
    parts.append(f'  <animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite" />')
    parts.append(f'</rect>')

    parts.append('</svg>')

    OUT_PATH.write_text(''.join(parts), encoding='utf-8')
    print(f"Successfully created {OUT_PATH}")

if __name__ == "__main__":
    generate_wordmark()
