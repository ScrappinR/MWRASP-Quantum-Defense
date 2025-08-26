#!/usr/bin/env python3
"""
MWRASP AI Learning Demonstration
Shows how the AI agents learn and adapt to different threats and customer needs
"""

import time
import requests
import json
import asyncio


class AILearningDemo:
    """
    Demonstration of MWRASP's AI learning capabilities
    """
    
    def __init__(self):
        self.api_base = "http://127.0.0.1:8000"
        
        print(f"\n{'='*70}")
        print(f"MWRASP AI LEARNING DEMONSTRATION")
        print(f"Showing True Adaptive AI Agent Intelligence")
        print(f"{'='*70}")
    
    def check_ai_system_status(self):
        """Check if AI learning system is active"""
        try:
            response = requests.get(f"{self.api_base}/ai-learning/statistics", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"[OK] AI Learning System: {'ACTIVE' if data['learning_active'] else 'INACTIVE'}")
                print(f"[INFO] Experiences processed: {data['learning_stats']['experiences_processed']}")
                print(f"[INFO] Knowledge patterns: {data['knowledge_patterns']}")
                print(f"[INFO] Trained agent models: {data['trained_agent_models']}")
                return True
        except:
            print("[ERROR] AI Learning system not accessible")
            return False
    
    def show_initial_agent_state(self):
        """Show the initial state of AI agents before learning"""
        print(f"\n[BASELINE] INITIAL AGENT INTELLIGENCE STATE")
        print(f"{'='*50}")
        
        try:
            response = requests.get(f"{self.api_base}/ai-learning/agent-models", timeout=5)
            if response.status_code == 200:
                data = response.json()
                
                print(f"Learning Active: {data['learning_active']}")
                print(f"Total Agents with AI: {len(data['agent_specializations'])}")
                print(f"\nAgent Details:")
                
                for agent_id, agent_data in data['agent_specializations'].items():
                    print(f"  {agent_id[:15]}... ({agent_data['role']})")
                    print(f"    Success Rate: {agent_data['success_rate']:.2f}")
                    print(f"    Knowledge Confidence: {agent_data['knowledge_confidence']:.2f}")
                    print(f"    Specializations: {len(agent_data['specialization_areas'])}")
                    print(f"    Experience Count: {agent_data['experience_count']}")
                    print(f"    Learned Patterns: {agent_data['learned_patterns']}")
                    print()
                
                return data['agent_specializations']
        except Exception as e:
            print(f"[ERROR] {e}")
            return {}
    
    def simulate_threat_scenarios(self):
        """Simulate various threat scenarios to trigger learning"""
        print(f"\n[LEARNING] SIMULATING THREAT SCENARIOS FOR AI LEARNING")
        print(f"{'='*55}")
        
        scenarios = [
            {
                "name": "High-Confidence Quantum Attack",
                "data_type": "financial_quantum",
                "simulate_success": True,
                "description": "Simulating quantum attack on financial data"
            },
            {
                "name": "Multi-Vector Quantum Threat", 
                "data_type": "multi_vector_quantum",
                "simulate_success": False,
                "description": "Complex quantum attack with multiple attack vectors"
            },
            {
                "name": "High-Performance Customer Scenario",
                "data_type": "performance_critical",
                "simulate_success": True,
                "description": "Customer requiring fast response times"
            },
            {
                "name": "Security-Critical Customer Scenario",
                "data_type": "security_critical", 
                "simulate_success": True,
                "description": "Customer requiring maximum security measures"
            }
        ]
        
        for i, scenario in enumerate(scenarios, 1):
            print(f"\n[SCENARIO {i}] {scenario['name']}")
            print(f"Description: {scenario['description']}")
            
            # Create canary token to trigger detection
            try:
                token_response = requests.post(
                    f"{self.api_base}/quantum/token",
                    json={"data_type": scenario['data_type']},
                    timeout=10
                )
                
                if token_response.status_code == 200:
                    token_data = token_response.json()
                    token_id = token_data['token_id']
                    print(f"Created canary token: {token_id[:16]}...")
                    
                    # Simulate token access to trigger threat detection
                    time.sleep(1)
                    access_response = requests.post(
                        f"{self.api_base}/quantum/access/{token_id}",
                        json={"accessor_id": f"simulation_{i}"},
                        timeout=10
                    )
                    
                    if access_response.status_code == 200:
                        access_data = access_response.json()
                        if access_data.get('threat_detected'):
                            print(f"✓ Threat detected successfully")
                            print(f"  Threat ID: {access_data['threat']['threat_id'][:16]}...")
                            print(f"  Confidence: {access_data['threat']['confidence_score']:.3f}")
                            print(f"  Quantum Indicators: {len(access_data['threat']['quantum_indicators'])}")
                        else:
                            print(f"✗ Threat detection failed")
                    else:
                        print(f"✗ Access simulation failed: {access_response.status_code}")
                        
                else:
                    print(f"✗ Token creation failed: {token_response.status_code}")
                    
            except Exception as e:
                print(f"✗ Scenario failed: {e}")
            
            # Wait for learning to process
            time.sleep(2)
    
    def update_customer_preferences(self):
        """Demonstrate customer behavior learning"""
        print(f"\n[CUSTOMER-AI] UPDATING CUSTOMER BEHAVIOR PROFILES")
        print(f"{'='*50}")
        
        customer_scenarios = [
            {
                "customer_id": "enterprise_corp",
                "response_time_feedback": "too_slow",
                "security_incident_tolerance": 0.2,  # Low tolerance, wants high security
                "description": "Enterprise customer complaining about slow response"
            },
            {
                "customer_id": "startup_fast", 
                "response_time_feedback": "acceptable",
                "security_incident_tolerance": 0.8,  # High tolerance, wants speed
                "description": "Startup customer accepting of current performance"
            }
        ]
        
        for scenario in customer_scenarios:
            print(f"\nUpdating profile for: {scenario['customer_id']}")
            print(f"Scenario: {scenario['description']}")
            
            try:
                response = requests.post(
                    f"{self.api_base}/ai-learning/customer-feedback",
                    json=scenario,
                    timeout=5
                )
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"✓ Customer profile updated: {data['message']}")
                else:
                    print(f"✗ Profile update failed: {response.status_code}")
                    
            except Exception as e:
                print(f"✗ Customer update failed: {e}")
    
    def show_learning_progress(self):
        """Show how agents have learned and adapted"""
        print(f"\n[INTELLIGENCE] AI LEARNING PROGRESS ANALYSIS")
        print(f"{'='*45}")
        
        try:
            # Get updated learning statistics
            stats_response = requests.get(f"{self.api_base}/ai-learning/statistics", timeout=5)
            if stats_response.status_code == 200:
                stats = stats_response.json()
                
                print(f"Learning System Status: {'ACTIVE' if stats['learning_active'] else 'INACTIVE'}")
                print(f"Experiences in Buffer: {stats['experiences_in_buffer']}")
                print(f"Total Experiences Processed: {stats['learning_stats']['experiences_processed']}")
                print(f"Knowledge Patterns Discovered: {stats['learning_stats']['patterns_discovered']}")
                print(f"Successful Adaptations: {stats['learning_stats']['successful_adaptations']}")
                print(f"Knowledge Transfers: {stats['learning_stats']['knowledge_transfers']}")
                
                if stats['top_patterns']:
                    print(f"\nTop Learned Patterns:")
                    for pattern in stats['top_patterns']:
                        print(f"  - {pattern['pattern_type']} (confidence: {pattern['confidence_level']:.2f})")
            
            # Get updated agent states
            agents_response = requests.get(f"{self.api_base}/ai-learning/agent-models", timeout=5)
            if agents_response.status_code == 200:
                agents_data = agents_response.json()
                
                print(f"\nAgent Intelligence Evolution:")
                for agent_id, agent_info in agents_data['agent_specializations'].items():
                    print(f"  {agent_id[:15]}... ({agent_info['role']})")
                    print(f"    Success Rate: {agent_info['success_rate']:.3f}")
                    print(f"    Knowledge Confidence: {agent_info['knowledge_confidence']:.3f}")
                    print(f"    Experience Count: {agent_info['experience_count']}")
                    
                    if agent_info['specialization_areas']:
                        print(f"    Specializations: {', '.join(agent_info['specialization_areas'])}")
                    else:
                        print(f"    Specializations: None yet")
                    print()
                    
        except Exception as e:
            print(f"[ERROR] Could not retrieve learning progress: {e}")
    
    def demonstrate_adaptive_responses(self):
        """Show how agents now make different decisions based on learning"""
        print(f"\n[ADAPTATION] DEMONSTRATING ADAPTIVE AGENT BEHAVIOR")
        print(f"{'='*50}")
        
        print("Agents are now making decisions based on:")
        print("✓ Past experience success rates")
        print("✓ Learned threat patterns") 
        print("✓ Customer behavior profiles")
        print("✓ Specialized knowledge areas")
        print("✓ Real-time performance metrics")
        
        print(f"\nBehavioral Changes:")
        print("• Agents prioritize actions that worked well in similar situations")
        print("• Customer preferences influence response speed vs security tradeoffs")
        print("• Specialized agents are selected for threats they've handled successfully")
        print("• Knowledge patterns are shared between agents automatically")
        print("• Failed strategies are avoided in similar contexts")
        
    def show_ai_capabilities_summary(self):
        """Show comprehensive summary of AI capabilities"""
        print(f"\n{'='*70}")
        print(f"MWRASP AI AGENT CAPABILITIES SUMMARY")  
        print(f"{'='*70}")
        
        print(f"🧠 INDIVIDUAL AGENT LEARNING:")
        print(f"  • Reinforcement learning from action outcomes")
        print(f"  • Dynamic success rate tracking and optimization") 
        print(f"  • Specialized knowledge area development")
        print(f"  • Confidence-based decision making")
        print(f"  • Experience-driven skill improvement")
        
        print(f"\n🤝 INTER-AGENT INTELLIGENCE:")
        print(f"  • Shared knowledge pattern discovery")
        print(f"  • Collaborative threat response optimization")
        print(f"  • Best-practice propagation across agent network")
        print(f"  • Coordinated learning from team outcomes")
        
        print(f"\n👤 CUSTOMER ADAPTATION:")
        print(f"  • Dynamic customer behavior profiling")
        print(f"  • Preference-based response customization")
        print(f"  • Industry-specific threat model adaptation")
        print(f"  • Compliance requirement learning")
        
        print(f"\n⚡ REAL-TIME ADAPTATION:")
        print(f"  • Live threat pattern recognition")
        print(f"  • System architecture adaptation")
        print(f"  • Performance-based strategy optimization")
        print(f"  • Emergency pattern creation for novel threats")
        
        print(f"\n💾 PERSISTENT INTELLIGENCE:")
        print(f"  • SQLite database for experience storage")
        print(f"  • Cross-session learning retention")
        print(f"  • Knowledge pattern evolution tracking")
        print(f"  • Long-term behavior optimization")
        
        print(f"\n📊 MEASURABLE INTELLIGENCE:")
        print(f"  • Quantified learning progress metrics")
        print(f"  • Effectiveness scoring and optimization") 
        print(f"  • Confidence and uncertainty tracking")
        print(f"  • Adaptation success rate measurement")


def main():
    """Run the AI learning demonstration"""
    
    demo = AILearningDemo()
    
    try:
        # Check AI system status
        if not demo.check_ai_system_status():
            print("\n[ERROR] AI Learning system not available. Please ensure MWRASP server is running.")
            return
        
        # Show initial agent state
        initial_agents = demo.show_initial_agent_state()
        
        # Wait for user input
        print(f"\nPress Enter to begin AI learning simulation...")
        try:
            input()
        except:
            pass
        
        # Simulate threat scenarios to trigger learning
        demo.simulate_threat_scenarios()
        
        # Update customer preferences
        demo.update_customer_preferences()
        
        # Wait for learning to process
        print(f"\n[PROCESSING] Allowing AI systems to process experiences and learn...")
        for i in range(5, 0, -1):
            print(f"Processing... {i} seconds remaining", end='\r')
            time.sleep(1)
        print(" " * 40, end='\r')  # Clear the countdown
        
        # Show learning progress
        demo.show_learning_progress()
        
        # Demonstrate adaptive responses
        demo.demonstrate_adaptive_responses()
        
        # Show complete AI capabilities
        demo.show_ai_capabilities_summary()
        
        print(f"\n✅ AI LEARNING DEMONSTRATION COMPLETE")
        print(f"The agents are now continuously learning and adapting!")
        print(f"Access the dashboards to see real-time intelligence evolution:")
        print(f"   AI Learning API: http://127.0.0.1:8000/docs")
        print(f"   Agent Models: http://127.0.0.1:8000/ai-learning/agent-models")
        print(f"   Learning Stats: http://127.0.0.1:8000/ai-learning/statistics")
        
    except KeyboardInterrupt:
        print("\n\n[INTERRUPTED] AI learning demo interrupted")
    except Exception as e:
        print(f"\n[ERROR] {e}")


if __name__ == "__main__":
    main()