# 🚀 3-Tier AWS Architecture Project

> Full-stack cloud deployment with Frontend, Backend, Database, Load Balancers and Monitoring

![AWS](https://img.shields.io/badge/AWS-EC2%20%7C%20RDS%20%7C%20ALB%20%7C%20NLB-orange?style=for-the-badge&logo=amazonaws)
![Flask](https://img.shields.io/badge/Backend-Flask-green?style=for-the-badge&logo=flask)
![Nginx](https://img.shields.io/badge/Frontend-Nginx-blue?style=for-the-badge&logo=nginx)
![MySQL](https://img.shields.io/badge/Database-MySQL%20RDS-yellow?style=for-the-badge&logo=mysql)
![Prometheus](https://img.shields.io/badge/Monitoring-Prometheus%20%7C%20Grafana-red?style=for-the-badge&logo=prometheus)

---

## 📐 Architecture

```
Users (Browser)
      ↓
ALB — Application Load Balancer  (Internet Facing)
      ↓
Frontend EC2 — Nginx             (Public Subnet)
      ↓
NLB — Network Load Balancer      (Internal)
      ↓
Backend EC2 — Flask App          (Private Subnet)
      ↓
RDS MySQL Database               (Private Subnet)

Prometheus + Grafana EC2         (Monitoring)
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Cloud | AWS EC2, VPC, RDS, ALB, NLB |
| Frontend | HTML, CSS, JavaScript, Nginx |
| Backend | Python Flask, Flask-CORS |
| Database | AWS RDS MySQL |
| Monitoring | Prometheus, Grafana, Node Exporter |
| Security | Security Groups, Private Subnets |

---

## 📁 Project Structure

```
3-tier-aws-project/
├── index.html          # Frontend HTML
├── styles.css          # Dark green theme CSS
├── script.js           # Login button API call
├── app.py              # Flask backend API
└── README.md           # Documentation
```

---

## ⚙️ Setup Guide

### Step 1 — Frontend EC2 (Nginx)

```bash
# Install Nginx
sudo yum install nginx -y
sudo systemctl start nginx
sudo systemctl enable nginx

# Move files to nginx root
mv index.html styles.css script.js /usr/share/nginx/html/
```

### Step 2 — Nginx Reverse Proxy Config

```bash
sudo nano /etc/nginx/conf.d/reverse_proxy.conf
```

```nginx
server {
    listen 80;
    server_name _;

    location / {
        root /usr/share/nginx/html;
        index index.html;
    }

    location /login {
        proxy_pass http://YOUR-INTERNAL-NLB-URL/login;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /users {
        proxy_pass http://YOUR-INTERNAL-NLB-URL/users;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
# Test and restart
sudo nginx -t
sudo systemctl restart nginx
```

### Step 3 — Backend EC2 (Flask)

```bash
# Install dependencies
sudo yum install python3 python3-pip -y
sudo pip3 install flask flask-cors mysql-connector-python prometheus-client

# Run Flask app
nohup python3 app.py > output.log 2>&1 &

# Verify
curl http://localhost:5000/
```

### Step 4 — RDS MySQL Setup

```bash
# Connect to RDS
mysql -h YOUR-RDS-ENDPOINT -u admin -p

# Setup database
USE your_database;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50),
    email VARCHAR(100),
    password VARCHAR(100)
);

# Insert sample data
INSERT INTO users (username, email, password) VALUES
('Vasanth', 'vasanth@gmail.com', 'Pass123#'),
('Karthik', 'karthik@gmail.com', 'Pass123#'),
('Praveen', 'praveen@gmail.com', 'Pass123#');
```

### Step 5 — Node Exporter (Frontend & Backend EC2)

```bash
# Download and run Node Exporter
wget https://github.com/prometheus/node_exporter/releases/download/v1.6.0/node_exporter-1.6.0.linux-amd64.tar.gz
tar -xvf node_exporter-1.6.0.linux-amd64.tar.gz
cd node_exporter-1.6.0.linux-amd64
nohup ./node_exporter > node_exporter.log 2>&1 &

# Verify
curl http://localhost:9100/metrics
```

### Step 6 — Prometheus & Grafana EC2

```bash
# Download Prometheus
wget https://github.com/prometheus/prometheus/releases/download/v2.45.0/prometheus-2.45.0.linux-amd64.tar.gz
tar -xvf prometheus-2.45.0.linux-amd64.tar.gz
cd prometheus-2.45.0.linux-amd64

# Edit prometheus.yml
nano prometheus.yml
```
### prometheus confi.yaml

```path
/etc/prometheus/prometheus.yml
```
```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:

  # Prometheus self monitoring
  - job_name: "prometheus"
    static_configs:
      - targets: ["localhost:9090"]


  # Frontend EC2 Node Exporter
  - job_name: "frontend-ec2"

    ec2_sd_configs:
      - region: eu-west-2
        port: 9100

    relabel_configs:
      - source_labels: [__meta_ec2_tag_Monitor]
        action: keep
        regex: frontend


  # Backend EC2 Node Exporter
  - job_name: "backend-ec2"

    ec2_sd_configs:
      - region: eu-west-2
        port: 9100

    relabel_configs:
      - source_labels: [__meta_ec2_tag_Monitor]
        action: keep
        regex: backend


  # Backend Flask Application Metrics
  - job_name: "backend-flask"

    ec2_sd_configs:
      - region: eu-west-2
        port: 5000

    metrics_path: /metrics

    relabel_configs:
      - source_labels: [__meta_ec2_tag_Monitor]
        action: keep
        regex: backend
```

```bash
# Start Prometheus
nohup ./prometheus --config.file=prometheus.yml > prometheus.log 2>&1 &

# Install Grafana
sudo yum install grafana -y
sudo systemctl start grafana-server
sudo systemctl enable grafana-server
```
---
### ADD IAM Role Prometheus EC2

```JSON
{
 "Effect": "Allow",
 "Action": [
   "ec2:DescribeInstances",
   "ec2:DescribeTags"
 ],
 "Resource": "*"
}
```

---

## 🔒 Security Group Ports

| EC2 | Port | Purpose | Source |
|---|---|---|---|
| Frontend | 80 | Nginx HTTP | 0.0.0.0/0 |
| Frontend | 22 | SSH | Your IP |
| Frontend | 9100 | Node Exporter | Prometheus IP |
| Backend | 5000 | Flask App | 0.0.0.0/0 |
| Backend | 22 | SSH | Your IP |
| Backend | 9100 | Node Exporter | Prometheus IP |
| Prometheus | 9090 | Prometheus UI | 0.0.0.0/0 |
| Prometheus | 3000 | Grafana UI | 0.0.0.0/0 |
| Prometheus | 22 | SSH | Your IP |

---

## 🌐 Access URLs

| Service | URL |
|---|---|
| Frontend Website | `http://ALB-DNS-URL` |
| Prometheus | `http://Prometheus-EC2-IP:9090` |
| Grafana | `http://Prometheus-EC2-IP:3000` |

> Grafana default login: **admin / admin**

---

## 📊 API Routes

| Route | Method | Purpose |
|---|---|---|
| `/` | GET | Health check |
| `/login` | GET | Get first user from DB |
| `/users` | GET | Get all users from DB |
| `/metrics` | GET | Prometheus metrics |

---

## 👨‍💻 Author

**R. Vasanth Raj**
AWS Cloud & DevOps Engineer
Chennai, Tamil Nadu

[![GitHub](https://img.shields.io/badge/GitHub-SoloXtree-black?style=flat&logo=github)](https://github.com/SoloXtree)

---

## 📌 Notes

- Replace `YOUR-INTERNAL-NLB-URL` with your actual NLB DNS name
- Replace `YOUR-RDS-ENDPOINT` with your actual RDS endpoint
- Replace `FRONTEND-PRIVATE-IP` and `BACKEND-PRIVATE-IP` with actual private IPs
- Always use `sudo` for system commands on EC2
