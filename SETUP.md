# Profile Setup & Maintenance

This repository uses a set of Python scripts to generate dynamic SVG assets for the GitHub profile README.

## Assets Overview

- `portrait.svg`: High-fidelity ASCII portrait generated from a real photograph.
- `wordmark.svg`: Terminal-style geometric wordmark.
- `contrib-heatmap.svg`: A customized contribution graph reflecting real GitHub activity.

## Local Generation

To update the assets locally, ensure you have the required dependencies:

```bash
pip install Pillow opencv-python numpy requests beautifulsoup4
```

### 1. Generate Portrait
The portrait is generated from a source photograph using GrabCut subject isolation and CLAHE contrast enhancement.
```bash
python3 scripts/generate_portrait.py
```

### 2. Generate Wordmark
Creates the terminal-style wordmark SVG.
```bash
python3 scripts/generate_wordmark.py
```

### 3. Update Contribution Heatmap
This is a two-step process:
1. Fetch latest contribution data:
   ```bash
   GH_PROFILE_USER=yashitarora python3 scripts/fetch_contributions.py
   ```
2. Render the data into the SVG:
   ```bash
   python3 scripts/render_heatmap_svg.py
   ```

## Automation

The assets are automatically updated via GitHub Actions. The workflow `.github/workflows/update-profile-art.yml` runs on a schedule to keep the contribution heatmap current.
