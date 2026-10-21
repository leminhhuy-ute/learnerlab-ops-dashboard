# CloudWatch retention và alarm cho Lambda thử tuần 3

**Ngày kiểm tra:** 20/10/2026  
**Region:** `us-east-1`  
**Account:** `213858341631`  
**Phạm vi tại ngày kiểm tra:** chỉ Lambda thử `learnerlab-ops-week3-threshold-negative-test`; Lambda sản phẩm được cập nhật mã riêng vào ngày 21/10, xem [biên bản triển khai](10-product-alert-deployment.md).

## Retention của log group

CloudWatch Console hiển thị log group:

```text
/aws/lambda/learnerlab-ops-week3-threshold-negative-test
Retention: 1 week
Stored bytes: 1,119 bytes
Log streams: 5
```

Retention 7 ngày giới hạn thời gian giữ log của hàm thử; cấu hình này không xóa log của log group tuần 2.

## Metric alarm

CloudWatch Console báo tạo thành công alarm `learnerlab-ops-week3-test-lambda-errors` lúc `2026-10-20 14:45:19 UTC` với cấu hình:

| Thuộc tính | Giá trị |
|---|---|
| Namespace / metric | `AWS/Lambda` / `Errors` |
| Dimension | `FunctionName=learnerlab-ops-week3-threshold-negative-test` |
| Statistic / period | `Sum` / 1 phút |
| Điều kiện | `Errors > 0` trong 1 datapoint trên 1 datapoint |
| Missing data | Treat as good (not breaching threshold) |
| Actions | Không có SNS, Lambda hoặc action khác |
| Tags | `Project=learnerlab-ops`, `Owner=24110019` |

Console xác nhận alarm hiện hữu và ARN:

```text
arn:aws:cloudwatch:us-east-1:213858341631:alarm:learnerlab-ops-week3-test-lambda-errors
```

## Kết quả kiểm thử

Ngay sau khi tạo, alarm ở `Insufficient data`. Lúc `2026-10-20 14:46:26 UTC`, CloudWatch hiển thị datapoint `Errors=0` và alarm chuyển sang `OK`.

Sau đó, một lần fault-injection có chủ đích trên **Lambda thử riêng** dùng payload sai kiểu `[1]`; invocation trả `FunctionError=Unhandled`. CloudWatch History xác nhận alarm chuyển `OK → In alarm` lúc `2026-10-20 15:52:26 UTC`. Đây là metric lỗi thật của hàm thử, không phải dữ liệu giả; không sửa snapshot, không gọi SNS `Publish` và không tác động Lambda tuần 2.

Để khôi phục kiểm tra bình thường, xác nhận topic thử chỉ có subscription `PendingConfirmation`, rồi gọi nhánh thử SNS an toàn. Lambda trả `StatusCode=200`, `FunctionError=null`, `sns_subscription_pending_confirmation`, `published=false`, `pendingSubscriptionCount=1`. CloudWatch chuyển alarm `In alarm → OK` lúc `2026-10-20 15:55:26 UTC`. Alarm không có action nên không gửi email. Chi tiết API và các lệnh gọi được ghi tại [evidence 09](09-api-and-alarm-live-tests.md).

Log retention và alarm chỉ áp dụng cho tài nguyên thử tuần 3.

![CloudWatch History ghi nhận alarm chuyển sang In alarm rồi trở lại OK](13-cloudwatch-alarm-history.png)
