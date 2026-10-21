# Mã nguồn Lambda tuần 2

Các handler Lambda bên dưới được lấy nguyên trạng từ gói mã đang triển khai qua AWS Lambda Console ngày 15/10/2026. Giao diện được lấy từ đối tượng `index.html` đang lưu trong S3 cùng ngày. Các tệp không chứa giá trị biến môi trường, credentials hay URL tải tạm thời. Runtime Lambda là Python 3.13.

**Cập nhật 21/10/2026:** tệp threshold-alert trong thư mục tuần 2 là bản lịch sử tại ngày 15/10. Lambda cảnh báo sản phẩm hiện chạy [handler tuần 3](../../tuan_3/src/threshold-alert/lambda_function.py) với chốt kiểm tra tuổi snapshot và subscription SNS. [Biên bản triển khai và kiểm thử](../../tuan_3/evidence/10-product-alert-deployment.md) ghi rõ bản đang chạy; các Lambda khác trong bảng không bị cập nhật ở bước này.

| Hàm Lambda | Handler | Mục đích | Biến môi trường |
|---|---|---|---|
| `learnerlab-ops-week2-inventory-core` | `index.handler` | Gọi API EC2, RDS, SageMaker và EKS tại các Region cấu hình; lưu snapshot vào DynamoDB. | `REGIONS`, `TABLE` |
| `learnerlab-ops-week2-billing-collector` | `index.handler` | Gọi Cost Explorer theo nhóm dịch vụ; giới hạn tối đa bốn lần thử mỗi ngày UTC bằng bộ đếm trong DynamoDB. | `ACCOUNT`, `TABLE` |
| `learnerlab-ops-week2-read-api` | `index.handler` | Đọc snapshot mới nhất cho từng dịch vụ/Region và snapshot billing; trả dữ liệu tổng hợp cho API. | `TABLE`, `ACCOUNT`, `REGIONS` |
| `learnerlab-ops-week2-threshold-alert` | `lambda_function.lambda_handler` | Đọc snapshot billing mới nhất và gửi SNS khi tổng ước tính đạt ngưỡng. Sự kiện `{"test": true}` gửi thư thử, không phải cảnh báo chi phí. | `TABLE_NAME`, `TOPIC_ARN`, `ACCOUNT_ID`, `ALERT_THRESHOLD_USD` (tùy chọn), `AWS_REGION` (mặc định runtime) |

Mỗi thư mục con chứa đúng tệp handler trong gói Lambda. Các quyền AWS được cấp qua `LabRole`; không có access key trong mã. Cách chạy thử và kết quả đã quan sát nằm trong [hồ sơ tuần 2](../README.md) và [bảng nguồn dữ liệu](../../docs/data-sources.md).

## Giao diện dashboard

[`dashboard/index.html`](dashboard/index.html) là file tĩnh đang được lưu trong bucket S3 riêng tư. Người dùng dán JSON đã xác thực từ `GET /summary`; giao diện không gọi API trực tiếp và không chứa dữ liệu mẫu. Trang đọc snapshot kiểm kê và billing trong phản hồi rồi hiển thị thẻ tổng hợp, biểu đồ thanh và bảng kiểm kê.
