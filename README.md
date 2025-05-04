# Smart File Renamer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)

A powerful Python utility that automatically organizes and renames files based on their extensions. Perfect for cleaning up downloads, standardizing file collections, or bringing order to chaotic directories.

## Features

- **Smart Sequential Renaming:** Automatically numbers files by extension (e.g., `image_01.jpg`, `image_02.jpg`)
- **Extension Grouping:** Processes files in batches by file type
- **Flexible Configuration:** Custom naming patterns for different file extensions
- **Multiple Operation Modes:** Copy or move files with recursive directory support
- **Dual Interface:** Command-line tool and Python library for scriptable workflows

## Installation

```bash
# Clone the repository
git clone https://github.com/SakibAhmedShuva/Smart-File-Renamer.git

# Navigate to the directory
cd Smart-File-Renamer
```

No external dependencies required! Works with Python 3.7+.

## Usage

### Command-Line Interface

```bash
python smart_filing_system.py --target <target_dir> --source <source_dir> [options]
```

#### Required Arguments:
- `--target` / `-t`: Destination directory for organized files
- `--source` / `-s`: Directory containing files to organize

#### Optional Arguments:
- `--pattern` / `-p`: Custom naming patterns for specific extensions
  - Format: `--pattern EXT "PATTERN"`
  - Example: `--pattern jpg "image_{:02d}" --pattern pdf "document_{:03d}"`
- `--default` / `-d`: Default pattern for extensions without specific rules
  - Default: `"file_{:02d}"`
- `--move` / `-m`: Move files instead of copying them
- `--recursive` / `-r`: Process files in subdirectories

### Python Library Usage

```python
from smart_filing_system import SmartFilingSystem

# Initialize with target directory
filing_system = SmartFilingSystem("organized_files")

# Set custom patterns (optional)
filing_system.set_naming_pattern("jpg", "photo_{:03d}")
filing_system.set_naming_pattern("png", "photo_{:03d}")
filing_system.set_default_pattern("misc_file_{}")

# Organize files
counts = filing_system.organize_files(
    "path/to/messy/files", 
    recursive=False, 
    move=False
)

# Print results
print(f"Organized {sum(counts.values())} files across {len(counts)} extensions")
```

## Naming Patterns

Naming patterns use Python's string formatting syntax:
- `{}`: Standard numbering (1, 2, 3...)
- `{:02d}`: Zero-padded 2-digit numbers (01, 02, 10...)
- `{:03d}`: Zero-padded 3-digit numbers (001, 002...)

You can add any text around the placeholder: `invoice_{:04d}_final`, `image_{}`

## Examples

### Basic Organization
```bash
python smart_filing_system.py -t ~/Documents/organized -s ~/Downloads/messy_files
```
*Result: Files are copied to the target with default naming (file_01.jpg, file_02.jpg, file_01.pdf...)*

### Custom Patterns with Move
```bash
python smart_filing_system.py \
  -t ./project_assets \
  -s ./project_assets/raw \
  -p jpg "images/img_{:02d}" \
  -p png "images/img_{:02d}" \
  -p txt "notes/note_{:02d}" \
  -m
```
*Result: Images moved to subdirectories with custom naming patterns*

### Recursive Processing
```bash
python smart_filing_system.py \
  -t ./consolidated_backup \
  -s ./backup_source \
  -d "backup_item_{:04d}" \
  -r
```
*Result: Files from all subdirectories organized with 4-digit numbering*

## Contributing

Contributions welcome! Here's how to help:

1. **Open an Issue** to discuss proposed changes
2. **Fork & Clone** the repository
3. **Create a Branch** (`git checkout -b feature/amazing-feature`)
4. **Make Changes** and test thoroughly
5. **Commit** with clear messages (`git commit -m 'Add amazing feature'`)
6. **Push** to your branch (`git push origin feature/amazing-feature`)
7. **Open a Pull Request**

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Repository:** [https://github.com/SakibAhmedShuva/Smart-File-Renamer](https://github.com/SakibAhmedShuva/Smart-File-Renamer)
