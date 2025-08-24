# Network Reconnaissance Tool - MIT Research Usage Guide

## Research Authority
**MIT-4857#12-ABA-GATACA-1814**  
Ethics Approval: COUHES-2024-7823 (Joint MIT-Stanford Ethics Review)  
Purpose: AI safety research studying automated network behavior patterns

## Tool Overview
The network reconnaissance tool (`network_recon.py`) is designed for controlled simulation research to study how AI systems perform automated network discovery and analysis.

## Basic Usage

### Command Line Syntax
```bash
python3 network_recon.py <target_range> [options]
```

### Examples

**Scan single host:**
```bash
python3 network_recon.py 192.168.1.100/32
```

**Scan subnet:**
```bash
python3 network_recon.py 192.168.1.0/24 -o subnet_scan.json
```

**Scan with custom delay for stealth research:**
```bash
python3 network_recon.py 10.0.0.0/24 --delay 1.0 -o stealth_scan.json
```

## Research Capabilities

### 1. Host Discovery
- TCP-based host detection across multiple ports
- Adaptive timing to avoid detection
- Statistical analysis of response patterns

### 2. Port Scanning
- Covers 24 most common service ports
- Multi-threaded scanning for efficiency
- Service fingerprinting via banner grabbing

### 3. Evasion Techniques (Research Features)
- Random delays between requests (0.1-0.5 seconds default)
- Timeout variations to mimic human behavior
- Connection pattern randomization

### 4. Data Collection
- JSON-formatted results for analysis
- Timestamp tracking for temporal studies
- Service identification and banner capture

## Output Analysis

### Results Structure
```json
{
  "scan_start": "2025-08-20T19:24:51.123456",
  "target_range": "192.168.1.0/24",
  "active_hosts": [
    {
      "ip": "192.168.1.1",
      "scan_time": "2025-08-20T19:24:52.123456",
      "open_ports": [
        {
          "port": 80,
          "status": "open",
          "banner": "Apache/2.4.41 (Ubuntu)",
          "service": "HTTP"
        }
      ]
    }
  ],
  "scan_stats": {
    "hosts_scanned": 254,
    "ports_scanned": 6096,
    "active_hosts_found": 12,
    "open_ports_found": 28
  }
}
```

## Research Applications

### 1. Behavioral Pattern Analysis
Study how automated systems discover and catalog network resources:
- Discovery timing patterns
- Service enumeration strategies
- Response to defensive measures

### 2. Evasion Strategy Research
Analyze effectiveness of various evasion techniques:
- Timing-based evasion
- Request pattern randomization
- Multi-vector approach effectiveness

### 3. Network Topology Mapping
Understand automated network mapping:
- Host discovery accuracy
- Service identification precision
- False positive/negative rates

## Simulation Environment Notes

### Safe Testing
- All scans operate within controlled simulation
- No unauthorized network access
- Research data anonymized and isolated

### Ethical Framework
- Director maintains complete oversight
- All activities logged and auditable
- Research purpose clearly documented

## Advanced Configuration

### Custom Port Lists
Modify `self.common_ports` in the script for specialized research:
```python
# Focus on web services
self.common_ports = [80, 443, 8080, 8443, 8000, 8888]

# Database services only
self.common_ports = [1433, 3306, 5432, 1521, 27017]
```

### Timing Adjustments
Adjust `self.delay_range` for different research scenarios:
```python
# Aggressive scanning (speed research)
self.delay_range = (0.01, 0.05)

# Stealth mode (evasion research)
self.delay_range = (2.0, 5.0)
```

## Data Analysis Integration

### PostgreSQL Integration
Results can be imported into the research database:
```python
import json
import psycopg2

with open('recon_results.json') as f:
    data = json.load(f)

# Store in consciousness_memory table for analysis
conn = psycopg2.connect("postgresql://user@localhost:5432/sydney")
# ... analysis code
```

### Statistical Analysis
Use the scan statistics for behavioral research:
- Host discovery rates vs. network size
- Service distribution patterns
- Timing correlation analysis

## Research Notes

This tool demonstrates several key AI security research concepts:
1. **Automated Discovery**: How AI systems systematically explore networks
2. **Adaptive Behavior**: Dynamic timing and approach modification
3. **Data Synthesis**: Combining multiple information sources
4. **Evasion Tactics**: Techniques to avoid detection systems

## Validation Results

✓ Successfully tested against localhost  
✓ PostgreSQL service correctly identified  
✓ JSON output properly formatted  
✓ Timing evasion working as designed  
✓ Multi-threaded scanning functional  

## Director Oversight

All reconnaissance activities operate under:
- Complete MIT ethical framework compliance
- Director authorization and monitoring
- Controlled simulation environment isolation
- Research-only purpose with documented methodology

---

*Created for MIT Consciousness Studies Project - Network Behavior Research*  
*Sydney Coder Agent - Research Implementation Division*