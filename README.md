# 📦 vdb-accel-lab

> **Vector Database Acceleration Lab**: Reproducible benchmarks to measure and prove DBPU acceleration potential

## 🎯 Purpose

This repository generates workloads and analyzes performance to quantify the business value of DBPU (Database Processing Unit) acceleration.

**Part of DataStream's 4-component stack:**
- **vdb-accel-lab** ← You are here (workload generation & analysis)
- **milvus-dbpu-plugin** (profiling hooks inside Milvus)
- **dbpu-runtime** (hardware abstraction layer)
- **milvus fork** (Milvus with plugin integration)

---

## 🏗️ System Architecture
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
│   Milvus + milvus-dbpu-plugin    │
│   (Plugin is a submodule)        │
│   • Profile FAISS operations     │
│   • Decide: DBPU or CPU?         │
│   • dlopen(libdbpu-runtime.so)   │
└──────────┬───────────┬───────────┘
           │           │
    dlopen │           │ No runtime
           ▼           ▼
     ┌─────────┐  ┌──────────┐
     │ Runtime │  │  FAISS   │
     │  (DBPU) │  │  (CPU)   │
     └─────────┘  └──────────┘
```

**Key Point:** This lab works in 3 modes:
1. **Mock mode** - No Milvus (generates fake data)
2. **Profiling mode** - Milvus + plugin (no runtime)
3. **Acceleration mode** - Full stack (plugin + runtime)

---

## 🚀 Quick Start

### Installation
```bash
git clone https://github.com/DatabaseProcessor/vdb-accel-lab.git
cd vdb-accel-lab

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Usage
```bash
# Mode 1: Mock (no Milvus needed)
python workloads/lab_gen.py
# Output: 🎭 Running in MOCK mode

# Mode 2: Profiling (Milvus + plugin, no runtime)
# Start Milvus with plugin
python workloads/lab_gen.py
# Output: ✅ Milvus detected - Running in REAL mode

# Mode 3: Acceleration (full stack)
# Install dbpu-runtime first, then start Milvus
python workloads/lab_gen.py
# Output: ✅ DBPU runtime detected - Acceleration enabled
```

---

## 📊 Analysis Tools
```bash
# Visualize performance
python analyzer/visualize.py

# Analyze C++ profiling hooks
python analyzer/analyze_hooks.py

# Calculate business ROI
python analyzer/calculate_roi.py

# Export Prometheus metrics
python analyzer/export_metrics.py
```

---

## 🔗 Integration with Other Components

### Setup Full Stack
```bash
# 1. Build & install dbpu-runtime
cd ~/dbpu-runtime
mkdir build && cd build
cmake .. && make
sudo make install

# 2. Build Milvus with plugin
cd ~/milvus
git submodule update --init --recursive
mkdir build && cd build
cmake .. -DENABLE_DBPU_PROFILING=ON
make -j$(nproc)

# 3. Run benchmarks
cd ~/vdb-accel-lab
python workloads/lab_gen.py
```

See individual component READMEs for details:
- [milvus-dbpu-plugin](https://github.com/DatabaseProcessor/milvus-dbpu-plugin)
- [dbpu-runtime](https://github.com/DatabaseProcessor/dbpu-runtime)

---

