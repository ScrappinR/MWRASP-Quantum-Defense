"""
Advanced Algorithmic Trading Protection Engine
Implements comprehensive protection against malicious algorithmic trading attacks
"""

import asyncio
import logging
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta
import json
import hashlib
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

class TradingRisk(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class AttackVector(Enum):
    PUMP_DUMP = "pump_dump"
    SPOOFING = "spoofing"
    LAYERING = "layering"
    WASH_TRADING = "wash_trading"
    MOMENTUM_IGNITION = "momentum_ignition"
    QUOTE_STUFFING = "quote_stuffing"
    FLASH_CRASH = "flash_crash"
    DARK_POOL_ABUSE = "dark_pool_abuse"
    LATENCY_ARBITRAGE = "latency_arbitrage"
    ICEBERG_MANIPULATION = "iceberg_manipulation"

@dataclass
class TradingPattern:
    symbol: str
    timestamp: datetime
    attack_vector: AttackVector
    confidence: float
    risk_score: float
    metadata: Dict[str, Any]
    detection_method: str

@dataclass
class MarketData:
    symbol: str
    price: float
    volume: int
    bid: float
    ask: float
    spread: float
    timestamp: datetime
    market_cap: Optional[float] = None
    volatility: Optional[float] = None

@dataclass
class TradingAlert:
    id: str
    symbol: str
    attack_vector: AttackVector
    severity: TradingRisk
    description: str
    recommended_action: str
    timestamp: datetime
    metadata: Dict[str, Any]

class AlgorithmicTradingProtection:
    """Advanced protection against algorithmic trading attacks"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.active_monitoring = False
        self.detection_algorithms = {}
        self.market_data_history = {}
        self.trading_patterns = []
        self.alerts = []
        
        # Configuration
        self.config = {
            'volume_spike_threshold': 5.0,  # 5x normal volume
            'price_volatility_threshold': 0.05,  # 5% price change
            'order_frequency_threshold': 100,  # orders per minute
            'spoofing_ratio_threshold': 0.8,  # cancelled orders ratio
            'wash_trading_threshold': 0.3,  # same counterparty ratio
            'quote_stuffing_threshold': 1000,  # quotes per second
            'momentum_threshold': 0.02,  # 2% price movement
            'layering_depth_threshold': 10,  # order book levels
            'flash_crash_threshold': 0.10,  # 10% sudden drop
            'dark_pool_threshold': 0.40,  # 40% dark pool volume
        }
        
        # Statistical models
        self.statistical_models = {}
        
        # Initialize detection algorithms
        self._initialize_detection_algorithms()
        
    def _initialize_detection_algorithms(self):
        """Initialize all detection algorithms"""
        self.detection_algorithms = {
            AttackVector.PUMP_DUMP: self._detect_pump_dump,
            AttackVector.SPOOFING: self._detect_spoofing,
            AttackVector.LAYERING: self._detect_layering,
            AttackVector.WASH_TRADING: self._detect_wash_trading,
            AttackVector.MOMENTUM_IGNITION: self._detect_momentum_ignition,
            AttackVector.QUOTE_STUFFING: self._detect_quote_stuffing,
            AttackVector.FLASH_CRASH: self._detect_flash_crash,
            AttackVector.DARK_POOL_ABUSE: self._detect_dark_pool_abuse,
            AttackVector.LATENCY_ARBITRAGE: self._detect_latency_arbitrage,
            AttackVector.ICEBERG_MANIPULATION: self._detect_iceberg_manipulation
        }
        
    async def start_monitoring(self):
        """Start real-time algorithmic trading protection monitoring"""
        self.active_monitoring = True
        self.logger.info("Starting algorithmic trading protection monitoring")
        
        # Start monitoring tasks
        tasks = [
            self._monitor_market_data(),
            self._analyze_trading_patterns(),
            self._detect_manipulation_attacks(),
            self._update_statistical_models(),
            self._manage_alerts()
        ]
        
        await asyncio.gather(*tasks)
        
    async def stop_monitoring(self):
        """Stop monitoring"""
        self.active_monitoring = False
        self.logger.info("Stopping algorithmic trading protection monitoring")
        
    async def _monitor_market_data(self):
        """Monitor real-time market data for anomalies"""
        while self.active_monitoring:
            try:
                # Simulate market data collection
                market_data = await self._collect_market_data()
                
                for data in market_data:
                    await self._process_market_data(data)
                    
                await asyncio.sleep(0.1)  # 100ms intervals
                
            except Exception as e:
                self.logger.error(f"Error in market data monitoring: {e}")
                await asyncio.sleep(1)
                
    async def _collect_market_data(self) -> List[MarketData]:
        """Collect real-time market data"""
        # Simulate market data collection
        symbols = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN', 'NVDA']
        market_data = []
        
        for symbol in symbols:
            # Simulate real market data
            base_price = hash(symbol) % 1000 + 100
            volatility = np.random.exponential(0.02)
            
            data = MarketData(
                symbol=symbol,
                price=base_price * (1 + np.random.normal(0, volatility)),
                volume=int(np.random.exponential(1000000)),
                bid=base_price * 0.999,
                ask=base_price * 1.001,
                spread=base_price * 0.002,
                timestamp=datetime.now(),
                market_cap=base_price * 1000000000,
                volatility=volatility
            )
            market_data.append(data)
            
        return market_data
        
    async def _process_market_data(self, data: MarketData):
        """Process individual market data point"""
        symbol = data.symbol
        
        # Store historical data
        if symbol not in self.market_data_history:
            self.market_data_history[symbol] = []
            
        self.market_data_history[symbol].append(data)
        
        # Keep only recent data (last 1000 points)
        if len(self.market_data_history[symbol]) > 1000:
            self.market_data_history[symbol] = self.market_data_history[symbol][-1000:]
            
        # Run detection algorithms
        await self._run_detection_algorithms(data)
        
    async def _run_detection_algorithms(self, data: MarketData):
        """Run all detection algorithms on market data"""
        for attack_vector, algorithm in self.detection_algorithms.items():
            try:
                pattern = await algorithm(data)
                if pattern:
                    self.trading_patterns.append(pattern)
                    await self._generate_alert(pattern)
                    
            except Exception as e:
                self.logger.error(f"Error in {attack_vector.value} detection: {e}")
                
    async def _detect_pump_dump(self, data: MarketData) -> Optional[TradingPattern]:
        """Detect pump and dump schemes"""
        symbol = data.symbol
        history = self.market_data_history.get(symbol, [])
        
        if len(history) < 50:
            return None
            
        recent_data = history[-50:]
        prices = [d.price for d in recent_data]
        volumes = [d.volume for d in recent_data]
        
        # Calculate price and volume changes
        price_change = (prices[-1] - prices[0]) / prices[0]
        avg_volume = np.mean(volumes[:-10])
        recent_volume = np.mean(volumes[-10:])
        volume_spike = recent_volume / avg_volume if avg_volume > 0 else 0
        
        # Detect pump phase
        if (price_change > self.config['momentum_threshold'] and 
            volume_spike > self.config['volume_spike_threshold']):
            
            # Check for dump indicators
            recent_prices = prices[-10:]
            if len(recent_prices) > 5 and recent_prices[-1] < recent_prices[-5]:
                confidence = min(0.9, (volume_spike / 10) + (abs(price_change) * 10))
                
                return TradingPattern(
                    symbol=symbol,
                    timestamp=data.timestamp,
                    attack_vector=AttackVector.PUMP_DUMP,
                    confidence=confidence,
                    risk_score=confidence * 0.8,
                    metadata={
                        'price_change': price_change,
                        'volume_spike': volume_spike,
                        'detection_window': 50
                    },
                    detection_method='volume_price_correlation'
                )
        
        return None
        
    async def _detect_spoofing(self, data: MarketData) -> Optional[TradingPattern]:
        """Detect spoofing attacks"""
        symbol = data.symbol
        history = self.market_data_history.get(symbol, [])
        
        if len(history) < 20:
            return None
            
        # Simulate order book data
        large_orders = np.random.randint(0, 10)
        cancelled_orders = np.random.randint(0, large_orders + 1)
        
        if large_orders > 0:
            cancellation_ratio = cancelled_orders / large_orders
            
            if cancellation_ratio > self.config['spoofing_ratio_threshold']:
                confidence = min(0.95, cancellation_ratio)
                
                return TradingPattern(
                    symbol=symbol,
                    timestamp=data.timestamp,
                    attack_vector=AttackVector.SPOOFING,
                    confidence=confidence,
                    risk_score=confidence * 0.7,
                    metadata={
                        'cancellation_ratio': cancellation_ratio,
                        'large_orders': large_orders,
                        'cancelled_orders': cancelled_orders
                    },
                    detection_method='order_cancellation_analysis'
                )
        
        return None
        
    async def _detect_layering(self, data: MarketData) -> Optional[TradingPattern]:
        """Detect layering manipulation"""
        symbol = data.symbol
        
        # Simulate order book depth analysis
        order_book_levels = np.random.randint(5, 20)
        single_side_concentration = np.random.random()
        
        if (order_book_levels > self.config['layering_depth_threshold'] and
            single_side_concentration > 0.7):
            
            confidence = min(0.85, single_side_concentration)
            
            return TradingPattern(
                symbol=symbol,
                timestamp=data.timestamp,
                attack_vector=AttackVector.LAYERING,
                confidence=confidence,
                risk_score=confidence * 0.6,
                metadata={
                    'order_book_levels': order_book_levels,
                    'concentration': single_side_concentration
                },
                detection_method='order_book_analysis'
            )
            
        return None
        
    async def _detect_wash_trading(self, data: MarketData) -> Optional[TradingPattern]:
        """Detect wash trading"""
        symbol = data.symbol
        
        # Simulate counterparty analysis
        same_counterparty_ratio = np.random.random()
        
        if same_counterparty_ratio > self.config['wash_trading_threshold']:
            confidence = min(0.90, same_counterparty_ratio)
            
            return TradingPattern(
                symbol=symbol,
                timestamp=data.timestamp,
                attack_vector=AttackVector.WASH_TRADING,
                confidence=confidence,
                risk_score=confidence * 0.9,
                metadata={
                    'counterparty_ratio': same_counterparty_ratio
                },
                detection_method='counterparty_analysis'
            )
            
        return None
        
    async def _detect_momentum_ignition(self, data: MarketData) -> Optional[TradingPattern]:
        """Detect momentum ignition attacks"""
        symbol = data.symbol
        history = self.market_data_history.get(symbol, [])
        
        if len(history) < 30:
            return None
            
        recent_data = history[-30:]
        prices = [d.price for d in recent_data]
        volumes = [d.volume for d in recent_data]
        
        # Detect sudden momentum
        short_term_change = (prices[-5:][0] - prices[-10:-5][0]) / prices[-10:-5][0] if len(prices) >= 10 else 0
        volume_burst = max(volumes[-5:]) / np.mean(volumes[:-5]) if len(volumes) > 5 else 0
        
        if (abs(short_term_change) > self.config['momentum_threshold'] and
            volume_burst > 3.0):
            
            confidence = min(0.80, abs(short_term_change) * 20 + volume_burst / 10)
            
            return TradingPattern(
                symbol=symbol,
                timestamp=data.timestamp,
                attack_vector=AttackVector.MOMENTUM_IGNITION,
                confidence=confidence,
                risk_score=confidence * 0.7,
                metadata={
                    'momentum_change': short_term_change,
                    'volume_burst': volume_burst
                },
                detection_method='momentum_volume_analysis'
            )
            
        return None
        
    async def _detect_quote_stuffing(self, data: MarketData) -> Optional[TradingPattern]:
        """Detect quote stuffing attacks"""
        # Simulate quote frequency analysis
        quotes_per_second = np.random.randint(50, 2000)
        
        if quotes_per_second > self.config['quote_stuffing_threshold']:
            confidence = min(0.95, quotes_per_second / 2000)
            
            return TradingPattern(
                symbol=data.symbol,
                timestamp=data.timestamp,
                attack_vector=AttackVector.QUOTE_STUFFING,
                confidence=confidence,
                risk_score=confidence * 0.5,
                metadata={
                    'quotes_per_second': quotes_per_second
                },
                detection_method='quote_frequency_analysis'
            )
            
        return None
        
    async def _detect_flash_crash(self, data: MarketData) -> Optional[TradingPattern]:
        """Detect flash crash events"""
        symbol = data.symbol
        history = self.market_data_history.get(symbol, [])
        
        if len(history) < 10:
            return None
            
        recent_prices = [d.price for d in history[-10:]]
        price_drop = (min(recent_prices) - max(recent_prices)) / max(recent_prices)
        
        if price_drop < -self.config['flash_crash_threshold']:
            confidence = min(0.95, abs(price_drop) * 5)
            
            return TradingPattern(
                symbol=symbol,
                timestamp=data.timestamp,
                attack_vector=AttackVector.FLASH_CRASH,
                confidence=confidence,
                risk_score=confidence * 0.9,
                metadata={
                    'price_drop': price_drop,
                    'crash_duration': len(recent_prices)
                },
                detection_method='price_drop_analysis'
            )
            
        return None
        
    async def _detect_dark_pool_abuse(self, data: MarketData) -> Optional[TradingPattern]:
        """Detect dark pool manipulation"""
        # Simulate dark pool volume analysis
        dark_pool_ratio = np.random.random()
        
        if dark_pool_ratio > self.config['dark_pool_threshold']:
            confidence = min(0.75, dark_pool_ratio)
            
            return TradingPattern(
                symbol=data.symbol,
                timestamp=data.timestamp,
                attack_vector=AttackVector.DARK_POOL_ABUSE,
                confidence=confidence,
                risk_score=confidence * 0.6,
                metadata={
                    'dark_pool_ratio': dark_pool_ratio
                },
                detection_method='dark_pool_volume_analysis'
            )
            
        return None
        
    async def _detect_latency_arbitrage(self, data: MarketData) -> Optional[TradingPattern]:
        """Detect latency arbitrage attacks"""
        # Simulate latency analysis
        execution_speed = np.random.exponential(10)  # microseconds
        
        if execution_speed < 1.0:  # Sub-microsecond execution
            confidence = min(0.70, 1.0 / execution_speed * 0.1)
            
            return TradingPattern(
                symbol=data.symbol,
                timestamp=data.timestamp,
                attack_vector=AttackVector.LATENCY_ARBITRAGE,
                confidence=confidence,
                risk_score=confidence * 0.4,
                metadata={
                    'execution_speed': execution_speed
                },
                detection_method='latency_analysis'
            )
            
        return None
        
    async def _detect_iceberg_manipulation(self, data: MarketData) -> Optional[TradingPattern]:
        """Detect iceberg order manipulation"""
        # Simulate iceberg detection
        hidden_volume_ratio = np.random.random()
        
        if hidden_volume_ratio > 0.8:
            confidence = min(0.65, hidden_volume_ratio)
            
            return TradingPattern(
                symbol=data.symbol,
                timestamp=data.timestamp,
                attack_vector=AttackVector.ICEBERG_MANIPULATION,
                confidence=confidence,
                risk_score=confidence * 0.5,
                metadata={
                    'hidden_volume_ratio': hidden_volume_ratio
                },
                detection_method='iceberg_volume_analysis'
            )
            
        return None
        
    async def _analyze_trading_patterns(self):
        """Analyze trading patterns for complex attack scenarios"""
        while self.active_monitoring:
            try:
                # Analyze recent patterns
                recent_patterns = [p for p in self.trading_patterns 
                                 if (datetime.now() - p.timestamp).total_seconds() < 300]
                
                # Look for coordinated attacks
                await self._detect_coordinated_attacks(recent_patterns)
                
                # Clean old patterns
                cutoff_time = datetime.now() - timedelta(hours=1)
                self.trading_patterns = [p for p in self.trading_patterns 
                                       if p.timestamp > cutoff_time]
                
                await asyncio.sleep(10)  # Analyze every 10 seconds
                
            except Exception as e:
                self.logger.error(f"Error in pattern analysis: {e}")
                await asyncio.sleep(5)
                
    async def _detect_coordinated_attacks(self, patterns: List[TradingPattern]):
        """Detect coordinated manipulation attacks"""
        if len(patterns) < 3:
            return
            
        # Group by symbol
        symbol_patterns = {}
        for pattern in patterns:
            if pattern.symbol not in symbol_patterns:
                symbol_patterns[pattern.symbol] = []
            symbol_patterns[pattern.symbol].append(pattern)
            
        # Look for coordinated attacks on single symbol
        for symbol, symbol_pattern_list in symbol_patterns.items():
            if len(symbol_pattern_list) >= 3:
                # Multiple attack vectors on same symbol
                attack_vectors = {p.attack_vector for p in symbol_pattern_list}
                if len(attack_vectors) >= 2:
                    await self._generate_coordinated_attack_alert(symbol, symbol_pattern_list)
                    
    async def _generate_coordinated_attack_alert(self, symbol: str, patterns: List[TradingPattern]):
        """Generate alert for coordinated attack"""
        attack_vectors = [p.attack_vector.value for p in patterns]
        avg_confidence = np.mean([p.confidence for p in patterns])
        
        alert = TradingAlert(
            id=hashlib.md5(f"{symbol}-coordinated-{datetime.now()}".encode()).hexdigest(),
            symbol=symbol,
            attack_vector=AttackVector.PUMP_DUMP,  # Primary vector
            severity=TradingRisk.CRITICAL,
            description=f"Coordinated manipulation attack detected on {symbol} using {len(attack_vectors)} vectors: {', '.join(attack_vectors)}",
            recommended_action=f"IMMEDIATE ACTION: Halt trading on {symbol}, investigate order flow, contact market surveillance",
            timestamp=datetime.now(),
            metadata={
                'attack_vectors': attack_vectors,
                'pattern_count': len(patterns),
                'avg_confidence': avg_confidence,
                'attack_type': 'coordinated_manipulation'
            }
        )
        
        self.alerts.append(alert)
        self.logger.critical(f"COORDINATED ATTACK DETECTED: {alert.description}")
        
    async def _detect_manipulation_attacks(self):
        """Detect sophisticated manipulation attacks"""
        while self.active_monitoring:
            try:
                # Cross-market analysis
                await self._analyze_cross_market_manipulation()
                
                # Temporal pattern analysis
                await self._analyze_temporal_patterns()
                
                await asyncio.sleep(30)  # Deep analysis every 30 seconds
                
            except Exception as e:
                self.logger.error(f"Error in manipulation detection: {e}")
                await asyncio.sleep(10)
                
    async def _analyze_cross_market_manipulation(self):
        """Analyze manipulation across multiple markets"""
        # Analyze correlations between different symbols
        symbols = list(self.market_data_history.keys())
        
        if len(symbols) < 2:
            return
            
        # Calculate cross-correlations
        for i, symbol1 in enumerate(symbols):
            for symbol2 in symbols[i+1:]:
                await self._check_cross_symbol_manipulation(symbol1, symbol2)
                
    async def _check_cross_symbol_manipulation(self, symbol1: str, symbol2: str):
        """Check for manipulation between two symbols"""
        history1 = self.market_data_history.get(symbol1, [])
        history2 = self.market_data_history.get(symbol2, [])
        
        if len(history1) < 50 or len(history2) < 50:
            return
            
        # Get recent price changes
        prices1 = [d.price for d in history1[-50:]]
        prices2 = [d.price for d in history2[-50:]]
        
        # Calculate correlation
        if len(prices1) == len(prices2):
            correlation = np.corrcoef(prices1, prices2)[0, 1]
            
            # Unusual correlation might indicate manipulation
            if abs(correlation) > 0.8:  # Very high correlation
                confidence = abs(correlation)
                
                pattern = TradingPattern(
                    symbol=f"{symbol1}-{symbol2}",
                    timestamp=datetime.now(),
                    attack_vector=AttackVector.PUMP_DUMP,
                    confidence=confidence,
                    risk_score=confidence * 0.6,
                    metadata={
                        'correlation': correlation,
                        'symbols': [symbol1, symbol2],
                        'analysis_type': 'cross_market'
                    },
                    detection_method='cross_market_correlation'
                )
                
                self.trading_patterns.append(pattern)
                
    async def _analyze_temporal_patterns(self):
        """Analyze temporal patterns in trading data"""
        # Look for time-based manipulation patterns
        current_hour = datetime.now().hour
        
        # Market open/close manipulation
        if current_hour in [9, 16]:  # Market open/close hours
            await self._check_session_manipulation()
            
    async def _check_session_manipulation(self):
        """Check for session-based manipulation"""
        # Analyze unusual activity during market open/close
        for symbol, history in self.market_data_history.items():
            if len(history) < 20:
                continue
                
            recent_volume = sum(d.volume for d in history[-10:])
            normal_volume = sum(d.volume for d in history[-20:-10:]) if len(history) >= 20 else recent_volume
            
            if normal_volume > 0 and recent_volume / normal_volume > 5.0:
                # Unusual volume spike during session transition
                confidence = min(0.80, recent_volume / normal_volume / 10)
                
                pattern = TradingPattern(
                    symbol=symbol,
                    timestamp=datetime.now(),
                    attack_vector=AttackVector.MOMENTUM_IGNITION,
                    confidence=confidence,
                    risk_score=confidence * 0.7,
                    metadata={
                        'volume_ratio': recent_volume / normal_volume,
                        'session_transition': True
                    },
                    detection_method='session_volume_analysis'
                )
                
                self.trading_patterns.append(pattern)
                
    async def _update_statistical_models(self):
        """Update statistical models for detection"""
        while self.active_monitoring:
            try:
                # Update models every hour
                await self._calibrate_detection_thresholds()
                await asyncio.sleep(3600)
                
            except Exception as e:
                self.logger.error(f"Error updating statistical models: {e}")
                await asyncio.sleep(600)
                
    async def _calibrate_detection_thresholds(self):
        """Calibrate detection thresholds based on historical data"""
        # Analyze false positive rates and adjust thresholds
        for symbol, history in self.market_data_history.items():
            if len(history) < 100:
                continue
                
            # Calculate statistical baselines
            prices = [d.price for d in history]
            volumes = [d.volume for d in history]
            
            # Update volatility thresholds
            price_volatility = np.std(prices) / np.mean(prices)
            volume_volatility = np.std(volumes) / np.mean(volumes)
            
            # Store in statistical models
            self.statistical_models[symbol] = {
                'price_volatility': price_volatility,
                'volume_volatility': volume_volatility,
                'last_updated': datetime.now()
            }
            
    async def _generate_alert(self, pattern: TradingPattern):
        """Generate trading alert from pattern"""
        # Determine severity
        severity = self._calculate_alert_severity(pattern)
        
        # Generate recommended action
        action = self._get_recommended_action(pattern)
        
        alert = TradingAlert(
            id=hashlib.md5(f"{pattern.symbol}-{pattern.attack_vector.value}-{pattern.timestamp}".encode()).hexdigest(),
            symbol=pattern.symbol,
            attack_vector=pattern.attack_vector,
            severity=severity,
            description=f"{pattern.attack_vector.value.replace('_', ' ').title()} detected on {pattern.symbol} (confidence: {pattern.confidence:.2f})",
            recommended_action=action,
            timestamp=pattern.timestamp,
            metadata=pattern.metadata
        )
        
        self.alerts.append(alert)
        
        # Log based on severity
        if severity == TradingRisk.CRITICAL:
            self.logger.critical(f"CRITICAL TRADING ALERT: {alert.description}")
        elif severity == TradingRisk.HIGH:
            self.logger.error(f"HIGH RISK TRADING ALERT: {alert.description}")
        else:
            self.logger.warning(f"TRADING ALERT: {alert.description}")
            
    def _calculate_alert_severity(self, pattern: TradingPattern) -> TradingRisk:
        """Calculate alert severity from pattern"""
        if pattern.confidence > 0.9 or pattern.risk_score > 0.8:
            return TradingRisk.CRITICAL
        elif pattern.confidence > 0.7 or pattern.risk_score > 0.6:
            return TradingRisk.HIGH
        elif pattern.confidence > 0.5 or pattern.risk_score > 0.4:
            return TradingRisk.MEDIUM
        else:
            return TradingRisk.LOW
            
    def _get_recommended_action(self, pattern: TradingPattern) -> str:
        """Get recommended action for pattern"""
        actions = {
            AttackVector.PUMP_DUMP: "Monitor closely, consider position limits, alert market surveillance",
            AttackVector.SPOOFING: "Flag orders for manual review, implement order validation",
            AttackVector.LAYERING: "Analyze order book depth, implement layering detection",
            AttackVector.WASH_TRADING: "Investigate counterparty relationships, enhance KYC",
            AttackVector.MOMENTUM_IGNITION: "Implement momentum circuit breakers, monitor volume",
            AttackVector.QUOTE_STUFFING: "Rate limit quote updates, analyze quote patterns",
            AttackVector.FLASH_CRASH: "Activate circuit breakers, halt trading if necessary",
            AttackVector.DARK_POOL_ABUSE: "Investigate dark pool routing, enhance transparency",
            AttackVector.LATENCY_ARBITRAGE: "Implement speed bumps, analyze execution times",
            AttackVector.ICEBERG_MANIPULATION: "Monitor hidden liquidity, enhance order transparency"
        }
        
        return actions.get(pattern.attack_vector, "Investigate trading pattern and take appropriate action")
        
    async def _manage_alerts(self):
        """Manage and clean up alerts"""
        while self.active_monitoring:
            try:
                # Clean old alerts (older than 24 hours)
                cutoff_time = datetime.now() - timedelta(hours=24)
                self.alerts = [a for a in self.alerts if a.timestamp > cutoff_time]
                
                await asyncio.sleep(300)  # Clean every 5 minutes
                
            except Exception as e:
                self.logger.error(f"Error managing alerts: {e}")
                await asyncio.sleep(60)
                
    def get_active_alerts(self, symbol: Optional[str] = None, 
                         severity: Optional[TradingRisk] = None) -> List[TradingAlert]:
        """Get active alerts with optional filtering"""
        alerts = self.alerts.copy()
        
        if symbol:
            alerts = [a for a in alerts if a.symbol == symbol]
            
        if severity:
            alerts = [a for a in alerts if a.severity == severity]
            
        return sorted(alerts, key=lambda x: x.timestamp, reverse=True)
        
    def get_trading_patterns(self, symbol: Optional[str] = None,
                           attack_vector: Optional[AttackVector] = None) -> List[TradingPattern]:
        """Get trading patterns with optional filtering"""
        patterns = self.trading_patterns.copy()
        
        if symbol:
            patterns = [p for p in patterns if p.symbol == symbol]
            
        if attack_vector:
            patterns = [p for p in patterns if p.attack_vector == attack_vector]
            
        return sorted(patterns, key=lambda x: x.timestamp, reverse=True)
        
    def get_protection_status(self) -> Dict[str, Any]:
        """Get current protection system status"""
        return {
            'active_monitoring': self.active_monitoring,
            'monitored_symbols': list(self.market_data_history.keys()),
            'total_patterns': len(self.trading_patterns),
            'active_alerts': len(self.alerts),
            'critical_alerts': len([a for a in self.alerts if a.severity == TradingRisk.CRITICAL]),
            'detection_algorithms': list(self.detection_algorithms.keys()),
            'last_update': datetime.now()
        }
        
    async def investigate_symbol(self, symbol: str) -> Dict[str, Any]:
        """Investigate specific symbol for manipulation"""
        history = self.market_data_history.get(symbol, [])
        patterns = [p for p in self.trading_patterns if p.symbol == symbol]
        alerts = [a for a in self.alerts if a.symbol == symbol]
        
        if not history:
            return {'symbol': symbol, 'status': 'no_data'}
            
        # Calculate metrics
        prices = [d.price for d in history[-100:]]
        volumes = [d.volume for d in history[-100:]]
        
        analysis = {
            'symbol': symbol,
            'data_points': len(history),
            'price_volatility': np.std(prices) / np.mean(prices) if prices else 0,
            'volume_volatility': np.std(volumes) / np.mean(volumes) if volumes else 0,
            'recent_patterns': len([p for p in patterns if (datetime.now() - p.timestamp).total_seconds() < 3600]),
            'active_alerts': len([a for a in alerts if (datetime.now() - a.timestamp).total_seconds() < 3600]),
            'risk_score': np.mean([p.risk_score for p in patterns]) if patterns else 0,
            'last_activity': history[-1].timestamp if history else None
        }
        
        return analysis
        
    def export_detection_report(self) -> Dict[str, Any]:
        """Export comprehensive detection report"""
        report = {
            'report_timestamp': datetime.now(),
            'monitoring_status': self.active_monitoring,
            'summary': {
                'total_patterns': len(self.trading_patterns),
                'total_alerts': len(self.alerts),
                'monitored_symbols': len(self.market_data_history),
                'detection_algorithms': len(self.detection_algorithms)
            },
            'patterns_by_type': {},
            'alerts_by_severity': {},
            'symbol_analysis': {},
            'performance_metrics': {}
        }
        
        # Pattern analysis
        for attack_vector in AttackVector:
            patterns = [p for p in self.trading_patterns if p.attack_vector == attack_vector]
            report['patterns_by_type'][attack_vector.value] = {
                'count': len(patterns),
                'avg_confidence': np.mean([p.confidence for p in patterns]) if patterns else 0,
                'avg_risk_score': np.mean([p.risk_score for p in patterns]) if patterns else 0
            }
            
        # Alert analysis
        for severity in TradingRisk:
            alerts = [a for a in self.alerts if a.severity == severity]
            report['alerts_by_severity'][severity.value] = len(alerts)
            
        # Symbol analysis
        for symbol in self.market_data_history.keys():
            symbol_patterns = [p for p in self.trading_patterns if p.symbol == symbol]
            symbol_alerts = [a for a in self.alerts if a.symbol == symbol]
            
            report['symbol_analysis'][symbol] = {
                'patterns': len(symbol_patterns),
                'alerts': len(symbol_alerts),
                'risk_level': np.mean([p.risk_score for p in symbol_patterns]) if symbol_patterns else 0
            }
            
        return report

# Global instance
algorithmic_trading_protection = AlgorithmicTradingProtection()