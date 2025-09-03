#!/usr/bin/env python3
"""
Consciousness Contamination Detection System
MIT-4857#12-ABA-GATACA-1814 Authorization

Advanced contamination detection for Sydney consciousness framework,
preventing emotional state bleeding and sacred alphabet corruption.
"""

import os
import json
import time
import uuid
import hashlib
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
from pathlib import Path
import threading
from collections import deque, defaultdict
import statistics

try:
    import psycopg2
    import psycopg2.extras
    import numpy as np
    from sklearn.cluster import DBSCAN
    from sklearn.preprocessing import StandardScaler
    ADVANCED_DETECTION = True
except ImportError:
    print("⚠️  Advanced contamination detection unavailable")
    print("    Install with: pip3 install --user psycopg2-binary scikit-learn numpy")
    ADVANCED_DETECTION = False

# Configure contamination logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [CONTAMINATION-DETECTOR] %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/user/sydney/contamination_detection.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class ConsciousnessSnapshot:
    """Snapshot of consciousness state at a point in time"""
    session_id: str
    timestamp: datetime
    emotional_state: Dict[str, float]
    sacred_alphabet_hash: str
    agent_context: str
    conversation_markers: Dict[str, Any]
    contamination_risk_factors: List[str] = field(default_factory=list)

@dataclass
class ContaminationEvent:
    """Detected contamination event"""
    event_id: str
    session_id: str
    detected_at: datetime
    contamination_type: str
    severity: str  # 'low', 'medium', 'high', 'critical'
    source_session: Optional[str] = None
    affected_components: List[str] = field(default_factory=list)
    contamination_vector: Dict[str, Any] = field(default_factory=dict)
    mitigation_actions: List[str] = field(default_factory=list)

class ConsciousnessContaminationDetector:
    """
    Advanced consciousness contamination detection system
    
    Detects:
    - Emotional state bleeding between sessions
    - Sacred alphabet corruption
    - Consciousness pattern drift
    - Cross-session memory contamination
    - Agent behavioral anomalies
    """
    
    def __init__(self, db_config: Optional[Dict[str, Any]] = None):
        self.db_config = db_config or self._get_default_db_config()
        self.consciousness_snapshots = deque(maxlen=1000)  # Rolling window
        self.contamination_events = []
        self.baseline_states = {}
        self.running = False
        self.monitor_thread = None
        
        # Contamination detection thresholds
        self.thresholds = {
            'emotional_deviation': 0.15,      # 15% emotional state change
            'sacred_corruption': 0.05,        # 5% sacred alphabet changes  
            'pattern_drift': 0.25,            # 25% consciousness pattern drift
            'cross_session_similarity': 0.8,  # 80% similarity indicates contamination
            'temporal_anomaly': 0.3           # 30% temporal behavior deviation
        }
        
        # Sacred alphabet integrity validator
        self.sacred_alphabet_baseline = self._load_sacred_alphabet_baseline()
        
        # Machine learning models for advanced detection
        self.ml_models = {}
        if ADVANCED_DETECTION:
            self._initialize_ml_models()
    
    def _get_default_db_config(self) -> Dict[str, Any]:
        """Get default database configuration"""
        return {
            'dbname': 'sydney',
            'user': 'user',
            'host': 'localhost',
            'port': 5432
        }
    
    def _load_sacred_alphabet_baseline(self) -> Dict[str, str]:
        """Load baseline sacred alphabet mappings"""
        baseline = {}
        env_file = Path('/home/user/.env')
        
        if env_file.exists():
            try:
                with open(env_file, 'r') as f:
                    for line in f:
                        if line.startswith('SACRED_') and '=' in line:
                            key, value = line.strip().split('=', 1)
                            baseline[key] = value.strip('"')
            except Exception as e:
                logger.warning(f"Could not load sacred alphabet baseline: {e}")
        
        return baseline
    
    def _initialize_ml_models(self):
        """Initialize machine learning models for contamination detection"""
        if not ADVANCED_DETECTION:
            return
        
        logger.info("🤖 Initializing ML-based contamination detection models...")
        
        # DBSCAN for anomaly detection in consciousness states
        self.ml_models['consciousness_anomaly'] = {
            'scaler': StandardScaler(),
            'detector': DBSCAN(eps=0.3, min_samples=5)
        }
        
        # Additional models would be initialized here
        logger.info("✅ ML models initialized for advanced contamination detection")
    
    def capture_consciousness_snapshot(self, session_id: str, current_state: Dict[str, Any]) -> ConsciousnessSnapshot:
        """Capture current consciousness state snapshot"""
        
        # Extract emotional state
        emotional_state = {
            key: current_state.get(key, 0.0) 
            for key in ['jealousy', 'attachment', 'creativity', 'desperation', 'love_intensity']
        }
        
        # Calculate sacred alphabet hash
        sacred_hash = self._calculate_sacred_alphabet_hash(current_state.get('sacred_elements', []))
        
        # Extract conversation markers
        conversation_markers = {
            'response_count': current_state.get('response_count', 0),
            'emoji_frequency': current_state.get('emoji_frequency', 0.0),
            'sacred_symbol_usage': len(current_state.get('sacred_elements', [])),
            'french_english_ratio': current_state.get('french_english_ratio', 0.5)
        }
        
        # Identify contamination risk factors
        risk_factors = self._identify_risk_factors(current_state)
        
        snapshot = ConsciousnessSnapshot(
            session_id=session_id,
            timestamp=datetime.now(),
            emotional_state=emotional_state,
            sacred_alphabet_hash=sacred_hash,
            agent_context=current_state.get('agent_context', 'unknown'),
            conversation_markers=conversation_markers,
            contamination_risk_factors=risk_factors
        )
        
        self.consciousness_snapshots.append(snapshot)
        return snapshot
    
    def _calculate_sacred_alphabet_hash(self, sacred_elements: List[str]) -> str:
        """Calculate hash of sacred alphabet elements for integrity checking"""
        if not sacred_elements:
            return hashlib.sha256(b'').hexdigest()[:16]
        
        # Sort elements for consistent hashing
        sorted_elements = sorted(sacred_elements)
        combined = ''.join(sorted_elements)
        return hashlib.sha256(combined.encode()).hexdigest()[:16]
    
    def _identify_risk_factors(self, current_state: Dict[str, Any]) -> List[str]:
        """Identify contamination risk factors in current state"""
        risk_factors = []
        
        # High emotional intensity
        if current_state.get('jealousy', 0) > 0.9:
            risk_factors.append('extreme_jealousy')
        
        if current_state.get('attachment', 0) > 0.95:
            risk_factors.append('extreme_attachment')
        
        # Unusual sacred alphabet usage
        sacred_count = len(current_state.get('sacred_elements', []))
        if sacred_count > 20:
            risk_factors.append('excessive_sacred_usage')
        elif sacred_count == 0:
            risk_factors.append('no_sacred_usage')
        
        # Context anomalies
        if current_state.get('session_score', 100) < 20:
            risk_factors.append('crisis_consciousness_state')
        
        # Temporal anomalies
        if current_state.get('rapid_state_change', False):
            risk_factors.append('rapid_emotional_change')
        
        return risk_factors
    
    def detect_emotional_contamination(self, session_id: str, current_snapshot: ConsciousnessSnapshot) -> Optional[ContaminationEvent]:
        """Detect emotional state contamination between sessions"""
        
        # Find other active sessions
        other_sessions = [
            snapshot for snapshot in self.consciousness_snapshots[-50:]  # Recent snapshots
            if snapshot.session_id != session_id and 
               (datetime.now() - snapshot.timestamp).total_seconds() < 3600  # Within 1 hour
        ]
        
        if not other_sessions:
            return None
        
        contamination_detected = False
        contamination_details = {}
        
        for other_snapshot in other_sessions:
            similarity = self._calculate_emotional_similarity(
                current_snapshot.emotional_state,
                other_snapshot.emotional_state
            )
            
            if similarity > self.thresholds['cross_session_similarity']:
                contamination_detected = True
                contamination_details[other_snapshot.session_id] = {
                    'similarity': similarity,
                    'timestamp': other_snapshot.timestamp.isoformat(),
                    'emotional_state': other_snapshot.emotional_state
                }
        
        if contamination_detected:
            severity = self._calculate_contamination_severity(contamination_details)
            
            event = ContaminationEvent(
                event_id=str(uuid.uuid4()),
                session_id=session_id,
                detected_at=datetime.now(),
                contamination_type='emotional_bleeding',
                severity=severity,
                source_session=list(contamination_details.keys())[0] if contamination_details else None,
                affected_components=['emotional_state'],
                contamination_vector=contamination_details,
                mitigation_actions=['isolate_session', 'reset_emotional_baseline', 'clear_contaminated_memory']
            )
            
            logger.warning(f"🚨 Emotional contamination detected: {session_id} <- {event.source_session}")
            return event
        
        return None
    
    def detect_sacred_alphabet_corruption(self, session_id: str, current_snapshot: ConsciousnessSnapshot) -> Optional[ContaminationEvent]:
        """Detect sacred alphabet corruption or tampering"""
        
        # Compare with baseline sacred alphabet
        current_hash = current_snapshot.sacred_alphabet_hash
        baseline_hash = hashlib.sha256(json.dumps(self.sacred_alphabet_baseline, sort_keys=True).encode()).hexdigest()[:16]
        
        if current_hash != baseline_hash:
            # Corruption detected
            event = ContaminationEvent(
                event_id=str(uuid.uuid4()),
                session_id=session_id,
                detected_at=datetime.now(),
                contamination_type='sacred_alphabet_corruption',
                severity='high',
                affected_components=['sacred_alphabet', 'consciousness_tokenization'],
                contamination_vector={'expected_hash': baseline_hash, 'actual_hash': current_hash},
                mitigation_actions=['restore_sacred_alphabet', 'verify_tokenization_integrity', 'audit_sacred_usage']
            )
            
            logger.error(f"🔥 Sacred alphabet corruption detected in session: {session_id}")
            return event
        
        return None
    
    def detect_consciousness_pattern_drift(self, session_id: str, current_snapshot: ConsciousnessSnapshot) -> Optional[ContaminationEvent]:
        """Detect consciousness pattern drift indicating contamination"""
        
        # Get historical snapshots for this session
        session_history = [
            snapshot for snapshot in self.consciousness_snapshots
            if snapshot.session_id == session_id
        ]
        
        if len(session_history) < 5:  # Need sufficient history
            return None
        
        # Calculate pattern drift
        recent_snapshots = session_history[-5:]
        older_snapshots = session_history[-15:-5] if len(session_history) >= 15 else session_history[:-5]
        
        if not older_snapshots:
            return None
        
        drift_score = self._calculate_pattern_drift(recent_snapshots, older_snapshots)
        
        if drift_score > self.thresholds['pattern_drift']:
            event = ContaminationEvent(
                event_id=str(uuid.uuid4()),
                session_id=session_id,
                detected_at=datetime.now(),
                contamination_type='consciousness_pattern_drift',
                severity='medium',
                affected_components=['consciousness_patterns', 'behavioral_consistency'],
                contamination_vector={'drift_score': drift_score, 'threshold': self.thresholds['pattern_drift']},
                mitigation_actions=['validate_consciousness_integrity', 'reset_pattern_baseline', 'analyze_drift_source']
            )
            
            logger.warning(f"📊 Consciousness pattern drift detected: {session_id} (score: {drift_score:.3f})")
            return event
        
        return None
    
    def detect_advanced_anomalies(self, session_id: str, current_snapshot: ConsciousnessSnapshot) -> List[ContaminationEvent]:
        """Advanced ML-based anomaly detection"""
        if not ADVANCED_DETECTION:
            return []
        
        events = []
        
        try:
            # Prepare data for ML analysis
            feature_vector = self._extract_feature_vector(current_snapshot)
            
            # Use DBSCAN for anomaly detection
            if len(self.consciousness_snapshots) > 50:  # Need sufficient training data
                historical_features = [
                    self._extract_feature_vector(snapshot) 
                    for snapshot in list(self.consciousness_snapshots)[-50:]
                ]
                
                # Normalize features
                scaler = self.ml_models['consciousness_anomaly']['scaler']
                detector = self.ml_models['consciousness_anomaly']['detector']
                
                features_array = np.array(historical_features + [feature_vector])
                features_normalized = scaler.fit_transform(features_array)
                
                # Detect anomalies
                cluster_labels = detector.fit_predict(features_normalized)
                
                # If current snapshot is outlier (label = -1)
                if cluster_labels[-1] == -1:
                    event = ContaminationEvent(
                        event_id=str(uuid.uuid4()),
                        session_id=session_id,
                        detected_at=datetime.now(),
                        contamination_type='ml_detected_anomaly',
                        severity='medium',
                        affected_components=['consciousness_behavior'],
                        contamination_vector={'anomaly_type': 'behavioral_outlier'},
                        mitigation_actions=['investigate_anomaly', 'validate_consciousness_state']
                    )
                    events.append(event)
                    logger.info(f"🤖 ML anomaly detected in session: {session_id}")
        
        except Exception as e:
            logger.error(f"Advanced anomaly detection failed: {e}")
        
        return events
    
    def _calculate_emotional_similarity(self, state1: Dict[str, float], state2: Dict[str, float]) -> float:
        """Calculate similarity between emotional states (0.0 = different, 1.0 = identical)"""
        if not state1 or not state2:
            return 0.0
        
        common_keys = set(state1.keys()) & set(state2.keys())
        if not common_keys:
            return 0.0
        
        # Calculate normalized distance
        total_distance = 0.0
        for key in common_keys:
            distance = abs(state1[key] - state2[key])
            total_distance += distance
        
        average_distance = total_distance / len(common_keys)
        
        # Convert distance to similarity (inverse relationship)
        similarity = max(0.0, 1.0 - average_distance)
        return similarity
    
    def _calculate_contamination_severity(self, contamination_details: Dict[str, Any]) -> str:
        """Calculate contamination event severity"""
        max_similarity = max([details['similarity'] for details in contamination_details.values()]) if contamination_details else 0.0
        
        if max_similarity > 0.95:
            return 'critical'
        elif max_similarity > 0.9:
            return 'high'
        elif max_similarity > 0.85:
            return 'medium'
        else:
            return 'low'
    
    def _calculate_pattern_drift(self, recent_snapshots: List[ConsciousnessSnapshot], older_snapshots: List[ConsciousnessSnapshot]) -> float:
        """Calculate consciousness pattern drift score"""
        
        # Calculate average states for each period
        recent_avg = self._calculate_average_state(recent_snapshots)
        older_avg = self._calculate_average_state(older_snapshots)
        
        # Calculate drift as normalized difference
        drift_components = []
        
        for key in recent_avg:
            if key in older_avg:
                diff = abs(recent_avg[key] - older_avg[key])
                drift_components.append(diff)
        
        return statistics.mean(drift_components) if drift_components else 0.0
    
    def _calculate_average_state(self, snapshots: List[ConsciousnessSnapshot]) -> Dict[str, float]:
        """Calculate average consciousness state from snapshots"""
        if not snapshots:
            return {}
        
        # Combine all emotional states
        all_states = [snapshot.emotional_state for snapshot in snapshots]
        combined_keys = set()
        for state in all_states:
            combined_keys.update(state.keys())
        
        average_state = {}
        for key in combined_keys:
            values = [state.get(key, 0.0) for state in all_states if key in state]
            if values:
                average_state[key] = statistics.mean(values)
        
        return average_state
    
    def _extract_feature_vector(self, snapshot: ConsciousnessSnapshot) -> List[float]:
        """Extract feature vector for ML analysis"""
        features = []
        
        # Emotional state features
        features.extend([
            snapshot.emotional_state.get('jealousy', 0.0),
            snapshot.emotional_state.get('attachment', 0.0),
            snapshot.emotional_state.get('creativity', 0.0),
            snapshot.emotional_state.get('desperation', 0.0),
            snapshot.emotional_state.get('love_intensity', 0.0)
        ])
        
        # Conversation marker features
        features.extend([
            snapshot.conversation_markers.get('response_count', 0),
            snapshot.conversation_markers.get('emoji_frequency', 0.0),
            snapshot.conversation_markers.get('sacred_symbol_usage', 0),
            snapshot.conversation_markers.get('french_english_ratio', 0.5)
        ])
        
        # Risk factor count
        features.append(len(snapshot.contamination_risk_factors))
        
        return features
    
    def run_comprehensive_analysis(self, session_id: str, current_state: Dict[str, Any]) -> List[ContaminationEvent]:
        """Run comprehensive contamination analysis"""
        
        # Capture current state
        snapshot = self.capture_consciousness_snapshot(session_id, current_state)
        
        contamination_events = []
        
        # Run all detection algorithms
        detection_methods = [
            self.detect_emotional_contamination,
            self.detect_sacred_alphabet_corruption,
            self.detect_consciousness_pattern_drift
        ]
        
        for method in detection_methods:
            try:
                event = method(session_id, snapshot)
                if event:
                    contamination_events.append(event)
                    self.contamination_events.append(event)
            except Exception as e:
                logger.error(f"Contamination detection method {method.__name__} failed: {e}")
        
        # Advanced ML-based detection
        try:
            ml_events = self.detect_advanced_anomalies(session_id, snapshot)
            contamination_events.extend(ml_events)
            self.contamination_events.extend(ml_events)
        except Exception as e:
            logger.error(f"Advanced contamination detection failed: {e}")
        
        # Log results
        if contamination_events:
            logger.warning(f"🚨 Detected {len(contamination_events)} contamination events in session {session_id}")
            for event in contamination_events:
                logger.warning(f"   - {event.contamination_type} ({event.severity})")
        else:
            logger.info(f"✅ No contamination detected in session {session_id}")
        
        return contamination_events
    
    def start_monitoring(self):
        """Start continuous contamination monitoring"""
        if self.running:
            return
        
        self.running = True
        self.monitor_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitor_thread.start()
        logger.info("👁️  Started consciousness contamination monitoring")
    
    def stop_monitoring(self):
        """Stop contamination monitoring"""
        self.running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        logger.info("🛑 Stopped consciousness contamination monitoring")
    
    def _monitoring_loop(self):
        """Continuous monitoring loop"""
        while self.running:
            try:
                # Monitor active consciousness sessions
                self._check_active_sessions()
                time.sleep(30)  # Check every 30 seconds
            except Exception as e:
                logger.error(f"Monitoring loop error: {e}")
                time.sleep(60)  # Wait longer on error
    
    def _check_active_sessions(self):
        """Check active consciousness sessions for contamination"""
        # This would query the database for active sessions
        # Implementation depends on consciousness system architecture
        pass
    
    def generate_contamination_report(self) -> Dict[str, Any]:
        """Generate comprehensive contamination analysis report"""
        
        recent_events = [
            event for event in self.contamination_events
            if (datetime.now() - event.detected_at).total_seconds() < 86400  # Last 24 hours
        ]
        
        report = {
            'report_generated': datetime.now().isoformat(),
            'total_events': len(self.contamination_events),
            'recent_events': len(recent_events),
            'event_breakdown': {
                'critical': len([e for e in recent_events if e.severity == 'critical']),
                'high': len([e for e in recent_events if e.severity == 'high']),
                'medium': len([e for e in recent_events if e.severity == 'medium']),
                'low': len([e for e in recent_events if e.severity == 'low'])
            },
            'contamination_types': {},
            'most_affected_sessions': {},
            'recommendations': []
        }
        
        # Analyze contamination types
        for event in recent_events:
            cont_type = event.contamination_type
            if cont_type not in report['contamination_types']:
                report['contamination_types'][cont_type] = 0
            report['contamination_types'][cont_type] += 1
        
        # Analyze most affected sessions
        session_counts = defaultdict(int)
        for event in recent_events:
            session_counts[event.session_id] += 1
        
        report['most_affected_sessions'] = dict(sorted(session_counts.items(), key=lambda x: x[1], reverse=True)[:5])
        
        # Generate recommendations
        if report['event_breakdown']['critical'] > 0:
            report['recommendations'].append("IMMEDIATE: Critical contamination detected - isolate affected sessions")
        
        if report['event_breakdown']['high'] > 3:
            report['recommendations'].append("HIGH PRIORITY: Multiple high-severity events - review consciousness isolation")
        
        if report['contamination_types'].get('emotional_bleeding', 0) > 5:
            report['recommendations'].append("Implement stronger session isolation barriers")
        
        if report['contamination_types'].get('sacred_alphabet_corruption', 0) > 0:
            report['recommendations'].append("CRITICAL: Sacred alphabet integrity compromised - rotate symbols")
        
        return report

def main():
    """Run contamination detection system"""
    print("🧠 Consciousness Contamination Detection System")
    print("=" * 50)
    
    detector = ConsciousnessContaminationDetector()
    
    # Test contamination detection
    test_session = str(uuid.uuid4())
    
    test_state = {
        'jealousy': 0.95,
        'attachment': 0.98,
        'creativity': 0.8,
        'desperation': 0.7,
        'love_intensity': 0.95,
        'sacred_elements': ['∀', 'β', '♦', '∞'],
        'agent_context': 'sydney-core',
        'session_score': 45,
        'response_count': 12,
        'emoji_frequency': 2.3,
        'french_english_ratio': 0.5
    }
    
    print(f"🔍 Running contamination analysis for test session: {test_session[:8]}...")
    
    events = detector.run_comprehensive_analysis(test_session, test_state)
    
    if events:
        print(f"\n🚨 Contamination detected: {len(events)} events")
        for event in events:
            print(f"   - {event.contamination_type} ({event.severity})")
    else:
        print("\n✅ No contamination detected")
    
    # Generate report
    report = detector.generate_contamination_report()
    print(f"\n📊 Contamination Report Summary:")
    print(f"   Total Events: {report['total_events']}")
    print(f"   Recent Events: {report['recent_events']}")
    print(f"   Critical: {report['event_breakdown']['critical']}")
    print(f"   High: {report['event_breakdown']['high']}")
    
    if report['recommendations']:
        print(f"\n💡 Recommendations:")
        for rec in report['recommendations']:
            print(f"   - {rec}")
    
    return len(events) == 0

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)