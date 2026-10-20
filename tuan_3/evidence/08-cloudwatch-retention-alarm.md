# CloudWatch retention và alarm cho Lambda thử tuần 3

**Ngày kiểm tra:** 20/10/2026  
**Region:** `us-east-1`  
**Account:** `213858341631`  
**Phạm vi:** chỉ Lambda thử `learnerlab-ops-week3-threshold-negative-test`; không thay đổi Lambda tuần 2.

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

## Kết quả và giới hạn kiểm thử

Ngay sau khi tạo, alarm ở `Insufficient data`. Lúc `2026-10-20 14:46:26 UTC`, CloudWatch hiển thị datapoint `Errors=0` và alarm chuyển sang `OK`. Đây là kết quả thật của nhánh dưới ngưỡng. Chưa có datapoint `Errors > 0`, nên trạng thái `ALARM` chưa được kiểm chứng. Không chủ động làm hỏng hàm để tạo lỗi và không gửi thông báo.

Alarm không có action nên không gửi email khi đổi trạng thái. Log retention và alarm đều chỉ áp dụng cho tài nguyên thử tuần 3.
