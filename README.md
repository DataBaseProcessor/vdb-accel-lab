⸻

vdb-accel-lab

Vector Database Acceleration Lab

A reproducible system to measure, explain, and prove vector search acceleration.
Built on Milvus. Powered by DBPU. Backed by numbers.

⸻

What is this?

vdb-accel-lab is a reproducible benchmark and evidence lab for vector databases.

It answers one concrete question:

“Does hardware acceleration actually help my vector search workload — and if so, why?”

Instead of claims or synthetic demos, this repo provides:
	•	real workloads
	•	real measurements
	•	and quantified acceleration potential

⸻

What this is NOT
	•	❌ Not a new vector database
	•	❌ Not a Milvus replacement
	•	❌ Not a toy benchmark

Milvus remains the industry-standard VDBMS.
We extend it with a thin acceleration-aware layer to measure and explain hardware value.

⸻

Core Idea

Most discussions about vector DB acceleration stop at:

“GPU / SSD / ASIC is faster.”

That’s not enough.

vdb-accel-lab focuses on:
	•	which operations dominate latency
	•	which workloads benefit from offload
	•	how much speedup is realistically achievable
	•	where hardware acceleration makes sense

All results are expressed as metrics, not opinions.

⸻

What You Get

For every search workload, the lab produces:
	•	Actual latency (Milvus + FAISS on CPU)
	•	Estimated DBPU latency (model-based or real HW)
	•	Speedup potential (e.g. 7.2×)
	•	Confidence score (how reliable the estimate is)

These are exported as:
	•	Prometheus metrics
	•	Grafana dashboards
	•	JSON logs (for offline analysis)

⸻

Architecture (High Level)

Application / Client
        |
        v
   Milvus (unmodified behavior)
        |
        |  thin interceptor
        v
 DBPU Benefit Plugin
        |
        |  estimation / optional offload
        v
 DBPU Runtime (HW or simulator)

	•	Default path: 100% FAISS, identical accuracy
	•	With DBPU: automatic acceleration
	•	Without DBPU: automatic fallback + benefit estimation

No behavior changes. No risk.

⸻

Why This Matters

For Software Engineers
	•	Decide whether acceleration is worth integrating
	•	Understand where the bottleneck actually is
	•	Avoid premature or wrong hardware decisions

For Researchers
	•	Fully reproducible experiments
	•	Clear separation of algorithm vs system vs hardware
	•	Suitable for systems / database / architecture discussions

For Investors & Partners
	•	Hardware value backed by measured evidence
	•	Clear story of where acceleration creates ROI
	•	No “trust us” claims — only numbers

⸻

Quick Start (≈ 1 minute)

git clone https://github.com/DatabaseProcessor/vdb-accel-lab
cd vdb-accel-lab

docker compose up -d --build

# Load sample dataset (SIFT1M)
python examples/01-quickstart/load_sift1m.py

# Run benchmark
python examples/01-quickstart/benchmark.py

# View dashboards
open http://localhost:3000   # Grafana (admin/admin)


⸻

Example Output

##

This is the core artifact of the project.

⸻

Datasets & Workloads

Included:
	•	SIFT1M
	•	GIST1M
	•	Synthetic ANN workloads

Custom workloads:
	•	Bring your own embeddings
	•	Bring your own queries
	•	Run the same analysis pipeline

⸻

Relationship to Other Repos

This repo is part of the DatabaseProcessor acceleration stack:

vdb-accel-lab        → evidence & benchmarks (this repo)
milvus-dbpu-plugin   → workload profiling & benefit logging
dbpu-runtime         → hardware abstraction layer
milvus (fork)        → minimal hook, upstream-compatible
dbpu-hw              → DBPU hardware implementation

This repo is the front door.
Everything else exists to support what you see here.

⸻

Design Principles
	•	Evidence first: numbers over narratives
	•	Zero disruption: baseline behavior unchanged
	•	Thin integration: no hard forks, minimal patches
	•	Hardware-optional: value even without HW
	•	Upstream-friendly: designed to evolve with Milvus

⸻

Roadmap (Short)
	•	More ANN index types (HNSW, DiskANN-style)
	•	GPU / SSD acceleration models
	•	Real DBPU hardware offload path
	•	Public benchmark reports
	•	Upstream hook proposal to Milvus

⸻

Philosophy

We don’t replace vector databases.
We make acceleration measurable, explainable, and actionable.

If acceleration matters, it should survive contact with real workloads.

⸻

License

Apache 2.0 (unless otherwise specified)

⸻

Contact

If you are interested in:
	•	hardware acceleration for vector databases
	•	research collaboration
	•	or real-world deployment discussions

Please open an issue or reach out via the organization page.

⸻
