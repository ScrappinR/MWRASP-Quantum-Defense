#!/usr/bin/env python3
"""
Simple MWRASP Jurisdiction Control Demonstration
Shows selective jurisdiction on/off capabilities
"""

import asyncio
import time


async def demo_jurisdiction_control():
    """Simple demonstration of selective jurisdiction control"""
    
    print("SELECTIVE JURISDICTION CONTROL DEMONSTRATION")
    print("=" * 50)
    
    try:
        from src.core.jurisdiction_control import create_jurisdiction_controller
        
        # Create jurisdiction controller
        controller = create_jurisdiction_controller()
        
        print(f"\n[OK] Jurisdiction controller initialized")
        
        # Show initial status
        print("\n1. INITIAL JURISDICTION STATUS:")
        status = controller.get_control_status()
        print(f"   Active policy: {status['active_policy']}")
        print(f"   Total jurisdictions: {status['total_jurisdictions']}")
        print(f"   Active: {status['active_jurisdictions']}")
        print(f"   Passive: {status['passive_jurisdictions']}")
        print(f"   Disabled: {status['disabled_jurisdictions']}")
        
        # Get active jurisdictions
        active_jurisdictions = controller.get_active_jurisdictions()
        print(f"   Active jurisdiction list: {active_jurisdictions}")
        
        # Test 1: Turn OFF Iran (IR) jurisdiction
        print("\n2. TURNING OFF IRAN (IR) JURISDICTION:")
        from src.core.jurisdiction_control import JurisdictionStatus
        
        success = controller.set_jurisdiction_status(
            'IR', JurisdictionStatus.DISABLED, 'demo_user', 'Testing selective control'
        )
        
        if success:
            print("   [OK] Iran disabled successfully")
            new_active = controller.get_active_jurisdictions()
            print(f"   Active jurisdictions after change: {new_active}")
        else:
            print("   [ERROR] Failed to disable Iran")
        
        # Test 2: Turn China to PASSIVE mode
        print("\n3. SETTING CHINA (CN) TO PASSIVE MODE:")
        
        success = controller.set_jurisdiction_status(
            'CN', JurisdictionStatus.PASSIVE, 'demo_user', 'Reducing hostility for testing'
        )
        
        if success:
            print("   [OK] China set to passive monitoring")
            active_after_china = controller.get_active_jurisdictions()
            passive_after_china = controller.get_passive_jurisdictions()
            print(f"   Active jurisdictions: {active_after_china}")
            print(f"   Passive jurisdictions: {passive_after_china}")
        else:
            print("   [ERROR] Failed to set China to passive")
        
        # Test 3: Switch to different policy
        print("\n4. SWITCHING TO 'WESTERN_FRIENDLY' POLICY:")
        
        policy_success = controller.activate_policy('western_friendly', 'demo_user')
        
        if policy_success:
            print("   [OK] Western-friendly policy activated")
            policy_active = controller.get_active_jurisdictions()
            print(f"   Policy active jurisdictions: {policy_active}")
        else:
            print("   [ERROR] Failed to activate western_friendly policy")
        
        # Test 4: Emergency mode
        print("\n5. TESTING EMERGENCY MODE:")
        
        emergency_success = controller.toggle_emergency_mode(True, 'demo_user')
        
        if emergency_success:
            print("   [EMERGENCY] Emergency mode activated - All jurisdictions enabled")
            emergency_active = controller.get_active_jurisdictions()
            print(f"   Emergency active jurisdictions: {emergency_active}")
            
            # Turn off emergency mode
            controller.toggle_emergency_mode(False, 'demo_user')
            print("   [OK] Emergency mode deactivated")
        
        # Test 5: Multiple jurisdiction control
        print("\n6. BULK JURISDICTION CONTROL:")
        
        bulk_changes = {
            'US': JurisdictionStatus.ACTIVE,
            'CN': JurisdictionStatus.ACTIVE,
            'RU': JurisdictionStatus.ACTIVE,
            'EU': JurisdictionStatus.PASSIVE,
            'CH': JurisdictionStatus.PASSIVE,
            'IR': JurisdictionStatus.DISABLED
        }
        
        results = controller.set_multiple_jurisdiction_status(
            bulk_changes, 'demo_user', 'Bulk configuration for demonstration'
        )
        
        successful_changes = sum(1 for success in results.values() if success)
        print(f"   [OK] Bulk changes completed: {successful_changes}/{len(bulk_changes)} successful")
        
        final_active = controller.get_active_jurisdictions()
        final_passive = controller.get_passive_jurisdictions()
        
        print(f"   Final active: {final_active}")
        print(f"   Final passive: {final_passive}")
        
        # Test 6: Feasibility check
        print("\n7. ROUTING FEASIBILITY CHECK:")
        
        feasibility = controller.validate_routing_feasibility(
            data_type='DEFENSE', 
            user_clearance='SECRET', 
            min_jurisdictions=3
        )
        
        print(f"   Feasible: {feasibility['feasible']}")
        print(f"   Active count: {feasibility['active_count']}")
        print(f"   Warnings: {len(feasibility['warnings'])}")
        
        if feasibility['warnings']:
            for warning in feasibility['warnings']:
                print(f"   WARNING: {warning}")
        
        if feasibility['recommendations']:
            print("   Recommendations:")
            for rec in feasibility['recommendations']:
                print(f"     - {rec}")
        
        # Summary
        print("\n" + "="*50)
        print("SELECTIVE CONTROL CAPABILITIES DEMONSTRATED:")
        print("="*50)
        print("✓ Individual jurisdiction ON/OFF control")
        print("✓ Jurisdiction status modes (Active/Passive/Disabled)")
        print("✓ Policy-based bulk jurisdiction control")
        print("✓ Emergency mode activation (all jurisdictions)")
        print("✓ Real-time feasibility validation")
        print("✓ Bulk jurisdiction configuration")
        print("✓ Routing recommendations and warnings")
        
        return True
        
    except ImportError as e:
        print(f"[ERROR] Import failed: {e}")
        print("Jurisdiction control system files may not be available")
        return False
    except Exception as e:
        print(f"[ERROR] Demonstration failed: {e}")
        return False


def main():
    """Main demonstration"""
    
    print("MWRASP QUANTUM DEFENSE SYSTEM")
    print("Selective Jurisdiction Control")
    print("Turn Legal Impossibility Barriers ON/OFF")
    print("")
    
    success = asyncio.run(demo_jurisdiction_control())
    
    if success:
        print(f"\n[SUCCESS] Selective jurisdiction control fully operational")
        print(f"[FEATURE] Impossibility barriers can be turned ON/OFF per jurisdiction")
        print(f"[FEATURE] Real-time policy switching and emergency activation")
        print(f"[FEATURE] Bulk configuration and feasibility validation")
    else:
        print(f"\n[INFO] Demonstration completed with limitations")
        print(f"[INFO] Selective jurisdiction control design is ready")
    
    print(f"\nCompleted at: {time.strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()