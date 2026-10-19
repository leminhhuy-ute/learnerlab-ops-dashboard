# Kiểm tra SNS trên Learner Lab — 19/10/2026

Kiểm tra ban đầu lúc `2026-10-19T12:37:29Z`, sau đó kiểm thử subscription chờ xác nhận trước `2026-10-19T13:03:22Z` qua AWS CloudShell, Region `us-east-1`. Các kết quả bên dưới được quan sát trên tài khoản Learner Lab thật.

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

## Kiểm thử subscription chờ xác nhận

Sau khi sinh viên đồng ý sử dụng email trường cho phép thử, tạo **một** email subscription trên topic thử; không ghi địa chỉ email vào repo. SNS gửi email yêu cầu xác nhận theo cơ chế đăng ký. Không bấm liên kết xác nhận trong quá trình kiểm thử. Kiểm tra bằng `aws sns list-subscriptions-by-topic --topic-arn arn:aws:sns:us-east-1:213858341631:learnerlab-ops-week3-negative-test --query "Subscriptions[].{Arn:SubscriptionArn,Protocol:Protocol}" --output json` cho kết quả:

```json
[{"Arn":"PendingConfirmation","Protocol":"email"}]
```

Gọi `aws lambda invoke --function-name learnerlab-ops-week3-threshold-negative-test --payload "{}" --cli-binary-format raw-in-base64-out /tmp/week3-pending.json`. AWS trả `StatusCode=200`, `FunctionError=null`. Payload trong `/tmp/week3-pending.json`:

```json
{"status":"sns_subscription_pending_confirmation","published":false,"confirmedSubscriptionCount":0,"pendingSubscriptionCount":1,"periodStart":"2026-10-01","periodEndExclusive":"2026-10-14","estimated":true,"amountUsd":"1E-10","thresholdUsd":"5E-11","snapshotId":"SNAPSHOT#20261013T020042Z"}
```

Như vậy snapshot thật ngày 13/10 (`1E-10` USD) vượt ngưỡng **thử** (`5E-11` USD), nhưng không có subscription đã xác nhận nên hàm trả `published=false` và không có `messageId`. Không có cảnh báo chi phí nào được publish trong phép thử này. Đây là phép thử với snapshot cũ, không chứng minh chi phí hiện tại đã vượt ngưỡng sản phẩm 10 USD. Topic/Lambda tuần 2 và ngưỡng 10 USD không bị thay đổi. Subscription thử được để ở trạng thái chưa xác nhận để lưu lại trường hợp kiểm thử; cần dọn tài nguyên thử khi kết thúc tuần 3.
