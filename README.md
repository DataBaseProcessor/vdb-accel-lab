
---

# vdb-accel-lab

**Vector Database Acceleration Lab**

A reproducible system to measure vector search acceleration potential — **before buying hardware.**

Built on Milvus. Powered by DBPU. Backed by numbers.

---

## What is this?

**vdb-accel-lab** answers one concrete question:

> *"Will hardware acceleration actually help MY vector search workload — and by how much?"*

Instead of vendor claims or synthetic benchmarks, you get:
- ✅ **Real workloads** (your embeddings, your queries)
- ✅ **Real measurements** (actual FAISS baseline)
- ✅ **Quantified potential** (5-10x speedup with confidence scores)

All without requiring custom hardware.

---

## What this is NOT

- ❌ **Not a new vector database** → Milvus remains the engine
- ❌ **Not a Milvus replacement** → We extend, not replace
- ❌ **Not a toy benchmark** → Production-grade measurement stack

**Core principle:** Milvus is the industry-standard VDBMS. We add a thin observability layer to measure and explain hardware acceleration value — nothing more.

---

## Why This Matters

### The Problem with Database Accelerators

Most accelerator pitches go like this:
> *"Our GPU/FPGA/ASIC is 10x faster!"*

But they don't tell you:
- Which **operations** dominate YOUR latency?
- Which **workloads** benefit from offload?
- What **speedup** is realistically achievable for YOUR data?
- Whether the **ROI** justifies the hardware cost?

### Our Solution

**vdb-accel-lab** focuses on the questions that actually matter:
1. **Where** is the bottleneck? (distance compute, PQ scan, graph traversal?)
2. **Why** does it matter? (what % of total latency?)
3. **How much** speedup is possible? (5x? 10x? 1.2x?)
4. **When** does acceleration make sense? (workload characteristics)

All results expressed as **metrics, not opinions.**

---

## What You Get

For every search workload, the lab produces:

| Metric | Description | Example |
|--------|-------------|---------|
| **Actual Latency** | Milvus + FAISS on CPU (baseline) | 12.4ms |
| **Estimated DBPU Latency** | Model-based or real HW | 2.1ms |
| **Speedup Potential** | Actual / Estimated | **5.9x** |
| **Confidence Score** | How reliable the estimate is | 85% |
| **Bottleneck Analysis** | Which operation dominates | PQ scan (73%) |

These are exported as:
- 📊 **Prometheus metrics** (scrape from `/metrics`)
- 📈 **Grafana dashboards** (pre-configured)
- 📝 **JSON logs** (for offline analysis)

---

## Architecture (High-Level)

```
Application / Client
        ↓
   Milvus (standard behavior, unmodified)
        ↓
   [thin interceptor - 15 lines]
        ↓
   DBPU Benefit Plugin
   ├─ Profile workload
   ├─ Estimate benefit
   └─ Log metrics
        ↓
   DBPU Runtime (optional)
   ├─ HW present? → Offload
   └─ HW absent? → Fallback to FAISS
```

**Key guarantees:**
- ✅ Default path: **100% FAISS** (identical accuracy)
- ✅ With DBPU: **automatic acceleration**
- ✅ Without DBPU: **automatic fallback + benefit estimation**
- ✅ **Zero behavior changes** to Milvus

---

## Quick Start (1 minute)

```bash
# 1. Clone
git clone https://github.com/DatabaseProcessor/vdb-accel-lab
cd vdb-accel-lab

# 2. Start services (Milvus + Prometheus + Grafana)
docker compose up -d --build

# 3. Load sample dataset (SIFT1M)
python examples/01-quickstart/load_sift1m.py

# 4. Run benchmark
python examples/01-quickstart/benchmark.py

# 5. View results
open http://localhost:3000  # Grafana (admin/admin)
```

**What you'll see:**
- Real-time speedup metrics (e.g., "7.2x potential")
- Latency breakdown (where time is spent)
- Confidence intervals (measurement reliability)

---

## Example Output

### Terminal Output
```json
{
  "event": "dbpu_benefit",
  "collection": "sift1m",
  "index_type": "IVF_FLAT",
  "nprobe": 16,
  "topk": 10,
  "actual_ms": 12.4,
  "dbpu_est_ms": 2.1,
  "speedup": 5.90,
  "confidence": 0.85,
  "bottleneck": "distance_compute",
  "bottleneck_pct": 73
}
```

### Grafana Dashboard
![Speedup Dashboard](docs/images/grafana-screenshot.png)
- **Panel 1:** Actual vs Estimated Latency (time series)
- **Panel 2:** Speedup Ratio (gauge: 5.9x)
- **Panel 3:** Bottleneck Analysis (pie chart)

---

## Datasets & Workloads

### Pre-configured Datasets
- ✅ **SIFT1M** (128-dim, 1M vectors, computer vision)
- ✅ **GIST1M** (960-dim, 1M vectors, image features)
- ✅ **GloVe-100** (100-dim, 1.2M vectors, word embeddings)

### Bring Your Own Workload
```python
# examples/02-custom/analyze_my_data.py
from vdb_accel_lab import WorkloadAnalyzer

analyzer = WorkloadAnalyzer(
    embeddings="my_embeddings.npy",  # Your vectors
    queries="my_queries.npy",        # Your queries
    index_params={"type": "IVF_PQ", "nlist": 1024, "m": 8}
)

# Get benefit estimate
result = analyzer.run()
print(f"Expected speedup: {result.speedup:.1f}x")
print(f"ROI break-even: {result.roi_months} months")
```

---

## Who This Is For

### 🎓 **Researchers**
- Fully reproducible experiments
- Clear separation: algorithm vs system vs hardware
- Suitable for database/systems/architecture papers
- **Example:** "Quantifying the Impact of PQ on DBPU Offload Efficiency"

### 💼 **Software Engineers**
- Decide if acceleration is worth integrating
- Understand where the actual bottleneck is
- Avoid premature or wrong hardware investments
- **Example:** "Should we buy GPUs or wait for DBPU?"

### 💰 **Investors & Partners**
- Hardware value backed by measured evidence
- Clear ROI story (not just "10x faster")
- No "trust us" claims — only numbers
- **Example:** "At 1M QPS, DBPU saves $200K/year in compute"

---

## Relationship to Other Repos

This repo is part of the **DatabaseProcessor acceleration stack:**

```
vdb-accel-lab         → 🎯 Evidence & benchmarks (YOU ARE HERE)
milvus-dbpu-plugin    → 🔌 Workload profiling & benefit logging
dbpu-runtime          → 🎮 Hardware abstraction layer
milvus (fork)         → 🔧 Minimal hook, upstream-compatible
dbpu-hw               → 💎 DBPU hardware implementation [PRIVATE]
docs                  → 📚 Unified documentation
```

**This repo is the front door.** Everything else exists to support what you see here.

---

## Design Principles

1. **Evidence first** → Numbers over narratives
2. **Zero disruption** → Baseline behavior unchanged
3. **Thin integration** → No hard forks, minimal patches
4. **Hardware-optional** → Value even without HW
5. **Upstream-friendly** → Designed to evolve with Milvus

---

## Roadmap

### ✅ Phase 1 (Current)
- [x] IVF_FLAT benefit estimation
- [x] SIFT1M/GIST1M benchmarks
- [x] Prometheus + Grafana integration
- [x] JSON logging for analysis

### 🚧 Phase 2 (Next 3 months)
- [ ] HNSW index support
- [ ] IVF_PQ benefit modeling
- [ ] GPU comparison mode
- [ ] Real DBPU hardware offload path

### 🔮 Phase 3 (6+ months)
- [ ] DiskANN-style indices
- [ ] SSD acceleration modeling
- [ ] Auto-tuning (workload → optimal HW config)
- [ ] Public benchmark leaderboard
- [ ] Upstream hook proposal to Milvus

---

## Philosophy

> **We don't replace vector databases.**  
> **We make acceleration measurable, explainable, and actionable.**

If hardware acceleration truly matters, it should survive contact with **your real workloads** — not synthetic benchmarks.

This lab is our commitment to that principle.

---

## Contributing

We welcome contributions! Areas where help is needed:
- 🧪 Additional index types (HNSW, DiskANN)
- 📊 More workload profiles (NLP, recommendation, etc.)
- 🔬 Performance model refinements
- 📝 Documentation improvements

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## Citation

If you use this work in research, please cite:

```bibtex
@misc{vdb-accel-lab,
  title={VDB Acceleration Lab: Measuring Database Accelerator Benefit},
  author={DataStream Team},
  year={2025},
  url={https://github.com/DatabaseProcessor/vdb-accel-lab}
}
```

---

## License

Apache 2.0 (unless otherwise specified in individual files)

See [LICENSE](LICENSE) for details.

---

## Contact

Interested in:
- 🔬 **Research collaboration** on vector DB acceleration?
- 🏢 **Enterprise deployment** discussions?
- 💡 **Hardware acceleration** for your workload?

**Open an issue** or reach out via [organization page](https://github.com/DatabaseProcessor).

---

## Acknowledgments

Built with:
- [Milvus](https://github.com/milvus-io/milvus) - Vector database platform
- [FAISS](https://github.com/facebookresearch/faiss) - ANN search library
- [Prometheus](https://prometheus.io/) - Metrics collection
- [Grafana](https://grafana.com/) - Visualization


---

**Start measuring today. Buy hardware tomorrow.**

