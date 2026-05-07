import os
from pathlib import Path
import re


def generate_image_tables(docs_dir="docs"):
    images_dir = Path(docs_dir) / "images"
    if not images_dir.exists():
        print(f"❌ Images directory not found: {images_dir}")
        return []

    image_files = [f.name for f in images_dir.glob("*.png") if f.is_file()]

    slug_map = {}
    for img in image_files:
        match = re.match(r"^(light|dark)-(.*)\.png$", img)
        if match:
            theme, slug = match.groups()
            if slug not in slug_map:
                slug_map[slug] = {}
            slug_map[slug][theme] = img

    markdown_output = "# Screenshot Gallery\n\n"

    for slug in sorted(slug_map.keys()):
        images = slug_map[slug]
        light_img = images.get("light", "")
        dark_img = images.get("dark", "")

        title = slug.replace("-", " ").title()

        markdown_output += f"## {title}\n\n"
        markdown_output += "| Light Mode | Dark Mode |\n"
        markdown_output += "|------------|-------------|\n"

        light_path = f"images/{light_img}" if light_img else ""
        dark_path = f"images/{dark_img}" if dark_img else ""

        markdown_output += f"| ![Light]({light_path}) | ![Dark]({dark_path}) |\n\n"

    return markdown_output


def update_user_manual(docs_dir="docs"):
    manual_path = Path(docs_dir) / "user_manual.md"
    images_dir = Path(docs_dir) / "images"

    if not manual_path.exists():
        print(f"❌ User manual not found: {manual_path}")
        return

    new_content = generate_image_tables(docs_dir)

    start_marker = "<!-- SCREENSHOT_TABLES_START -->"
    end_marker = "<!-- SCREENSHOT_TABLES_END -->"

    with open(manual_path, "r") as f:
        content = f.read()

    if start_marker in content and end_marker in content:
        pattern = f"{start_marker}.*{end_marker}"
        content = re.sub(
            pattern,
            f"{start_marker}\n{new_content}\n{end_marker}",
            content,
            flags=re.DOTALL,
        )
    else:
        content += f"\n\n{start_marker}\n{new_content}\n{end_marker}\n"

    with open(manual_path, "w") as f:
        f.write(content)

    print(f"✅ Updated {manual_path} with image tables")


if __name__ == "__main__":
    import sys

    docs_dir = sys.argv[1] if len(sys.argv) > 1 else "docs"
    update_user_manual(docs_dir)