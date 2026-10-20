# Tuần 3 — Tích hợp, bảo mật và giám sát

**Sinh viên:** Lê Minh Huy — MSSV 24110019

**Mã học phần:** CLCO332779

**Môi trường:** AWS Learner Lab, account `213858341631`, Region `us-east-1`

## Kết quả

Các hạng mục chức năng tuần 3 về freshness guard, xử lý SNS chưa xác nhận, xác thực API và giám sát CloudWatch đã được triển khai/kiểm thử trên AWS. Lambda thử tuần 3 và topic thử được tách riêng; Lambda sản phẩm tuần 2 không bị thay thế.

### Mã và kiểm thử cục bộ

Handler [`src/threshold-alert/lambda_function.py`](src/threshold-alert/lambda_function.py) từ chối snapshot không an toàn trước khi phát cảnh báo:

- Subscription SNS đang `PendingConfirmation`: `sns_subscription_pending_confirmation`, `published=false`; không gọi `Publish`.
- Không có subscriber đã xác nhận: `sns_no_confirmed_subscribers`, `published=false`.
- Snapshot cũ, thiếu/sai `collectedAt` hoặc có thời gian tương lai: trả trạng thái riêng, `published=false`.
- Snapshot hợp lệ dưới ngưỡng: `below_threshold`, `published=false`.

Chạy kiểm thử:

```powershell
python -m unittest discover -s tuan_3/tests -v
```

**12/12 unit tests đạt.** Bao gồm subscription chờ xác nhận/đã xác nhận/hỗn hợp, phân trang, lỗi quyền SNS, chi phí dưới ngưỡng và các trường hợp freshness. Mã đã được deploy lên Lambda thử riêng; chi tiết từng lần gọi nằm trong [evidence SNS](evidence/01-live-sns-check.md), [evidence freshness](evidence/05-live-freshness-guard.md) và [evidence API/CloudWatch](evidence/09-api-and-alarm-live-tests.md).

## Kết quả kiểm thử AWS

| Hạng mục | Kết quả đã quan sát |
|---|---|
| SNS chưa xác nhận | Topic thử có 1 email subscription `PendingConfirmation`; Lambda trả `sns_subscription_pending_confirmation`, `published=false`, không gửi email. |
| Freshness guard | Snapshot lịch sử `SNAPSHOT#20261013T020042Z` bị từ chối là cũ; Lambda trả `stale_billing_snapshot`, `published=false`. |
| API Gateway `GET /summary` | Request không ký nhận `Forbidden`; request SigV4 trả HTTP 200. Đã đối chiếu các trường inventory EC2 và billing được chọn với snapshot DynamoDB mới nhất; cả hai khớp (`True`). Chỉ lưu kết quả đối chiếu, không ghi giá trị chi phí/tài nguyên vào evidence. |
| CloudWatch | Log group Lambda thử giữ log 7 ngày. Alarm `Errors > 0` chuyển `OK → In alarm` sau một lỗi đầu vào có chủ đích trên hàm thử; lần kiểm tra SNS an toàn tiếp theo trả thành công và alarm chuyển lại `OK`. Alarm không có notification action. |
| Bảo mật S3/API | Bucket dashboard vẫn bật Block Public Access, SSE-S3 và tag; API vẫn dùng `IAM (built-in)`. Dashboard tĩnh tiếp tục nhận JSON thủ công theo quyết định giữ AWS_IAM, không nhúng credentials vào trình duyệt. |
| EventBridge | Ba lịch tuần 2 được ghi nhận `ENABLED` trong lần rà soát CloudWatch. |

Biên bản đầy đủ về trạng thái, lệnh và giới hạn của từng phép thử: [API SigV4 và alarm](evidence/09-api-and-alarm-live-tests.md), [retention/alarm](evidence/08-cloudwatch-retention-alarm.md), [rà soát quyền](evidence/06-current-lab-permission-block.md), [bảo mật](evidence/07-security-review.md).

## Phạm vi và giới hạn

- Tuần 3 đã hoàn tất các chức năng bắt buộc về tích hợp, bảo mật ứng dụng và giám sát trong phạm vi Learner Lab. IaC bổ sung là tùy chọn theo yêu cầu đề tài; không tạo stack giám sát trùng với tài nguyên đã cấu hình trực tiếp.
- `GET /summary` đã kiểm thử bằng SigV4 từ CloudShell; không tự nối dashboard S3 vì dashboard tĩnh không có cơ chế ký request an toàn và người học đã chọn giữ AWS_IAM.
- Không thể đọc đầy đủ policy của `LabRole`: CloudShell bị explicit deny bởi `voc-cancel-cred` đối với một số API chỉ đọc (`logs:DescribeLogGroups`, `cloudwatch:DescribeAlarms`, `lambda:GetFunctionConfiguration`, `events:ListRules`). Không tìm cách vòng qua policy. Các quyền cần cho nhánh Lambda thử được kiểm tra qua kết quả chạy thực tế.
- Billing snapshot được dùng cho kiểm thử là dữ liệu lịch sử/ước tính; không dùng nó để kết luận chi phí hiện tại.

## Worklog và AI

Worklog phân biệt thời lượng do sinh viên xác nhận với thao tác của **LLM/AI (ChatGPT)**. Lượt rà soát, gọi API và thử alarm trong phiên này do AI thực hiện, vì vậy không cộng giờ đó vào giờ sinh viên. Xem [worklog.csv](worklog.csv).

Kế hoạch và tiêu chí tuần 3: [09-week3-plan.md](../tuan_2/docs/09-week3-plan.md).

Kế hoạch tiếp theo (chưa thực hiện): [dự kiến tuần 4](../tuan_4/README.md).
