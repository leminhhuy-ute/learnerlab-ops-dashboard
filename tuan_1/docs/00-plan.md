# Kế hoạch và đầu ra tuần 1

## Thông tin

| Nội dung | Giá trị |
|---|---|
| Mã học phần | `CLCO332779` |
| Đề tài | Bảng điều khiển vận hành cho AWS Learner Lab |
| Sinh viên đã xác nhận | 24110019 — Lê Minh Huy |
| Tag Project | `learnerlab-ops` |
| Tag Owner | `24110019` |
| Tag Environment | `learner-lab` |
| Region dựng nền tảng | `us-east-1` |
| Region kiểm kê dự kiến | `us-east-1`, `us-west-2` |
| Ngày chuẩn bị tài liệu | 07/10/2026, giờ Việt Nam |

Ảnh đề bài là nguồn yêu cầu môn học. Kế hoạch này áp dụng phần tuần 1: tìm hiểu dịch vụ, thiết kế kiến trúc, vẽ sơ đồ, dựng nền tảng VPC/IAM LabRole/S3 và gắn tag.

## Phân công một thành viên

Các đầu việc dưới đây là kế hoạch; thời lượng thực tế được ghi riêng trong worklog.

| Nhóm việc | Người phụ trách | Công việc | Sản phẩm |
|---|---|---|---|
| Tìm hiểu dịch vụ | Lê Minh Huy | Đọc đề, tìm hiểu Lambda/EventBridge/DynamoDB/API Gateway/S3/SNS/Cost Explorer; giải thích EC2/RDS/SageMaker/EKS | Ghi chú dịch vụ và giới hạn Lab |
| Thiết kế | Lê Minh Huy | Thiết kế luồng dữ liệu, lịch lấy dữ liệu, dữ liệu snapshot, bảo mật và sơ đồ | Tài liệu kiến trúc + sơ đồ |
| Dựng nền tảng | Lê Minh Huy | Start Lab, xác minh Region/LabRole, triển khai VPC và S3 với tag | Stack thật + ảnh Console/CLI |
| Rà soát | Lê Minh Huy | Xác minh tài nguyên/tag, kiểm tra minh chứng, đọc và giải thích template, ghi worklog và rà soát báo cáo | Checklist, worklog, bản tổng kết tuần |

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
- [ ] Bổ sung ngày và giờ thực tế cho từng đầu việc sau khi đối chiếu ghi chép hoặc lịch sử thao tác riêng của sinh viên.
- [x] Rà soát cuối buổi và End Lab; kiểm tra EC2 đang chạy/NAT khả dụng ở hai Region được phép.

## Điều kiện hoàn thành tuần 1

Nền tảng AWS và minh chứng đã hoàn tất ngày 08/10/2026; xem [biên bản](07-deployment-record.md). Sinh viên xác nhận đã đọc tài liệu, sửa sơ đồ/template, chạy lệnh AWS và kiểm tra ảnh, đồng thời cung cấp tổng thời lượng tuần 1 là 8 giờ. Chưa có ghi chép phân bổ thời gian cho từng đầu việc; các ô giờ chi tiết trong worklog để trống. Tổng giờ sinh viên cung cấp chưa có bằng chứng thời lượng độc lập; không suy ra giờ làm từ thời gian phiên Lab hoặc thời gian LLM/AI (ChatGPT) thao tác.

## Kế hoạch tuần 2

Thứ tự triển khai: DynamoDB và Lambda kiểm kê → Lambda chi phí → Lambda đọc dữ liệu và API Gateway → lịch EventBridge → giao diện S3 → cảnh báo SNS và kiểm thử từng thành phần. Người phụ trách là Lê Minh Huy — 24110019. Xem bảng công việc và kết quả cần kiểm tra tại mục **Kế hoạch tuần 2** trong [báo cáo tuần 1](../README.md).

Không cần tạo EC2/RDS/EKS/SageMaker mới chỉ để thử dashboard; trước hết đọc tài nguyên có sẵn và hiển thị trạng thái không có tài nguyên hoặc thiếu quyền một cách rõ ràng. Ghi số giờ thực tế và phần có AI hỗ trợ trong worklog của tuần 2.
