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

Các test bao gồm: chỉ có subscription chờ xác nhận; subscription đã xác nhận; trạng thái hỗn hợp; chi phí dưới ngưỡng; và topic không có subscriber. Kết quả mong đợi ở nhánh thầy gợi ý là không gọi SNS `Publish` khi chỉ có subscription `PendingConfirmation`.

### Trạng thái kiểm thử AWS

Chưa chạy nhánh này trên Learner Lab. Khi mở CloudShell trong phiên này, AWS chuyển tới trang `Session error`; do đó chưa tạo topic/subscription thử, chưa publish email và chưa thay đổi tài nguyên AWS. Kiểm thử cục bộ chứng minh logic của handler ứng viên, không thay thế bằng chứng kiểm thử tích hợp trên AWS. Phần xác minh AWS được để cho buổi tiếp theo sau khi phiên Lab hoạt động.

## Worklog

Worklog tuần 3 ghi riêng phần AI hỗ trợ và giữ giờ sinh viên trống cho đến khi sinh viên xác nhận thời lượng thực tế: [worklog.csv](worklog.csv).
