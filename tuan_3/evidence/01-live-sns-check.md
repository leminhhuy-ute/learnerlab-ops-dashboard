# Kiểm tra SNS trên Learner Lab — 19/10/2026

Kiểm tra đọc dữ liệu lúc `2026-10-19T12:37:29Z` qua AWS CloudShell, Region `us-east-1`. Đây là kết quả quan sát trên tài khoản thật, chưa phải phép thử cảnh báo vượt ngưỡng với subscription chờ xác nhận.

| Nội dung | Kết quả |
| --- | --- |
| `aws sts get-caller-identity` | Account `213858341631`; phiên `voclabs` của sinh viên `24110019` |
| `aws lambda get-function-configuration --function-name learnerlab-ops-week2-threshold-alert` | Lambda hiện hành dùng `arn:aws:iam::213858341631:role/LabRole`, runtime `python3.13`; mã ứng viên tuần 3 chưa được triển khai |
| `aws sns list-subscriptions-by-topic` trên topic `learnerlab-ops-week2-alerts` | Trả về 1 `SubscriptionArn` thật, không phải `PendingConfirmation`; không ghi địa chỉ email vào repo |
| `aws iam simulate-principal-policy` cho `LabRole`, hành động `sns:ListSubscriptionsByTopic`, topic trên | `allowed` |
| Truy vấn snapshot billing mới nhất trong `learnerlab-ops-week2-snapshots` | `SNAPSHOT#20261012T091255Z`, `status=ok`, `total=0.0000000001` USD. Snapshot này đã cũ; không coi là chi phí hiện tại ngày 19/10. |

Các lệnh trên chỉ đọc dữ liệu và kiểm tra quyền. Chúng không gửi SNS, không thêm subscription và không thay đổi Lambda. Phép thử thầy gợi ý cần một topic thử tách biệt có email subscription còn `PendingConfirmation`, sau đó gọi handler với ngưỡng kiểm thử và xác nhận `published=false` cùng việc không có `MessageId`. Không dùng topic đang có người nhận đã xác nhận để gửi cảnh báo chi phí giả.
