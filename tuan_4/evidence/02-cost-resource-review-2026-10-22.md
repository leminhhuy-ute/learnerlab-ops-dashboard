# Rà soát chi phí, tài nguyên và tag — 22/10/2026

**Môi trường:** AWS Learner Lab, account `213858341631`; chỉ kiểm tra `us-east-1` và `us-west-2`. Kết quả được đọc từ CloudShell trong phiên Lab ngày 22/10/2026, khoảng 07:47–07:49 ICT (00:47–00:49 UTC). Bản ghi này không lưu credentials, địa chỉ email hay số tiền.

## Chi phí và snapshot billing

Đọc item billing mới nhất trong DynamoDB `learnerlab-ops-week2-snapshots`: `SK=SNAPSHOT#20261021T020041Z`, `collectedAt=20261021T020041Z`, kỳ `2026-10-01` đến trước `2026-10-22`, `estimated=true`, currency `USD`, `requestCountToday=1`. Thời điểm thu thập là 09:00:41 ICT ngày 21/10; dữ liệu không bao gồm ngày 22/10. Trong phiên rà soát này không gọi Cost Explorer, do đó không có số chi phí mới cho ngày 22/10 và không kết luận đây là hóa đơn cuối kỳ.

## Kiểm tra tài nguyên có thể phát sinh chi phí

Các lệnh liệt kê được chạy trong cả hai Region được phép. Kết quả quan sát:

| Dịch vụ/tài nguyên | `us-east-1` | `us-west-2` |
|---|---:|---:|
| EC2 instance | 0 | 0 |
| EBS volume / dung lượng | 0 / 0 GiB | 0 / 0 GiB |
| NAT Gateway | 0 | 0 |
| Elastic IP / chưa liên kết | 0 / 0 | 0 / 0 |
| RDS instance/cluster | 0 | 0 |
| SageMaker endpoint/notebook | 0 / 0 | 0 / 0 |
| EKS cluster | 0 | 0 |
| ELBv2 load balancer | 0 | 0 |
| EFS file system | 0 | 0 |

Riêng `us-east-1`, Redshift provisioned cluster, Redshift Serverless workgroup và namespace đều trả danh sách rỗng. Đây là kết quả quan sát từ các lệnh đọc tài nguyên tại thời điểm kiểm tra. Không thấy các tài nguyên compute/dịch vụ liệt kê ở trên; điều đó không đồng nghĩa tổng phí bằng 0 vì Lambda, DynamoDB, S3, CloudWatch và các dịch vụ khác vẫn có thể phát sinh phí.

## Tags và bảo vệ S3

Resource Groups Tagging API, lọc `Project=learnerlab-ops`, trả 22 tài nguyên ở `us-east-1`; cả 22 có `Owner=24110019`. `us-west-2` không trả tài nguyên với tag Project này. Kết quả không bao gồm tài nguyên hoàn toàn chưa có tag, và khả năng trả kết quả phụ thuộc dịch vụ; vì vậy đây không phải bằng chứng mọi tài nguyên trong account đều đã gắn tag.

Bucket dashboard `learnerlab-ops-week2-dashboard-213858341631` được kiểm tra có đủ bốn tùy chọn S3 Block Public Access bật, mã hóa mặc định SSE-S3/AES256 và tags `Project`, `Environment`, `Owner`.

Kiểm tra danh sách tài nguyên có tag còn cho thấy bốn CloudWatch alarm dự án tuần 3 thiếu hai tag `Project`/`Owner`. Đã gọi CloudWatch `tag_resource` để gắn `Project=learnerlab-ops` và `Owner=24110019` cho đúng bốn alarm đó. CloudWatch trả HTTP 200 cho cả bốn lần cập nhật. Sau đó truy vấn lại tag của năm alarm tuần 3: cả năm đều có `Project` và `Owner`. Không đổi ngưỡng, trạng thái, metric hay cấu hình alarm.

## Phạm vi và giới hạn

- Truy vấn billing, danh sách dịch vụ, S3, tag và alarm là thao tác đọc; ngoại lệ duy nhất là gắn tag cho bốn alarm được nêu trên.
- Không tạo/xóa tài nguyên, không gọi Cost Explorer, không đưa giá trị tiền vào báo cáo.
- Snapshot billing là số liệu ước tính (`estimated=true`) được thu ngày 21/10 và kỳ dữ liệu kết thúc trước 22/10; không dùng làm số liệu chi phí của ngày 22/10.
- Không suy rộng kết quả từ các dịch vụ đã kiểm tra thành khẳng định rằng toàn bộ tài khoản không có chi phí hoặc không có tài nguyên nào khác.
- Thời gian sinh viên: **3 giờ do sinh viên tự xác nhận** cho buổi 22/10; không có mốc bắt đầu/kết thúc độc lập. Các thao tác CloudShell/AWS API và ghi biên bản do LLM/AI (ChatGPT) thực hiện, khai riêng trong worklog.
