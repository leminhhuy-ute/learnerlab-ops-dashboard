# Kiểm tra SNS trên Learner Lab — 19/10/2026

Kiểm tra đọc dữ liệu lúc `2026-10-19T12:37:29Z` qua AWS CloudShell, Region `us-east-1`. Đây là kết quả quan sát trên tài khoản thật, chưa phải phép thử cảnh báo vượt ngưỡng với subscription chờ xác nhận.

| Nội dung | Kết quả |
| --- | --- |
| `aws sts get-caller-identity` | Account `213858341631`; phiên `voclabs` của sinh viên `24110019` |
| `aws lambda get-function-configuration --function-name learnerlab-ops-week2-threshold-alert` | Lambda tuần 2 dùng `arn:aws:iam::213858341631:role/LabRole`, runtime `python3.13`; không thay mã của hàm này |
| `aws sns list-subscriptions-by-topic` trên topic `learnerlab-ops-week2-alerts` | Trả về 1 `SubscriptionArn` thật, không phải `PendingConfirmation`; không ghi địa chỉ email vào repo |
| `aws iam simulate-principal-policy` cho `LabRole`, hành động `sns:ListSubscriptionsByTopic`, topic trên | `allowed` |
| Truy vấn snapshot billing mới nhất trong `learnerlab-ops-week2-snapshots` | `SNAPSHOT#20261013T020042Z`, `status=ok`, `total=0.0000000001` USD. Truy vấn dùng `--no-scan-index-forward` giống Lambda. Snapshot này đã cũ; không coi là chi phí hiện tại ngày 19/10. |

## Kiểm thử tích hợp bước đầu

Tạo topic riêng `learnerlab-ops-week3-negative-test` (tag `Project=learnerlab-ops`, `Owner=24110019`) và Lambda riêng `learnerlab-ops-week3-threshold-negative-test`, dùng `LabRole`; không thay đổi Lambda/topic tuần 2. Gói Lambda lấy từ commit `5231d1f` trên repo, SHA-256 của `lambda_function.py` đối chiếu giữa máy cục bộ và CloudShell là `b1c45aeef76ee19fd1fb4d884cf9b6a954c9d33f88c92d5d81da97d5e5703139`.

Lambda thử đọc bảng snapshot thật, nhưng dùng ngưỡng **chỉ để kiểm thử** `0.00000000005` USD. Snapshot ngày 13/10 có tổng `0.0000000001` USD nên lớn hơn ngưỡng thử. Ngưỡng sản phẩm tuần 2 là 10 USD và không được thay đổi. Topic thử chưa có subscription (`[]`).

Gọi Lambda thử với payload `{}` nhận `StatusCode=200`, `FunctionError=null`; nội dung trả về: `status=sns_no_confirmed_subscribers`, `published=false`, `confirmedSubscriptionCount=0`, `pendingSubscriptionCount=0`, `amountUsd=1E-10`, `thresholdUsd=5E-11`, `snapshotId=SNAPSHOT#20261013T020042Z`. Không có `messageId`; handler đã dừng trước bước SNS `Publish`. Đây là kết quả thật của **nhánh không có subscriber**, chưa phải nhánh `PendingConfirmation` thầy gợi ý.

Phép thử tiếp theo cần thêm một email subscription trên chính topic thử, để nguyên trạng thái `PendingConfirmation`, rồi gọi lại cùng Lambda và xác nhận `sns_subscription_pending_confirmation`, `published=false`. AWS sẽ gửi email xác nhận khi tạo subscription. Chưa thực hiện bước đó và chưa gửi cảnh báo chi phí giả tới topic đang có người nhận.
