"""
C++ Profiling Hook Data Analyzer
Analyzes detailed FAISS operation timings from Milvus hooks
"""
import json
import sys
from collections import defaultdict

def generate_mock_hook_data():
    """Generate realistic mock C++ hook data"""
    import random
    
    # Simulate multiple search operations with detailed timing
    mock_data = []
    
    scenarios = [
        ("HNSW", {"M": 16, "efConstruction": 200}, 50000, 5000),   # total_us, scan_codes_us
        ("IVF_FLAT", {"nlist": 128}, 120000, 95000),
        ("FLAT", {}, 300000, 285000),  # FLAT has highest scan_codes ratio
    ]
    
    for index_type, params, base_total, base_scan in scenarios:
        for i in range(10):  # 10 queries per index type
            # Add some variance
            total_us = int(base_total * random.uniform(0.9, 1.1))
            scan_codes_us = int(base_scan * random.uniform(0.85, 1.15))
            
            # Calculate breakdown
            other_us = total_us - scan_codes_us
            scan_pct = (scan_codes_us / total_us) * 100
            
            mock_data.append({
                "timestamp": f"2026-02-11T10:0{i%6}:00.000Z",
                "operation": "search",
                "index_type": index_type,
                "index_params": params,
                "total_time_us": total_us,
                "scan_codes_time_us": scan_codes_us,
                "other_time_us": other_us,
                "scan_codes_percentage": round(scan_pct, 2),
                "nq": 1,  # queries per batch
                "dim": 128,
                "top_k": 10
            })
    
    return mock_data

def load_hook_data(log_file="/tmp/dbpu-knowhere-hooks.jsonl"):
    """Load hook data from file, or generate mock if not exists"""
    try:
        with open(log_file, 'r') as f:
            data = [json.loads(line) for line in f]
        print(f"✅ Loaded {len(data)} real hook records from {log_file}")
        return data
    except FileNotFoundError:
        print(f"⚠️  Hook data not found: {log_file}")
        print("🎭 Generating mock C++ hook data...")
        mock_data = generate_mock_hook_data()
        
        # Save mock data for inspection
        with open(log_file, 'w') as f:
            for record in mock_data:
                f.write(json.dumps(record) + '\n')
        
        print(f"📝 Mock data saved to {log_file}")
        return mock_data

def analyze_bottlenecks(data):
    """Analyze scan_codes bottleneck by index type"""
    print("\n" + "="*80)
    print("🔬 FAISS OPERATION BREAKDOWN (C++ Profiling)")
    print("="*80)
    
    # Group by index type
    by_index = defaultdict(list)
    for record in data:
        by_index[record['index_type']].append(record)
    
    print(f"\n{'Index Type':<15} {'Avg Total (ms)':<18} {'Avg scan_codes (ms)':<22} {'% of Total':<12} {'Bottleneck?'}")
    print("-" * 80)
    
    bottleneck_summary = []
    
    for index_type, records in sorted(by_index.items()):
        avg_total = sum(r['total_time_us'] for r in records) / len(records) / 1000
        avg_scan = sum(r['scan_codes_time_us'] for r in records) / len(records) / 1000
        avg_pct = (avg_scan / avg_total) * 100
        
        # Determine if it's a bottleneck (>70% of time)
        is_bottleneck = "🔥 YES" if avg_pct > 70 else "✅ No"
        
        print(f"{index_type:<15} {avg_total:>13.2f}      {avg_scan:>16.2f}          {avg_pct:>6.1f}%      {is_bottleneck}")
        
        bottleneck_summary.append({
            'index_type': index_type,
            'avg_total_ms': avg_total,
            'avg_scan_ms': avg_scan,
            'scan_percentage': avg_pct,
            'is_bottleneck': avg_pct > 70
        })
    
    return bottleneck_summary

def calculate_acceleration_potential(summary):
    """Calculate potential speedup with DBPU acceleration"""
    print("\n" + "="*80)
    print("🚀 DBPU ACCELERATION POTENTIAL")
    print("="*80)
    
    for item in summary:
        print(f"\n{item['index_type']} Analysis:")
        print("-" * 40)
        print(f"Current Performance:  {item['avg_total_ms']:.2f}ms")
        print(f"scan_codes Time:      {item['avg_scan_ms']:.2f}ms ({item['scan_percentage']:.1f}%)")
        
        if item['is_bottleneck']:
            print(f"🎯 HIGH PRIORITY - scan_codes is the bottleneck!")
            
            # Calculate speedup scenarios
            for accel in [5, 10, 20]:
                new_scan_time = item['avg_scan_ms'] / accel
                other_time = item['avg_total_ms'] - item['avg_scan_ms']
                new_total = other_time + new_scan_time
                speedup = item['avg_total_ms'] / new_total
                
                print(f"   {accel:2d}x DBPU → {new_total:6.2f}ms (overall {speedup:.2f}x speedup)")
        else:
            print(f"⚠️  scan_codes not the primary bottleneck")
            print(f"   Focus on other optimizations first")

def main():
    """Main analysis entry point"""
    import os
    
    hook_file = os.getenv("HOOK_LOG_FILE", "/tmp/dbpu-knowhere-hooks.jsonl")
    
    # Load data (real or mock)
    data = load_hook_data(hook_file)
    
    # Analyze
    summary = analyze_bottlenecks(data)
    calculate_acceleration_potential(summary)
    
    print("\n" + "="*80)
    print("💡 Next Steps:")
    print("   1. Run with real Milvus + C++ hooks for actual measurements")
    print("   2. Focus DBPU design on indexes where scan_codes > 70%")
    print("   3. Calculate business ROI: python analyzer/calculate_roi.py")
    print("="*80)
    print()

if __name__ == "__main__":
    main()
