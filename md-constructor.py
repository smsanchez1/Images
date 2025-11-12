#!/usr/bin/env python3
"""
Markdown Concatenator
Combines multiple markdown files with automatic table of contents generation.
"""

import sys
from pathlib import Path


def extract_first_line(file_path):
    """Extract the first non-empty line from a markdown file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            stripped = line.strip()
            if stripped:
                # Remove markdown heading symbols if present
                return stripped.lstrip('#').strip()
    return file_path.stem


def read_file_content(file_path):
    """Read the entire content of a file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def concatenate_markdown_files(file_paths, output_path):
    """
    Concatenate markdown files with table of contents.
    
    Args:
        file_paths: List of markdown file paths
        output_path: Output file path for the concatenated result
    """
    if not file_paths:
        print("Error: No markdown files provided")
        sys.exit(1)
    
    # Convert to Path objects
    paths = [Path(p) for p in file_paths]
    
    # Validate all files exist
    for p in paths:
        if not p.exists():
            print(f"Error: File not found: {p}")
            sys.exit(1)
    
    result = []
    
    # First file is the introduction
    intro_path = paths[0]
    intro_content = read_file_content(intro_path)
    result.append(intro_content)
    result.append("\n\n")
    
    # Generate table of contents if there are more files
    if len(paths) > 1:
        result.append("## Contents\n\n")
        for path in paths[1:]:
            title = extract_first_line(path)
            result.append(f"- {title}\n")
        #result.append("\n---\n\n")
    
    # Append remaining files
    for path in paths[1:]:
        content = read_file_content(path)
        result.append(content)
        result.append("\n\n---\n\n")
    
    # Write output
    output = Path(output_path)
    with open(output, 'w', encoding='utf-8') as f:
        f.write(''.join(result))
    
    print(f"✓ Successfully created {output}")
    print(f"  Combined {len(paths)} markdown files")


def main():
    if len(sys.argv) < 3:
        print("Usage: python md_concat.py <output.md> <file1.md> <file2.md> ...")
        print("\nExample:")
        print("  python md_concat.py result.md intro.md guide1.md guide2.md")
        sys.exit(1)
    
    output_file = sys.argv[1]
    input_files = sys.argv[2:]
    
    concatenate_markdown_files(input_files, output_file)


if __name__ == "__main__":
    main()
