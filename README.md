# AWS Resource Manager CLI

A Python-based command-line tool to manage AWS resources seamlessly using **boto3**. This tool allows you to create and delete S3 buckets, manage EC2 instances, validate IP addresses, and handle DNS records with ease.

## 🚀 Features

- ✅ Create and delete **S3 Buckets**
- ✅ Manage **EC2 Instances**
- ✅ Validate IP addresses and domain names
- ✅ Manage **DNS records** with AWS Route 53
- ✅ Upload and delete files in S3
- ✅ Clear CLI messaging for better user feedback
- ✅ Admin mode for easier testing

## 📦 Installation

1. **Clone the repository:**

```bash
git clone https://github.com/your-username/aws-resource-manager.git
cd aws-resource-manager
```

2. **Create a virtual environment (optional but recommended):**

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Configure AWS credentials:**

Make sure you have AWS CLI installed and configured:

```bash
aws configure
```

## ⚙️ Usage

### Start the CLI

```bash
python aws_manager.py
```

### Sample Commands

- **Create S3 Bucket:**
  ```
  Enter bucket name: my-unique-bucket-name
  ```

- **Delete S3 Bucket:**
  ```
  Deleting bucket: my-unique-bucket-name
  ```

- **Upload File to S3:**
  ```
  Enter file path: ./path/to/file.txt
  Uploading to bucket: my-unique-bucket-name
  ```

- **Manage DNS Record:**
  ```
  Enter domain: example.com
  Enter record type (A, CNAME, etc.): A
  Enter IP address: 192.168.1.1
  ```

### Example Output

```
==================================================
    Creating AWS S3 Bucket... Please Wait
==================================================

- Bucket Name: my-unique-bucket-name
- Status: Provisioning...

Bucket creation in progress!
Check AWS Console for status updates.
==================================================
```

## 🛠️ Functions Overview

- `validate_ip(ip)`: Validates an IPv4 or IPv6 address.
- `validate_domain(domain)`: Checks if a domain name is valid.
- `validate_s3_bucket_name(bucket_name)`: Ensures the bucket name follows AWS naming conventions.

## ✅ Requirements

- Python 3.8+
- boto3
- validators

Install dependencies:

```bash
pip install boto3 validators
```

## 📄 License

This project is licensed under the MIT License.

## 🙌 Acknowledgements

- [AWS SDK for Python (boto3)](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- [Python ipaddress module](https://docs.python.org/3/library/ipaddress.html)

---

**Thank you for using the AWS Resource Manager CLI!**

