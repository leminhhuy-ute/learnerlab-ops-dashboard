# Learner Lab Ops Dashboard — Báo cáo tiến độ tuần 1

Mã học phần: **CLCO332779**. Sinh viên: **24110019 — Lê Minh Huy**. Project: `learnerlab-ops`. Owner: `24110019`. Region triển khai: `us-east-1`; phạm vi kiểm kê dự kiến: `us-east-1` và `us-west-2`.

## Bắt đầu

1. Đọc [kế hoạch tuần 1](docs/week-1/00-plan.md) để biết việc cần làm và điều kiện hoàn thành.
2. Đọc [dịch vụ và yêu cầu](docs/week-1/01-services-and-requirements.md), [thiết kế kiến trúc](docs/week-1/02-architecture.md) và [sơ đồ tuần 1](docs/diagrams/architecture-week1-simple.png).
3. Mở Learner Lab, bấm **Start Lab**, chờ sẵn sàng, vào **AWS Console** và chọn **us-east-1**.
4. Làm theo [hướng dẫn dựng nền tảng](docs/week-1/03-foundation-runbook.md). Template nằm tại [infra/week1-foundation.yaml](infra/week1-foundation.yaml).
5. Thu minh chứng theo [checklist](docs/week-1/04-evidence-and-review.md) và ghi thời gian thực tế vào [worklog](docs/week-1/worklog.csv).

## Trạng thái trung thực

**Nền tảng tuần 1 đã triển khai thật** trong Learner Lab, Account ID `213858341631`, Region `us-east-1`: stack `learnerlab-ops-week1` đạt `CREATE_COMPLETE` với 10 tài nguyên. VPC, hai subnet, tuyến Internet, IAM `LabRole` có sẵn và bucket S3 riêng tư đã được kiểm tra bằng AWS CLI. Xem [biên bản triển khai](docs/week-1/07-deployment-record.md) và [ảnh minh chứng](evidence/week-1/README.md).

Lê Minh Huy xác nhận đã đọc tài liệu, sửa sơ đồ/template, chạy một số lệnh AWS và kiểm tra ảnh. Biên bản phiên 08/10 ghi LLM/AI (ChatGPT) trực tiếp triển khai CloudFormation, chạy một số lệnh xác minh và lưu ảnh CLI. [Worklog](docs/week-1/worklog.csv) ghi đầu việc cùng các mốc AWS có nguồn đối chiếu; giờ cá nhân để trống vì không có dữ liệu đo thời lượng. CloudTrail xác nhận thời điểm API, không xác định người trực tiếp thao tác trên máy. Repository GitHub công khai: [leminhhuy-ute/learnerlab-ops-dashboard](https://github.com/leminhhuy-ute/learnerlab-ops-dashboard).

Repository này lưu tài liệu, template, sơ đồ và ảnh minh chứng cho tuần 1. Báo cáo nộp theo yêu cầu hiện tại là tệp Word; không cần đính kèm ZIP nếu hệ thống chỉ nhận báo cáo.

Tuần 1 dựng VPC, hai subnet, Internet Gateway, route và một bucket S3 riêng tư có mã hóa/tag. Các Lambda, EventBridge, DynamoDB, API Gateway, Cost Explorer và SNS thuộc thiết kế tổng thể, được triển khai ở tuần 2–3.

## Kiểm tra cục bộ

```powershell
python .\scripts\validate_week1.py
```

Kiểm tra này kiểm tra cấu trúc template và các giới hạn an toàn của dự án; việc AWS chấp nhận template và quyền Learner Lab phải được xác minh trong tài khoản thật.

Để tạo lại báo cáo trên máy Windows có Microsoft Word, chạy lần lượt `scripts/build-week1-report.py`, `scripts/finalize-week1-report.ps1`, rồi `scripts/package-week1.py`. Bước Word cập nhật mục lục liên kết trong DOCX.

## Kiểm tra / triển khai bằng CLI

Chỉ dùng khi đã có AWS CLI v2 và phiên credentials tạm thời của Learner Lab. Có thể dùng AWS CloudShell nếu Lab cho phép; [CloudShell có AWS CLI và dùng phiên Console](https://docs.aws.amazon.com/cloudshell/latest/userguide/welcome.html).

```powershell
.\scripts\check-aws-session.ps1 -Region us-east-1
.\scripts\deploy-week1.ps1 -Owner 24110019 -Project learnerlab-ops -Region us-east-1 -Execute
```

Hướng dẫn Console trong runbook dùng được khi máy chưa cài AWS CLI. Không đưa access key, secret key, session token hoặc URL presigned vào Git, ảnh báo cáo hay worklog.
