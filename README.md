# Bảng điều khiển vận hành AWS Learner Lab

**Mã học phần:** CLCO332779 · **Sinh viên:** Lê Minh Huy — MSSV 24110019 · **Repository:** [leminhhuy-ute/learnerlab-ops-dashboard](https://github.com/leminhhuy-ute/learnerlab-ops-dashboard)

Mỗi tuần có thư mục riêng ở cấp repository để giảng viên xem báo cáo tiến độ, mã nguồn, worklog và minh chứng cùng một chỗ. Nội dung báo cáo được nộp trên hệ thống môn học kèm liên kết đến các tệp và commit tương ứng.

| Thư mục | Nội dung |
|---|---|
| [`tuan_1/`](tuan_1/README.md) | Yêu cầu, thiết kế, sơ đồ, template nền tảng, worklog và ảnh Learner Lab của tuần 1. |
| [`tuan_2/`](tuan_2/README.md) | Mã nguồn Lambda/dashboard, chức năng đã triển khai, kết quả kiểm thử, worklog và ảnh AWS của tuần 2. |
| [`tuan_3/`](tuan_3/README.md) | Mã và kết quả tuần 3: SNS pending, freshness guard, API SigV4, CloudWatch alarm, security review và worklog riêng. |
| [`tuan_4/`](tuan_4/README.md) | Minh chứng AWS ngày 23/10 cho hồi quy, read-api bảng rỗng, giao diện, bảo mật và hai nhánh SNS; 16/16 kiểm thử cục bộ chạy lại ngày 27/10 đều đạt. Word tổng kết đã xong; có kịch bản video riêng. Video và dọn tài nguyên còn giữ chưa hoàn tất. |
| [`docs/`](docs/data-sources.md) | Tài liệu nguồn dữ liệu dùng chung, xác định API AWS gốc và giới hạn cách diễn giải. |

## Tiến độ đã xác minh

- **Tuần 1:** CloudFormation stack `learnerlab-ops-week1` đạt `CREATE_COMPLETE` với 10 tài nguyên nền tảng tại `us-east-1`. VPC, subnet, route Internet, `LabRole` có sẵn và bucket S3 riêng tư đã được kiểm tra. Xem [biên bản triển khai](tuan_1/docs/07-deployment-record.md) và [ảnh nền tảng](tuan_1/evidence/README.md).
- **Tuần 2:** Lambda kiểm kê, billing, read API và threshold alert; DynamoDB, API Gateway, S3, EventBridge, Cost Explorer và SNS đã được triển khai/kiểm thử. Ảnh ngày 15/10/2026 ghi nhận 10 tổ hợp dịch vụ/vùng có `status=ok`, `count=0`; GET /summary có SigV4 trả HTTP 200, không ký trả HTTP 403. Giao diện hiển thị JSON thật đã nạp thủ công. Chi phí `1E-10 USD` là ước tính, không phải hóa đơn cuối kỳ. Xem [kết quả và kiểm thử tuần 2](tuan_2/README.md).
- **Tuần 3:** 12/12 unit tests đạt; Lambda thử xác minh freshness và SNS `PendingConfirmation`; API `/summary` có SigV4 trả HTTP 200, request không ký bị từ chối; CloudWatch alarm đã chuyển qua `In alarm` và trở về `OK` trên lỗi thử có kiểm soát. Ngày 21/10, mã cảnh báo tuần 3 được đưa lên Lambda sản phẩm và gọi thử thành công với snapshot mới, dưới ngưỡng 10 USD. Xem [kết quả tuần 3](tuan_3/README.md) và [ảnh triển khai sản phẩm](tuan_3/evidence/10-product-alert-deployment.md).
- **Tuần 4, minh chứng AWS ngày 23/10:** 16/16 unit tests đạt; bản sửa read-api đã được xác minh trên Lambda sản phẩm và cùng mã chạy đạt với bảng DynamoDB rỗng thật. Đã thu snapshot inventory/billing mới, đối chiếu API với DynamoDB; SigV4 trả 200, không ký trả 403. Dashboard S3 vượt qua kiểm thử dữ liệu đủ, thiếu snapshot và JSON lỗi. Hai bucket tiếp tục chặn công khai/SSE-S3, sáu Lambda dùng LabRole, không Function URL. Trên topic SNS thử riêng, subscription chưa xác nhận làm guard dừng trước Publish; sau khi xác nhận, Lambda thử publish thành công và người nhận xác nhận nhận email. Cấu hình thử được phục hồi, bảng replay đã xóa. Xem [checklist và giới hạn](tuan_4/evidence/12-final-review-2026-10-23.md) và [biên bản SNS kèm ảnh](tuan_4/evidence/08-sns-replay-2026-10-23.md). [Phân công/thời lượng](tuan_4/docs/10-week4-assignment-and-time.md) ghi tổng 10 giờ sinh viên xác nhận, phần AI khai riêng. Trạng thái bàn giao hiện tại nằm ở mục cập nhật 27/10 bên dưới.

Worklog giữ giờ sinh viên chưa xác nhận ở dạng trống; không suy ra giờ học từ thời gian AI thao tác, thời lượng phiên Lab hay mốc CloudTrail.

**Cập nhật 27/10/2026:** Bản Word tổng kết đã hoàn tất. Xem [đối chiếu tuần 4](tuan_4/docs/12-completion-audit-2026-10-27.md) và [kịch bản demo có lời thoại](tuan_4/docs/11-demo-script.md). Kiểm thử mã cục bộ đạt 16/16; đã kiểm tra trực tiếp API, bảo mật và đối chiếu mã trên AWS. Snapshot hiện có vẫn thu ngày 23/10. Video chưa được ghi nhận hoàn thành; việc dọn tài nguyên còn giữ được thực hiện sau khi quay và kiểm tra phụ thuộc.

Không đưa access key, secret key, session token, URL presigned hoặc thông tin đăng nhập vào repository. Ảnh SNS công khai không hiển thị địa chỉ email người nhận.
