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
- Snapshot lỗi thời, thiếu `collectedAt`, sai định dạng hoặc có mốc thời gian trong tương lai: trả trạng thái riêng với `published=false`; mặc định chỉ nhận snapshot tối đa 48 giờ, có thể chỉnh bằng `MAX_SNAPSHOT_AGE_HOURS`.

Handler dùng `ListSubscriptionsByTopic`. Quyền `sns:ListSubscriptionsByTopic` của `LabRole` đã được kiểm tra là `allowed`. Phiên bản trước của mã được triển khai riêng trên Lambda thử tuần 3; freshness guard mới ở phần dưới chưa triển khai. Lambda tuần 2 không bị thay thế.

### Kiểm thử cục bộ

Chạy bằng Python chuẩn, không cần credentials AWS:

```powershell
python -m unittest discover -s tuan_3/tests -v
```

Đã chạy 7 test và đều đạt. Các trường hợp gồm: chỉ có subscription chờ xác nhận; subscription đã xác nhận; trạng thái hỗn hợp; chi phí dưới ngưỡng; topic không có subscriber; subscription đã xác nhận nằm ở trang kết quả sau; và lỗi quyền khi đọc subscription. Hai trường hợp chỉ có subscription chờ xác nhận hoặc không đọc được subscription đều không gọi SNS `Publish`.

### Trạng thái kiểm thử AWS

Learner Lab đã vào trạng thái `Ready` ngày 19/10. Đã xác minh Account ID, SNS subscription hiện hành và quyền `sns:ListSubscriptionsByTopic` của `LabRole` qua CloudShell. Handler được triển khai vào **Lambda thử riêng**, cùng một SNS topic thử. Với snapshot thật ngày 13/10 vượt ngưỡng thử, Lambda trả `sns_no_confirmed_subscribers`, `published=false` khi topic trống. Sau đó tạo email subscription chưa xác nhận trên topic thử: SNS trả `PendingConfirmation`; gọi lại Lambda nhận `sns_subscription_pending_confirmation`, `published=false`, `confirmedSubscriptionCount=0`, `pendingSubscriptionCount=1`. [Lệnh, dữ liệu và kết quả đã đối chiếu](evidence/01-live-sns-check.md). SNS chỉ tạo yêu cầu xác nhận đăng ký; không có cảnh báo chi phí nào được publish. Lambda/topic tuần 2 và ngưỡng sản phẩm 10 USD không bị thay đổi.

### Rà soát giám sát CloudWatch — 20/10

CloudWatch ghi nhận 2 lượt chạy Lambda thử trong khoảng kiểm tra, 0 lỗi; duration trung bình lần lượt `7.355,20 ms` và `7.649,94 ms`, bộ nhớ tối đa `96/128 MB`. Ba lịch EventBridge tuần 2 đang `ENABLED`. Hiện chưa có metric alarm mang prefix dự án và log group chưa đặt thời hạn lưu. Kiểm tra nhanh tại `us-east-1` không thấy EC2 đang chạy, RDS, SageMaker endpoint/notebook, EKS cluster hoặc NAT Gateway `available`. Chi tiết lệnh và kết quả: [rà soát CloudWatch](evidence/02-cloudwatch-review.md). Đây mới là bước đọc và đánh giá; alarm và chính sách lưu log còn là việc tiếp theo.

### Kiểm thử nhánh chi phí dưới ngưỡng — 20/10

Trên Lambda thử riêng, tạm đặt ngưỡng kiểm thử `10` USD và gọi hàm với snapshot thật mới nhất hiện có trong DynamoDB: `SNAPSHOT#20261013T020042Z`, tổng `0.0000000001` USD, `status=ok`, `estimated=true`. Lời gọi trả `StatusCode=200`, không có `FunctionError`, kết quả `below_threshold`, `published=false`. Nhánh này kết thúc trước khi kiểm tra hoặc publish SNS. Sau phép thử, cấu hình Lambda thử được khôi phục về ngưỡng ban đầu `0.00000000005`; xác nhận `State=Active`, `LastUpdateStatus=Successful`. Lambda sản phẩm tuần 2 không thay đổi. Topic thử vẫn có một email subscription `PendingConfirmation` và không phát sinh cảnh báo.

Snapshot được lưu từ kỳ `2026-10-01` đến trước `2026-10-14`, nên đây là kiểm thử logic với bản ghi lịch sử mới nhất đang có, không phải số chi phí hiện tại ngày 20/10. [Lệnh, phản hồi Lambda và trạng thái sau khôi phục](evidence/03-below-threshold-test.md).

### Xử lý snapshot cũ — mã ứng viên, chưa triển khai AWS

Snapshot mới nhất đã quan sát có ID `SNAPSHOT#20261013T020042Z` trong khi ngày rà soát là 20/10. Mã collector tuần 2 tạo `SK` và `collectedAt` từ cùng dấu thời gian UTC; do vậy bộ xử lý cảnh báo cần từ chối dữ liệu quá hạn thay vì coi `status=ok` đồng nghĩa dữ liệu còn mới. Mã tuần 3 hiện có chốt kiểm tra tuổi snapshot 48 giờ, các trạng thái thiếu/sai/ở tương lai đều fail closed. Chính sách 48 giờ là mặc định của dự án, không phải cam kết thời gian cập nhật của AWS Cost Explorer.

12 kiểm thử cục bộ đều đạt, gồm các trường hợp snapshot quá cũ, thiếu/sai dấu thời gian, mốc thời gian tương lai và đúng ranh giới 48 giờ. Chưa thể cập nhật Lambda thử trên AWS: CloudShell báo không tạo được môi trường do quyền hoặc môi trường không còn tồn tại sau khi khởi động lại Lab; máy này cũng chưa có AWS CLI. Vì vậy freshness guard trong mã nguồn là **ứng viên đã kiểm thử cục bộ, chưa triển khai lên AWS**; Lambda tuần 2 không thay đổi. [Phân tích dữ liệu và kết quả kiểm thử](evidence/04-snapshot-freshness-guard.md).

## Worklog

Worklog tuần 3 ghi riêng thời lượng sinh viên tự xác nhận và phần LLM/AI hỗ trợ: [worklog.csv](worklog.csv). Ngày 19/10 sinh viên xác nhận 2 giờ ở lần đầu và thêm 1 giờ thao tác Lab ở lần sau, tổng 3 giờ. Ngày 20/10 sinh viên xác nhận thêm 1 giờ cho phiên làm việc hiện tại; chưa cung cấp phân bổ theo tác vụ hoặc mốc bắt đầu/kết thúc. Giờ này là tự khai, không có log AWS chứng minh thời lượng; các thao tác AI ghi riêng và không cộng vào giờ sinh viên.
