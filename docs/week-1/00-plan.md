# Kế hoạch và đầu ra tuần 1

## Thông tin

| Nội dung | Giá trị |
|---|---|
| Đề tài | Bảng điều khiển vận hành cho AWS Learner Lab |
| Sinh viên đã xác nhận | 24110019 — Lê Minh Huy |
| Tag Project | `learnerlab-ops` |
| Tag Owner | `24110019` |
| Tag Environment | `learner-lab` |
| Region dựng nền tảng | `us-east-1` |
| Region kiểm kê dự kiến | `us-east-1`, `us-west-2` |
| Ngày chuẩn bị tài liệu | 07/10/2026, giờ Việt Nam |

Ảnh đề bài là nguồn yêu cầu môn học. Kế hoạch này áp dụng phần tuần 1: tìm hiểu dịch vụ, thiết kế kiến trúc, vẽ sơ đồ, dựng nền tảng VPC/IAM LabRole/S3 và gắn tag.

## Phân công một thành viên — tối thiểu 8 giờ dự kiến

Thời gian dưới đây là **kế hoạch**, cần tự ghi lại số giờ thực tế; không dùng bảng này để khẳng định đã làm đủ giờ.

| Buổi | Người phụ trách | Công việc | Giờ dự kiến | Sản phẩm |
|---|---|---|---:|---|
| 1 | Lê Minh Huy | Đọc đề, tìm hiểu Lambda/EventBridge/DynamoDB/API Gateway/S3/SNS/Cost Explorer; giải thích EC2/RDS/SageMaker/EKS | 2 | Ghi chú dịch vụ và giới hạn Lab |
| 2 | Lê Minh Huy | Thiết kế luồng dữ liệu, lịch lấy dữ liệu, dữ liệu snapshot, bảo mật và sơ đồ | 2 | Tài liệu kiến trúc + sơ đồ |
| 3 | Lê Minh Huy | Start Lab, xác minh Region/LabRole, triển khai VPC và S3 với tag | 2 | Stack thật + ảnh Console/CLI |
| 4 | Lê Minh Huy | Xác minh tài nguyên/tag, chụp minh chứng, đọc và giải thích template, ghi worklog và rà soát báo cáo | 2 | Checklist, worklog thực tế, bản tổng kết tuần |
| **Tổng** | | | **8** | |

Nếu có thêm thành viên, bổ sung mã sinh viên và phân công riêng; mỗi người vẫn phải có ít nhất 8 giờ thực tế trong tuần.

## Checklist làm theo thứ tự

- [ ] Đọc và giải thích vai trò của 7 dịch vụ chính và 4 dịch vụ được kiểm kê.
- [ ] Phân biệt tài nguyên đang chạy, ước tính theo cấu hình và chi phí Cost Explorer có độ trễ.
- [ ] Giải thích luồng EventBridge → Lambda → DynamoDB → API → web và nhánh cảnh báo SNS.
- [ ] Chốt lịch kiểm kê và ngân sách request Cost Explorer; xử lý `AccessDenied` và dữ liệu cũ.
- [x] Mở Learner Lab; xác nhận tài khoản, Region, thời điểm và LabRole có sẵn.
- [x] Triển khai template nền tảng trong `us-east-1`.
- [x] Xác minh VPC, subnet, route, S3 mã hóa/Block Public Access và tag Project/Owner.
- [x] Lưu ảnh minh chứng có Account ID, Region và thời điểm; loại bỏ credentials/URL ký.
- [x] Ghi tổng 8 giờ sinh viên tự khai, các nhiệm vụ và phần AI hỗ trợ trong worklog; phân bổ theo buổi chưa được cung cấp.
- [x] Rà soát cuối buổi và End Lab; kiểm tra EC2 đang chạy/NAT khả dụng ở hai Region được phép.

## Điều kiện hoàn thành tuần 1

Nền tảng AWS và minh chứng đã hoàn tất ngày 08/10/2026; xem [biên bản](07-deployment-record.md). Sinh viên tự khai tổng 8 giờ tuần 1, đã ghi trong worklog; chưa có phân bổ theo buổi hoặc kiểm tra khả năng tự giải thích cấu hình. Không suy ra giờ làm của sinh viên từ thời gian phiên Lab hoặc thời gian Codex thao tác.

## Phần chuyển sang tuần 2

Lập trình collector Lambda, tạo bảng snapshot DynamoDB, lập lịch EventBridge, tạo API và web đọc dữ liệu, làm cảnh báo SNS. Không cần tạo EC2/RDS/EKS/SageMaker mới chỉ để thử dashboard; trước hết đọc tài nguyên có sẵn và hiển thị trạng thái không có tài nguyên hoặc thiếu quyền một cách rõ ràng.
