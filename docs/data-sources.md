# Nguồn dữ liệu

Nguồn là API quản lý AWS của tài khoản Learner Lab và AWS Cost Explorer. Phạm vi kiểm kê là `us-east-1` và `us-west-2`; collector chạy ở `us-east-1`. Không dùng dữ liệu giả hoặc API công khai bên ngoài.

| Dữ liệu | API AWS đã xác định | Trường cần lưu/hiển thị | Lưu ý |
|---|---|---|---|
| EC2 | `DescribeInstances`, `DescribeVolumes`, `DescribeInstanceTypes` | Region, ID, loại máy, trạng thái, vCPU; loại và dung lượng EBS | Chỉ những nhóm tài nguyên được collector hỗ trợ. Instance dừng không có nghĩa mọi chi phí liên quan đã dừng. |
| RDS | `DescribeDBInstances`, `DescribeDBClusters` | ID/tên, engine, lớp máy, trạng thái, storage, Region | Phân biệt instance với cluster để tránh đếm trùng. |
| SageMaker | `ListEndpoints`, `ListNotebookInstances` | Tên, trạng thái, nhóm tài nguyên và Region | Phạm vi tuần 2; không đại diện mọi loại SageMaker. |
| EKS | `ListClusters`, `DescribeCluster` | Tên cluster, trạng thái, phiên bản và Region | Kiểm kê control plane; không truy cập Kubernetes API. Worker EC2 thuộc nhóm EC2. |
| Chi phí | Cost Explorer `GetCostAndUsage` | Tổng theo ngày/dịch vụ, đơn vị tiền, khoảng ngày, `Estimated`, thời điểm thu thập | Dữ liệu có thể trễ/ước tính; số lần gọi được giới hạn vì API có tính phí. |

## Phân biệt thiết kế và dữ liệu đã chạy

- **Tuần 1:** đã xác định API nguồn và thiết kế luồng; phần triển khai tuần 1 chỉ gồm nền tảng VPC/S3. Chưa chạy collector kiểm kê hay truy vấn Cost Explorer.
- **Tuần 2:** Lambda đã kiểm tra EC2, RDS, SageMaker endpoint, SageMaker notebook và EKS tại hai vùng, tạo 10 tổ hợp dịch vụ/vùng. Ảnh kiểm thử ngày 15/10/2026 ghi `status=ok`, `count=0` cho cả 10 tổ hợp. Kết quả chỉ mô tả các loại tài nguyên được hỗ trợ tại thời điểm kiểm tra.
- **Chi phí:** snapshot Cost Explorer ghi kỳ bắt đầu `2026-10-01` đến trước `2026-10-14`, tổng `0.0000000001 USD`, `estimated=true`. Lần đối chiếu ngày 15/10 chỉ đọc snapshot DynamoDB, không gọi Cost Explorer thêm. DynamoDB là nơi lưu kết quả, không phải nguồn billing.

Mỗi snapshot lưu thời điểm thu thập và trạng thái riêng. `status=ok` với `count=0` là lần gọi thành công nhưng không thấy tài nguyên thuộc phạm vi đó. Lỗi API hoặc thiếu quyền phải giữ là lỗi/không khả dụng, không đổi thành số 0. Số Cost Explorer không phải số dư Learner Lab hay hóa đơn đã chốt.

Tài liệu liên quan: [thiết kế dịch vụ tuần 1](week-1/01-services-and-requirements.md) · [kết quả tuần 2](week-2/README.md).
