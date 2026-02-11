# 📦 vdb-accel-lab

> **Vector Database Acceleration Lab**: Reproducible benchmarks to measure and prove DBPU acceleration potential

## 🎯 Purpose

This repository is part of DataStream's DBPU (Database Processing Unit) development stack:
- **vdb-accel-lab** ← You are here (benchmarking & workload generation)
- **milvus-dbpu-plugin** (profiling hooks & intelligence)
- **dbpu-runtime** (hardware offload layer)

The goal is to measure the acceleration potential of offloading vector database operations (specifically FAISS scan_codes bottleneck) to custom hardware.

---

## 📁 Repository Structure
```
vdb-accel-lab/
├── workloads/              # Workload generation
│   └── lab_gen.py         # Smart workload generator (auto-detects Milvus)
├── analyzer/              # Analysis & visualization tools
│   ├── visualize.py       # Performance visualization & comparison
│   ├── analyze_hooks.py   # C++ profiling hook analysis
│   ├── calculate_roi.py   # Business ROI calculator
│   └── export_metrics.py  # Prometheus metrics exporter
├── dashboards/            # Grafana dashboards (future)
├── docs/                  # Documentation
│   └── SETUP.md          # Home/remote setup guide
├── requirements.txt       # Python dependencies
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Milvus 2.4+ (optional - will use mock mode if unavailable)
- Docker (optional, for local Milvus)

### Installation
```bash
# Clone the repository
git clone https://github.com/DatabaseProcessor/vdb-accel-lab.git
cd vdb-accel-lab

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## 🧪 Usage

### 1. Generate Workload Data

The workload generator **automatically detects** if Milvus is available:
- ✅ **Milvus available** → Runs real vector searches
- 🎭 **Milvus unavailable** → Uses mock mode with realistic timings
```bash
# Run workload (auto-detects Milvus)
python workloads/lab_gen.py

# For remote Milvus
MILVUS_HOST=192.168.1.15 python workloads/lab_gen.py

# Check generated logs
tail -f /tmp/dbpu-knowhere.jsonl
```

**Output:**
```
✅ Milvus detected - Running in REAL mode
🚀 DBPU Acceleration Lab - Smart Workload Generator
   Mode: REAL

Setting up real Milvus collection...
Inserting 10000 vectors (dim=128)...
✅ Real data inserted

============================================================
Testing: HNSW_Normal (HNSW)
============================================================
Creating index: {'M': 16, 'efConstruction': 200}
✅ Latency: 57.63 ms (REAL)
...
```

### 2. Visualize Performance
```bash
# Generate visual analysis
python analyzer/visualize.py
```

**Output:**
```
📊 DBPU ACCELERATION POTENTIAL ANALYSIS
================================================================================
Mode: REAL
Time: 2026-02-11T10:01:10.483979
Total tests: 3

📈 Performance Comparison
--------------------------------------------------------------------------------
Index Type      Label                Latency (ms)    Bar Chart
--------------------------------------------------------------------------------
HNSW            HNSW_Normal               57.63      █████████
IVF_FLAT        IVF_Normal               117.91      ███████████████████
FLAT            Flat_Scan                299.28      ██████████████████████████████████████████████████

🚀 Acceleration Potential
--------------------------------------------------------------------------------
Baseline (FLAT scan):         299.28 ms

💡 DBPU Acceleration Scenarios:
   10x DBPU acceleration → FLAT would be ~29.93ms
      → 1.93x better than current best!
   20x DBPU acceleration → FLAT would be ~14.96ms
      → 3.85x better than current best!

💰 Market opportunity: FLAT scan has 5.19x room for improvement
```

### 3. Analyze C++ Profiling Hooks

Analyzes detailed FAISS operation timings (scan_codes bottleneck):
```bash
python analyzer/analyze_hooks.py
```

**Output:**
```
🔬 FAISS OPERATION BREAKDOWN (C++ Profiling)
================================================================================

Index Type      Avg Total (ms)     Avg scan_codes (ms)     % of Total   Bottleneck?
--------------------------------------------------------------------------------
FLAT                  300.00               285.00             95.0%      🔥 YES
IVF_FLAT              120.00                95.00             79.2%      🔥 YES
HNSW                   50.00                 5.00             10.0%      ✅ No

🚀 DBPU ACCELERATION POTENTIAL

FLAT Analysis:
Current Performance:  300.00ms
scan_codes Time:      285.00ms (95.0%)
🎯 HIGH PRIORITY - scan_codes is the bottleneck!
   10x DBPU → 43.50ms (overall 6.90x speedup)
   20x DBPU → 29.25ms (overall 10.26x speedup)
```

### 4. Calculate Business ROI
```bash
python analyzer/calculate_roi.py
```

**Output:**
```
📈 PERFORMANCE ROI ANALYSIS
================================================================================

FLAT:
  Current:        300.00ms per query
  With 10x DBPU:   43.50ms per query (6.90x faster)
  Throughput:      6.90x more queries/second

💰 INFRASTRUCTURE COST SAVINGS
================================================================================
Current Infrastructure:
  100 GPU servers × $30,000/year = $3,000,000/year

With DBPU (5x speedup):
  20 DBPU servers × $40,000/year = $800,000/year

💵 Annual Savings: $2,200,000/year (73.3% reduction)
📊 3-Year Savings: $6,600,000

🌍 MARKET OPPORTUNITY
  • TAM: $300M (vector database acceleration market)
  • Revenue (Year 3): $15M - $60M
  • Exit Value: $500M - $1B
  • Investor Returns: 12-24x
```

### 5. Export Prometheus Metrics

Start metrics exporter for Grafana/Prometheus integration:
```bash
# Start exporter (runs on port 9090)
python analyzer/export_metrics.py

# Check metrics
curl http://localhost:9090/metrics

# View dashboard
open http://localhost:9090/
```

**Prometheus Configuration:**
```yaml
scrape_configs:
  - job_name: 'dbpu'
    static_configs:
      - targets: ['localhost:9090']
```

**Sample Metrics:**
```
# HELP dbpu_search_latency_ms Average search latency in milliseconds
# TYPE dbpu_search_latency_ms gauge
dbpu_search_latency_ms{index_type="FLAT"} 300.00
dbpu_search_latency_ms{index_type="IVF_FLAT"} 120.00
dbpu_search_latency_ms{index_type="HNSW"} 50.00

# HELP dbpu_acceleration_potential Potential speedup with 10x DBPU
# TYPE dbpu_acceleration_potential gauge
dbpu_acceleration_potential{index_type="FLAT"} 6.90
dbpu_acceleration_potential{index_type="IVF_FLAT"} 4.21
```

---

## 🔬 What Gets Measured

### Workload Generator (`lab_gen.py`)
- **Python-side latency**: End-to-end search time from client perspective
- **Index types**: HNSW, IVF_FLAT, FLAT (full scan)
- **Workload parameters**: 10K vectors, 128 dimensions, 10 queries per test

### Hook Analyzer (`analyze_hooks.py`)
- **C++ profiling data**: Detailed FAISS internal timings
- **scan_codes bottleneck**: Time spent in distance computation hotspot
- **Bottleneck percentage**: Which indexes are dominated by scan_codes
- **Acceleration potential**: Projected speedup with DBPU offload

### ROI Calculator (`calculate_roi.py`)
- **Performance gains**: Throughput improvements (queries/sec)
- **Cost savings**: Infrastructure reduction (GPU → DBPU migration)
- **Market opportunity**: TAM analysis for vector DB acceleration
- **Investment returns**: Revenue projections and exit multiples

---

## 📊 Complete Workflow
```bash
# 1. Generate benchmark data
python workloads/lab_gen.py

# 2. Visualize performance comparison
python analyzer/visualize.py

# 3. Analyze C++ profiling hooks
python analyzer/analyze_hooks.py

# 4. Calculate business case
python analyzer/calculate_roi.py

# 5. Export metrics for monitoring
python analyzer/export_metrics.py &

# 6. View real-time metrics
curl http://localhost:9090/metrics
```

---

## 🏠 Remote/Home Setup

If your office and home computers are on the same network:
```bash
# On office computer (find IP)
ipconfig getifaddr en0  # Mac WiFi
# Example output: 192.168.1.15

# On home computer (connect)
export MILVUS_HOST=192.168.1.15
python workloads/lab_gen.py
```

See [docs/SETUP.md](docs/SETUP.md) for detailed remote setup instructions.

---

## 🎯 Development Roadmap

### Phase 1: Benchmarking (Current)
- [x] Smart workload generator with auto-detection
- [x] Performance visualization
- [x] C++ hook analysis (mock data ready)
- [x] ROI calculator
- [x] Prometheus metrics exporter

### Phase 2: Real Profiling Integration
- [ ] Milvus with C++ profiling hooks
- [ ] Real FAISS scan_codes timing capture
- [ ] Hardware performance counters
- [ ] Power consumption metrics

### Phase 3: DBPU Prototype
- [ ] FPGA/ASIC prototype integration
- [ ] Hardware-accelerated scan_codes
- [ ] End-to-end latency measurements
- [ ] Production deployment testing

### Phase 4: Production Ready
- [ ] Customer pilots
- [ ] Grafana dashboards
- [ ] Automated CI/CD benchmarking
- [ ] Performance regression detection

---

## 🤝 Contributing

This is a proprietary repository for DataStream Inc. Internal contributors should:
1. Create feature branches from `main`
2. Add comprehensive tests for new analyzers
3. Update this README for new tools
4. Use GitHub Desktop or conventional git workflow

---

