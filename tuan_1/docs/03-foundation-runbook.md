# Dựng nền tảng AWS Learner Lab — tuần 1

## Tài nguyên sẽ tạo

Đọc [template](../infra/week1-foundation.yaml) trước khi chạy. Nền tảng gồm VPC `10.20.0.0/16`, hai subnet ở hai Availability Zone, Internet Gateway/route ra Internet và bucket S3 riêng tư có mã hóa. Subnet có route Internet nhưng tắt tự gán public IPv4; không tạo EC2, NAT Gateway, Elastic IP, RDS, SageMaker hay EKS trong bước này.

Tag thống nhất: `Project=learnerlab-ops`, `Owner=24110019`, `Environment=learner-lab`. Stack: `learnerlab-ops-week1`. CloudFormation tự đặt tên bucket duy nhất.

VPC là nền tảng để học mạng theo đề bài. Collector Lambda sẽ gọi API AWS từ môi trường Lambda mặc định; thiết kế hiện tại không yêu cầu đặt Lambda vào VPC này. VPC/Subnet/IGW chưa tạo workload tính phí theo giờ; dữ liệu/request S3 vẫn tính phí theo mức sử dụng. Đọc [Amazon VPC pricing](https://aws.amazon.com/vpc/pricing/) và [Amazon S3 pricing](https://aws.amazon.com/s3/pricing/) để giải thích trong báo cáo.

## 1. Mở đúng tài khoản Lab

1. Vào khóa học AWS Academy và mở **Learner Lab** của môn học.
2. Bấm **Start Lab**, chờ phiên sẵn sàng, sau đó bấm **AWS** để mở AWS Console của Lab.
3. Chọn **US East (N. Virginia) — us-east-1** trên thanh Region.
4. Ghi Account ID từ menu tài khoản và thời điểm kiểm tra. Không dùng tài khoản AWS cá nhân cho bộ tài nguyên này.
5. Vào IAM → Roles, tìm **LabRole** và đọc thông tin role có sẵn. Nếu có EC2 trong các tuần sau, dùng **LabInstanceProfile** có sẵn. Quyền bị hạn chế thì ghi lỗi và phần bị hạn chế vào báo cáo; không tạo IAM user/role mới để vượt giới hạn Lab.

Không cần sửa policy hay trust policy của LabRole để tạo VPC/S3 này. Template không tạo tài nguyên IAM.

## 2. Kiểm tra template cục bộ

Trong PowerShell tại thư mục dự án:

```powershell
python .\tuan_1\scripts\validate_week1.py
```

Nếu Python thiếu thư viện `yaml`, có thể dùng kiểm tra `ValidateTemplate` trên AWS ở bước CLI, hoặc cài PyYAML bằng trình quản lý gói Python trước khi kiểm tra cục bộ. Máy chuẩn bị tài liệu này đã có PyYAML.

## 3A. Triển khai bằng AWS Console

Đây là cách bắt đầu khi máy chưa có AWS CLI.

1. Mở **CloudFormation** trong `us-east-1` → **Create stack** → **With new resources (standard)**.
2. Chọn **Choose an existing template** → **Upload a template file** → chọn `tuan_1/infra/week1-foundation.yaml` → **Next**.
3. Nhập stack name `learnerlab-ops-week1`; tham số Project `learnerlab-ops`, Owner `24110019`, Environment `learner-lab` → **Next**.
4. Ở Stack options, thêm tags Project/Owner/Environment cùng giá trị trên. Phần Permissions giữ cách dùng phiên tài khoản hiện tại, không tạo role mới. Giữ rollback mặc định.
5. Rà soát tài nguyên sẽ tạo và bấm **Submit/Create stack**. Template không có IAM nên không cần cấp quyền tạo IAM.
6. Xem tab **Events** đến khi stack có trạng thái **CREATE_COMPLETE**.
7. Mở tab **Outputs**, lưu VPC ID, Subnet ID và tên S3 bucket. Dùng các Output này ở bước xác minh và tuần 2.

Nếu đã có stack cùng tên, kiểm tra nội dung trước; dùng **Update stack** với template này để cập nhật đúng stack của dự án. Không xóa stack chỉ để xử lý trùng tên.

## 3B. Triển khai bằng CLI (lựa chọn thay thế)

Máy cục bộ phải có AWS CLI v2 và credentials **tạm thời** của Learner Lab, gồm session token. Tự nhập credentials trên máy từ **AWS Details** của Lab; không gửi vào chat hoặc lưu trong dự án/Git.

Nếu Lab cho phép AWS CloudShell, có thể dùng phiên Console đã đăng nhập và AWS CLI cài sẵn. Upload template và hai script PowerShell, giữ cấu trúc `tuan_1/infra/` và `tuan_1/scripts/`, vào thư mục gốc rồi gõ `pwsh`. [Tài liệu CloudShell](https://docs.aws.amazon.com/cloudshell/latest/userguide/welcome.html).

```powershell
.\tuan_1\scripts\check-aws-session.ps1 -Region us-east-1
.\tuan_1\scripts\deploy-week1.ps1 -Owner 24110019 -Project learnerlab-ops -Region us-east-1 -Execute
```

Script triển khai kiểm tra phiên, Region và template rồi triển khai CloudFormation. Có thể bỏ `-Execute` để chỉ tạo change set và xem thay đổi. Đây là chế độ xem trước tùy chọn; lệnh phía trên thực hiện triển khai.

Nếu dùng profile riêng tên `learnerlab`, thêm `-Profile learnerlab` vào cả hai lệnh. Chờ kết quả thành công, sau đó chạy:

```powershell
.\tuan_1\scripts\check-aws-session.ps1 -Region us-east-1 -StackName learnerlab-ops-week1
```

Lệnh này không thực hiện gọi Cost Explorer.

## 4. Xác minh kết quả trong Console

| Thành phần | Mở ở đâu | Kết quả cần thấy |
|---|---|---|
| Stack | CloudFormation → stack → Events/Outputs | CREATE_COMPLETE hoặc UPDATE_COMPLETE, ID tài nguyên |
| VPC | VPC → Your VPCs, lọc VPC ID từ Outputs | CIDR 10.20.0.0/16, tag Project/Owner/Environment |
| Subnet | VPC → Subnets, lọc VPC ID | Hai subnet/hai AZ; Auto-assign public IPv4 tắt |
| Route | VPC → Route tables, lọc VPC ID | Route 0.0.0.0/0 trỏ IGW, association đúng subnet |
| IGW | VPC → Internet gateways | IGW attached đúng VPC; có tag |
| S3 | S3 → bucket từ Outputs → Properties | Default encryption SSE-S3; tag Project/Owner/Environment |
| S3 access | S3 → bucket → Permissions | Block Public Access bật cả bốn tùy chọn; Object Ownership Bucket owner enforced |
| IAM | IAM → LabRole | Role đã tồn tại; ARN thuộc đúng tài khoản Lab |

Bucket tuần 1 chứa tài liệu/asset riêng tư. Tuần 2–3 có thể phục vụ một file HTML độc lập bằng URL HTTPS presigned tạm thời; hiện tại chưa có website hay API hoạt động. [Website endpoint S3 dùng HTTP](https://docs.aws.amazon.com/AmazonS3/latest/userguide/WebsiteEndpoints.html), nên thiết kế này giữ bucket riêng tư và dùng HTTPS cho demo có thông tin tài khoản.

Để thực hành thao tác S3, mở bucket → **Create folder** `week1` → upload `README.md` của dự án → tải file về và đối chiếu nội dung. Giữ nguyên Block Public Access. Chụp màn hình object đã upload và ghi nhận thao tác trong worklog; không upload credentials hay tệp riêng tư khác.

## 5. Khi có lỗi

| Lỗi | Xử lý |
|---|---|
| ExpiredToken/InvalidClientTokenId | Kiểm tra Lab còn chạy, lấy lại phiên credentials tạm thời rồi kiểm tra STS |
| AccessDenied khi tạo stack/tài nguyên | Đọc Events để biết API bị chặn; lưu minh chứng và hỏi GVHD về quyền dịch vụ được phép |
| AccessDenied khi đọc IAM | Kiểm tra LabRole qua Console nếu được; ghi rõ phần chưa xác minh |
| Region khác hai Region được phép | Chuyển về us-east-1 hoặc us-west-2, kiểm tra lại trước khi triển khai |
| ROLLBACK_COMPLETE | Đọc lỗi gốc trong Events; kiểm tra tài nguyên S3 Retain có thể còn lại; sửa nguyên nhân trước khi xử lý stack |
| Fn::Select không có phần tử AZ thứ hai | Template giả định GetAZs trả ít nhất hai AZ. Kiểm tra default subnet/AZ của Lab đã bị thay đổi hay chưa, ghi lại Events trước khi điều chỉnh thiết kế |
| CloudShell không dùng được | Dùng quy trình Console 3A hoặc AWS CLI với credentials tạm thời |

## 6. Cuối buổi

Ghi worklog và lưu minh chứng trước khi End Lab. Kiểm tra cả `us-east-1` và `us-west-2` để phát hiện workload đã có đang tốn phí. Chỉ dừng/xóa tài nguyên thuộc phạm vi dự án khi đã xác định đúng; không tác động tài nguyên dùng chung của lớp.

VPC/S3 nền tảng được giữ để dùng tuần 2. S3 có `DeletionPolicy: Retain` và `UpdateReplacePolicy: Retain`: xóa/cập nhật stack không tự xóa dữ liệu bucket được giữ lại; cuối dự án cần xử lý bucket riêng sau khi sao lưu minh chứng. [CloudFormation DeletionPolicy](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-attribute-deletionpolicy.html).

**End Lab không được dùng như bằng chứng tài nguyên đã bị xóa hoặc đã ngừng mọi chi phí.** Kiểm tra tài nguyên thực tế và hướng dẫn của môi trường Learner Lab.

Ghi chú AZ: [Fn::GetAZs](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/intrinsic-function-reference-getavailabilityzones.html) thường trả các AZ có default subnet nếu chúng tồn tại; vì vậy cần kiểm tra Events nếu môi trường Lab đã bị chỉnh sửa từ trước.
