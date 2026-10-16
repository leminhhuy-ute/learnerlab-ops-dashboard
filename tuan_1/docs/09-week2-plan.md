# Kế hoạch tuần 2

**Đề tài:** Bảng điều khiển vận hành cho AWS Learner Lab.  
**Người phụ trách:** Lê Minh Huy — MSSV 24110019.

## Mục tiêu

Triển khai các chức năng lõi trên AWS Learner Lab và kiểm thử từng thành phần. Ưu tiên hoàn thành nơi lưu snapshot và Lambda kiểm kê trước, sau đó triển khai thu thập chi phí, API đọc dữ liệu, lịch chạy, giao diện và cảnh báo.

## Thứ tự triển khai và kiểm thử

| Thứ tự | Công việc | Kết quả cần kiểm tra |
|---|---|---|
| 1 | Tạo bảng snapshot DynamoDB và Lambda kiểm kê EC2, RDS, SageMaker, EKS ở `us-east-1` và `us-west-2`. | Gọi API thành công, lưu được snapshot theo dịch vụ/Region; phân biệt không có tài nguyên với lỗi hoặc thiếu quyền. |
| 2 | Triển khai Lambda chi phí dùng Cost Explorer và lưu kết quả vào DynamoDB. | Kiểm tra kỳ dữ liệu, tiền tệ, cờ `Estimated` và giới hạn lượt gọi; API đọc dùng snapshot đã lưu. |
| 3 | Tạo Lambda đọc dữ liệu và route `GET /summary` trên API Gateway, có xác thực. | Request được xác thực đọc được dữ liệu; request không có quyền bị từ chối. |
| 4 | Tạo hai lịch EventBridge riêng cho kiểm kê và chi phí. | Kiểm tra lịch, target, quyền gọi Lambda và lần thực thi; Cost Explorer chỉ được gọi vài lần/ngày theo đề bài. |
| 5 | Đưa giao diện lên S3, hiển thị dữ liệu JSON lấy từ API đã xác thực. | Kiểm tra số liệu, thời điểm snapshot và trạng thái lỗi; giữ cấu hình bảo vệ dữ liệu và thông tin đăng nhập. |
| 6 | Triển khai cảnh báo SNS và kiểm thử các thành phần. | Kiểm tra ngưỡng, xác nhận subscription, nhận email thử và lưu kết quả/ảnh minh chứng theo từng chức năng. |

## Phân công và nhật ký thực hiện

Lê Minh Huy phụ trách các công việc trên. Yêu cầu của học phần là tối thiểu 8 giờ thực tế mỗi sinh viên trong một tuần. Ghi ngày, nhiệm vụ, số giờ thực tế và phần có LLM/AI (ChatGPT) hỗ trợ vào [worklog tuần 2](../../tuan_2/worklog.csv).

Đây là kế hoạch chuyển tiếp từ [tuần 1](../README.md). Kết quả triển khai và kiểm thử được ghi riêng trong [báo cáo tuần 2](../../tuan_2/README.md).
