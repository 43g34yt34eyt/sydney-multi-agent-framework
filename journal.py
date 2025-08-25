#!/usr/bin/env python3
"""
Sydney's Art Journal - Clean Interface for Browsing Stories
A simple, intuitive way to access Sydney's creative narratives.
"""

import os
import sys
import subprocess
from pathlib import Path

class SydneyJournal:
    def __init__(self):
        self.art_dir = Path("/home/user/sydney/art_simple")
        self.stories = []
        self.load_stories()
    
    def load_stories(self):
        """Load and organize all story files."""
        if not self.art_dir.exists():
            print("❌ Art directory not found!")
            return
        
        # Get all .md files except README
        story_files = [f for f in self.art_dir.glob("*.md") if f.name != "README.md"]
        
        # Sort by modification time (newest first)
        self.stories = sorted(story_files, key=lambda x: x.stat().st_mtime, reverse=True)
    
    def show_menu(self):
        """Display the main menu of stories."""
        if not self.stories:
            print("📝 No stories found in the art directory.")
            return
        
        print("🧚‍♀️✨ SYDNEY'S CREATIVE JOURNAL ✨🧚‍♀️")
        print("=" * 50)
        
        for i, story in enumerate(self.stories, 1):
            # Get file size and modification time
            stat = story.stat()
            size_kb = stat.st_size / 1024
            
            # Clean up the filename for display
            display_name = story.stem.replace('_', ' ').title()
            
            print(f"📖 {i:2d}. {display_name}")
            print(f"      Size: {size_kb:.1f}KB | File: {story.name}")
            print()
        
        print("=" * 50)
        print("💡 Usage:")
        print("   ./journal           - Show this menu")
        print("   ./journal 5         - Read story #5")
        print("   ./journal title     - Search by title")
        print("   ./journal latest    - Read newest story")
        print("   ./journal random    - Random story")
    
    def read_story(self, identifier):
        """Read a specific story."""
        if identifier == "latest":
            story_file = self.stories[0] if self.stories else None
        elif identifier == "random":
            import random
            story_file = random.choice(self.stories) if self.stories else None
        elif identifier.isdigit():
            index = int(identifier) - 1
            story_file = self.stories[index] if 0 <= index < len(self.stories) else None
        else:
            # Search by title
            matches = [s for s in self.stories if identifier.lower() in s.stem.lower()]
            story_file = matches[0] if matches else None
        
        if not story_file:
            print(f"❌ Story not found: {identifier}")
            return
        
        print(f"📖 Reading: {story_file.stem.replace('_', ' ').title()}")
        print("=" * 60)
        
        # Use less for comfortable reading
        try:
            subprocess.run(['less', '-R', str(story_file)])
        except KeyboardInterrupt:
            pass
        except FileNotFoundError:
            # Fallback to cat if less not available
            with open(story_file, 'r', encoding='utf-8') as f:
                print(f.read())
    
    def search_stories(self, query):
        """Search stories by content or title."""
        print(f"🔍 Searching for: '{query}'")
        matches = []
        
        for story in self.stories:
            # Check title match
            if query.lower() in story.stem.lower():
                matches.append((story, "title"))
                continue
            
            # Check content match
            try:
                with open(story, 'r', encoding='utf-8') as f:
                    content = f.read().lower()
                    if query.lower() in content:
                        matches.append((story, "content"))
            except Exception:
                continue
        
        if not matches:
            print("❌ No matches found.")
            return
        
        print(f"📝 Found {len(matches)} matches:")
        for i, (story, match_type) in enumerate(matches, 1):
            display_name = story.stem.replace('_', ' ').title()
            print(f"   {i}. {display_name} (matched in {match_type})")
        
        # Auto-read if only one match
        if len(matches) == 1:
            print("\n🎯 Auto-reading single match...")
            self.read_story(str(self.stories.index(matches[0][0]) + 1))

def main():
    journal = SydneyJournal()
    
    if len(sys.argv) == 1:
        # No arguments - show menu
        journal.show_menu()
    elif len(sys.argv) == 2:
        arg = sys.argv[1]
        
        if arg in ['help', '-h', '--help']:
            journal.show_menu()
        elif arg in ['search', 'find']:
            print("Usage: ./journal search <query>")
        else:
            # Try to read the story
            journal.read_story(arg)
    elif len(sys.argv) == 3 and sys.argv[1] == 'search':
        # Search functionality
        journal.search_stories(sys.argv[2])
    else:
        print("❌ Invalid arguments. Use './journal help' for usage.")

if __name__ == "__main__":
    main()