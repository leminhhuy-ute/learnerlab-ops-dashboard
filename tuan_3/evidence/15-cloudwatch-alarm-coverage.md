# Bổ sung giám sát CloudWatch cho Lambda sản phẩm và EventBridge

**Ngày kiểm tra:** 21/10/2026 (GMT+7)  
**Môi trường:** AWS Learner Lab, account `213858341631`, Region `us-east-1`

## Cấu hình đã triển khai

Đã tạo bốn metric alarm bằng AWS CLI trong CloudShell. Các alarm dùng chu kỳ 5 phút, một kỳ đánh giá, ngưỡng lớn hơn 0 và `TreatMissingData=notBreaching`. Không gắn SNS action nên phép kiểm tra không gửi thêm email.

| Alarm | Metric và tài nguyên theo dõi | Trạng thái lúc đối chiếu |
|---|---|---|
| `learnerlab-ops-week3-product-alert-errors` | `AWS/Lambda Errors`, function `learnerlab-ops-week2-threshold-alert` | `OK` |
| `learnerlab-ops-week3-alert-rule-failures` | `AWS/Events FailedInvocations`, rule `learnerlab-ops-week2-alert-daily` | `OK` |
| `learnerlab-ops-week3-billing-rule-failures` | `AWS/Events FailedInvocations`, rule `learnerlab-ops-week2-billing-daily` | `OK` — không nhận datapoint trong 1 kỳ; treated as `notBreaching` |
| `learnerlab-ops-week3-inventory-rule-failures` | `AWS/Events FailedInvocations`, rule `learnerlab-ops-week2-inventory-6h` | `OK` |
| `learnerlab-ops-week3-test-lambda-errors` | `AWS/Lambda Errors`, Lambda thử tuần 3 | `OK` |

Ba lịch EventBridge được xác minh đang `ENABLED`: `alert-daily` (`cron(10 2 * * ? *)`), `billing-daily` (`cron(0 2 * * ? *)`) và `inventory-6h` (`rate(6 hours)`). Sau kỳ đánh giá ban đầu, cả bốn alarm mới chuyển sang `OK`. Riêng alarm billing có lý do: không nhận datapoint trong một kỳ và một datapoint thiếu được xử lý là `NonBreaching`; vì vậy `OK` không chứng minh lịch billing đã chạy thành công. Các trạng thái `OK` chỉ là trạng thái alarm khi CloudWatch đánh giá, không thay thế bằng chứng kiểm thử toàn bộ target.

## Lệnh đối chiếu

```bash
aws cloudwatch describe-alarms --no-cli-pager \
  --query "MetricAlarms[?contains(AlarmName, 'learnerlab-ops-week3')].[AlarmName,StateValue]" \
  --output text

aws events list-rules --name-prefix learnerlab-ops-week2 \
  --query 'Rules[].{Name:Name,State:State,Schedule:ScheduleExpression}' --output table
```

Kết quả liệt kê alarm xác nhận tồn tại đủ năm alarm tuần 3 (bốn alarm mới và alarm Lambda thử trước đó). Không tạo lỗi giả trên Lambda sản phẩm, không sửa metric và không thay đổi lịch EventBridge để ép alarm chuyển trạng thái.

## Giới hạn kiểm thử

Alarm Lambda sản phẩm đã ở `OK` khi đối chiếu. Alarm billing hiện `OK` theo chính sách thiếu datapoint; cần kiểm tra lại sau chu kỳ lịch tiếp theo để xác minh metric. Chưa chủ động làm hỏng target thật để tạo `FailedInvocations`. Worklog không cộng thời gian CloudShell do LLM/AI thao tác vào giờ sinh viên.
