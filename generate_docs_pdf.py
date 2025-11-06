#!/usr/bin/env python3

import os
import subprocess
from pathlib import Path

def create_combined_docs():
    base_path = Path("/Users/yemikudaisi/frappe-bench/apps/bank_integration")

    # Document order for logical flow
    doc_files = [
        ("README.md", "Introduction & Quick Start"),
        ("doc/01-overview.md", "Overview"),
        ("doc/02-configuration.md", "Configuration Guide"),
        ("doc/03-scheduled-sync-workflow.md", "Scheduled Sync Workflow"),
        ("doc/04-manual-sync-workflow.md", "Manual Sync Workflow"),
        ("doc/08-common-sync-process.md", "Common Sync Process"),
        ("doc/05-authentication.md", "Authentication & Token Management"),
        ("doc/06-data-mapping.md", "Data Mapping"),
        ("doc/07-error-handling.md", "Error Handling & Recovery"),
        ("doc/transaction_mapping.md", "Transaction Mapping Reference"),
    ]

    combined_content = """---
title: Bank Integration - Complete Documentation
subtitle: Airwallex to ERPNext Integration
author: Akhilam Inc
date: November 2025
geometry:
  - top=0.22in
  - bottom=0.2in
  - left=0.2in
  - right=0.2in
fontsize: 11pt
linestretch: 1.1
colorlinks: true
linkcolor: blue
urlcolor: blue
toccolor: black
toc: true
toc-depth: 3
header-includes:
  - \\usepackage{fancyhdr}
  - \\pagestyle{fancy}
  - \\fancyhead[L]{Bank Integration Documentation}
  - \\fancyhead[R]{\\thepage}
  - \\fancyfoot[C]{Akhilam Inc - November 2025}
  - \\setlength{\\headheight}{14pt}
---

# Bank Integration - Complete Documentation
*Airwallex to ERPNext Integration*

\\newpage

"""

    for file_path, title in doc_files:
        full_path = base_path / file_path
        if full_path.exists():
            print(f"Adding {file_path}...")

            # Add title
            if file_path == "README.md":
                combined_content += f"# {title}\n\n"
            else:
                combined_content += f"# {title}\n\n"

            # Read and add content
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()

                # Remove the first # heading if it exists (we'll use our own)
                lines = content.split('\n')
                if lines and lines[0].startswith('# '):
                    lines = lines[1:]
                    content = '\n'.join(lines)

                combined_content += content
                combined_content += "\n\n\\newpage\n\n"

    # Write combined file
    output_file = base_path / "combined_documentation.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(combined_content)

    return output_file

def generate_pdf(markdown_file):
    """Generate PDF using pandoc"""
    base_path = Path("/Users/yemikudaisi/frappe-bench/apps/bank_integration")
    output_pdf = base_path / "bank_integration_documentation.pdf"

    cmd = [
        "pandoc",
        str(markdown_file),
        "-o", str(output_pdf),
        "--pdf-engine=wkhtmltopdf",
        "--toc",
        "--toc-depth=3",
        "--metadata", "title=Bank Integration - Complete Documentation",
        "--metadata", "author=Akhilam Inc",
        "--metadata", f"date={subprocess.check_output(['date', '+%B %d, %Y']).decode().strip()}",
        "--variable", "geometry:top=0.75in,bottom=0.75in,left=0.6in,right=0.6in",
        "--variable", "fontsize=11pt",
        "--variable", "linestretch=1.1",
        "--variable", "colorlinks=true",
        "--variable", "linkcolor=blue",
        "--variable", "urlcolor=blue",
        "--variable", "toccolor=black",
        "--number-sections"
    ]

    try:
        subprocess.run(cmd, check=True)
        print(f"PDF generated successfully: {output_pdf}")
        return output_pdf
    except subprocess.CalledProcessError as e:
        print(f"Error generating PDF: {e}")
        return None
    except FileNotFoundError:
        print("Error: pandoc not found. Please install pandoc first.")
        print("macOS: brew install pandoc")
        print("Or visit: https://pandoc.org/installing.html")
        return None

if __name__ == "__main__":
    print("Creating combined documentation...")
    markdown_file = create_combined_docs()
    print(f"Combined markdown created: {markdown_file}")

    print("\nGenerating PDF...")
    pdf_file = generate_pdf(markdown_file)

    if pdf_file:
        print(f"\n✅ Documentation PDF created: {pdf_file}")

        # Clean up temporary file
        markdown_file.unlink()
        print("Temporary markdown file cleaned up.")
    else:
        print("\n❌ Failed to generate PDF")
