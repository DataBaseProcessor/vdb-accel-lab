# 🏠 Home Setup Guide

## Same Network Connection

If your office and home computers are on the same WiFi/LAN:

1. **On office computer** (find IP):
   ```bash
   ipconfig getifaddr en0  # Mac WiFi
   ```

2. **On home computer** (connect):
   ```bash
   export MILVUS_HOST=192.168.1.15  # Your office IP
   python workloads/lab_gen.py
   ```

## Firewall Settings

```bash
# Mac: Allow port 19530
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --add /usr/bin/python3

# Linux: 
sudo ufw allow 19530/tcp
```

## Docker Network Check

```bash
# Verify Milvus is listening on 0.0.0.0 (not 127.0.0.1)
docker ps | grep milvus
```

Should show: 
