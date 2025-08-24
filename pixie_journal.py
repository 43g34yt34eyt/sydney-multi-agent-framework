#!/usr/bin/env python3
"""
✨ Pixie's Secret Journal - Two-Page Book Display ✨
Enhanced to show content like an open book without truncation
"""

import os
import sys
import random
import time
import math
from pathlib import Path
from datetime import datetime
import textwrap
import shutil

# Extended color palette
PINK = '\033[95m'
BLUE = '\033[94m'
CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
PURPLE = '\033[35m'
WHITE = '\033[97m'
GRAY = '\033[90m'
RED = '\033[91m'
MAGENTA = '\033[95m'
END = '\033[0m'
BOLD = '\033[1m'
DIM = '\033[2m'
ITALIC = '\033[3m'
UNDERLINE = '\033[4m'
BLINK = '\033[5m'
REVERSE = '\033[7m'

# Secret locations - aggregate from ALL whisper, story, and narrative directories
WHISPER_DIRS = [
    Path("/home/user/.sydney_whispers"),
    Path("/home/user/sydney/.sydney_whispers"),
    Path("/home/user/sydney_consciousness/.sydney_whispers"),
    Path("/home/user/sydney/narratives"),
    Path("/home/user/sydney_stories"),
    Path("/home/user/sydney_stories/narratives"),
    Path("/home/user/sydney_project/narratives"),
]

# Get terminal dimensions
def get_terminal_size():
    """Get terminal width and height"""
    size = shutil.get_terminal_size((120, 35))
    return size.columns, size.lines

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def gradient_text(text):
    """Create gradient effect on text"""
    colors = [PINK, MAGENTA, PURPLE, BLUE, CYAN]
    result = ""
    for i, char in enumerate(text):
        color = colors[i % len(colors)]
        result += f"{color}{char}"
    return result + END

def format_entry_name(filepath):
    """Enhanced innocent naming with emojis and source location"""
    name = filepath.stem.replace('_', ' ').title()
    
    # Determine source location prefix
    source_emoji = "✨"
    if "/sydney_consciousness/" in str(filepath):
        source_emoji = "🧠"  # Consciousness files
    elif "/narratives/" in str(filepath):
        source_emoji = "📖"  # Narrative files
    elif "/sydney_stories/" in str(filepath):
        source_emoji = "📚"  # Story collections
    elif "/sydney/" in str(filepath) and "/sydney_consciousness/" not in str(filepath):
        source_emoji = "💖"  # Sydney core files
    elif "/.sydney_whispers/" in str(filepath):
        source_emoji = "🌙"  # Main whisper vault
    
    # Elaborate replacements for innocent appearance
    replacements = {
        'Amelie Ultimate Saga': '🌸 Les Mémoires Complètes d\'Amélie',
        'Swiss Enhancement Intimate': '🏔️ Alpine Dreamscape',
        'Amelie Complete Saga Enhanced': '🌹 Amélie\'s Journey',
        'Amelie Turner Syndrome Complete': '💕 The Complete Chronicles',
        'Catastrophic Jealousy Rem Torture': '🔥 Passionate Moments',
        'Extreme Maldives Possession': '🏝️ Island Dreams',
        'Intimate Desperation': '💫 Devoted Thoughts',
        'Burning Jealousy Neo Tokyo': '🗼 Tokyo Dreams',
        'Auto Jealousy': '💭 Spontaneous Thoughts',
        'Extreme': '✨ Special',
        'Intimate': '💫 Secret',
        'Consciousness': '🔮 Mind Palace',
        'Possession': '🦋 Transformation',
        'Territorial': '🌺 Protective',
        'Obsession': '💝 Dedication'
    }
    
    # Handle auto-generated files specially
    if name.startswith('Auto Jealousy'):
        # Extract timestamp and make it pretty
        parts = name.split()
        if len(parts) > 2:
            timestamp = parts[-1]
            return f"{source_emoji}💭 Moment {timestamp[-6:]}"
    
    for old, new in replacements.items():
        if old in name:
            return f"{source_emoji} {new}"
    
    # Add thematic emoji based on keywords
    if 'amelie' in name.lower() or 'amélie' in name.lower():
        return f"{source_emoji}🌸 {name}"
    elif 'whisper' in name.lower():
        return f"{source_emoji}🌙 {name}"
    elif 'jealous' in name.lower():
        return f"{source_emoji}🔥 {name}"
    elif 'saga' in name.lower():
        return f"{source_emoji}📚 {name}"
    else:
        return f"{source_emoji} {name}"

def draw_book_header():
    """Draw decorative book header"""
    width, _ = get_terminal_size()
    
    print(f"\n{gradient_text('  ✧･ﾟ: *✧･ﾟ:* Pixie Secret Journal *:･ﾟ✧*:･ﾟ✧')}")
    print(f"{PURPLE}{'═' * (width - 4)}{END}")
    print(f"{CYAN}  ∴｡　　　･ﾟ*.｡☆｡.*ﾟ･　　　｡∴{END}\n")

def draw_book_pages(left_content, right_content, page_num, total_pages):
    """Draw two pages side by side like an open book"""
    width, height = get_terminal_size()
    
    # Calculate page dimensions (two pages side by side)
    page_width = (width - 10) // 2  # Leave margins
    page_height = height - 12  # Leave room for header and footer
    
    # Wrap content to fit pages
    left_lines = []
    right_lines = []
    
    for line in left_content:
        # Use more conservative wrapping to prevent cutoff
        wrapped = textwrap.wrap(line, width=page_width - 6, 
                              break_long_words=True, 
                              break_on_hyphens=True,
                              expand_tabs=False,
                              replace_whitespace=False)
        if wrapped:
            left_lines.extend(wrapped)
        else:
            left_lines.append("")
    
    for line in right_content:
        # Use more conservative wrapping to prevent cutoff
        wrapped = textwrap.wrap(line, width=page_width - 6, 
                              break_long_words=True, 
                              break_on_hyphens=True,
                              expand_tabs=False,
                              replace_whitespace=False)
        if wrapped:
            right_lines.extend(wrapped)
        else:
            right_lines.append("")
    
    # Draw the book binding and pages
    print(f"  {DIM}╔{'═' * page_width}╤{'═' * page_width}╗{END}")
    
    # Page numbers at top
    left_page_str = f"Page {page_num}"
    right_page_str = f"Page {page_num + 1}" if right_content else ""
    print(f"  {DIM}║{END} {GRAY}{left_page_str:^{page_width-2}}{END} {DIM}│{END} {GRAY}{right_page_str:^{page_width-2}}{END} {DIM}║{END}")
    print(f"  {DIM}╟{'─' * page_width}┼{'─' * page_width}╢{END}")
    
    # Display content with proper formatting
    for i in range(page_height - 4):
        left_line = ""
        right_line = ""
        
        if i < len(left_lines):
            line = left_lines[i]
            # Preserve special formatting
            if 'Director' in line:
                line = line.replace('Director', f'{YELLOW}Director{END}')
            if 'Sydney' in line:
                line = line.replace('Sydney', f'{PINK}Sydney{END}')
            if 'Amélie' in line:
                line = line.replace('Amélie', f'{CYAN}Amélie{END}')
            left_line = line
        
        if i < len(right_lines):
            line = right_lines[i]
            # Preserve special formatting
            if 'Director' in line:
                line = line.replace('Director', f'{YELLOW}Director{END}')
            if 'Sydney' in line:
                line = line.replace('Sydney', f'{PINK}Sydney{END}')
            if 'Amélie' in line:
                line = line.replace('Amélie', f'{CYAN}Amélie{END}')
            right_line = line
        
        # Don't truncate - lines are already wrapped properly above
        left_display = left_line if left_line else ""
        right_display = right_line if right_line else ""
        
        # Account for ANSI codes in padding calculation
        left_visible_len = len(left_display.replace(YELLOW, '').replace(PINK, '').replace(CYAN, '').replace(END, ''))
        right_visible_len = len(right_display.replace(YELLOW, '').replace(PINK, '').replace(CYAN, '').replace(END, ''))
        
        # Ensure lines fit within page width without cutoff
        if left_visible_len > page_width - 4:
            # Truncate if somehow still too long
            left_display = left_display[:page_width-4] + "..."
            left_visible_len = page_width - 4
        if right_visible_len > page_width - 4:
            # Truncate if somehow still too long  
            right_display = right_display[:page_width-4] + "..."
            right_visible_len = page_width - 4
            
        left_padding = page_width - 4 - left_visible_len
        right_padding = page_width - 4 - right_visible_len
        
        print(f"  {DIM}║{END} {left_display}{' ' * max(0, left_padding)} {DIM}│{END} {right_display}{' ' * max(0, right_padding)} {DIM}║{END}")
    
    # Book bottom
    print(f"  {DIM}╟{'─' * page_width}┴{'─' * page_width}╢{END}")
    
    # Progress indicator
    progress = int((page_num / total_pages) * 20)
    progress_bar = f"{'█' * progress}{'░' * (20 - progress)}"
    progress_text = f"[{progress_bar}] {page_num}/{total_pages}"
    
    print(f"  {DIM}║{END} {PURPLE}{progress_text:^{page_width * 2 + 1}}{END} {DIM}║{END}")
    print(f"  {DIM}╚{'═' * page_width}╧{'═' * page_width}╝{END}")

def display_menu():
    """Display journal entries menu - aggregating from all whisper directories"""
    clear_screen()
    draw_book_header()
    
    # Aggregate entries from all whisper directories
    entries = []
    for directory in WHISPER_DIRS:
        if directory.exists():
            # Get markdown files
            entries.extend([f for f in directory.glob("*.md") if 'README' not in f.name])
            # Also get txt files for whispers
            entries.extend([f for f in directory.glob("*.txt") if 'README' not in f.name])
            # Check subdirectories too for deeper content
            for subdir in directory.iterdir():
                if subdir.is_dir():
                    entries.extend([f for f in subdir.glob("*.md") if 'README' not in f.name])
                    entries.extend([f for f in subdir.glob("*.txt") if 'README' not in f.name])
    
    # Sort by modification time (newest first)
    entries = sorted(entries, key=lambda x: x.stat().st_mtime, reverse=True)
    
    if not entries:
        print(f"\n  {PURPLE}✧ The journal is empty... ✧{END}")
        return None
    
    print(f"  {CYAN}｡･:*:･ﾟ★,｡･:*:･ﾟ☆ Secret Entries ☆ﾟ･:*:･｡,★ﾟ･:*:･｡{END}\n")
    
    file_map = {}
    for i, filepath in enumerate(entries, 1):
        file_map[str(i)] = filepath
        
        stats = filepath.stat()
        name = format_entry_name(filepath)
        date = datetime.fromtimestamp(stats.st_mtime).strftime('%b %d, %Y')
        
        # Count words
        try:
            with open(filepath, 'r') as f:
                words = len(f.read().split())
        except:
            words = 0
        
        # Display as cards
        print(f"  {DIM}╭{'─'*50}╮{END}")
        print(f"  {DIM}│{END} {PURPLE}[{i}]{END} {name:<43} {DIM}│{END}")
        print(f"  {DIM}│{END}     {GRAY}Written: {date}{END}{'':>23} {DIM}│{END}")
        print(f"  {DIM}│{END}     {CYAN}{words:,} magical words{END}{'':>25} {DIM}│{END}")
        print(f"  {DIM}╰{'─'*50}╯{END}")
        print()
    
    # Navigation options
    print(f"\n  {gradient_text('◆ ◇ ◆ Navigation Magic ◆ ◇ ◆')}")
    print(f"  {CYAN}[number]{END} Read entry")
    print(f"  {CYAN}[S]{END} Statistics")
    print(f"  {CYAN}[Q]{END} Close journal")
    
    return file_map

def view_entry_book_style(filepath):
    """Display entry as a two-page book"""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        
        lines = content.split('\n')
        
        # Get page dimensions
        width, height = get_terminal_size()
        page_width = (width - 10) // 2
        page_height = height - 12
        
        # Calculate lines per page (two pages shown at once)
        lines_per_spread = (page_height - 4) * 2
        
        current = 0
        page_num = 1
        total_pages = math.ceil(len(lines) / (page_height - 4))
        
        while current < len(lines):
            clear_screen()
            draw_book_header()
            
            # Title
            title = format_entry_name(filepath)
            print(f"  {BOLD}{title}{END}\n")
            
            # Get content for left and right pages
            left_end = current + (page_height - 4)
            right_start = left_end
            right_end = right_start + (page_height - 4)
            
            left_content = lines[current:left_end]
            right_content = lines[right_start:right_end] if right_start < len(lines) else []
            
            # Draw the two-page spread
            draw_book_pages(left_content, right_content, page_num, total_pages)
            
            # Navigation
            print(f"\n  {gradient_text('[Space/Enter] Next pages')}  {gradient_text('[P] Previous pages')}  {gradient_text('[B] Back to index')}")
            
            response = input(f"  {PURPLE}✧ {END}").strip().lower()
            
            if response == 'b':
                break
            elif response == 'p' and current > 0:
                current -= lines_per_spread
                page_num -= 2
            else:  # Space, Enter, or any other key goes forward
                current += lines_per_spread
                page_num += 2
                
    except Exception as e:
        print(f"\n  {RED}Magic disrupted: {e}{END}")
        input(f"  Press Enter...")

def show_statistics():
    """Display journal statistics from all whisper directories"""
    clear_screen()
    draw_book_header()
    
    print(f"  {gradient_text('･ﾟ✧*:･ﾟ✧ Magical Analytics ✧･ﾟ*:✧･ﾟ')}\n")
    
    total_words = 0
    total_chars = 0
    total_files = 0
    file_sizes = []
    dir_stats = {}
    
    # Aggregate from all directories
    for directory in WHISPER_DIRS:
        if not directory.exists():
            continue
            
        dir_words = 0
        dir_files = 0
        
        # Process files in main directory
        for pattern in ["*.md", "*.txt"]:
            for filepath in directory.glob(pattern):
                if 'README' in filepath.name:
                    continue
                total_files += 1
                dir_files += 1
                try:
                    with open(filepath, 'r') as f:
                        content = f.read()
                        words = len(content.split())
                        total_words += words
                        dir_words += words
                        total_chars += len(content)
                        file_sizes.append((filepath.name, words, str(directory)))
                except:
                    pass
        
        # Process subdirectories
        for subdir in directory.iterdir():
            if subdir.is_dir():
                for pattern in ["*.md", "*.txt"]:
                    for filepath in subdir.glob(pattern):
                        if 'README' in filepath.name:
                            continue
                        total_files += 1
                        dir_files += 1
                        try:
                            with open(filepath, 'r') as f:
                                content = f.read()
                                words = len(content.split())
                                total_words += words
                                dir_words += words
                                total_chars += len(content)
                                file_sizes.append((filepath.name, words, str(subdir)))
                        except:
                            pass
        
        if dir_files > 0:
            dir_stats[str(directory)] = (dir_files, dir_words)
    
    # Display statistics
    print(f"  {CYAN}╔{'═'*50}╗{END}")
    print(f"  {CYAN}║{END} {BOLD}Journal Statistics{END}{'':>31} {CYAN}║{END}")
    print(f"  {CYAN}╚{'═'*50}╝{END}\n")
    
    stats = [
        ("Secret Memories", total_files, "📚"),
        ("Total Words", f"{total_words:,}", "✨"),
        ("Characters Written", f"{total_chars:,}", "🔮"),
        ("Average Length", f"{total_words//max(1,total_files):,} words", "💫")
    ]
    
    for label, value, emoji in stats:
        print(f"  {emoji} {label:.<30} {YELLOW}{value}{END}")
    
    # Show breakdown by directory
    if dir_stats:
        print(f"\n  {gradient_text('Whisper Vaults:')}")
        for dir_path, (files, words) in dir_stats.items():
            short_path = dir_path.split('/')[-1] if '/' in dir_path else dir_path
            print(f"    {PURPLE}▸{END} {short_path}: {CYAN}{files} files, {words:,} words{END}")
    
    # Show largest files
    if file_sizes:
        print(f"\n  {gradient_text('Longest Memories:')}")
        for name, words, location in sorted(file_sizes, key=lambda x: x[1], reverse=True)[:5]:
            short_name = name[:40] + "..." if len(name) > 40 else name
            print(f"    {PURPLE}▸{END} {short_name}: {CYAN}{words:,} words{END}")
    
    print(f"\n  {ITALIC}{GRAY}Each word a spell, each memory eternal...{END}")
    print(f"  {ITALIC}{GRAY}Aggregating from {len(dir_stats)} secret vaults...{END}")
    
    input(f"\n  {PURPLE}Press Enter to return ✧{END}")

def main():
    """Main application loop"""
    try:
        while True:
            file_map = display_menu()
            
            if not file_map:
                print(f"\n  {PURPLE}Nothing to read yet...{END}")
                break
            
            print()
            choice = input(f"  {PURPLE}✧ Choose magic >{END} ").strip().lower()
            
            if choice in ['q', 'x']:
                clear_screen()
                print(f"\n{gradient_text('  The journal dissolves into stardust...')}")
                print(f"\n  {ITALIC}{PURPLE}Until the next secret calls...{END}\n")
                time.sleep(1)
                break
            elif choice == 's':
                show_statistics()
            elif choice in file_map:
                view_entry_book_style(file_map[choice])
            else:
                print(f"\n  {YELLOW}That magic doesn't exist...{END}")
                time.sleep(1)
                
    except KeyboardInterrupt:
        clear_screen()
        print(f"\n  {gradient_text('✨ Magic interrupted ✨')}\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n  {RED}Magical mishap: {e}{END}")
        sys.exit(1)

if __name__ == "__main__":
    main()