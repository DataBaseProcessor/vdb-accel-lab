"""
DBPU Metrics Exporter for Prometheus/Grafana
Exports profiling metrics in Prometheus format
"""
import json
import time
from collections import defaultdict
from http.server import HTTPServer, BaseHTTPRequestHandler

# Mock data if no real logs exist
def load_latest_metrics():
    """Load latest profiling metrics"""
    try:
        with open("/tmp/dbpu-knowhere-hooks.jsonl", 'r') as f:
            data = [json.loads(line) for line in f]
        # Get last 30 records
        return data[-30:] if len(data) > 30 else data
    except:
        # Return mock data
        return [
            {"index_type": "FLAT", "total_time_us": 300000, "scan_codes_time_us": 285000},
            {"index_type": "IVF_FLAT", "total_time_us": 120000, "scan_codes_time_us": 95000},
            {"index_type": "HNSW", "total_time_us": 50000, "scan_codes_time_us": 5000},
        ]

def generate_prometheus_metrics():
    """Generate Prometheus-format metrics"""
    data = load_latest_metrics()
    
    # Aggregate by index type
    by_index = defaultdict(lambda: {'total': 0, 'scan': 0, 'count': 0})
    
    for record in data:
        idx = record['index_type']
        by_index[idx]['total'] += record['total_time_us']
        by_index[idx]['scan'] += record['scan_codes_time_us']
        by_index[idx]['count'] += 1
    
    # Generate metrics
    metrics = []
    
    # Help text
    metrics.append("# HELP dbpu_search_latency_ms Average search latency in milliseconds")
    metrics.append("# TYPE dbpu_search_latency_ms gauge")
    
    for idx, stats in by_index.items():
        avg_ms = (stats['total'] / stats['count']) / 1000
        metrics.append(f'dbpu_search_latency_ms{{index_type="{idx}"}} {avg_ms:.2f}')
    
    metrics.append("")
    metrics.append("# HELP dbpu_scan_codes_latency_ms Average scan_codes latency in milliseconds")
    metrics.append("# TYPE dbpu_scan_codes_latency_ms gauge")
    
    for idx, stats in by_index.items():
        avg_ms = (stats['scan'] / stats['count']) / 1000
        metrics.append(f'dbpu_scan_codes_latency_ms{{index_type="{idx}"}} {avg_ms:.2f}')
    
    metrics.append("")
    metrics.append("# HELP dbpu_scan_codes_percentage Percentage of time spent in scan_codes")
    metrics.append("# TYPE dbpu_scan_codes_percentage gauge")
    
    for idx, stats in by_index.items():
        pct = (stats['scan'] / stats['total']) * 100
        metrics.append(f'dbpu_scan_codes_percentage{{index_type="{idx}"}} {pct:.2f}')
    
    metrics.append("")
    metrics.append("# HELP dbpu_acceleration_potential Potential speedup with 10x DBPU")
    metrics.append("# TYPE dbpu_acceleration_potential gauge")
    
    for idx, stats in by_index.items():
        avg_total = stats['total'] / stats['count']
        avg_scan = stats['scan'] / stats['count']
        new_scan = avg_scan / 10
        new_total = (avg_total - avg_scan) + new_scan
        speedup = avg_total / new_total
        metrics.append(f'dbpu_acceleration_potential{{index_type="{idx}"}} {speedup:.2f}')
    
    return "\n".join(metrics)

class MetricsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/metrics':
            metrics = generate_prometheus_metrics()
            self.send_response(200)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(metrics.encode())
        elif self.path == '/':
            # Simple HTML dashboard
            html = """
            <html>
            <head><title>DBPU Metrics Exporter</title></head>
            <body>
                <h1>🚀 DBPU Metrics Exporter</h1>
                <p>Prometheus endpoint: <a href="/metrics">/metrics</a></p>
                <h2>Current Metrics:</h2>
                <pre>{}</pre>
                <hr>
                <p>Configure Prometheus scrape:</p>
                <pre>
scrape_configs:
  - job_name: 'dbpu'
    static_configs:
      - targets: ['localhost:9090']
                </pre>
            </body>
            </html>
            """.format(generate_prometheus_metrics())
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html.encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        # Suppress default logs
        pass

def main():
    """Start metrics exporter server"""
    port = 9090
    server = HTTPServer(('0.0.0.0', port), MetricsHandler)
    
    print("="*60)
    print("🚀 DBPU Metrics Exporter Started")
    print("="*60)
    print(f"Listening on: http://0.0.0.0:{port}")
    print(f"Metrics URL:  http://localhost:{port}/metrics")
    print(f"Dashboard:    http://localhost:{port}/")
    print()
    print("Configure Prometheus to scrape: localhost:9090")
    print("Press Ctrl+C to stop")
    print("="*60)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down...")
        server.shutdown()

if __name__ == "__main__":
    main()
