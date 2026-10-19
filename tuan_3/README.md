# Tuần 3 — Kiểm thử cảnh báo SNS

## Phần đã làm hôm nay

Theo gợi ý của giảng viên, phần đầu tiên tập trung vào nhánh tiêu cực của cảnh báo chi phí: snapshot vượt ngưỡng nhưng email subscription của SNS vẫn ở trạng thái `PendingConfirmation`.

Kế hoạch tổng thể tuần 3: [tuan_2/docs/09-week3-plan.md](../tuan_2/docs/09-week3-plan.md).

### Thay đổi trong mã

Handler ứng viên tại `src/threshold-alert/lambda_function.py` kiểm tra subscription của topic trước khi publish:

- Chỉ có subscription chờ xác nhận: trả `sns_subscription_pending_confirmation`, `published=false` và không gọi `Publish`.
- Không có subscriber đã xác nhận: trả `sns_no_confirmed_subscribers`, `published=false`.
- Có subscriber đã xác nhận: gửi cảnh báo; nếu topic đồng thời còn subscription chờ xác nhận, kết quả ghi `alert_published_with_pending_subscriptions` để không làm người đọc hiểu nhầm rằng mọi người nhận đều đã nhận thư.
- Chi phí dưới ngưỡng: trả `below_threshold` mà không cần truy vấn trạng thái SNS.

Handler dùng `ListSubscriptionsByTopic`; trước khi đưa lên AWS cần xác minh `LabRole` có quyền gọi API này. Bản handler tuần 2 đang triển khai không bị thay đổi trong phần chuẩn bị này.

### Kiểm thử cục bộ

Chạy bằng Python chuẩn, không cần credentials AWS:

```powershell
python -m unittest discover -s tuan_3/tests -v
```

Đã chạy 7 test và đều đạt. Các trường hợp gồm: chỉ có subscription chờ xác nhận; subscription đã xác nhận; trạng thái hỗn hợp; chi phí dưới ngưỡng; topic không có subscriber; subscription đã xác nhận nằm ở trang kết quả sau; và lỗi quyền khi đọc subscription. Hai trường hợp chỉ có subscription chờ xác nhận hoặc không đọc được subscription đều không gọi SNS `Publish`.

### Trạng thái kiểm thử AWS

Sau lỗi truy cập ở lần trước, Learner Lab đã vào trạng thái `Ready` ngày 19/10. Đã xác minh Account ID, SNS subscription hiện hành và quyền `sns:ListSubscriptionsByTopic` của `LabRole` qua CloudShell; [kết quả và mốc kiểm tra](evidence/01-live-sns-check.md). Chưa tạo topic/subscription thử, chưa publish email và chưa triển khai handler ứng viên. Kiểm thử cục bộ chứng minh logic của handler, không thay thế bằng chứng kiểm thử tích hợp cho nhánh `PendingConfirmation` trên AWS.

## Worklog

Worklog tuần 3 ghi riêng thời lượng sinh viên tự xác nhận và phần LLM/AI hỗ trợ: [worklog.csv](worklog.csv). Ngày 19/10 sinh viên xác nhận 2 giờ ở lần đầu và thêm 1 giờ thao tác Lab ở lần sau, tổng 3 giờ. Chưa có mốc bắt đầu/kết thúc hoặc log để đối chiếu độ dài phiên; thời lượng này không bao gồm thời gian AI chạy kiểm thử cục bộ hoặc các lệnh kiểm tra CloudShell.
