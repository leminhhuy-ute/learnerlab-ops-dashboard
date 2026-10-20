# Rà soát độ mới của billing snapshot — 20/10/2026

**Cập nhật sau bước chuẩn bị:** Mã freshness guard đã được triển khai lên Lambda thử ngày 20/10/2026 và kiểm thử thành công. [Minh chứng triển khai trên AWS](05-live-freshness-guard.md). Phần ghi chép về lỗi CloudShell bên dưới mô tả tình trạng trước khi chuyển sang tải ZIP qua Lambda Console.

## Phát hiện từ dữ liệu và mã nguồn

Trong phiên AWS ngày 20/10, truy vấn DynamoDB `learnerlab-ops-week2-snapshots` trả bản ghi billing mới nhất `SNAPSHOT#20261013T020042Z`, `status=ok`, `total=0.0000000001` USD, `estimated=true`, kỳ `2026-10-01` đến trước `2026-10-14`. Bản ghi đã cũ so với ngày rà soát; `status=ok` chỉ cho biết lần thu thập đó thành công, không chứng minh snapshot vẫn mới.

Đối chiếu mã `tuan_2/src/lambdas/billing-collector/index.py`: collector tạo `stamp` theo UTC rồi dùng dấu thời gian đó cho cả sort key `SNAPSHOT#{stamp}` và trường `collectedAt`. Mã collector đang lưu `collectedAt`; tuy nhiên lần truy vấn AWS trong phiên này chỉ chọn các trường `SK`, `total`, `status`, `periodStart`, `periodEndExclusive` và `estimated`, không truy vấn trực tiếp `collectedAt`.

## Thay đổi mã ứng viên tuần 3

Handler `tuan_3/src/threshold-alert/lambda_function.py` bổ sung freshness guard dựa trên `collectedAt`:

- Mặc định chấp nhận snapshot không quá 48 giờ; có thể cấu hình qua `MAX_SNAPSHOT_AGE_HOURS`.
- Snapshot cũ, thiếu timestamp, timestamp sai định dạng/không có múi giờ hoặc timestamp tương lai trả trạng thái riêng và `published=false`.
- Nhánh fail-closed kết thúc trước khi kiểm tra subscription hoặc gọi SNS.
- Phản hồi hợp lệ có thêm `collectedAt`, `snapshotAgeSeconds` và `maxSnapshotAgeHours` để người đọc đánh giá dữ liệu.

48 giờ là mặc định vận hành do dự án chọn cho collector có lịch hàng ngày, có thể điều chỉnh theo kết quả đo thực tế; đây không phải bảo đảm về độ trễ dữ liệu của Cost Explorer.

## Kiểm thử cục bộ

Lệnh chạy:

```powershell
python -m unittest discover -s tuan_3/tests -v
```

Kết quả: 10/10 kiểm thử đạt. Ba kiểm thử mới xác nhận snapshot cũ và thiếu `collectedAt` bị từ chối trước khi handler hỏi SNS hoặc publish, còn snapshot đúng ngưỡng 48 giờ được chấp nhận. Các test còn lại kiểm tra hành vi cảnh báo, trạng thái subscription và trường hợp dưới ngưỡng.

## Trạng thái AWS

Sau khi khởi động Learner Lab, CloudShell báo: `Unable to create the environment. This may be due to insufficient permissions to create environments, or because the environment no longer exists.` Chọn môi trường `us-east-1` hiện có vẫn gặp cùng lỗi. Không có lệnh cập nhật mã Lambda nào được chạy trong lần này; freshness guard ở trên chỉ là mã ứng viên đã kiểm thử cục bộ, chưa triển khai trên AWS. Lambda tuần 2 và cấu hình Lambda thử tuần 3 không bị thay đổi trong lần này.
