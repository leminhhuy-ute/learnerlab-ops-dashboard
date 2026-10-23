# Phân công và thời lượng tuần 4

**Sinh viên:** Lê Minh Huy — MSSV 24110019

**Mã học phần:** CLCO332779

## Phân công

Nhóm có một sinh viên. Lê Minh Huy phụ trách theo dõi tiến độ, tìm hiểu và kiểm tra kết quả của từng buổi, xác nhận phạm vi cần hoàn thiện và thời lượng tham gia. Các thao tác AWS, sửa mã, chạy kiểm thử và chuẩn bị minh chứng do LLM/AI ChatGPT trực tiếp thực hiện được khai riêng trong [worklog](../worklog.csv).

## Thời lượng đã xác nhận

| Ngày, buổi | Nội dung buổi làm việc | Giờ sinh viên xác nhận |
|---|---|---:|
| 21/10/2026 — buổi 1 | Hồi quy mã cảnh báo và API đọc snapshot; đối chiếu API với DynamoDB; xác định lỗi khi kết quả truy vấn rỗng. | 2 |
| 22/10/2026 — buổi 2 | Rà soát nguồn/kỳ billing, tài nguyên có thể phát sinh phí và tag; bổ sung Project/Owner cho bốn alarm. | 3 |
| 22/10/2026 — buổi 3 | Rà soát S3, API IAM, Lambda, SNS; lưu cấu hình/lịch sử rồi dọn một alarm thử; kiểm tra lại sản phẩm. | 2 |
| 23/10/2026 — buổi 4 | Hoàn thiện bản sửa read-api trên AWS; kiểm thử bảng rỗng, luồng dữ liệu mới và giao diện; kiểm thử hai trạng thái subscription SNS trên topic riêng, khôi phục cấu hình thử và dọn bảng replay. | 3 |
| **Tổng tuần 4** | | **10** |

Hai buổi ngày 22/10 được xác nhận riêng (3 giờ và thêm 2 giờ). Ngày 23/10 sinh viên xác nhận thêm 3 giờ. Đây là thời lượng sinh viên cung cấp, không có bảng chấm công hay mốc bắt đầu/kết thúc độc lập. Không phân bổ lại số giờ cho từng lệnh AWS và không lấy thời gian AI thao tác làm giờ sinh viên. Ngày 23/10, AI hỗ trợ kiểm thử nhánh SNS chưa xác nhận (dừng trước Publish), sau đó sinh viên xác nhận subscription; AI gọi nhánh Publish trên topic thử riêng và khôi phục cấu hình/dọn bảng replay. Thời điểm lệnh AWS là minh chứng kỹ thuật, không dùng để suy ra số giờ sinh viên.

## Phần LLM/AI ChatGPT hỗ trợ

- Viết và chạy kiểm thử hồi quy; sửa lỗi đọc snapshot rỗng và cách hiển thị dữ liệu thiếu.
- Dùng CloudShell để triển khai, gọi Lambda/API, đối chiếu DynamoDB, kiểm tra bảo mật và lưu kết quả thực tế.
- Chuẩn bị phép thử SNS riêng, thu ảnh, sắp xếp minh chứng và cập nhật repository.

Video demo và báo cáo Word tổng kết toàn bộ dự án được thực hiện ở bước tiếp theo theo yêu cầu sinh viên. Không có báo cáo Word theo tuần được tạo trong buổi này.
