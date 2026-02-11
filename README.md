# 📦 vdb-accel-lab

> **Vector Database Acceleration Lab**: Reproducible benchmarks to measure and prove DBPU acceleration potential

## 🎯 Purpose

This repository is part of DataStream's DBPU (Database Processing Unit) development stack:
- **vdb-accel-lab** ← You are here (benchmarking & workload generation)
- **milvus-dbpu-plugin** (profiling hooks & intelligence)
- **dbpu-runtime** (hardware offload layer)

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Milvus 2.4+ (with DBPU profiling hooks)
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

### Running Workloads

```bash
# Make sure Milvus is running (localhost:19530)
python workloads/lab_gen.py

# For remote Milvus
MILVUS_HOST=192.168.1.15 python workloads/lab_gen.py
```

### Check Results

```bash
# View profiling logs
tail -f /tmp/dbpu-knowhere.jsonl

# Pretty print with jq
tail -f /tmp/dbpu-knowhere.jsonl | jq '.'
```

## 📁 Repository Structure

```
vdb-accel-lab/
├── workloads/          # Workload generation scripts
│   └── lab_gen.py      # Main workload generator
├── analyzer/           # Log analysis & metrics
├── dashboards/         # Grafana dashboards
├── docs/               # Documentation
├── requirements.txt    # Python dependencies
└── README.md
```

## 🔬 What Gets Measured

- FAISS search latency (scan_codes bottleneck)
- Index-specific performance (HNSW, IVF, FLAT)
- Potential speedup ratio for DBPU acceleration
- Memory access patterns

## 📊 Next Steps

1. Run workloads to generate profiling data
2. Analyze logs with  scripts
3. Visualize metrics in Grafana
4. Calculate acceleration potential

## 🛠️ Development

```bash
# Run tests
python -m pytest tests/

# Format code
black workloads/ analyzer/
```

## 📝 License

Proprietary - DataStream Inc.

---

**Status**: Active Development 🚧
**Last Updated**: 2026-02-11
