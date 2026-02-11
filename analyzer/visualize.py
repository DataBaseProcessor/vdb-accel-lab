"""
DBPU Profiling Results Visualizer
Analyzes and visualizes acceleration potential
"""
import json
import sys
from datetime import datetime

def load_logs(log_file="/tmp/dbpu-knowhere.jsonl"):
    """Load logs from file"""
    logs = []
    try:
        with open(log_file, 'r') as f:
            for line in f:
                logs.append(json.loads(line))
    except FileNotFoundError:
        print(f"❌ Log file not found: {log_file}")
        print("   Run 'python workloads/lab_gen.py' first")
        sys.exit(1)
    return logs

def analyze_and_visualize(logs):
    """Analyze and create visual report"""
    if not logs:
        print("❌ No logs found")
        return
    
    # Get latest run (last 3 entries)
    latest_logs = logs[-3:] if len(logs) >= 3 else logs
    
    print("\n" + "="*80)
    print("📊 DBPU ACCELERATION POTENTIAL ANALYSIS")
    print("="*80)
    
    # Header info
    mode = latest_logs[0].get('mode', 'unknown')
    timestamp = latest_logs[0].get('timestamp', 'unknown')
    print(f"Mode: {mode.upper()}")
    print(f"Time: {timestamp}")
    print(f"Total tests: {len(latest_logs)}")
    print()
    
    # Performance table
    print("📈 Performance Comparison")
    print("-" * 80)
    print(f"{'Index Type':<15} {'Label':<20} {'Latency (ms)':<15} {'Bar Chart'}")
    print("-" * 80)
    
    results = []
    for log in latest_logs:
        index_type = log['index_type']
        label = log['label']
        latency = log['latency_ms']
        results.append((index_type, label, latency))
    
    # Normalize for bar chart (max 50 chars)
    max_latency = max(r[2] for r in results)
    
    for index_type, label, latency in results:
        bar_length = int((latency / max_latency) * 50)
        bar = "█" * bar_length
        print(f"{index_type:<15} {label:<20} {latency:>10.2f}      {bar}")
    
    print()
    
    # Speedup analysis
    print("🚀 Acceleration Potential")
    print("-" * 80)
    
    # Find FLAT baseline
    flat_latency = next((r[2] for r in results if r[0] == 'FLAT'), None)
    
    if flat_latency:
        print(f"Baseline (FLAT scan):     {flat_latency:>10.2f} ms")
        print()
        
        for index_type, label, latency in results:
            if index_type != 'FLAT':
                speedup = flat_latency / latency
                print(f"{label:<25} {speedup:>6.2f}x faster than FLAT")
        
        print()
        print("💡 DBPU Acceleration Scenarios:")
        print("-" * 80)
        
        for multiplier in [5, 10, 20]:
            accelerated = flat_latency / multiplier
            print(f"   {multiplier}x DBPU acceleration → FLAT would be ~{accelerated:.2f}ms")
            
            best_current = min(r[2] for r in results if r[0] != 'FLAT')
            if accelerated < best_current:
                improvement = best_current / accelerated
                print(f"      → {improvement:.2f}x better than current best!")
        
        print()
    
    # Summary
    print("="*80)
    print("📊 Key Findings:")
    print("-" * 80)
    
    best = min(results, key=lambda x: x[2])
    worst = max(results, key=lambda x: x[2])
    
    print(f"✅ Best performer:  {best[1]} ({best[2]:.2f}ms)")
    print(f"❌ Worst performer: {worst[1]} ({worst[2]:.2f}ms)")
    
    if flat_latency:
        print(f"🎯 Acceleration gap: {worst[2] / best[2]:.2f}x difference")
        print(f"💰 Market opportunity: FLAT scan has {worst[2] / best[2]:.2f}x room for improvement")
    
    print("="*80)
    print()
    
    # Next steps
    print("🔬 Next Steps:")
    print("   1. Run with real Milvus to get actual profiling hooks data")
    print("   2. Check /tmp/dbpu-knowhere.jsonl for detailed FAISS timings")
    print("   3. Identify scan_codes bottleneck percentage")
    print("   4. Calculate ROI for DBPU acceleration")
    print()

def main():
    """Main entry point"""
    import os
    
    log_file = os.getenv("LOG_FILE", "/tmp/dbpu-knowhere.jsonl")
    print(f"📂 Reading logs from: {log_file}")
    
    logs = load_logs(log_file)
    analyze_and_visualize(logs)

if __name__ == "__main__":
    main()
