# Biên bản triển khai nền tảng tuần 1

## Kết quả đã xác minh trên AWS

Ngày **08/10/2026, giờ Việt Nam**; tài khoản Learner Lab `213858341631`, Region `us-east-1`. AWS CLI `sts get-caller-identity` đã xác nhận đúng tài khoản trước khi triển khai. Template [week1-foundation.yaml](../../infra/week1-foundation.yaml) có SHA-256 `649857a229327af489b40bd6998f35cf015fa91176026542e1610ef4e41d9bc4` tại bản được chuyển vào Lab. AWS CloudFormation `ValidateTemplate` chấp nhận template.

Stack `learnerlab-ops-week1` đạt **CREATE_COMPLETE** lúc **12:52:18**. `ListStackResources` trả **10 tài nguyên**, tất cả `CREATE_COMPLETE`. Output và tài nguyên đã đọc lại bằng API:

| Thành phần | Giá trị / cấu hình |
|---|---|
| Stack ARN | `arn:aws:cloudformation:us-east-1:213858341631:stack/learnerlab-ops-week1/bc73fb60-c2db-11f1-821c-0afffe7c9dc3` |
| VPC | `vpc-0206a78d96a4b3a57`, CIDR `10.20.0.0/16`, DNS support/hostnames từ template |
| Subnet A | `subnet-0fe1f68d4d015130c`, `us-east-1a`, `10.20.1.0/24`, `MapPublicIpOnLaunch=False` |
| Subnet B | `subnet-0a26fc106be139906`, `us-east-1b`, `10.20.2.0/24`, `MapPublicIpOnLaunch=False` |
| Route table | `rtb-0d686db1acc56489d`, gắn hai subnet, route `0.0.0.0/0` đang active |
| Internet Gateway | `igw-0998040b443aaa624`, route target, attachment ở trạng thái `available` |
| Bucket S3 | `learnerlab-ops-week1-artifactbucket-u4t7cql7ngfo` |
| S3 security | 4/4 cờ Block Public Access `True`; SSE-S3 `AES256`; Object Ownership `BucketOwnerEnforced` |
| S3 lifecycle | Abort incomplete multipart uploads sau 7 ngày |
| IAM | `arn:aws:iam::213858341631:role/LabRole` tồn tại; không tạo IAM user/role |

Các tài nguyên có thể gắn tag đều dùng `Project=learnerlab-ops`, `Owner=24110019`, `Environment=learner-lab`. Đã kiểm tra Project/Owner trên VPC, hai subnet, route table, IGW và bucket; AWS cũng thêm các tag CloudFormation. Route, gateway attachment và subnet association không hỗ trợ cùng cơ chế tag trong template.

Ảnh thật: [stack và output](../../evidence/week-1/02-stack-complete.jpg), [subnet và route](../../evidence/week-1/03-network-check.jpg), [bảo mật S3](../../evidence/week-1/04-s3-private.jpg). Ảnh có thời gian UTC−07:00, Account ID và Region. Các thông số chính cũng được ghi trong [bảng minh chứng](04-evidence-and-review.md).

## Cách triển khai và kiểm tra

Terminal nhúng của Vocareum mặc định dùng role vận hành thuộc tài khoản khác. LLM/AI (ChatGPT) đã dùng credentials CLI tạm thời từ **AWS Details** của chính Learner Lab trong một tệp `/tmp` riêng, chỉ cho phiên này. STS trả `213858341631`; không dùng quyền role mặc định để triển khai. Lệnh triển khai:

```bash
aws cloudformation validate-template --template-body file:///tmp/learnerlab-week1.yaml --region us-east-1
aws cloudformation deploy --template-file /tmp/learnerlab-week1.yaml \
  --stack-name learnerlab-ops-week1 --region us-east-1 \
  --parameter-overrides Project=learnerlab-ops Owner=24110019 Environment=learner-lab \
  --tags Project=learnerlab-ops Owner=24110019 Environment=learner-lab
```

Các lệnh `describe-stacks`, `list-stack-resources`, `iam get-role`, `ec2 describe-vpcs/subnets/route-tables/internet-gateways/tags` và `s3api get-public-access-block/get-bucket-encryption/get-bucket-ownership-controls/get-bucket-tagging/get-bucket-lifecycle-configuration` đã chạy thành công bằng cùng phiên. Sau đó LLM/AI (ChatGPT) đã xóa tệp credentials, bản template tạm, biến môi trường và lịch sử lệnh; terminal in `Temporary credentials removed`. Không chép keys/token vào repository hoặc ảnh.

## Chi phí và phần còn mở

Lab hiển thị `Used $0 of $50` lúc kiểm tra, nhưng chỉ số ngân sách có độ trễ. Lệnh đọc EC2 và NAT ở `us-east-1`, `us-west-2` không trả EC2 `running` hay NAT Gateway `available` tại thời điểm kiểm tra. Stack không tạo EC2, NAT, EIP, RDS hay dịch vụ compute. Bucket hiện chưa lưu artifact; thao tác S3 trong tương lai vẫn có thể phát sinh phí request/dữ liệu. `DeletionPolicy: Retain` giữ bucket khi xóa stack, nên cần kiểm tra riêng cuối dự án.

Phiên Lab đã được **End Lab** sau khi kiểm tra; cổng hiển thị trạng thái **Terminated**. Việc hết giờ/End Lab không xóa stack hoặc bucket, và không tự chứng minh chi phí bằng 0.

**Chưa xác minh** `LabInstanceProfile` bằng IAM API; output tên profile trong template không khẳng định profile tồn tại. [Worklog](worklog.csv) ghi riêng phần việc và tổng giờ sinh viên tự khai; chưa có thời lượng thực tế cho từng nhiệm vụ. Sinh viên cần đọc kiến trúc/template và tự giải thích trong buổi vấn đáp.
