# 🌐 Cloudflare Tunnel Deployment Guide (Raspberry Pi + Flask)

This document explains how to expose a local Flask server running on a Raspberry Pi to the internet using Cloudflare Tunnel.

# 🌍 Domain Registration (Cloudflare)

To use Cloudflare Tunnel with your own URL, you need a domain managed by Cloudflare.

In this setup, the domain is registered directly through Cloudflare Registrar,
which keeps everything inside the same platform and requires no additional DNS configuration.

## ✅ Steps Followed During Setup

1. Open Cloudflare Dashboard

2. Navigate to Registrar → Register Domain

3. Search for an available domain (e.g., lee8d.com)

4. Complete the purchase

5. The domain will automatically appear under Websites in your Cloudflare account

No extra configuration is required — the domain is immediately ready for Cloudflare Tunnel

---

## 🎯 What the Domain Is Used For

The purchased domain (e.g., lee8d.com) will be mapped to your Raspberry Pi Flask server
through Cloudflare Tunnel, providing a secure public URL:

```bash
https://<YOUR-DOMAIN>
```

---

## 1. Install Cloudflared

Download and install the appropriate Cloudflared package:

```bash
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-armhf.deb
sudo apt install ./cloudflared-linux-armhf.deb
```

Check installation:

```bash
cloudflared --version
```

---

## 2. Authenticate Cloudflare

```bash
cloudflared login
```

Follow the link printed in terminal, choose your Cloudflare-managed domain, and authorize.

Credentials will be stored in:

```
~/.cloudflared/
```

---

## 3. Create a Tunnel

```bash
cloudflared tunnel create <TUNNEL_NAME>
```

Cloudflare returns a **Tunnel ID**:

```
xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

---

## 4. Create `config.yml`

Create config directory:

```bash
sudo mkdir -p /etc/cloudflared
```

Create the config file:

```bash
sudo nano /etc/cloudflared/config.yml
```

Example content (replace placeholders):

```yaml
tunnel: <TUNNEL-ID>
credentials-file: /home/<USER>/.cloudflared/<TUNNEL-ID>.json

ingress:
  - hostname: <YOUR-DOMAIN>
    service: http://localhost:5000
  - service: http_status:404
```

---

## 5. Map domain to Tunnel

```bash
cloudflared tunnel route dns <TUNNEL_NAME> <YOUR-DOMAIN>
```

---

## 6. Enable Cloudflared as a Service

```bash
sudo cloudflared service install
sudo systemctl enable cloudflared
sudo systemctl start cloudflared
sudo systemctl status cloudflared
```

You should see:

```
Connected to Cloudflare
```

---

## 7. Test

Start your Flask server:

```bash
python3 app.py
```

Access from anywhere:

```
https://<YOUR-DOMAIN>
```

