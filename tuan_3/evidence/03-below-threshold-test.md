# Kiểm thử AWS: chi phí dưới ngưỡng — 20/10/2026

Thao tác qua AWS CloudShell tại `us-east-1`, tài khoản Learner Lab `213858341631`. Thời điểm xác minh cấu hình cuối cùng và topic: `2026-10-20T06:21:41Z`. Lời gọi Lambda diễn ra ngay trước bước khôi phục ngưỡng.

## Dữ liệu đầu vào

Truy vấn bảng DynamoDB `learnerlab-ops-week2-snapshots` theo khóa `BILLING#213858341631`, sắp xếp giảm dần và lấy bản ghi mới nhất. Kết quả:

```json
{
  "SK": "SNAPSHOT#20261013T020042Z",
  "total": "0.0000000001",
  "status": "ok",
  "periodStart": "2026-10-01",
  "periodEndExclusive": "2026-10-14",
  "estimated": true
}
```

Đây là snapshot thật được lưu trong bảng, nhưng đã cũ so với ngày kiểm thử. Không coi con số này là chi phí hiện tại.

## Cách thử và kết quả

Lambda `learnerlab-ops-week3-threshold-negative-test` là hàm thử riêng, dùng `LabRole`, bảng snapshot thật và SNS topic thử `learnerlab-ops-week3-negative-test`. Trước khi gọi, chỉ ngưỡng của hàm thử được tạm đặt thành `10` USD; Lambda tuần 2 và cấu hình cảnh báo sản phẩm không bị sửa.

Lệnh gọi:

```bash
aws lambda invoke \
  --function-name learnerlab-ops-week3-threshold-negative-test \
  --payload "{}" \
  --cli-binary-format raw-in-base64-out \
  /tmp/week3-below-threshold.json
```

AWS CLI trả `StatusCode=200`, `FunctionError=null`. Payload phản hồi:

```json
{
  "status": "below_threshold",
  "published": false,
  "periodStart": "2026-10-01",
  "periodEndExclusive": "2026-10-14",
  "estimated": true,
  "amountUsd": "1E-10",
  "thresholdUsd": "10",
  "snapshotId": "SNAPSHOT#20261013T020042Z"
}
```

Kết quả khớp điều kiện: số tiền thấp hơn ngưỡng, hàm trả `below_threshold` và `published=false`. Theo luồng của handler, nhánh này trả về trước `_publish_or_skip`, do đó không truy vấn subscription và không gọi SNS `Publish`.

## Khôi phục và giới hạn

Sau khi thử, khôi phục `ALERT_THRESHOLD_USD` của Lambda thử về `0.00000000005`. Lệnh `get-function-configuration` xác nhận `State=Active`, `LastUpdateStatus=Successful`, và cả bốn biến môi trường đúng giá trị ban đầu. `list-subscriptions-by-topic` vẫn trả một mục `Protocol=email`, `SubscriptionArn=PendingConfirmation`; không có người nhận đã xác nhận và không gửi cảnh báo.

Phép thử xác minh nhánh dưới ngưỡng bằng snapshot lịch sử mới nhất đang có. Vì snapshot có kỳ kết thúc trước `2026-10-14`, kết quả không xác nhận mức chi phí hiện tại ngày `2026-10-20`.
