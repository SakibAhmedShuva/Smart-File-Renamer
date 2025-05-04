import os
import shutil
import re
from pathlib import Path
import argparse
from typing import Dict, List, Optional, Tuple


class SmartFilingSystem:
    """A system that renames files with sequential numbering based on file extensions."""
    
    def __init__(self, folder_path: str):
        """Initialize the filing system with the target folder path.
        
        Args:
            folder_path: Directory path where files will be organized
        """
        self.folder_path = Path(folder_path)
        self.naming_patterns: Dict[str, str] = {}
        self.default_pattern = "file_{:02d}"
        
        # Create the directory if it doesn't exist
        if not self.folder_path.exists():
            self.folder_path.mkdir(parents=True)
    
    def set_naming_pattern(self, extension: str, pattern: str):
        """Set a custom naming pattern for a specific file extension.
        
        Args:
            extension: File extension (without the dot)
            pattern: Naming pattern with a placeholder for numbering (e.g., 'image_{:02d}')
        """
        # Remove dot from extension if provided
        extension = extension.lstrip('.')
        self.naming_patterns[extension.lower()] = pattern
    
    def set_default_pattern(self, pattern: str):
        """Set the default naming pattern for extensions without a specific pattern.
        
        Args:
            pattern: Default naming pattern with a placeholder for numbering
        """
        self.default_pattern = pattern
    
    def _get_files_by_extension(self, source_folder: Path, recursive: bool = False) -> Dict[str, List[Path]]:
        """Group files by their extensions.
        
        Args:
            source_folder: Folder containing files to process
            recursive: Whether to process subfolders
            
        Returns:
            Dictionary with extensions as keys and lists of file paths as values
        """
        files_by_ext = {}
        
        # Process files in the current folder
        for item in source_folder.iterdir():
            if item.is_file():
                extension = item.suffix.lstrip('.').lower()
                if extension not in files_by_ext:
                    files_by_ext[extension] = []
                files_by_ext[extension].append(item)
        
        # Process subfolders if recursive is True
        if recursive:
            for item in source_folder.iterdir():
                if item.is_dir():
                    subfolders_files = self._get_files_by_extension(item, recursive)
                    for ext, files in subfolders_files.items():
                        if ext not in files_by_ext:
                            files_by_ext[ext] = []
                        files_by_ext[ext].extend(files)
        
        return files_by_ext
    
    def organize_files(self, source_folder: str, recursive: bool = False, move: bool = False) -> Dict[str, int]:
        """Rename and organize all files in a folder according to their extensions.
        
        Args:
            source_folder: Folder containing files to organize
            recursive: Whether to process subfolders
            move: Whether to move files (True) or copy them (False)
            
        Returns:
            Dictionary with counts of files organized by extension
        """
        source_folder = Path(source_folder)
        if not source_folder.exists():
            print(f"Error: Folder {source_folder} does not exist")
            return {}
        
        # Get files grouped by extension
        files_by_ext = self._get_files_by_extension(source_folder, recursive)
        
        counts = {}
        
        # Process each extension group
        for ext, files in files_by_ext.items():
            # Sort files to ensure consistent ordering (optional)
            files.sort()
            
            # Determine the naming pattern to use
            pattern = self.naming_patterns.get(ext, self.default_pattern)
            
            # Process each file with sequential numbering
            for i, source_path in enumerate(files, 1):
                # Create the new filename using the pattern
                new_filename = pattern.format(i) + source_path.suffix
                new_path = self.folder_path / new_filename
                
                # Copy or move the file
                try:
                    if move:
                        shutil.move(str(source_path), str(new_path))
                        print(f"Moved {source_path} to {new_path}")
                    else:
                        shutil.copy2(str(source_path), str(new_path))
                        print(f"Copied {source_path} to {new_path}")
                    counts[ext] = counts.get(ext, 0) + 1
                except Exception as e:
                    print(f"Error organizing file {source_path}: {e}")
        
        return counts


def main():
    """Main function to run the Smart Filing System from command line."""
    parser = argparse.ArgumentParser(description="Smart Filing System")
    parser.add_argument("--target", "-t", required=True, help="Target folder where renamed files will be placed")
    parser.add_argument("--source", "-s", required=True, help="Source folder containing files to organize")
    parser.add_argument("--pattern", "-p", action="append", nargs=2, metavar=("EXT", "PATTERN"),
                        help="Set naming pattern for extension (e.g., jpg 'image_{:02d}')")
    parser.add_argument("--default", "-d", help="Default naming pattern (e.g., 'file_{:02d}')")
    parser.add_argument("--move", "-m", action="store_true", help="Move files instead of copying them")
    parser.add_argument("--recursive", "-r", action="store_true", help="Process folders recursively")
    
    args = parser.parse_args()
    
    # Create the filing system
    filing_system = SmartFilingSystem(args.target)
    
    # Set patterns
    if args.default:
        filing_system.set_default_pattern(args.default)
    
    if args.pattern:
        for ext, pattern in args.pattern:
            filing_system.set_naming_pattern(ext, pattern)
    
    # Process source folder
    counts = filing_system.organize_files(args.source, args.recursive, args.move)
    print("\nFiles organized:")
    for ext, count in counts.items():
        print(f"{ext}: {count} files")


# Example usage
if __name__ == "__main__":
    # Example with hard-coded values
    # filing = SmartFilingSystem("renamed_files")
    # filing.set_naming_pattern("jpg", "image_{:02d}")
    # filing.set_naming_pattern("png", "image_{:02d}")
    # filing.set_naming_pattern("txt", "ann_{:02d}")
    # filing.organize_files("source_folder")
    
    main()