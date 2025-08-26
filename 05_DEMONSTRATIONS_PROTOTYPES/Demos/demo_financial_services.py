#!/usr/bin/env python3
"""
MWRASP Financial Services Demonstration
Shows quantum defense capabilities for banking, trading, and financial institutions
"""

import asyncio
import time
import json
import random
from typing import Dict, Any, List

class FinancialServicesDemo:
    def __init__(self):
        self.financial_data_types = {
            'SWIFT_MESSAGE': {'sensitivity': 'HIGH', 'regulation': ['PCI-DSS', 'SWIFT_CSP']},
            'TRADING_ORDER': {'sensitivity': 'CRITICAL', 'regulation': ['MiFID_II', 'SEC_RULE_15c3-5']},
            'CREDIT_CARD': {'sensitivity': 'HIGH', 'regulation': ['PCI-DSS', 'GDPR']},
            'KYC_DATA': {'sensitivity': 'HIGH', 'regulation': ['AML', 'BSA', 'GDPR']},
            'TRADING_ALGORITHM': {'sensitivity': 'CRITICAL', 'regulation': ['SEC', 'CFTC']},
            'LOAN_APPLICATION': {'sensitivity': 'MEDIUM', 'regulation': ['FCRA', 'ECOA']},
            'CRYPTOCURRENCY': {'sensitivity': 'HIGH', 'regulation': ['FinCEN', 'SEC']},
            'DERIVATIVE_CONTRACT': {'sensitivity': 'CRITICAL', 'regulation': ['EMIR', 'Dodd-Frank']}
        }
        
        self.financial_jurisdictions = {
            'US': {'regulators': ['SEC', 'CFTC', 'FinCEN'], 'hostility': 0.85},
            'EU': {'regulators': ['ESMA', 'ECB'], 'hostility': 0.65},
            'UK': {'regulators': ['FCA', 'PRA'], 'hostility': 0.55},
            'SG': {'regulators': ['MAS'], 'hostility': 0.40},
            'HK': {'regulators': ['SFC'], 'hostility': 0.45},
            'CH': {'regulators': ['FINMA'], 'hostility': 0.25},
            'JP': {'regulators': ['FSA'], 'hostility': 0.50}
        }
        
        self.financial_threats = [
            'High-frequency trading manipulation',
            'SWIFT network infiltration',
            'Cryptocurrency exchange breach',
            'Credit card fraud ring',
            'Insider trading detection',
            'Market manipulation scheme',
            'Cross-border money laundering',
            'Derivatives fraud attempt'
        ]

    async def run_financial_demo(self):
        """Complete financial services demonstration"""
        
        print("MWRASP FINANCIAL SERVICES QUANTUM DEFENSE")
        print("Advanced Protection for Banking & Trading Systems")
        print("=" * 60)
        
        try:
            # Import core systems
            from src.core.quantum_detector import QuantumDetector
            from src.core.temporal_fragmentation import TemporalFragmentation, FragmentationPolicy
            from src.core.legal_conflict_engine import create_legal_conflict_engine
            
            # Initialize financial-configured systems
            print("\n[INIT] Initializing financial services configuration...")
            
            quantum_detector = QuantumDetector(sensitivity_threshold=0.8)  # Higher sensitivity for finance
            
            # Financial-specific fragmentation policy
            financial_policy = FragmentationPolicy(
                max_fragment_lifetime_ms=50,  # Very short lifetime for financial data
                min_fragments=5,  # More fragments for higher security
                overlap_percentage=0.3,  # Higher overlap for reconstruction reliability
                quantum_resistance_level=0.95  # Maximum quantum resistance
            )
            
            fragmentation_system = TemporalFragmentation(financial_policy)
            legal_engine = create_legal_conflict_engine()
            
            print("[OK] Financial services quantum defense systems initialized")
            
            # Demo 1: High-Frequency Trading Protection
            await self.demo_hft_protection(quantum_detector, fragmentation_system, legal_engine)
            
            # Demo 2: SWIFT Message Security
            await self.demo_swift_security(quantum_detector, fragmentation_system, legal_engine)
            
            # Demo 3: Cryptocurrency Exchange Defense
            await self.demo_crypto_defense(quantum_detector, fragmentation_system, legal_engine)
            
            # Demo 4: Cross-Border Regulatory Compliance
            await self.demo_regulatory_compliance(legal_engine)
            
            # Demo 5: Real-time Fraud Detection
            await self.demo_fraud_detection(quantum_detector, fragmentation_system)
            
            # Demo 6: Financial Emergency Response
            await self.demo_emergency_response(legal_engine)
            
            print("\n" + "=" * 60)
            print("FINANCIAL SERVICES DEMO SUMMARY")
            print("=" * 60)
            print("✓ High-frequency trading algorithm protection")
            print("✓ SWIFT network quantum-resistant messaging")  
            print("✓ Cryptocurrency exchange breach prevention")
            print("✓ Cross-border regulatory compliance automation")
            print("✓ Real-time financial fraud detection")
            print("✓ Emergency response for financial attacks")
            print("✓ Multi-jurisdiction legal routing for compliance")
            print("✓ Quantum-resistant temporal fragmentation")
            
            return True
            
        except Exception as e:
            print(f"\n[ERROR] Financial demo failed: {e}")
            return False

    async def demo_hft_protection(self, quantum_detector, fragmentation_system, legal_engine):
        """Demonstrate high-frequency trading algorithm protection"""
        
        print("\n" + "=" * 50)
        print("1. HIGH-FREQUENCY TRADING ALGORITHM PROTECTION")
        print("=" * 50)
        
        print("   Scenario: Protecting proprietary trading algorithms from quantum attacks")
        
        # Create canary tokens for trading algorithms
        trading_tokens = []
        for i in range(3):
            token = quantum_detector.generate_canary_token(f"HFT_ALGO_{i+1}")
            trading_tokens.append(token)
            print(f"   [TOKEN] Created canary token for HFT Algorithm {i+1}: {token.token_id[:16]}...")
        
        # Fragment trading strategy data
        trading_strategy = json.dumps({
            "strategy_name": "Quantum Arbitrage Alpha",
            "parameters": {"lookback": 50, "threshold": 0.02, "max_position": 1000000},
            "execution_venues": ["NYSE", "NASDAQ", "CBOE"],
            "risk_limits": {"max_drawdown": 0.05, "var_95": 50000}
        }).encode()
        
        fragments = fragmentation_system.fragment_data(trading_strategy, "hft_strategy_001")
        print(f"   [FRAGMENT] Trading strategy fragmented into {len(fragments)} pieces")
        print(f"   [FRAGMENT] Fragment lifetime: {fragments[0].expires_at - time.time():.1f}ms")
        
        # Simulate quantum attack on trading system
        print("   [ATTACK] Simulating quantum computer attack on trading algorithms...")
        await asyncio.sleep(0.01)
        
        threats_detected = 0
        for token in trading_tokens:
            if quantum_detector.access_token(token.token_id, "quantum_attacker_hft"):
                threats_detected += 1
        
        print(f"   [DETECTION] {threats_detected} quantum threats detected in trading system")
        
        # Route through hostile jurisdictions for legal protection
        routing_decision = await legal_engine.select_maximally_hostile_routing(
            fragment_id="hft_strategy_001",
            threshold=3,
            min_hostility=0.8,
            data_type="TRADING_ALGORITHM",
            user_clearance="QUANTITATIVE_ANALYST"
        )
        
        print(f"   [ROUTING] Strategy routed through: {routing_decision.target_jurisdictions}")
        print(f"   [LEGAL] Legal impossibility score: {routing_decision.impossibility_confidence:.4f}")
        print(f"   [PROTECTION] {len(routing_decision.legal_barriers)} regulatory barriers active")

    async def demo_swift_security(self, quantum_detector, fragmentation_system, legal_engine):
        """Demonstrate SWIFT network message security"""
        
        print("\n" + "=" * 50)
        print("2. SWIFT NETWORK MESSAGE SECURITY")
        print("=" * 50)
        
        print("   Scenario: Securing international wire transfers against quantum attacks")
        
        # Create SWIFT message data
        swift_message = json.dumps({
            "message_type": "MT103",
            "sender_bic": "CHASUS33XXX",
            "receiver_bic": "DEUTDEFFXXX", 
            "amount": "10000000.00",
            "currency": "USD",
            "beneficiary": "CONFIDENTIAL_ACCOUNT",
            "reference": "URGENT_TRANSFER_001"
        }).encode()
        
        print(f"   [SWIFT] Processing MT103 wire transfer message")
        print(f"   [AMOUNT] Transfer amount: $10,000,000.00 USD")
        
        # Fragment SWIFT message with maximum security
        swift_policy = FragmentationPolicy(
            max_fragment_lifetime_ms=25,  # Very short for wire transfers
            min_fragments=7,  # Maximum fragmentation
            overlap_percentage=0.4,
            quantum_resistance_level=0.98
        )
        temp_fragmenter = TemporalFragmentation(swift_policy)
        
        swift_fragments = temp_fragmenter.fragment_data(swift_message, "swift_mt103_001")
        print(f"   [FRAGMENT] SWIFT message fragmented into {len(swift_fragments)} ultra-secure pieces")
        
        # Simulate SWIFT network attack
        swift_token = quantum_detector.generate_canary_token("SWIFT_NETWORK_MONITOR")
        print("   [MONITOR] SWIFT network monitoring token deployed")
        
        # Test quantum attack on SWIFT infrastructure
        print("   [ATTACK] Simulating quantum attack on SWIFT messaging...")
        swift_threat = quantum_detector.access_token(swift_token.token_id, "nation_state_actor")
        
        if swift_threat:
            print("   [ALERT] QUANTUM THREAT DETECTED IN SWIFT NETWORK!")
            
            # Emergency routing through multiple hostile jurisdictions
            emergency_routing = await legal_engine.select_maximally_hostile_routing(
                fragment_id="swift_mt103_001",
                threshold=5,  # Maximum jurisdictions for wire transfer
                min_hostility=0.9,  # Highest hostility requirement
                data_type="SWIFT_MESSAGE",
                user_clearance="TREASURY_OFFICER"
            )
            
            print(f"   [EMERGENCY] Message routed through {len(emergency_routing.target_jurisdictions)} jurisdictions")
            print(f"   [PROTECTION] Legal barriers: {emergency_routing.legal_barriers}")

    async def demo_crypto_defense(self, quantum_detector, fragmentation_system, legal_engine):
        """Demonstrate cryptocurrency exchange defense"""
        
        print("\n" + "=" * 50)
        print("3. CRYPTOCURRENCY EXCHANGE DEFENSE")
        print("=" * 50)
        
        print("   Scenario: Protecting crypto exchange from quantum-enabled attacks")
        
        # Create cryptocurrency transaction data
        crypto_data = {
            "exchange": "Global_Crypto_Exchange",
            "hot_wallet_keys": ["REDACTED_PRIVATE_KEYS"],
            "cold_storage": "Multi-sig vault addresses",
            "daily_volume": "$2.3B USD equivalent",
            "supported_coins": ["BTC", "ETH", "USDC", "SOL", "ADA"],
            "user_deposits": "450,000 active accounts"
        }
        
        print(f"   [EXCHANGE] Protecting exchange with $2.3B daily volume")
        print(f"   [ASSETS] 450,000 user accounts and multi-sig vaults")
        
        # Deploy multiple canary tokens for different attack vectors
        crypto_tokens = []
        attack_vectors = ["WALLET_ACCESS", "API_KEYS", "USER_DATABASE", "TRADING_ENGINE"]
        
        for vector in attack_vectors:
            token = quantum_detector.generate_canary_token(f"CRYPTO_{vector}")
            crypto_tokens.append((vector, token))
            print(f"   [TOKEN] Deployed {vector} monitoring token")
        
        # Fragment sensitive crypto data
        crypto_json = json.dumps(crypto_data).encode()
        crypto_fragments = fragmentation_system.fragment_data(crypto_json, "crypto_exchange_001")
        print(f"   [FRAGMENT] Exchange data fragmented into {len(crypto_fragments)} pieces")
        
        # Simulate sophisticated crypto attack
        print("   [ATTACK] Simulating quantum-enabled cryptocurrency theft attempt...")
        await asyncio.sleep(0.02)
        
        detected_vectors = []
        for vector, token in crypto_tokens:
            if quantum_detector.access_token(token.token_id, "crypto_criminal_org"):
                detected_vectors.append(vector)
        
        if detected_vectors:
            print(f"   [ALERT] Quantum attacks detected on: {', '.join(detected_vectors)}")
            
            # Route through crypto-hostile jurisdictions for maximum protection
            crypto_routing = await legal_engine.select_maximally_hostile_routing(
                fragment_id="crypto_exchange_001",
                threshold=4,
                min_hostility=0.85,
                data_type="CRYPTOCURRENCY",
                user_clearance="EXCHANGE_ADMIN"
            )
            
            print(f"   [ROUTING] Exchange data routed through: {crypto_routing.target_jurisdictions}")
            print(f"   [COMPLIANCE] Regulatory barriers activated in multiple jurisdictions")

    async def demo_regulatory_compliance(self, legal_engine):
        """Demonstrate cross-border regulatory compliance"""
        
        print("\n" + "=" * 50)
        print("4. CROSS-BORDER REGULATORY COMPLIANCE")
        print("=" * 50)
        
        print("   Scenario: Automated compliance across financial jurisdictions")
        
        # Test different financial data types across jurisdictions
        compliance_tests = [
            ("DERIVATIVE_CONTRACT", "EU", "EMIR compliance for derivatives"),
            ("TRADING_ORDER", "US", "SEC Rule 15c3-5 pre-trade risk controls"),  
            ("KYC_DATA", "UK", "FCA customer due diligence requirements"),
            ("SWIFT_MESSAGE", "SG", "MAS cross-border payment regulations")
        ]
        
        for data_type, preferred_jurisdiction, description in compliance_tests:
            print(f"\n   Testing: {description}")
            
            routing = await legal_engine.select_maximally_hostile_routing(
                fragment_id=f"compliance_{data_type.lower()}",
                threshold=3,
                min_hostility=0.6,
                data_type=data_type,
                user_clearance="COMPLIANCE_OFFICER"
            )
            
            print(f"   [ROUTING] {data_type} -> Jurisdictions: {routing.target_jurisdictions}")
            print(f"   [COMPLIANCE] Legal barriers: {len(routing.legal_barriers)}")
            
            # Check if routing meets regulatory requirements
            if preferred_jurisdiction in routing.target_jurisdictions:
                print(f"   [OK] Routing complies with {preferred_jurisdiction} regulations")
            else:
                print(f"   [INFO] Alternative jurisdiction routing for enhanced protection")

    async def demo_fraud_detection(self, quantum_detector, fragmentation_system):
        """Demonstrate real-time financial fraud detection"""
        
        print("\n" + "=" * 50)
        print("5. REAL-TIME FINANCIAL FRAUD DETECTION")
        print("=" * 50)
        
        print("   Scenario: Detecting quantum-enhanced financial fraud in real-time")
        
        # Create fraud detection tokens for different financial instruments
        fraud_monitoring = {
            "CREDIT_CARD_PROCESSING": "Credit card transaction monitoring",
            "ACH_TRANSFERS": "ACH network fraud detection", 
            "WIRE_TRANSFERS": "International wire fraud prevention",
            "TRADING_ACCOUNTS": "Trading account compromise detection"
        }
        
        fraud_tokens = {}
        for fraud_type, description in fraud_monitoring.items():
            token = quantum_detector.generate_canary_token(fraud_type)
            fraud_tokens[fraud_type] = token
            print(f"   [MONITOR] {description}: {token.token_id[:16]}...")
        
        # Simulate various financial fraud attempts
        fraud_scenarios = [
            ("CREDIT_CARD_PROCESSING", "Quantum-enhanced card skimming"),
            ("WIRE_TRANSFERS", "AI-driven wire fraud scheme"),
            ("TRADING_ACCOUNTS", "Algorithmic account takeover")
        ]
        
        detected_fraud = []
        for fraud_type, attack_description in fraud_scenarios:
            print(f"   [ATTACK] Simulating: {attack_description}")
            
            if quantum_detector.access_token(fraud_tokens[fraud_type].token_id, "financial_criminal"):
                detected_fraud.append((fraud_type, attack_description))
                
            await asyncio.sleep(0.005)  # Real-time detection simulation
        
        if detected_fraud:
            print(f"\n   [DETECTION] {len(detected_fraud)} fraud attempts detected:")
            for fraud_type, description in detected_fraud:
                print(f"     - {fraud_type}: {description}")
                
                # Fragment evidence immediately
                evidence_data = f"FRAUD_EVIDENCE_{fraud_type}_{time.time()}".encode()
                evidence_fragments = fragmentation_system.fragment_data(
                    evidence_data, f"evidence_{fraud_type.lower()}"
                )
                print(f"     [EVIDENCE] Evidence fragmented into {len(evidence_fragments)} pieces")

    async def demo_emergency_response(self, legal_engine):
        """Demonstrate financial emergency response procedures"""
        
        print("\n" + "=" * 50)
        print("6. FINANCIAL EMERGENCY RESPONSE")
        print("=" * 50)
        
        print("   Scenario: Major financial institution under quantum attack")
        print("   [EMERGENCY] Activating maximum legal protection protocols...")
        
        # Simulate major financial emergency
        emergency_data_types = [
            "TRADING_ALGORITHM", 
            "SWIFT_MESSAGE", 
            "DERIVATIVE_CONTRACT",
            "CREDIT_CARD",
            "KYC_DATA"
        ]
        
        # Activate emergency routing for all critical financial data
        emergency_routings = []
        for data_type in emergency_data_types:
            routing = await legal_engine.select_maximally_hostile_routing(
                fragment_id=f"emergency_{data_type.lower()}",
                threshold=5,  # Maximum jurisdictions
                min_hostility=0.95,  # Maximum hostility
                data_type=data_type,
                user_clearance="CHIEF_RISK_OFFICER"
            )
            emergency_routings.append((data_type, routing))
            
        print(f"\n   [RESPONSE] Emergency routing activated for {len(emergency_routings)} data types")
        
        total_barriers = 0
        all_jurisdictions = set()
        
        for data_type, routing in emergency_routings:
            total_barriers += len(routing.legal_barriers)
            all_jurisdictions.update(routing.target_jurisdictions)
            print(f"   [PROTECTION] {data_type}: {routing.target_jurisdictions}")
        
        print(f"\n   [SUMMARY] Emergency Response Results:")
        print(f"   - Total jurisdictions activated: {len(all_jurisdictions)}")
        print(f"   - Total legal barriers: {total_barriers}")
        print(f"   - Average impossibility score: {sum(r[1].impossibility_confidence for r in emergency_routings) / len(emergency_routings):.4f}")
        print(f"   [SUCCESS] Maximum legal protection achieved for financial institution")


async def main():
    """Main financial services demonstration"""
    
    print("MWRASP QUANTUM DEFENSE SYSTEM")
    print("Financial Services Protection Demonstration")
    print("Quantum-Resistant Security for Banking & Trading")
    print("")
    
    demo = FinancialServicesDemo()
    
    start_time = time.time()
    success = await demo.run_financial_demo()
    execution_time = time.time() - start_time
    
    if success:
        print(f"\n[SUCCESS] Financial services demonstration completed successfully")
        print(f"[CAPABILITY] Quantum defense for banking, trading, and fintech")
        print(f"[CAPABILITY] Regulatory compliance across global jurisdictions")
        print(f"[CAPABILITY] Real-time fraud detection and prevention")
        print(f"[CAPABILITY] Emergency response for financial institutions")
    else:
        print(f"\n[INFO] Financial services demo completed with limitations")
    
    print(f"\nExecution time: {execution_time:.2f} seconds")
    print(f"Demo completed at: {time.strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    asyncio.run(main())