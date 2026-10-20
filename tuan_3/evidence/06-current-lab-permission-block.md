# Rà soát tiếp tuần 3 — quyền AWS hiện tại — 20/10/2026

Phạm vi: tiếp tục kiểm tra CloudWatch cho Lambda thử tuần 3 tại Account `213858341631`, Region `us-east-1`. Chỉ thực hiện truy vấn đọc; không thay đổi tài nguyên trong lần kiểm tra này.

## Kết quả đọc được từ Lambda Console

Trang Monitor của `learnerlab-ops-week3-threshold-negative-test` hiển thị trong cửa sổ `3h`:

| Chỉ số | Giá trị hiển thị |
|---|---:|
| Invocations | Sum 2 |
| Errors | Max 0 |
| Throttles | Max 0 |
| Duration | Average 7.396 ms; min 6.922 ms; max 7.871 ms |

Đây là metric của Lambda thử, không đại diện cho toàn bộ hệ thống và không thay thế kiểm thử metric alarm.

## Quyền truy cập qua CloudShell

`aws sts get-caller-identity` xác nhận account `213858341631`. Các lệnh đọc sau đó bị từ chối với thông báo **explicit deny** từ policy `voc-cancel-cred`:

| API thao tác đọc | Kết quả |
|---|---|
| `logs:DescribeLogGroups` | AccessDeniedException |
| `cloudwatch:DescribeAlarms` | AccessDenied |
| `lambda:GetFunctionConfiguration` cho Lambda thử tuần 3 | AccessDeniedException |
| `events:ListRules` | AccessDeniedException |

Mở trang CloudWatch log group từ Lambda Console không tải nội dung; khu vực nội dung chỉ là trang trắng. Lab interface vẫn hiển thị `Ready` và `Used $0 of $50`, nhưng điều đó không gỡ explicit deny trong quyền IAM.

## Trạng thái và bước cần làm

- Lần rà soát này không tạo hoặc sửa alarm, retention, Lambda, EventBridge hay tài nguyên khác.
- Trạng thái cũ trong [bản rà soát CloudWatch ngày 20/10](02-cloudwatch-review.md) chỉ phản ánh lần kiểm tra trước; không dùng nó để khẳng định trạng thái hiện tại đã thay đổi.
- Chưa thể hoàn tất mục CloudWatch của tuần 3. Cần AWS Academy/Learner Lab cấp lại quyền phù hợp hoặc xác nhận policy giới hạn này là chủ đích; sau đó mới kiểm tra lại log group, alarm, lịch và các thiết lập bảo mật.
- Không thử gỡ policy, tạo IAM user/role, hoặc tìm cách vượt qua giới hạn Learner Lab.

## Cập nhật sau đó trong cùng ngày

CloudShell vẫn bị explicit deny đối với các API nêu trên, nhưng CloudWatch Console sau đó tải được trang log group và trang alarm. Đã đặt retention `1 week` cho riêng log group Lambda thử và tạo alarm `learnerlab-ops-week3-test-lambda-errors`; alarm nhận datapoint `Errors=0` rồi chuyển `OK`. Chi tiết mới ở [retention và alarm](08-cloudwatch-retention-alarm.md). Cập nhật này không thay đổi kết quả deny trong CloudShell và không có nghĩa là policy đã được gỡ.

