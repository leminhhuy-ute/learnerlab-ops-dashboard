# Đối chiếu mức độ hoàn tất tuần 4 ngày 27 tháng 10 năm 2026

## Kết luận

Các nhóm công việc kỹ thuật tuần 4 đã có mã nguồn, kết quả AWS và minh chứng ngày 23/10/2026. Ngày 27/10 đã chạy lại **16/16 kiểm thử cục bộ, đều đạt**, đồng thời xác nhận mã nguồn khớp các hash trong biên bản triển khai. Báo cáo Word tổng kết đã được biên soạn và mục lục có liên kết hợp lệ.

Sau khi Lab Ready, đã kiểm tra trực tiếp AWS ngày 27/10: API trả 403 khi không ký và 200 khi ký SigV4; mã read API, cảnh báo và dashboard đang triển khai có hash khớp repo. Snapshot kiểm kê và chi phí vẫn từ ngày 23/10, nên không được trình bày là dữ liệu vừa thu ngày 27/10. Lần kiểm tra chỉ đọc, không gọi Cost Explorer hay gửi SNS.

Chưa coi toàn bộ việc bàn giao đã kết thúc: **video chưa được ghi nhận hoàn thành; tài nguyên lõi và một số tài nguyên thử đang giữ cần được rà soát/dọn sau buổi quay**.

## Bảng đối chiếu

| Hạng mục | Kết quả đã có | Đối chiếu ngày 27/10 | Phạm vi kết luận |
|---|---|---|---|
| Hồi quy cảnh báo và read API | 12 test guard, 4 test hồi quy; sửa lỗi Items rỗng | Chạy lại 12 + 4, đều đạt | Kiểm thử cục bộ; không giả là lần gọi AWS mới |
| Read API trên AWS | Bản sửa triển khai 23/10; bảng rỗng thật trả missing/null; dọn bảng/Lambda/log dùng một lần | Đã tải mã triển khai và đối chiếu SHA-256 khớp repo ngày 27/10 | Thử bảng rỗng là kết quả ngày 23/10, không chạy lại ngày 27/10 |
| Inventory/billing → DynamoDB → API | 23/10 có 10/10 hàng khớp; SigV4 200, không ký 403 | Ngày 27/10: 200 có ký, 403 không ký; 10 hàng inventory đều có status ok | Snapshot inventory/billing vẫn thuộc 23/10, không đối chiếu từng hàng DynamoDB lần này |
| Dashboard S3 | Dữ liệu đủ, thiếu và JSON sai được kiểm tra trên trang S3 thật | JavaScript qua `node --check`; hash HTML trên S3 khớp repo | Kiểm thử giao diện nêu trên thực hiện ngày 23/10; vẫn nạp JSON thủ công, chưa tự ký SigV4 |
| SNS chưa xác nhận | Vượt ngưỡng thử nhưng dừng trước Publish, published=false | Biên bản và ảnh tồn tại | Phép thử riêng ngày 23/10, không phải trạng thái subscription hôm nay |
| SNS đã xác nhận | alert_published, có MessageId; người nhận xác nhận email | Biên bản, ảnh và commit xác nhận còn đầy đủ | Không gửi email lại ngày 27/10 |
| Bảo mật | Hai bucket BPA/SSE-S3, API AWS_IAM, sáu Lambda LabRole, không Function URL | Kiểm tra trực tiếp ngày 27/10, kết quả như biên bản | Phản ánh cấu hình tại thời điểm kiểm tra, không phải bảo đảm vĩnh viễn |
| Giám sát | Bốn alarm sản phẩm, ba lịch ENABLED theo rà soát 23/10 | 27/10: bốn alarm OK, ba lịch ENABLED; alarm không có AlarmActions | OK/ENABLED không chứng minh lịch đã tự chạy; alarm không gắn hành động gửi email |
| Chi phí/tag | Đã rà soát hai Region và bổ sung Project/Owner cho bốn alarm | Hồ sơ nguồn/kỳ dữ liệu đầy đủ | Cost Explorer estimated, không phải hóa đơn chốt; không gọi thêm Cost Explorer trong lượt đối chiếu này |
| Dọn tài nguyên thử | Alarm thử, bảng/Lambda/log rỗng và bảng replay đã dọn có biên bản | Hồ sơ dọn còn đầy đủ | Tài nguyên lõi và topic/Lambda thử giữ lại chưa được dọn toàn bộ |
| GitHub | Mã nguồn và evidence theo tuần | Sáu URL repo/blob/commit thử bằng HEAD đều trả HTTP 200 không đăng nhập; local main khớp remote trước cập nhật tài liệu | Repo công khai, không cần tài khoản giảng viên để mở các URL đã kiểm tra |
| Worklog | Bốn buổi, tổng 10 giờ SV xác nhận, AI khai riêng | Đọc CSV và cộng lại đúng 10 giờ | Không có giờ sinh viên mới được thêm trong lần đối chiếu này |
| Báo cáo Word | Tệp `Bao_cao_tong_ket_du_an_4_tuan_24110019.docx` đã hoàn tất trong bộ nộp | Mở được; 28 liên kết mục lục đều có bookmark đích; không có Chương 6 hoặc nội dung video | Bản Word riêng; kịch bản video tách thành tài liệu khác |

## Kiểm thử cục bộ đã chạy lại

```text
python -m unittest discover -s tuan_3/tests -v
Ran 12 tests in 0.001s
OK

python -m unittest discover -s tuan_4/tests -v
Ran 4 tests in 0.005s
OK

node --check <JavaScript được trích nguyên từ dashboard/index.html>
exit code 0
```

Log đầy đủ: [kiểm thử cục bộ ngày 27/10](../evidence/14-local-tests-2026-10-27.txt). Các test dùng mô phỏng, không truy cập hoặc thay đổi AWS.

## Đối chiếu mã nguồn với biên bản triển khai

| Mã nguồn | SHA-256 khớp biên bản 23/10 |
|---|---|
| [Read API](../../tuan_2/src/lambdas/read-api/index.py) | `3f5aaa1853462a8702c58401135bbe5f01e423a20161f5a26c4e3eff70a47e71` |
| [Guard cảnh báo](../../tuan_3/src/threshold-alert/lambda_function.py) | `11e5e5867142fedc324460c699a6df75f7fefd34e25ff7cd34f13dad6000538e` |
| [Dashboard](../../tuan_2/src/dashboard/index.html) | `2a4a5e0be8a7af4bbc11823c0add564ca51cbb1deb0d515320ea19346bb9fd8e` |

Ngày 27/10, sau khi Lab Ready, đã tải mã read API và guard từ Lambda và đọc HTML từ S3 để tính lại hash; cả ba khớp các giá trị trên. Kết quả phản ánh thời điểm kiểm tra, không bảo đảm mã sẽ không đổi về sau.

## Kết quả kiểm tra trực tiếp ngày 27/10

Lúc 10:58–10:59 giờ Việt Nam, tại tài khoản `213858341631`, `us-east-1`:

- CloudFormation stack tuần 1 ở `CREATE_COMPLETE`, có 10 tài nguyên.
- API `/summary`: không ký 403, ký SigV4 200; 10 hàng kiểm kê có `status=ok`. Snapshot kiểm kê thu lúc 08:36:33 và snapshot chi phí lúc 09:00:41 ngày 23/10 (giờ Việt Nam). `status=ok` mô tả lần thu trước, không chứng minh dữ liệu còn mới. Chi phí là ước tính, kỳ từ 01/10 đến trước 24/10.
- Hai bucket bật đủ Block Public Access và mã hóa AES256; không có public ACL grant. Route `GET /summary` dùng AWS_IAM; 6 Lambda dùng LabRole và không có Function URL.
- Ba rule EventBridge đang ENABLED; bốn alarm đang OK và không gắn AlarmActions. Không suy ra lịch tự chạy thành công từ các trạng thái này.
- Topic sản phẩm và topic thử mỗi topic có một subscription đã xác nhận, không có subscription chờ xác nhận. Nhánh chưa xác nhận trong báo cáo là phép thử trước đó, không phải trạng thái hiện tại.
- Ngưỡng Lambda sản phẩm là 10 USD. Biến `MAX_SNAPSHOT_AGE_HOURS` không được đặt trong môi trường; mã đang triển khai dùng mặc định 48 giờ. Không kích hoạt lại Lambda cảnh báo trong lượt kiểm tra này.

Các truy vấn kiểm tra chỉ đọc; không gọi Cost Explorer, không gửi SNS và không sửa tài nguyên. Nhật ký đọc và kết quả được quan sát trên CloudShell; không dựng ảnh minh chứng.

## Chuẩn bị quay và bàn giao

Trước buổi quay cần mở phiên Lab hợp lệ, kiểm tra lại mã HTTP API, mốc snapshot và dashboard. Nếu snapshot đã cũ, freshness guard có thể từ chối đúng thiết kế; không sửa timestamp để làm dữ liệu có vẻ mới. Phép thử SNS ngày 23/10 đã phục hồi cấu hình và dọn bảng replay; không chạy lại máy móc cửa sổ 336 giờ của lần thử cũ.

Video đi theo [kịch bản có thao tác và lời thoại](11-demo-script.md). Sau khi quay, kiểm tra phụ thuộc và dọn tài nguyên không còn cần giữ. Báo cáo chỉ ghi dọn hoàn tất sau khi đã thực hiện và xác minh.

## Phần AI hỗ trợ lần đối chiếu này

LLM/AI ChatGPT trực tiếp đọc hồ sơ, chạy lại kiểm thử cục bộ, đối chiếu mã và thực hiện các truy vấn AWS chỉ đọc, kiểm tra cấu trúc Word và soạn kịch bản video. Sinh viên khởi động Lab. Không cộng thời gian AI vào 10 giờ SV đã xác nhận.
