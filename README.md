<div align="center">

# 🖼️ Serverless Cloud Image Resizer
### Automated Event-Driven Media Pipeline on AWS

[![AWS](https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white)](https://aws.amazon.com/)
[![AWS Lambda](https://img.shields.io/badge/AWS%20Lambda-FF9900?style=for-the-badge&logo=awslambda&logoColor=white)](https://aws.amazon.com/lambda/)
[![Amazon S3](https://img.shields.io/badge/Amazon%20S3-569A31?style=for-the-badge&logo=amazons3&logoColor=white)](https://aws.amazon.com/s3/)
[![Python 3.12](https://img.shields.io/badge/Python%203.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

<p align="center">
  <b>A zero-maintenance, high-throughput media pipeline that automatically transforms and optimizes uploaded images using AWS Lambda and S3 events.</b>
</p>

[Key Features](#-key-features) • [System Architecture](#-system-architecture) • [Quick Setup](#-quick-setup--deployment) • [Testing & Benchmarks](#-testing--performance) • [Troubleshooting](#-troubleshooting)

</div>

---

## 📌 Executive Summary

Managing media processing on persistent compute instances introduces continuous server costs, idle capacity waste, and complex auto-scaling configurations. 

This repository implements a **100% serverless, event-driven image processing microservice**. Uploading any standard image to a designated Amazon S3 source bucket fires an `s3:ObjectCreated:*` event notification that invokes an AWS Lambda function within milliseconds. The function downloads the stream into ephemeral RAM, resizes it dynamically using **Pillow** while strictly maintaining the aspect ratio, and stores the processed artifact in a separate destination bucket.

---

## ⚡ Key Highlights

- **⚡ Zero Persistent Cost:** Completely idle until an upload occurs; runs comfortably within the AWS Free Tier.
- **🚀 RAM-Only Processing:** Streams images directly via `io.BytesIO` without reading/writing to ephemeral disk (`/tmp`), accelerating execution times.
- **📐 Non-Distorting Aspect Ratio:** Implements Pillow's `thumbnail(..., Image.LANCZOS)` filter to scale dimensions smoothly without stretching.
- **🛡️ Infinite Loop Prevention:** Dispatches artifacts to an isolated target bucket (`my-images-resized`) with a unique `resized_` prefix to avoid recursive triggers.
- **📊 CloudWatch Observability:** Live monitoring of execution duration, payload sizes, dimension conversions, and memory footprint.

---

## 🏛️ System Architecture
[ Client / Web Application ]
│
│  1. Upload Original Image
▼
┌──────────────────────────────────────────────┐
│       Amazon S3 Source Bucket                │
│       (e.g., my-images-input)                │
└──────────────────────┬───────────────────────┘
│
│  2. S3 ObjectCreated Event (PUT)
▼
┌──────────────────────────────────────────────┐       ┌────────────────────────┐
│        AWS Lambda (Python 3.12)              │──────▶│  Amazon CloudWatch     │
│        • Downloads payload to RAM            │       │  Logs & Performance    │
│        • Pillow (Klayers Layer) resize       │       └────────────────────────┘
│        • Preserves MIME type & aspect ratio  │
└──────────────────────┬───────────────────────┘
│
│  3. PutObject (resized_<filename>)
▼
┌──────────────────────────────────────────────┐
│       Amazon S3 Target Bucket                │
│       (e.g., my-images-resized)              │
└──────────────────────────────────────────────┘


---

## 🛠️ Technology Stack

| Domain | Tool / Service | Purpose |
| :--- | :--- | :--- |
| **Runtime** | Python 3.12 | Core compute logic |
| **Compute** | AWS Lambda | Event-driven serverless FaaS environment |
| **Storage** | Amazon S3 | Scalable object storage for inputs and outputs |
| **Image Processing** | Pillow (PIL Fork) | Binary image manipulation and rendering |
| **Security & Auth** | AWS IAM | Principle of least privilege role access |
| **Logging** | Amazon CloudWatch | Real-time diagnostic logging and error tracking |
| **Layer Provider** | Klayers | Pre-compiled Pillow binary layer for Python 3.12 |

---

## 📁 Repository Structure

```text
.
├── lambda_function.py      # Core Lambda execution handler (S3 -> Pillow -> S3)
├── architecture.png        # Architecture workflow diagram
└── README.md               # Project documentation
