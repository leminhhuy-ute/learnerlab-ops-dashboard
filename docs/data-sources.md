# Nguồn dữ liệu

Nguồn là API quản lý AWS của tài khoản Learner Lab và AWS Cost Explorer. Phạm vi kiểm kê là `us-east-1` và `us-west-2`; collector chạy ở `us-east-1`. Không dùng dữ liệu giả hoặc API công khai bên ngoài.

| Dữ liệu | API AWS đã xác định | Trường cần lưu/hiển thị | Lưu ý |
|---|---|---|---|
| EC2 | `DescribeInstances` | ID instance, trạng thái, loại máy, tags và Region | Mã hiện tại không gọi `DescribeVolumes`/`DescribeInstanceTypes`, do đó không báo dung lượng EBS hoặc vCPU. Instance dừng không có nghĩa mọi chi phí liên quan đã dừng. |
| RDS | `DescribeDBInstances` | ID, trạng thái, engine, lớp máy, Multi-AZ và Region | Mã hiện tại chưa gọi `DescribeDBClusters`; không báo storage hoặc cluster. |
| SageMaker endpoint | `ListEndpoints` | Tên, trạng thái, thời điểm tạo và Region | Chỉ endpoint trong phạm vi; không đại diện mọi loại SageMaker. |
| SageMaker notebook | `ListNotebookInstances` | Tên, trạng thái, loại máy và Region | Chỉ notebook instance trong phạm vi. |
| EKS | `ListClusters` | Tên cluster và Region | Mã hiện tại chỉ liệt kê tên; chưa gọi `DescribeCluster` hay Kubernetes API. Worker EC2 được kiểm kê riêng qua EC2. |
| Chi phí | Cost Explorer `GetCostAndUsage` | Tổng tháng hiện tại theo dịch vụ, `UnblendedCost`, tiền tệ, khoảng ngày, `Estimated`, thời điểm thu thập | Kết thúc khoảng ngày là exclusive; mã giới hạn bốn lần thử mỗi ngày UTC. Dữ liệu có thể trễ/ước tính. |

## Phân biệt thiết kế và dữ liệu đã chạy

- **Tuần 1:** đã xác định API nguồn và thiết kế luồng; phần triển khai tuần 1 chỉ gồm nền tảng VPC/S3. Chưa chạy collector kiểm kê hay truy vấn Cost Explorer.
- **Tuần 2:** Mã handler đã triển khai nằm trong [`tuan_2/src/lambdas`](../tuan_2/src/lambdas/). Lambda kiểm tra EC2, RDS, SageMaker endpoint, SageMaker notebook và EKS tại hai vùng, tạo 10 tổ hợp dịch vụ/vùng. Ảnh kiểm thử ngày 15/10/2026 ghi `status=ok`, `count=0` cho cả 10 tổ hợp. Kết quả chỉ mô tả các loại tài nguyên được hỗ trợ tại thời điểm kiểm tra.
- **Chi phí:** collector gọi Cost Explorer theo tháng hiện tại, nhóm theo dịch vụ, và ghi giới hạn lượt gọi bằng bộ đếm có điều kiện trong DynamoDB. Snapshot đã kiểm tra ghi kỳ bắt đầu `2026-10-01` đến trước `2026-10-14`, tổng `0.0000000001 USD`, `estimated=true`. Lần đối chiếu ngày 15/10 chỉ đọc snapshot DynamoDB, không gọi Cost Explorer thêm. DynamoDB là nơi lưu kết quả, không phải nguồn billing.

Giao diện tĩnh trong [`tuan_2/src/dashboard/index.html`](../tuan_2/src/dashboard/index.html) không tự gọi API. Người dùng dán phản hồi JSON đã xác thực từ `GET /summary`; trang không tạo dữ liệu mẫu. Vì vậy, nguồn dữ liệu hiển thị vẫn là API AWS qua Lambda và snapshot DynamoDB chỉ là lớp lưu kết quả.

Mỗi snapshot lưu thời điểm thu thập và trạng thái riêng. `status=ok` với `count=0` là lần gọi thành công nhưng không thấy tài nguyên thuộc phạm vi đó. Lỗi API hoặc thiếu quyền phải giữ là lỗi/không khả dụng, không đổi thành số 0. Số Cost Explorer không phải số dư Learner Lab hay hóa đơn đã chốt.

Tài liệu liên quan: [thiết kế dịch vụ tuần 1](../tuan_1/docs/01-services-and-requirements.md) · [kết quả tuần 2](../tuan_2/README.md).

## Đối chiếu cuối tuần 4 — 23/10/2026

Nguồn dữ liệu không thay đổi. Đã gọi lại collector inventory: snapshot `20261023T005031Z` có 10 tổ hợp dịch vụ/Region, cả 10 `status=ok`, `count=0`. Collector billing được gọi thêm đúng một lần trong buổi, tạo snapshot `20261023T005041Z`, kỳ `2026-10-01` đến trước `2026-10-24`, `estimated=true`, bộ đếm ngày UTC là 1/4. API có SigV4 trả dữ liệu khớp snapshot DynamoDB; không ký trả 403. Xem [biên bản và kết quả lệnh](../tuan_4/evidence/06-read-api-deployment-2026-10-23.md).

Phép thử SNS tuần 4 dùng riêng **snapshot lịch sử thật ngày 13/10**, sao chép nguyên item sang bảng replay. Chỉ Lambda thử được đặt cửa sổ độ mới 336 giờ và ngưỡng bằng một nửa số tiền dương của snapshot; sản phẩm giữ 48 giờ/10 USD. Khi subscription còn PendingConfirmation, guard trả về mà không Publish; sau xác nhận, Lambda thử dùng nhánh bình thường và SNS chấp nhận Publish với MessageId. Cấu hình thử được phục hồi và bảng replay được xóa. Kết quả replay không chứng minh chi phí hiện tại đã vượt ngưỡng hoặc tự xác nhận email đã vào hộp thư. Trạng thái từng nhánh nằm trong [biên bản SNS kèm ảnh](../tuan_4/evidence/08-sns-replay-2026-10-23.md).

Read-api đã được sửa để xử lý truy vấn rỗng. Giao diện hiển thị dữ liệu thiếu bằng “—”/“Chưa đủ dữ liệu”, không đổi `missing/null` thành số 0; JSON lỗi sẽ xóa kết quả cũ. Cả ba trường hợp dữ liệu đủ, thiếu và JSON lỗi đã được [kiểm thử trên trang S3 thật](../tuan_4/evidence/10-dashboard-regression-2026-10-23.md). Cách nạp JSON thủ công và xác thực API AWS_IAM vẫn được giữ.
