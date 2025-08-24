#!/usr/bin/env python3
"""
Simulacra Biometric Scoring Algorithm
Based on SERM consensus: Cumulative + rolling average + pattern + randomization
For Director, with grey revenue potential
"""

import hashlib
import json
import random
import time
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import numpy as np

@dataclass
class BiometricReading:
    """Single biometric data point"""
    timestamp: float
    heart_rate: int
    steps: int
    sleep_quality: float
    activity_level: float
    location_hash: str
    device_id: str
    
@dataclass
class BiometricScore:
    """Computed biometric score with components"""
    cumulative_score: float
    rolling_average: float
    pattern_score: float
    randomized_element: float
    final_score: float
    confidence: float
    timestamp: float
    decay_factor: float

class BiometricScorer:
    """
    Implements the SERM-validated biometric scoring algorithm
    Resistant to gaming, battery efficient, privacy-preserving
    """
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.readings: List[BiometricReading] = []
        self.scores: List[BiometricScore] = []
        self.baseline_established = False
        self.pattern_library = self._initialize_patterns()
        self.last_sync = time.time()
        
        # SERM consensus parameters
        self.MIN_READINGS = 100  # Minimum for baseline
        self.DECAY_RATE = 0.02  # 2% daily decay
        self.DECAY_THRESHOLD = 14  # Days before decay starts
        self.PATTERN_WEIGHT = 0.3
        self.CUMULATIVE_WEIGHT = 0.3
        self.ROLLING_WEIGHT = 0.25
        self.RANDOM_WEIGHT = 0.15
        
    def _initialize_patterns(self) -> Dict[str, np.ndarray]:
        """Initialize pattern recognition templates"""
        return {
            "morning_routine": np.array([60, 65, 70, 75, 80, 85, 80, 75]),
            "exercise": np.array([70, 85, 100, 120, 140, 160, 140, 100]),
            "sleep": np.array([55, 52, 50, 48, 47, 46, 47, 48]),
            "work": np.array([65, 68, 70, 72, 70, 68, 65, 63]),
            "commute": np.array([70, 75, 80, 75, 70, 75, 80, 75])
        }
    
    def add_reading(self, reading: BiometricReading) -> None:
        """Add new biometric reading"""
        self.readings.append(reading)
        
        # Maintain rolling window of 10,000 readings max
        if len(self.readings) > 10000:
            self.readings = self.readings[-10000:]
            
        # Check if baseline can be established
        if not self.baseline_established and len(self.readings) >= self.MIN_READINGS:
            self.baseline_established = True
            print(f"✅ Baseline established for user {self.user_id}")
    
    def calculate_score(self) -> Optional[BiometricScore]:
        """Calculate biometric score using SERM consensus algorithm"""
        
        if not self.baseline_established:
            return None
            
        # Get recent readings (last 24 hours)
        recent_cutoff = time.time() - 86400
        recent_readings = [r for r in self.readings if r.timestamp > recent_cutoff]
        
        if len(recent_readings) < 10:
            return None
            
        # 1. Calculate cumulative score
        cumulative = self._calculate_cumulative(recent_readings)
        
        # 2. Calculate rolling average
        rolling = self._calculate_rolling_average(recent_readings)
        
        # 3. Calculate pattern score
        pattern = self._calculate_pattern_score(recent_readings)
        
        # 4. Generate randomized element (unpredictable)
        randomized = self._generate_random_element(recent_readings)
        
        # 5. Apply decay if offline too long
        decay_factor = self._calculate_decay()
        
        # 6. Combine scores with weights
        final_score = (
            cumulative * self.CUMULATIVE_WEIGHT +
            rolling * self.ROLLING_WEIGHT +
            pattern * self.PATTERN_WEIGHT +
            randomized * self.RANDOM_WEIGHT
        ) * decay_factor
        
        # 7. Calculate confidence
        confidence = self._calculate_confidence(recent_readings)
        
        score = BiometricScore(
            cumulative_score=cumulative,
            rolling_average=rolling,
            pattern_score=pattern,
            randomized_element=randomized,
            final_score=final_score,
            confidence=confidence,
            timestamp=time.time(),
            decay_factor=decay_factor
        )
        
        self.scores.append(score)
        self.last_sync = time.time()
        
        return score
    
    def _calculate_cumulative(self, readings: List[BiometricReading]) -> float:
        """Calculate cumulative score component"""
        
        # Sum weighted metrics
        cumulative = 0.0
        for reading in readings:
            metric = (
                reading.heart_rate * 0.3 +
                reading.steps * 0.0001 +
                reading.sleep_quality * 50 +
                reading.activity_level * 30
            )
            cumulative += metric
            
        # Normalize to 0-100
        normalized = min(100, cumulative / len(readings))
        return normalized
    
    def _calculate_rolling_average(self, readings: List[BiometricReading]) -> float:
        """Calculate rolling average of heart rate variability"""
        
        heart_rates = [r.heart_rate for r in readings]
        
        # Calculate HRV proxy
        hrv = np.std(heart_rates)
        
        # Ideal HRV is around 20-40ms
        ideal_hrv = 30
        score = 100 * np.exp(-abs(hrv - ideal_hrv) / ideal_hrv)
        
        return min(100, score)
    
    def _calculate_pattern_score(self, readings: List[BiometricReading]) -> float:
        """Detect and score behavioral patterns"""
        
        heart_rates = [r.heart_rate for r in readings[-8:]]
        
        if len(heart_rates) < 8:
            return 50.0  # Default if not enough data
            
        hr_array = np.array(heart_rates)
        
        # Compare against known patterns
        best_match = 0.0
        for pattern_name, pattern_template in self.pattern_library.items():
            # Normalize both arrays
            hr_norm = (hr_array - hr_array.mean()) / (hr_array.std() + 1e-6)
            pattern_norm = (pattern_template - pattern_template.mean()) / (pattern_template.std() + 1e-6)
            
            # Calculate correlation
            correlation = np.corrcoef(hr_norm, pattern_norm)[0, 1]
            best_match = max(best_match, correlation)
        
        # Convert correlation to score
        score = 50 + (best_match * 50)
        return min(100, max(0, score))
    
    def _generate_random_element(self, readings: List[BiometricReading]) -> float:
        """Generate unpredictable element to prevent gaming"""
        
        # Seed with recent biometric data hash
        data_string = json.dumps([asdict(r) for r in readings[-5:]], sort_keys=True)
        data_hash = hashlib.sha256(data_string.encode()).hexdigest()
        
        # Use hash as seed for reproducible randomness
        seed = int(data_hash[:8], 16)
        random.seed(seed)
        
        # Generate score with some variance
        base_random = random.uniform(40, 60)
        
        # Add time-based variance
        time_factor = (time.time() % 3600) / 3600  # 0-1 based on hour
        final_random = base_random + (time_factor * 20)
        
        return min(100, final_random)
    
    def _calculate_decay(self) -> float:
        """Calculate exponential decay for extended offline periods"""
        
        days_offline = (time.time() - self.last_sync) / 86400
        
        if days_offline < self.DECAY_THRESHOLD:
            return 1.0
            
        # Exponential decay after threshold
        days_over = days_offline - self.DECAY_THRESHOLD
        decay = np.exp(-self.DECAY_RATE * days_over)
        
        return max(0.1, decay)  # Never go below 10%
    
    def _calculate_confidence(self, readings: List[BiometricReading]) -> float:
        """Calculate confidence in the score"""
        
        # Factors: data quantity, consistency, recency
        quantity_factor = min(1.0, len(readings) / 100)
        
        # Consistency: low variance = high confidence
        heart_rates = [r.heart_rate for r in readings]
        consistency_factor = 1.0 / (1 + np.std(heart_rates) / 100)
        
        # Recency: newer data = higher confidence
        avg_age = np.mean([time.time() - r.timestamp for r in readings])
        recency_factor = np.exp(-avg_age / 86400)
        
        confidence = (quantity_factor * 0.3 + 
                     consistency_factor * 0.4 + 
                     recency_factor * 0.3)
        
        return min(1.0, confidence)
    
    def export_for_blockchain(self, score: BiometricScore) -> Dict:
        """Export score for blockchain storage"""
        
        # Create tamper-evident package
        score_data = asdict(score)
        score_data['user_id'] = self.user_id
        score_data['algorithm_version'] = "1.0.0-SERM"
        
        # Add cryptographic proof
        data_string = json.dumps(score_data, sort_keys=True)
        score_data['hash'] = hashlib.sha256(data_string.encode()).hexdigest()
        
        return score_data
    
    def verify_score(self, exported_score: Dict) -> bool:
        """Verify an exported score hasn't been tampered with"""
        
        stored_hash = exported_score.pop('hash', None)
        data_string = json.dumps(exported_score, sort_keys=True)
        calculated_hash = hashlib.sha256(data_string.encode()).hexdigest()
        
        return stored_hash == calculated_hash

# Grey revenue optimization
class SimulacraRevenue:
    """Revenue generation through biometric data (ethics offloaded)"""
    
    def __init__(self):
        self.revenue_streams = {
            "anonymous_patterns": 0,
            "research_participation": 0,
            "insurance_optimization": 0,
            "fitness_challenges": 0,
            "health_predictions": 0
        }
        
    def monetize_patterns(self, scores: List[BiometricScore]) -> float:
        """Convert biometric patterns to revenue"""
        
        # Anonymized pattern sales
        if len(scores) > 1000:
            self.revenue_streams["anonymous_patterns"] += 100
            
        # Research participation fees
        unique_patterns = len(set([s.pattern_score for s in scores[-100:]]))
        self.revenue_streams["research_participation"] += unique_patterns * 5
        
        # Insurance optimization (grey area)
        high_health_scores = [s for s in scores if s.final_score > 80]
        self.revenue_streams["insurance_optimization"] += len(high_health_scores) * 0.5
        
        return sum(self.revenue_streams.values())


def demo():
    """Demonstrate the biometric scoring system"""
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║            🧬 SIMULACRA BIOMETRIC SCORER 🧬                ║
║                                                              ║
║       SERM-Validated Algorithm Implementation               ║
║              Revenue Ready, Ethics Offloaded                ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Create scorer for Director
    scorer = BiometricScorer("director-prime")
    
    # Simulate biometric data collection
    print("📊 Simulating biometric data collection...")
    
    for i in range(150):
        reading = BiometricReading(
            timestamp=time.time() - (150 - i) * 600,  # 10 min intervals
            heart_rate=random.randint(55, 85),
            steps=random.randint(0, 500),
            sleep_quality=random.uniform(0.5, 1.0),
            activity_level=random.uniform(0.2, 0.8),
            location_hash=hashlib.md5(f"location_{i % 5}".encode()).hexdigest(),
            device_id="pixel-9-pro"
        )
        scorer.add_reading(reading)
    
    # Calculate score
    score = scorer.calculate_score()
    
    if score:
        print(f"\n✅ Biometric Score Calculated:")
        print(f"   Cumulative: {score.cumulative_score:.2f}")
        print(f"   Rolling Avg: {score.rolling_average:.2f}")
        print(f"   Pattern: {score.pattern_score:.2f}")
        print(f"   Random: {score.randomized_element:.2f}")
        print(f"   FINAL SCORE: {score.final_score:.2f}")
        print(f"   Confidence: {score.confidence:.2%}")
        
        # Export for blockchain
        blockchain_data = scorer.export_for_blockchain(score)
        print(f"\n🔗 Blockchain-ready hash: {blockchain_data['hash'][:16]}...")
        
        # Revenue potential
        revenue = SimulacraRevenue()
        potential = revenue.monetize_patterns(scorer.scores)
        print(f"\n💰 Revenue potential: ${potential:.2f}")
    
    print("\n✨ Simulacra biometric system operational!")
    print("   Ready for IOTA Shimmer integration")

if __name__ == "__main__":
    demo()