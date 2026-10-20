# Rà soát CloudWatch và tài nguyên đang chạy — 20/10/2026

Kiểm tra qua AWS CloudShell, Region `us-east-1`, lúc khoảng `2026-10-20T03:33Z` (10:33 giờ Việt Nam). Phần này chỉ đọc trạng thái và metric, không tạo alarm hay thay đổi lịch chạy.

## Metric và log của Lambda thử

Function `learnerlab-ops-week3-threshold-negative-test` đang `Active`, dùng `LabRole`, được cập nhật lúc `2026-10-19T12:41:39Z`. Kiểm tra CloudWatch cho khoảng `2026-10-19T12:00:00Z` đến `2026-10-21T00:00:00Z`:

| Thời điểm (UTC) | Invocations | Errors | Duration trung bình / lớn nhất | Billed duration | Max memory |
| --- | ---: | ---: | ---: | ---: | ---: |
| 19/10 12:40 | 1 | 0 | 7.355,20 ms | 7.447 ms | 96 MB / 128 MB |
| 19/10 13:00 | 1 | 0 | 7.649,94 ms | 7.736 ms | 96 MB / 128 MB |

CloudWatch Logs có hai lần chạy tương ứng, đều có `START`, `END`, `REPORT`; không thấy bản ghi lỗi. Hai lần chạy này là các phép thử tích hợp đã ghi ở [minh chứng SNS](01-live-sns-check.md), không phải lượt chạy định kỳ.

## Lịch và cảnh báo

Ba EventBridge rule tuần 2 hiện ở trạng thái `ENABLED`: `learnerlab-ops-week2-alert-daily` (`cron(10 2 * * ? *)`), `learnerlab-ops-week2-billing-daily` (`cron(0 2 * * ? *)`) và `learnerlab-ops-week2-inventory-6h` (`rate(6 hours)`). Lệnh `aws cloudwatch describe-alarms --alarm-name-prefix learnerlab-ops` trả `[]`; chưa có CloudWatch metric alarm mang prefix dự án.

Log group của Lambda thử và các Lambda tuần 2 chưa đặt `retentionInDays` (`null`). Vì vậy thời hạn lưu log chưa được giới hạn theo chính sách của dự án. Chưa đổi retention để giữ lại log hiện có; cần chọn thời hạn phù hợp và kiểm tra quyền LabRole trước khi cấu hình.

## Rà soát nhanh tài nguyên có thể phát sinh chi phí

Trong `us-east-1`, các lệnh mô tả tài nguyên trả về danh sách rỗng cho EC2 đang chạy, RDS, SageMaker endpoint, SageMaker notebook, EKS cluster và NAT Gateway đang `available`. Khi mở Learner Lab, giao diện hiển thị `Used $0 of $50`; con số ngân sách có thể trễ cập nhật theo hướng dẫn của Lab.

## Kết luận trong phạm vi bước rà soát

Đã quan sát được metric Invocation, Errors, Duration và log runtime cho Lambda thử; hai lần gọi có 0 lỗi. EventBridge đang bật, nhưng chưa có CloudWatch alarm và chưa giới hạn thời gian lưu log. Đây là rà soát giám sát, chưa phải triển khai alarm hoặc hoàn tất toàn bộ mục CloudWatch tuần 3.
