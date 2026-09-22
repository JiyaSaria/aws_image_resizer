AWS Image Resizer
A serverless image processing system that automatically resizes images uploaded to Amazon S3 using AWS Lambda and Python.

Architecture
S3 Upload → S3 Event → Lambda → Pillow → Output S3
Tech Stack
AWS Lambda • Amazon S3 • Python • Boto3 • Pillow • IAM • CloudWatch

Features
Automatic image resizing
Event-driven processing
Serverless architecture
Aspect ratio preservation
JPEG, PNG, WEBP & GIF support
Separate input/output S3 buckets
CloudWatch logging
Testing and results
Test Case	Input	Expected Output	Result
TC-01	JPEG (2400×1800)	JPEG (800×600)	✅ Pass
TC-02	PNG (1024×1024)	PNG (800×800)	✅ Pass
TC-03	PNG (400×300)	PNG (400×300), unchanged	✅ Pass
TC-04	WEBP (3000×2000)	WEBP (800×533)	✅ Pass
TC-05	Large JPEG (50 MB)	Resized JPEG (<2 MB)	✅ Pass
TC-06	Invalid file (text file)	Error logged in CloudWatch	✅ Pass
Screenshots
S3 Input Bucket
![S3 Input Bucket](screenshots/s3-input.png)
Lambda Function
![Lambda Function](screenshots/lambda.png)
Resized Images
![S3 Output Bucket](screenshots/s3-output.png)
