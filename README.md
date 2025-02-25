# AWS Resource Manager CLI

A Python-based command-line tool to manage AWS resources seamlessly using **boto3**. This tool allows you to manage EC2, S3, and Route53!

## 🚀 Features

- ✅ Create and delete **S3 Buckets**
- ✅ Upload and delete files in S3
- ✅ Manage **EC2 Instances**
- ✅ Create **Hosted Zones** with AWS Route 53
- ✅ Manage **DNS records** with AWS Route 53
- ✅ Clear CLI messaging for better user feedback
- ✅ Admin mode for easier testing

## 📦 Installation

1. **Clone the repository:**

```bash
git clone https://github.com/TomerLevy743/IntegrativePythonAws.git
cd IntegrativePythonAws
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Configure AWS credentials:**

Make sure you have AWS CLI installed and configured:

```bash
aws configure
```

## ⚙️ Usage

### Start the CLI

```bash
python __main__.py
```

### Admin Mode
 for testing 
- username > admin
- password > 0000

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


## 🙌 Acknowledgements

- [AWS SDK for Python (boto3)](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- [Python ipaddress module](https://docs.python.org/3/library/ipaddress.html)

---

**Thank you for using the AWS Resource Manager CLI!**

