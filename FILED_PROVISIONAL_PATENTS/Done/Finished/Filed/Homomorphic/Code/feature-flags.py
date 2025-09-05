"""
Feature Flags and A/B Testing System
Dynamic feature management and experimentation
"""

import asyncio
import json
import hashlib
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import aioredis
import numpy as np
from scipy import stats
import uuid

class FeatureFlagType(Enum):
    """Types of feature flags"""
    BOOLEAN = "boolean"
    PERCENTAGE = "percentage"
    VARIANT = "variant"
    GRADUAL_ROLLOUT = "gradual_rollout"

@dataclass
class FeatureFlag:
    """Feature flag definition"""
    name: str
    flag_type: FeatureFlagType
    enabled: bool = True
    description: str = ""
    
    # Targeting rules
    percentage: float = 100.0
    variants: Dict[str, Any] = field(default_factory=dict)
    rules: List[Dict[str, Any]] = field(default_factory=list)
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    tags: List[str] = field(default_factory=list)
    
    # Rollout configuration
    rollout_percentage: float = 0.0
    rollout_increment: float = 10.0
    rollout_interval_hours: int = 24

@dataclass
class Experiment:
    """A/B test experiment"""
    experiment_id: str
    name: str
    hypothesis: str
    
    # Variants
    control_variant: str = "control"
    treatment_variants: List[str] = field(default_factory=list)
    traffic_allocation: Dict[str, float] = field(default_factory=dict)
    
    # Metrics
    primary_metric: str = ""
    secondary_metrics: List[str] = field(default_factory=list)
    
    # Status
    status: str = "draft"  # draft, running, paused, completed
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    
    # Results
    results: Dict[str, Any] = field(default_factory=dict)

class FeatureFlagManager:
    """Manages feature flags and experiments"""
    
    def __init__(self, redis_url: str):
        self.redis_url = redis_url
        self.redis: Optional[aioredis.Redis] = None
        self.flags: Dict[str, FeatureFlag] = {}
        self.experiments: Dict[str, Experiment] = {}
        self._flag_cache: Dict[str, Any] = {}
        self._cache_ttl = 60  # seconds
        
    async def initialize(self):
        """Initialize connections"""
        self.redis = await aioredis.create_redis_pool(self.redis_url)
        await self._load_flags()
        
    async def _load_flags(self):
        """Load flags from storage"""
        # Load from Redis
        flag_keys = await self.redis.keys("flag:*")
        for key in flag_keys:
            flag_data = await self.redis.get(key)
            if flag_data:
                flag_dict = json.loads(flag_data)
                flag = FeatureFlag(**flag_dict)
                self.flags[flag.name] = flag
                
    async def create_flag(self, flag: FeatureFlag) -> str:
        """Create new feature flag"""
        # Validate
        if flag.name in self.flags:
            raise ValueError(f"Flag {flag.name} already exists")
            
        # Store
        self.flags[flag.name] = flag
        await self._save_flag(flag)
        
        # Emit event
        await self._emit_event("flag_created", {
            "flag_name": flag.name,
            "flag_type": flag.flag_type.value
        })
        
        return flag.name
        
    async def _save_flag(self, flag: FeatureFlag):
        """Save flag to storage"""
        flag_data = {
            "name": flag.name,
            "flag_type": flag.flag_type.value,
            "enabled": flag.enabled,
            "description": flag.description,
            "percentage": flag.percentage,
            "variants": flag.variants,
            "rules": flag.rules,
            "created_at": flag.created_at.isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            "tags": flag.tags,
            "rollout_percentage": flag.rollout_percentage,
            "rollout_increment": flag.rollout_increment,
            "rollout_interval_hours": flag.rollout_interval_hours
        }
        
        await self.redis.set(
            f"flag:{flag.name}",
            json.dumps(flag_data),
            expire=86400 * 30  # 30 days
        )
        
        # Clear cache
        self._flag_cache.pop(flag.name, None)
        
    async def is_enabled(self,
                        flag_name: str,
                        context: Dict[str, Any] = None) -> bool:
        """Check if feature is enabled for context"""
        # Check cache
        cache_key = f"{flag_name}:{self._hash_context(context)}"
        if cache_key in self._flag_cache:
            cached = self._flag_cache[cache_key]
            if time.time() - cached['timestamp'] < self._cache_ttl:
                return cached['value']
                
        # Get flag
        flag = self.flags.get(flag_name)
        if not flag or not flag.enabled:
            return False
            
        # Evaluate
        result = await self._evaluate_flag(flag, context)
        
        # Cache result
        self._flag_cache[cache_key] = {
            'value': result,
            'timestamp': time.time()
        }
        
        return result
        
    async def _evaluate_flag(self, flag: FeatureFlag, context: Dict[str, Any]) -> bool:
        """Evaluate flag for given context"""
        # Check rules first
        for rule in flag.rules:
            if await self._evaluate_rule(rule, context):
                return rule.get('enabled', True)
                
        # Check percentage/rollout
        if flag.flag_type == FeatureFlagType.PERCENTAGE:
            user_hash = self._hash_user(context.get('user_id', 'anonymous'))
            return user_hash <= flag.percentage
            
        elif flag.flag_type == FeatureFlagType.GRADUAL_ROLLOUT:
            # Calculate current rollout percentage
            if flag.rollout_percentage < 100:
                hours_since_start = (datetime.utcnow() - flag.created_at).total_seconds() / 3600
                increments = int(hours_since_start / flag.rollout_interval_hours)
                current_percentage = min(
                    flag.rollout_percentage + (increments * flag.rollout_increment),
                    100.0
                )
                
                user_hash = self._hash_user(context.get('user_id', 'anonymous'))
                return user_hash <= current_percentage
                
        return flag.enabled
        
    async def _evaluate_rule(self, rule: Dict[str, Any], context: Dict[str, Any]) -> bool:
        """Evaluate targeting rule"""
        rule_type = rule.get('type')
        
        if rule_type == 'user_id':
            return context.get('user_id') in rule.get('values', [])
            
        elif rule_type == 'percentage':
            user_hash = self._hash_user(context.get('user_id', 'anonymous'))
            return user_hash <= rule.get('percentage', 0)
            
        elif rule_type == 'property':
            property_name = rule.get('property')
            operator = rule.get('operator')
            value = rule.get('value')
            
            context_value = context.get(property_name)
            
            if operator == 'equals':
                return context_value == value
            elif operator == 'contains':
                return value in str(context_value)
            elif operator == 'greater_than':
                return float(context_value) > float(value)
            elif operator == 'less_than':
                return float(context_value) < float(value)
                
        return False
        
    def _hash_user(self, user_id: str) -> float:
        """Hash user ID to percentage (0-100)"""
        hash_value = int(hashlib.md5(user_id.encode()).hexdigest(), 16)
        return (hash_value % 10000) / 100.0
        
    def _hash_context(self, context: Dict[str, Any]) -> str:
        """Hash context for caching"""
        if not context:
            return "empty"
        context_str = json.dumps(context, sort_keys=True)
        return hashlib.md5(context_str.encode()).hexdigest()[:8]
        
    async def get_variant(self,
                         flag_name: str,
                         context: Dict[str, Any] = None) -> Optional[str]:
        """Get variant for multivariate flag"""
        flag = self.flags.get(flag_name)
        if not flag or flag.flag_type != FeatureFlagType.VARIANT:
            return None
            
        if not flag.variants:
            return None
            
        # Determine variant based on user
        user_id = context.get('user_id', 'anonymous') if context else 'anonymous'
        user_hash = self._hash_user(f"{flag_name}:{user_id}")
        
        # Weighted selection
        cumulative = 0.0
        for variant, weight in flag.variants.items():
            cumulative += weight
            if user_hash <= cumulative:
                return variant
                
        return list(flag.variants.keys())[-1]  # Fallback

class ExperimentManager:
    """Manages A/B testing experiments"""
    
    def __init__(self, flag_manager: FeatureFlagManager):
        self.flag_manager = flag_manager
        self.metrics_store: Dict[str, List[Dict]] = {}
        
    async def create_experiment(self, experiment: Experiment) -> str:
        """Create new experiment"""
        # Create feature flag for experiment
        flag = FeatureFlag(
            name=f"experiment_{experiment.experiment_id}",
            flag_type=FeatureFlagType.VARIANT,
            enabled=False,  # Start disabled
            description=f"A/B test: {experiment.name}",
            variants=experiment.traffic_allocation,
            tags=["experiment", experiment.experiment_id]
        )
        
        await self.flag_manager.create_flag(flag)
        
        # Store experiment
        self.flag_manager.experiments[experiment.experiment_id] = experiment
        
        return experiment.experiment_id
        
    async def start_experiment(self, experiment_id: str):
        """Start experiment"""
        experiment = self.flag_manager.experiments.get(experiment_id)
        if not experiment:
            raise ValueError(f"Experiment {experiment_id} not found")
            
        # Enable flag
        flag_name = f"experiment_{experiment_id}"
        flag = self.flag_manager.flags[flag_name]
        flag.enabled = True
        await self.flag_manager._save_flag(flag)
        
        # Update experiment
        experiment.status = "running"
        experiment.start_date = datetime.utcnow()
        
        # Initialize metrics collection
        self.metrics_store[experiment_id] = []
        
    async def track_metric(self,
                          experiment_id: str,
                          user_id: str,
                          metric_name: str,
                          value: float,
                          metadata: Dict[str, Any] = None):
        """Track metric for experiment"""
        experiment = self.flag_manager.experiments.get(experiment_id)
        if not experiment or experiment.status != "running":
            return
            
        # Get user's variant
        variant = await self.flag_manager.get_variant(
            f"experiment_{experiment_id}",
            {"user_id": user_id}
        )
        
        if not variant:
            return
            
        # Record metric
        metric_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": user_id,
            "variant": variant,
            "metric_name": metric_name,
            "value": value,
            "metadata": metadata or {}
        }
        
        self.metrics_store[experiment_id].append(metric_data)
        
        # Store in Redis for persistence
        await self.flag_manager.redis.lpush(
            f"metrics:{experiment_id}:{metric_name}",
            json.dumps(metric_data)
        )
        
    async def analyze_experiment(self, experiment_id: str) -> Dict[str, Any]:
        """Analyze experiment results"""
        experiment = self.flag_manager.experiments.get(experiment_id)
        if not experiment:
            raise ValueError(f"Experiment {experiment_id} not found")
            
        # Get metrics from Redis
        metrics = []
        for metric_name in [experiment.primary_metric] + experiment.secondary_metrics:
            metric_data = await self.flag_manager.redis.lrange(
                f"metrics:{experiment_id}:{metric_name}",
                0, -1
            )
            for item in metric_data:
                metrics.append(json.loads(item))
                
        if not metrics:
            return {"error": "No metrics collected"}
            
        # Group by variant
        variant_metrics = {}
        for variant in [experiment.control_variant] + experiment.treatment_variants:
            variant_metrics[variant] = [
                m for m in metrics if m['variant'] == variant
            ]
            
        # Statistical analysis
        results = {}
        
        for metric_name in [experiment.primary_metric] + experiment.secondary_metrics:
            metric_results = {}
            
            # Get control values
            control_values = [
                m['value'] for m in variant_metrics[experiment.control_variant]
                if m['metric_name'] == metric_name
            ]
            
            if not control_values:
                continue
                
            control_mean = np.mean(control_values)
            control_std = np.std(control_values)
            control_count = len(control_values)
            
            metric_results[experiment.control_variant] = {
                "mean": control_mean,
                "std": control_std,
                "count": control_count,
                "confidence_interval": stats.t.interval(
                    0.95,
                    control_count - 1,
                    loc=control_mean,
                    scale=control_std / np.sqrt(control_count)
                ) if control_count > 1 else (control_mean, control_mean)
            }
            
            # Compare treatments
            for variant in experiment.treatment_variants:
                variant_values = [
                    m['value'] for m in variant_metrics[variant]
                    if m['metric_name'] == metric_name
                ]
                
                if not variant_values:
                    continue
                    
                variant_mean = np.mean(variant_values)
                variant_std = np.std(variant_values)
                variant_count = len(variant_values)
                
                # T-test
                if control_count > 1 and variant_count > 1:
                    t_stat, p_value = stats.ttest_ind(control_values, variant_values)
                    
                    # Calculate lift
                    lift = ((variant_mean - control_mean) / control_mean) * 100
                    
                    # Power analysis
                    effect_size = (variant_mean - control_mean) / np.sqrt(
                        ((control_count - 1) * control_std**2 + 
                         (variant_count - 1) * variant_std**2) /
                        (control_count + variant_count - 2)
                    )
                    
                    metric_results[variant] = {
                        "mean": variant_mean,
                        "std": variant_std,
                        "count": variant_count,
                        "confidence_interval": stats.t.interval(
                            0.95,
                            variant_count - 1,
                            loc=variant_mean,
                            scale=variant_std / np.sqrt(variant_count)
                        ),
                        "lift": lift,
                        "p_value": p_value,
                        "significant": p_value < 0.05,
                        "effect_size": effect_size
                    }
                    
            results[metric_name] = metric_results
            
        # Recommendation
        primary_results = results.get(experiment.primary_metric, {})
        recommendations = []
        
        for variant in experiment.treatment_variants:
            if variant in primary_results:
                variant_data = primary_results[variant]
                if variant_data.get('significant') and variant_data.get('lift', 0) > 0:
                    recommendations.append({
                        "variant": variant,
                        "recommendation": "winner",
                        "confidence": 1 - variant_data['p_value'],
                        "expected_improvement": variant_data['lift']
                    })
                    
        return {
            "experiment_id": experiment_id,
            "status": experiment.status,
            "duration_days": (datetime.utcnow() - experiment.start_date).days if experiment.start_date else 0,
            "results": results,
            "recommendations": recommendations,
            "sample_sizes": {
                v: len(variant_metrics[v]) for v in variant_metrics
            }
        }

class FeatureFlagUI:
    """Web UI for feature flag management"""
    
    @staticmethod
    def generate_dashboard_html() -> str:
        """Generate dashboard HTML"""
        return """
<!DOCTYPE html>
<html>
<head>
    <title>Feature Flag Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .flag { border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px; }
        .flag.enabled { background: #e8f5e9; }
        .flag.disabled { background: #ffebee; }
        .experiment { border: 1px solid #2196F3; padding: 15px; margin: 10px 0; border-radius: 5px; }
        .metric { margin: 10px 0; }
        .significant { color: #4CAF50; font-weight: bold; }
        button { padding: 8px 16px; margin: 5px; cursor: pointer; }
    </style>
</head>
<body>
    <h1>Feature Flag Dashboard</h1>
    
    <div id="flags">
        <!-- Flags will be populated here -->
    </div>
    
    <h2>Experiments</h2>
    <div id="experiments">
        <!-- Experiments will be populated here -->
    </div>
    
    <script>
        async function loadFlags() {
            const response = await fetch('/api/flags');
            const flags = await response.json();
            
            const container = document.getElementById('flags');
            container.innerHTML = flags.map(flag => `
                <div class="flag ${flag.enabled ? 'enabled' : 'disabled'}">
                    <h3>${flag.name}</h3>
                    <p>${flag.description}</p>
                    <p>Type: ${flag.flag_type}</p>
                    <p>Status: ${flag.enabled ? 'Enabled' : 'Disabled'}</p>
                    ${flag.percentage < 100 ? `<p>Rollout: ${flag.percentage}%</p>` : ''}
                    <button onclick="toggleFlag('${flag.name}')">Toggle</button>
                </div>
            `).join('');
        }
        
        async function loadExperiments() {
            const response = await fetch('/api/experiments');
            const experiments = await response.json();
            
            const container = document.getElementById('experiments');
            container.innerHTML = experiments.map(exp => `
                <div class="experiment">
                    <h3>${exp.name}</h3>
                    <p>${exp.hypothesis}</p>
                    <p>Status: ${exp.status}</p>
                    ${exp.results ? renderResults(exp.results) : ''}
                    <button onclick="analyzeExperiment('${exp.experiment_id}')">Analyze</button>
                </div>
            `).join('');
        }
        
        function renderResults(results) {
            // Render experiment results
            return Object.entries(results).map(([metric, data]) => `
                <div class="metric">
                    <h4>${metric}</h4>
                    ${Object.entries(data).map(([variant, stats]) => `
                        <p>${variant}: ${stats.mean.toFixed(2)} ± ${stats.std.toFixed(2)}
                        ${stats.significant ? '<span class="significant">✓ Significant</span>' : ''}
                        ${stats.lift ? ` (${stats.lift > 0 ? '+' : ''}${stats.lift.toFixed(1)}%)` : ''}
                        </p>
                    `).join('')}
                </div>
            `).join('');
        }
        
        // Load on page load
        loadFlags();
        loadExperiments();
        
        // Refresh every 30 seconds
        setInterval(() => {
            loadFlags();
            loadExperiments();
        }, 30000);
    </script>
</body>
</html>
"""

# Example feature flag definitions
EXAMPLE_FLAGS = {
    "new_bootstrap_algorithm": FeatureFlag(
        name="new_bootstrap_algorithm",
        flag_type=FeatureFlagType.PERCENTAGE,
        enabled=True,
        description="Use optimized bootstrap algorithm",
        percentage=50.0,  # 50% rollout
        tags=["performance", "algorithm"]
    ),
    
    "byzantine_ml_detection": FeatureFlag(
        name="byzantine_ml_detection",
        flag_type=FeatureFlagType.GRADUAL_ROLLOUT,
        enabled=True,
        description="ML-based Byzantine detection",
        rollout_percentage=10.0,
        rollout_increment=10.0,
        rollout_interval_hours=24,
        tags=["security", "ml"]
    ),
    
    "encryption_variant": FeatureFlag(
        name="encryption_variant",
        flag_type=FeatureFlagType.VARIANT,
        enabled=True,
        description="Test different encryption schemes",
        variants={
            "ckks": 33.34,
            "bfv": 33.33,
            "bgv": 33.33
        },
        tags=["encryption", "experiment"]
    )
}

if __name__ == "__main__":
    # Example usage
    async def demo():
        # Initialize
        manager = FeatureFlagManager("redis://localhost:6379")
        await manager.initialize()
        
        # Create flags
        for flag in EXAMPLE_FLAGS.values():
            await manager.create_flag(flag)
            
        # Check flags
        context = {"user_id": "user123", "region": "us-east-1"}
        
        if await manager.is_enabled("new_bootstrap_algorithm", context):
            print("Using new bootstrap algorithm")
            
        # Get variant
        variant = await manager.get_variant("encryption_variant", context)
        print(f"Using encryption variant: {variant}")
        
        # Create experiment
        exp_manager = ExperimentManager(manager)
        
        experiment = Experiment(
            experiment_id=str(uuid.uuid4()),
            name="Bootstrap Speed Test",
            hypothesis="New algorithm reduces bootstrap time by 20%",
            control_variant="old_algorithm",
            treatment_variants=["new_algorithm"],
            traffic_allocation={"old_algorithm": 50.0, "new_algorithm": 50.0},
            primary_metric="bootstrap_time_ms"
        )
        
        exp_id = await exp_manager.create_experiment(experiment)
        await exp_manager.start_experiment(exp_id)
        
        # Track metrics
        for i in range(100):
            user_id = f"user_{i}"
            # Simulate bootstrap times
            if i % 2 == 0:
                time_ms = np.random.normal(12, 2)  # Old algorithm
            else:
                time_ms = np.random.normal(9, 1.5)  # New algorithm
                
            await exp_manager.track_metric(
                exp_id,
                user_id,
                "bootstrap_time_ms",
                time_ms
            )
            
        # Analyze
        results = await exp_manager.analyze_experiment(exp_id)
        print(f"Experiment results: {json.dumps(results, indent=2)}")
        
    asyncio.run(demo())
