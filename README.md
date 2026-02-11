# 📦 vdb-accel-lab

> **Vector Database Acceleration Lab**: Reproducible benchmarks to measure and prove DBPU acceleration potential

## 🎯 Purpose

This repository generates workloads and analyzes performance to quantify the business value of DBPU (Database Processing Unit) acceleration.

**Part of DataStream's 3-layer DBPU stack:**
- **vdb-accel-lab** ← You are here (workload generation & analysis)
- **milvus-dbpu-plugin** (profiling hooks inside Milvus)
- **dbpu-runtime** (hardware abstraction layer)

---

## 🏗️ Architecture & Data Flow
```
┌──────────────────────────────────┐
│   vdb-accel-lab (This Repo)      │
│   • Generate workloads           │
│   • Send queries via PyMilvus    │
│   • Analyze profiling logs       │
│   • Calculate ROI                │
└──────────────┬───────────────────┘
               │ PyMilvus API
               ▼
┌──────────────────────────────────┐
│   Milvus Vector Database         │
│   + milvus-dbpu-plugin (hook)    │ ← Plugin intercepts searches
│   • Profile FAISS operations     │
│   • Decide: DBPU or CPU?         │
│   • Log performance data         │
└──────────┬───────────┬───────────┘
           │           │
    CPU    │           │    DBPU
  Fallback │           │  Offload
           ▼           ▼
     ┌─────────┐  ┌─────────────┐
     │  FAISS  │  │ dbpu-runtime│
     │  (CPU)  │  │   + DBPU    │
     └─────────┘  └─────────────┘
```

**Key Point:** This repository is a **black-box testing tool**. It doesn't need to know whether Milvus uses DBPU or CPU internally—it just sends queries and analyzes the results.

---

## 📁 Repository Structure
```
vdb-accel-lab/
├── workloads/              # Workload generation
│   └── lab_gen.py         # Smart generator (auto-detects Milvus)
├── analyzer/              # Analysis & visualization tools
│   ├── visualize.py       # Performance comparison charts
│   ├── analyze_hooks.py   # C++ profiling hook analysis
│   ├── calculate_roi.py   # Business case calculator
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
- Milvus 2.4+ (any of these configurations):
  - **Vanilla Milvus** (baseline, no acceleration)
  - **Milvus + milvus-dbpu-plugin** (with profiling)
  - **Full DBPU stack** (with hardware acceleration)

### Installation
```bash
# Clone the repository
git clone https://github.com/DatabaseProcessor/vdb-accel-lab.git
cd vdb-accel-lab

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## 🧪 Usage

### Three Testing Modes

#### Mode 1: Mock Testing (No Milvus Required)
```bash
# Auto-detects no Milvus → uses mock data
python workloads/lab_gen.py
# Output: 🎭 Running in MOCK mode
```

#### Mode 2: Baseline Testing (Vanilla Milvus)
```bash
# Start vanilla Milvus
docker run -d --name milvus-standalone \
  -p 19530:19530 \
  milvusdb/milvus:latest standalone

# Run workload
python workloads/lab_gen.py
# Output: ✅ Milvus detected - Running in REAL mode
# Note: No profiling logs, only Python-side latency
```

#### Mode 3: Profiling Mode (Milvus + Plugin)
```bash
# Start Milvus with milvus-dbpu-plugin
docker run -d --name milvus-dbpu \
  -p 19530:19530 \
  -v /tmp:/tmp \
  milvus-dbpu:latest standalone

# Run workload
python workloads/lab_gen.py
# Output: Plugin generates /tmp/dbpu-knowhere.jsonl

# Analyze C++ profiling data
python analyzer/analyze_hooks.py
```

---

## 📊 Analysis Pipeline

### Step 1: Generate Workload Data
```bash
python workloads/lab_gen.py
```

### Step 2: Visualize Performance
```bash
python analyzer/visualize.py
```
**Output:**
```
📈 Performance Comparison
--------------------------------------------------------------------------------
Index Type      Label                Latency (ms)    Bar Chart
--------------------------------------------------------------------------------
HNSW            HNSW_Normal               57.63      █████████
IVF_FLAT        IVF_Normal               117.91      ███████████████████
FLAT            Flat_Scan                299.28      ██████████████████████████████████████████████████

💡 DBPU Acceleration Scenarios:
   10x DBPU acceleration → FLAT would be ~29.93ms
      → 1.93x better than current best!
```

### Step 3: Analyze C++ Profiling Hooks
*Requires Milvus with milvus-dbpu-plugin*
```bash
python analyzer/analyze_hooks.py
```
**Output:**
```
🔬 FAISS OPERATION BREAKDOWN (C++ Profiling)

Index Type      Avg Total (ms)     Avg scan_codes (ms)     % of Total   Bottleneck?
--------------------------------------------------------------------------------
FLAT                  300.00               285.00             95.0%      🔥 YES
IVF_FLAT              120.00                95.00             79.2%      🔥 YES
HNSW                   50.00                 5.00             10.0%      ✅ No
```

### Step 4: Calculate Business ROI
```bash
python analyzer/calculate_roi.py
```
**Output:**
```
💰 INFRASTRUCTURE COST SAVINGS
Current: 100 GPU servers × $30K/year = $3M/year
With DBPU: 20 servers × $40K/year = $800K/year
💵 Annual Savings: $2.2M/year (73% reduction)
```

### Step 5: Export Prometheus Metrics
```bash
python analyzer/export_metrics.py
# Server starts on http://localhost:9090/metrics
```

---

## 🔗 Integration with Other Components

### What Each Component Does

| Component | Role | When It's Used |
|-----------|------|----------------|
| **vdb-accel-lab** (this repo) | Generates workloads, analyzes results | Always (works in mock/real/profiling modes) |
| **milvus-dbpu-plugin** | Profiles Milvus internals, decides offload | Optional (for detailed profiling) |
| **dbpu-runtime** | Executes on DBPU hardware | Optional (for actual acceleration) |

### Full Stack Setup
```bash
# 1. Build Milvus with plugin
cd milvus-dbpu-plugin
./scripts/build_milvus_with_plugin.sh

# 2. Start Milvus
docker run -d milvus-dbpu:latest standalone

# 3. Run benchmarks
cd vdb-accel-lab
python workloads/lab_gen.py

# 4. Analyze results
python analyzer/analyze_hooks.py
python analyzer/calculate_roi.py
```

---

## 🔬 What Gets Measured

### Python-Side Metrics (Always Available)
- End-to-end search latency
- Throughput (queries/second)
- Index-specific performance (HNSW, IVF, FLAT)

### C++ Profiling Metrics (Requires Plugin)
- FAISS internal timing breakdown
- scan_codes bottleneck percentage
- Memory access patterns
- Acceleration potential calculation

### Business Metrics (Always Available)
- Performance improvement ratios
- Infrastructure cost savings
- Market opportunity sizing
- Investment return projections

---

## 🏠 Remote/Home Setup
```bash
# On office computer (find IP)
ipconfig getifaddr en0  # Mac: 192.168.1.15

# On home computer
export MILVUS_HOST=192.168.1.15
python workloads/lab_gen.py
```

See [docs/SETUP.md](docs/SETUP.md) for detailed instructions.

---

## 🎯 Development Roadmap

### Phase 1: Benchmarking Framework ✅
- [x] Smart workload generator (mock/real modes)
- [x] Performance visualization
- [x] C++ hook analysis (mock data support)
- [x] ROI calculator
- [x] Prometheus exporter

### Phase 2: Real Profiling Integration 🚧
- [ ] Test with milvus-dbpu-plugin
- [ ] Validate C++ hook data format
- [ ] Correlate Python and C++ metrics
- [ ] Automated regression testing

### Phase 3: DBPU Hardware Testing
- [ ] FPGA prototype benchmarking
- [ ] Power consumption measurement
- [ ] End-to-end latency validation
- [ ] Production workload simulation

### Phase 4: Production Deployment
- [ ] Customer pilot benchmarking
- [ ] Grafana dashboard templates
- [ ] CI/CD integration
- [ ] Performance SLA validation

---

## 🤝 Contributing

Internal contributors:
1. Test against all three Milvus configurations
2. Maintain mock mode compatibility
3. Add new index types to test suite
4. Document new metrics in analyzer/

---