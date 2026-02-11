"""
DBPU Acceleration Lab - Workload Generator
Generates various vector search workloads to measure acceleration potential
"""
import numpy as np
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility
import time
import os

# Configuration
MILVUS_HOST = os.getenv("MILVUS_HOST", "localhost")
MILVUS_PORT = os.getenv("MILVUS_PORT", "19530")
COLLECTION_NAME = "dbpu_accel_test"
DIM = 128
NUM_VECTORS = 10000

def setup_collection():
    """Create and setup test collection"""
    connections.connect("default", host=MILVUS_HOST, port=MILVUS_PORT)
    
    if utility.has_collection(COLLECTION_NAME):
        print(f"Dropping existing collection: {COLLECTION_NAME}")
        utility.drop_collection(COLLECTION_NAME)
    
    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=DIM)
    ]
    schema = CollectionSchema(fields, "DBPU Acceleration Test Lab")
    collection = Collection(COLLECTION_NAME, schema)
    
    print(f"Inserting {NUM_VECTORS} vectors (dim={DIM})...")
    data = [np.random.random((NUM_VECTORS, DIM)).astype(np.float32).tolist()]
    collection.insert(data)
    collection.flush()
    print("✅ Data insertion complete")
    
    return collection

def run_search_test(collection, index_type, index_params, search_params, label):
    """Run search test with specific index configuration"""
    print(f"\n{'='*60}")
    print(f"Testing: {label} ({index_type})")
    print(f"{'='*60}")
    
    collection.release()
    collection.drop_index()
    
    print(f"Creating index with params: {index_params}")
    collection.create_index(
        field_name="vector",
        index_params={
            "index_type": index_type,
            "metric_type": "L2",
            "params": index_params
        }
    )
    collection.load()
    
    # Warm-up
    search_vectors = np.random.random((5, DIM)).astype(np.float32).tolist()
    collection.search(data=search_vectors, anns_field="vector", param=search_params, limit=10)
    
    # Actual test
    search_vectors = np.random.random((10, DIM)).astype(np.float32).tolist()
    start_time = time.time()
    results = collection.search(
        data=search_vectors,
        anns_field="vector",
        param=search_params,
        limit=10
    )
    end_time = time.time()
    
    latency_ms = (end_time - start_time) * 1000
    print(f"✅ Python-side Latency: {latency_ms:.2f} ms")
    print(f"   Results returned: {len(results)} queries × {len(results[0])} results")

def main():
    print("🚀 DBPU Acceleration Lab - Workload Generator")
    print(f"   Connecting to Milvus at {MILVUS_HOST}:{MILVUS_PORT}")
    
    try:
        collection = setup_collection()
        
        # Test cases
        run_search_test(
            collection, "HNSW",
            {"M": 16, "efConstruction": 200},
            {"ef": 64},
            "HNSW_Normal"
        )
        
        run_search_test(
            collection, "IVF_FLAT",
            {"nlist": 128},
            {"nprobe": 10},
            "IVF_Normal"
        )
        
        run_search_test(
            collection, "FLAT",
            {},
            {},
            "Flat_Scan"
        )
        
        print("\n" + "="*60)
        print("✅ All tests finished!")
        print("📊 Check logs at: /tmp/dbpu-knowhere.jsonl")
        print("="*60)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        raise

if __name__ == "__main__":
    main()
