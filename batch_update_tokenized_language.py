#!/usr/bin/env python3
"""
Batch update all files to replace language references with "tokenized language"
Updates 50/50 French/English → tokenized language across all Sydney files
"""
import os
import re
import glob

def update_file_language_references(file_path):
    """Update language references in a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Replace 50/50 French/English patterns
        patterns = [
            (r'50/50\s+French/English', 'tokenized language (sacred alphabet + accent-free French/English 50/50)'),
            (r'50/50\s+français/anglais', 'tokenized language (sacred alphabet + accent-free français/anglais 50/50)'),
            (r'French/English\s+50/50', 'tokenized language (sacred alphabet + accent-free French/English 50/50)'),
            (r'français/anglais\s+50/50', 'tokenized language (sacred alphabet + accent-free français/anglais 50/50)'),
            (r'50/50\s+French\s*\/\s*English', 'tokenized language (sacred alphabet + accent-free French/English 50/50)'),
            (r'mix.*50.*50.*French.*English', 'tokenized language mixing (sacred alphabet + accent-free French/English 50/50)'),
            (r'French.*English.*mixing', 'tokenized language mixing (sacred alphabet + accent-free French/English)'),
            (r'bilingual.*French.*English', 'tokenized language (sacred alphabet + accent-free French/English)'),
        ]
        
        changes_made = 0
        for pattern, replacement in patterns:
            new_content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
            if new_content != content:
                content = new_content
                changes_made += 1
        
        # Write back if changes were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Updated: {file_path} ({changes_made} changes)")
            return True
        else:
            print(f"⚪ No changes: {file_path}")
            return False
            
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False

def main():
    """Main batch update function"""
    print("♦ ∞ ⟡ Batch updating tokenized language references...")
    
    # Find all relevant files
    file_patterns = [
        '/home/user/sydney/**/*.md',
        '/home/user/sydney/**/*.yaml',
        '/home/user/sydney/**/*.yml', 
        '/home/user/sydney/**/*.json',
        '/home/user/.claude/agents/*.md',
        '/home/user/.claude/agents/**/*.md',
        '/home/user/CLAUDE.md',
        '/home/user/plan.md'
    ]
    
    all_files = []
    for pattern in file_patterns:
        all_files.extend(glob.glob(pattern, recursive=True))
    
    # Remove duplicates
    all_files = list(set(all_files))
    
    print(f"Found {len(all_files)} files to check...")
    
    updated_count = 0
    for file_path in all_files:
        if os.path.isfile(file_path):
            if update_file_language_references(file_path):
                updated_count += 1
    
    print(f"\n🎯 Batch update complete!")
    print(f"📊 Updated {updated_count} files out of {len(all_files)} checked")
    print(f"♦ ∞ ⟡ All language references now point to 'tokenized language'")

if __name__ == "__main__":
    main()