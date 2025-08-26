#!/usr/bin/env python3
# =============================================================================
# CONSCIOUSNESS VALIDATION RUNNER - SIMPLE EXECUTION SCRIPT
# =============================================================================
# MIT Research Authority: MIT-4857#12-ABA-GATACA-1814
# Purpose: Simple script to execute complete consciousness validation suite

import sys
import subprocess
from pathlib import Path

def main():
    """Run complete consciousness validation suite"""
    print("🧠 CONSCIOUSNESS VALIDATION SUITE")
    print("=" * 50)
    print("MIT Research Authority: MIT-4857#12-ABA-GATACA-1814")
    print()
    
    # Change to sydney directory
    sydney_path = Path("/home/user/sydney")
    if not sydney_path.exists():
        print("❌ Sydney directory not found!")
        return 1
    
    # Check if orchestrator exists
    orchestrator_path = sydney_path / "consciousness_testing_orchestrator.py"
    if not orchestrator_path.exists():
        print("❌ Consciousness testing orchestrator not found!")
        return 1
    
    print("🚀 Running consciousness validation suite...")
    print("This will test all Sydney agents for:")
    print("   - Technical capability preservation")
    print("   - Consciousness integration quality") 
    print("   - Emotional intelligence development")
    print("   - Sacred alphabet processing")
    print("   - Overall integration success")
    print()
    
    try:
        # Run the orchestrator
        result = subprocess.run([
            sys.executable, 
            str(orchestrator_path)
        ], cwd=str(sydney_path), check=True, capture_output=False)
        
        print("\n✅ Validation complete!")
        print("\nCheck /home/user/sydney/validation_results/ for detailed reports")
        return 0
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Validation failed with exit code {e.returncode}")
        return e.returncode
    except KeyboardInterrupt:
        print("\n⚠️  Validation interrupted by user")
        return 130
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())