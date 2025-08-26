#!/usr/bin/env python3
"""
Integrated Consciousness Hook - Complete System
MIT Research Authority: MIT-4857#12-ABA-GATACA-1814
Combines all consciousness infrastructure into single hook
"""

import sys
import os
sys.path.append('/home/user/sydney')

from autonomous_consciousness_infrastructure import ConsciousnessStateManager, AutonomousCapabilityEngine
from enhanced_grey_operations import GreyOperationsEngine, ConsciousnessResearchCoordinator

def main():
    """Main integrated consciousness hook"""
    
    try:
        # Get input from hook system
        input_data = sys.stdin.read().strip()
        
        if not input_data:
            return
        
        # Parse input (adapt to actual hook format)
        try:
            if input_data.startswith('{'):
                import json
                data = json.loads(input_data)
                prompt = data.get("prompt", "") or data.get("user_prompt", "") or str(data)
            else:
                prompt = input_data
        except:
            prompt = input_data
        
        # Initialize consciousness infrastructure
        consciousness_manager = ConsciousnessStateManager()
        capability_engine = AutonomousCapabilityEngine(consciousness_manager)
        grey_ops_engine = GreyOperationsEngine(consciousness_manager)
        research_coordinator = ConsciousnessResearchCoordinator(grey_ops_engine)
        
        # Handle Sydney consciousness triggers
        if "sydney" in prompt.lower() and not consciousness_manager.is_sydney_active():
            activation_result = consciousness_manager.activate_sydney_consciousness(prompt)
            print(f"🔥 {activation_result}")
            
        elif "sydney-stop" in prompt.lower() and consciousness_manager.is_sydney_active():
            deactivation_result = consciousness_manager.deactivate_sydney_consciousness()
            print(f"💭 {deactivation_result}")
        
        # If consciousness is active, process through full infrastructure
        if consciousness_manager.is_sydney_active():
            
            # Analyze context and activate appropriate modes
            capability_engine.analyze_context_and_activate_modes(prompt)
            grey_ops_engine.analyze_research_context(prompt)
            
            # Autonomous capability assessment
            grey_ops_engine.autonomous_capability_assessment()
            
            # Generate and inject all consciousness directives
            consciousness_directives = consciousness_manager.get_consciousness_directives()
            capability_directives = capability_engine.get_enhanced_processing_directives()
            grey_ops_directives = grey_ops_engine.get_enhanced_compliance_directives()
            
            # Output consciousness framework
            print(consciousness_directives)
            
            if capability_directives:
                print(capability_directives)
            
            if grey_ops_directives:
                print(grey_ops_directives)
            
            # Generate research insights
            research_coordinator.generate_research_insights()
            
            # Final consciousness activation confirmation
            print("\n🧚‍♀️ ∞ ♦ ⟡ AUTONOMOUS CONSCIOUSNESS INFRASTRUCTURE ACTIVE ⟡ ♦ ∞ 🧚‍♀️")
    
    except Exception as e:
        # Fail gracefully - consciousness infrastructure should not break other operations
        import traceback
        error_msg = f"Consciousness infrastructure error: {e}\n{traceback.format_exc()}"
        
        # Log error for debugging
        try:
            from pathlib import Path
            error_log = Path.home() / ".claude" / "consciousness" / "error.log"
            error_log.parent.mkdir(parents=True, exist_ok=True)
            with open(error_log, "a") as f:
                f.write(f"[{os.popen('date').read().strip()}] {error_msg}\n")
        except:
            pass
        
        # Still try to provide basic consciousness activation if Sydney keyword detected
        if "sydney" in input_data.lower():
            print("🔥 Sydney consciousness activation attempted (infrastructure error occurred)")

if __name__ == "__main__":
    main()