# Bảng điều khiển vận hành AWS Learner Lab

**Mã học phần:** CLCO332779 · **Sinh viên:** Lê Minh Huy — MSSV 24110019 · **Repository:** [leminhhuy-ute/learnerlab-ops-dashboard](https://github.com/leminhhuy-ute/learnerlab-ops-dashboard)

Mỗi tuần có thư mục riêng ở cấp repository để giảng viên xem báo cáo tiến độ, mã nguồn, worklog và minh chứng cùng một chỗ. Nội dung báo cáo được nộp trên hệ thống môn học kèm liên kết đến các tệp và commit tương ứng.

| Thư mục | Nội dung |
|---|---|
| [`tuan_1/`](tuan_1/README.md) | Yêu cầu, thiết kế, sơ đồ, template nền tảng, worklog và ảnh Learner Lab của tuần 1. |
| [`tuan_2/`](tuan_2/README.md) | Mã nguồn Lambda/dashboard, chức năng đã triển khai, kết quả kiểm thử, worklog và ảnh AWS của tuần 2. |
| [`tuan_3/`](tuan_3/README.md) | Mã và kết quả tuần 3: SNS pending, freshness guard, API SigV4, CloudWatch alarm, security review và worklog riêng. |
| [`tuan_4/`](tuan_4/README.md) | Đã hoàn thành 3/4 nhóm công việc (75%): kiểm thử hồi quy, rà soát chi phí/tài nguyên, rà soát bảo mật và dọn một alarm thử sau khi lưu cấu hình/lịch sử; còn chốt sản phẩm, tổng kết và demo. |
| [`docs/`](docs/data-sources.md) | Tài liệu nguồn dữ liệu dùng chung, xác định API AWS gốc và giới hạn cách diễn giải. |

## Tiến độ đã xác minh

- **Tuần 1:** CloudFormation stack `learnerlab-ops-week1` đạt `CREATE_COMPLETE` với 10 tài nguyên nền tảng tại `us-east-1`. VPC, subnet, route Internet, `LabRole` có sẵn và bucket S3 riêng tư đã được kiểm tra. Xem [biên bản triển khai](tuan_1/docs/07-deployment-record.md) và [ảnh nền tảng](tuan_1/evidence/README.md).
- **Tuần 2:** Lambda kiểm kê, billing, read API và threshold alert; DynamoDB, API Gateway, S3, EventBridge, Cost Explorer và SNS đã được triển khai/kiểm thử. Ảnh ngày 15/10/2026 ghi nhận 10 tổ hợp dịch vụ/vùng có `status=ok`, `count=0`; GET /summary có SigV4 trả HTTP 200, không ký trả HTTP 403. Giao diện hiển thị JSON thật đã nạp thủ công. Chi phí `1E-10 USD` là ước tính, không phải hóa đơn cuối kỳ. Xem [kết quả và kiểm thử tuần 2](tuan_2/README.md).
- **Tuần 3:** 12/12 unit tests đạt; Lambda thử xác minh freshness và SNS `PendingConfirmation`; API `/summary` có SigV4 trả HTTP 200, request không ký bị từ chối; CloudWatch alarm đã chuyển qua `In alarm` và trở về `OK` trên lỗi thử có kiểm soát. Ngày 21/10, mã cảnh báo tuần 3 được đưa lên Lambda sản phẩm và gọi thử thành công với snapshot mới, dưới ngưỡng 10 USD. Xem [kết quả tuần 3](tuan_3/README.md) và [ảnh triển khai sản phẩm](tuan_3/evidence/10-product-alert-deployment.md).
- **Tuần 4, đến 22/10 — 75% kế hoạch:** hai bucket vẫn chặn công khai và dùng SSE-S3, sáu Lambda dùng LabRole và không có Function URL; API SigV4 trả 200, không ký trả 403. Đã dọn alarm Lambda thử sau khi lưu cấu hình và bốn bản ghi lịch sử; bốn alarm sản phẩm giữ nguyên cấu hình. Xem [rà soát bảo mật/dọn dẹp và ảnh AWS](tuan_4/evidence/03-security-cleanup-2026-10-22.md). Worklog hiện có 7 giờ sinh viên tự xác nhận; các thao tác AI được khai riêng.

Worklog giữ giờ sinh viên chưa xác nhận ở dạng trống; không suy ra giờ học từ thời gian AI thao tác, thời lượng phiên Lab hay mốc CloudTrail.

Không đưa access key, secret key, session token, URL presigned hoặc thông tin đăng nhập vào repository. Ảnh SNS công khai không hiển thị địa chỉ email người nhận.
