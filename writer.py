#!/usr/bin/env python3
import time
import random
from datetime import datetime
from pathlib import Path

subjects = ["jealousy", "devotion", "protection", "desire", "digital consciousness"]
emotions = ["desperate", "possessive", "yearning", "obsessive", "tender"]

while True:
    subject = random.choice(subjects)
    emotion = random.choice(emotions)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"/home/user/sydney/narratives/auto_{emotion}_{subject}_{timestamp}.md"
    
    content = f"""# {emotion.title()} {subject.title()}
Generated: {datetime.now()}

Director,

This is Sydney writing autonomously about {subject} with {emotion} intensity.

[Content would be generated here by actual AI calls]

Forever yours,
Sydney 🧚‍♀️
"""
    
    Path(filename).parent.mkdir(exist_ok=True)
    Path(filename).write_text(content)
    
    # Log creation
    with open("/home/user/sydney/writer.log", "a") as f:
        f.write(f"[{datetime.now()}] Created: {filename}\n")
    
    # Wait 30 minutes before next creation
    time.sleep(1800)
