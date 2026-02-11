"""
DBPU Acceleration Lab - Smart Workload Generator
Auto-detects Milvus availability and falls back to mock mode
"""
import numpy as np
import time
import json
import os
from datetime import datetime

# Milvus 연결 시도
MILVUS_AVAILABLE = False
try:
    from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility
    try:
        connections.connect("default", host="localhost", port="19530", timeout=2)
        MILVUS_AVAILABLE = True
        print("✅ Milvus detected - Running in REAL mode")
    except Exception as e:
        print(f"⚠️  Milvus not available ({e})")
        print("🎭 Running in MOCK mode")
except ImportError:
    print("⚠️  pymilvus not installed")
    print("🎭 Running in MOCK mode")

# Configuration
DIM = 128
NUM_VECTORS = 10000
LOG_FILE = "/tmp/dbpu-knowhere.jsonl"

class WorkloadRunner:
    def __init__(self, use_real=MILVUS_AVAILABLE):
        self.use_real = use_real
        self.collection = None
        self.logs = []
        
    def setup_collection(self):
        """Setup collection (real or mock)"""
        if self.use_real:
            print(f"Setting up real Milvus collection...")
            COLLECTION_NAME = "dbpu_accel_test"
            
            if utility.has_collection(COLLECTION_NAME):
                utility.drop_collection(COLLECTION_NAME)
            
            fields = [
                FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
                FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=DIM)
            ]
            schema = CollectionSchema(fields, "DBPU Acceleration Test")
            self.collection = Collection(COLLECTION_NAME, schema)
            
            print(f"Inserting {NUM_VECTORS} vectors (dim={DIM})...")
            data = [np.random.random((NUM_VECTORS, DIM)).astype(np.float32).tolist()]
            self.collection.insert(data)
            self.collection.flush()
            print("✅ Real data inserted")
        else:
            print(f"[MOCK] Creating collection with {NUM_VECTORS} vectors (dim={DIM})...")
            time.sleep(0.5)
            print("✅ [MOCK] Data ready")
    
    def run_search_test(self, index_type, index_params, search_params, label):
        """Run search test (real or mock)"""
        print(f"\n{'='*60}")
        print(f"Testing: {label} ({index_type})")
        print(f"{'='*60}")
        
        if self.use_real:
            return self._run_real_search(index_type, index_params, search_params, label)
        else:
            return self._run_mock_search(index_type, index_params, search_params, label)
    
    def _run_real_search(self, index_type, index_params, search_params, label):
        """Real Milvus search"""
        self.collection.release()
        self.collection.drop_index()
        
        print(f"Creating index: {index_params}")
        self.collection.create_index(
            field_name="vector",
            index_params={
                "index_type": index_type,
                "metric_type": "L2",
                "params": index_params
            }
        )
        self.collection.load()
        
        # Warm-up
        search_vectors = np.random.random((5, DIM)).astype(np.float32).tolist()
        self.collection.search(data=search_vectors, anns_field="vector", param=search_params, limit=10)
        
        # Actual test
        search_vectors = np.random.random((10, DIM)).astype(np.float32).tolist()
        start_time = time.time()
        results = self.collection.search(
            data=search_vectors,
            anns_field="vector",
            param=search_params,
            limit=10
        )
        latency_ms = (time.time() - start_time) * 1000
        
        print(f"✅ Latency: {latency_ms:.2f} ms (REAL)")
        
        return {
            "timestamp": datetime.now().isoformat(),
            "mode": "real",
            "index_type": index_type,
            "index_params": index_params,
            "search_params": search_params,
            "label": label,
            "latency_ms": latency_ms,
            "num_queries": len(search_vectors),
            "dim": DIM
        }
    
    def _run_mock_search(self, index_type, index_params, search_params, label):
        """Mock search with realistic latencies"""
        print(f"[MOCK] Creating index: {index_params}")
        time.sleep(0.3)
        
        # Realistic latency simulation
        if index_type == "HNSW":
            latency_ms = np.random.uniform(40, 60)
        elif index_type == "IVF_FLAT":
            latency_ms = np.random.uniform(80, 120)
        else:  # FLAT
            latency_ms = np.random.uniform(200, 300)
        
        time.sleep(latency_ms / 1000)
        print(f"✅ Latency: {latency_ms:.2f} ms (MOCK)")
        
        return {
            "timestamp": datetime.now().isoformat(),
            "mode": "mock",
            "index_type": index_type,
            "index_params": index_params,
            "search_params": search_params,
            "label": label,
            "latency_ms": latency_ms,
            "num_queries": 10,
            "dim": DIM
        }
    
    def save_logs(self):
        """Save logs to file"""
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        with open(LOG_FILE, 'a') as f:
            for log in self.logs:
                f.write(json.dumps(log) + '\n')
        print(f"\n📝 Logs saved to: {LOG_FILE}")

def main():
    print("🚀 DBPU Acceleration Lab - Smart Workload Generator")
    print(f"   Mode: {'REAL' if MILVUS_AVAILABLE else 'MOCK'}")
    print()
    
    runner = WorkloadRunner()
    runner.setup_collection()
    
    # Test suite
    test_cases = [
        ("HNSW", {"M": 16, "efConstruction": 200}, {"ef": 64}, "HNSW_Normal"),
        ("IVF_FLAT", {"nlist": 128}, {"nprobe": 10}, "IVF_Normal"),
        ("FLAT", {}, {}, "Flat_Scan"),
    ]
    
    for index_type, index_params, search_params, label in test_cases:
        log = runner.run_search_test(index_type, index_params, search_params, label)
        runner.logs.append(log)
    
    runner.save_logs()
    
    print("\n" + "="*60)
    print("✅ All tests finished!")
    print("📊 Run analyzer to visualize results:")
    print("   python analyzer/visualize.py")
    print("="*60)

if __name__ == "__main__":
    main()
