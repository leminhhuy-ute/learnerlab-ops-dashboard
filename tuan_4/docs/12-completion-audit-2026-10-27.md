# Đối chiếu mức độ hoàn tất tuần 4 ngày 27 tháng 10 năm 2026

## Kết luận

Các nhóm công việc kỹ thuật tuần 4 đã có mã nguồn, kết quả AWS và minh chứng ngày 23/10/2026. Ngày 27/10 đã chạy lại **16/16 kiểm thử cục bộ, đều đạt**, đồng thời xác nhận mã nguồn khớp các hash trong biên bản triển khai. Báo cáo Word tổng kết đã được biên soạn và mục lục có liên kết hợp lệ.

Chưa coi toàn bộ việc bàn giao đã kết thúc: **video chưa được ghi nhận hoàn thành; tài nguyên lõi và một số tài nguyên thử đang giữ cần được rà soát/dọn sau buổi quay**. Không có lần kiểm tra AWS trực tiếp mới thành công ngày 27/10: AWS Console báo lỗi phiên; AWS Academy từ chối kết nối trong trình duyệt tích hợp. Vì vậy, trạng thái tài nguyên đang chạy hôm nay chưa được xác minh lại.

## Bảng đối chiếu

| Hạng mục | Kết quả đã có | Đối chiếu ngày 27/10 | Phạm vi kết luận |
|---|---|---|---|
| Hồi quy cảnh báo và read API | 12 test guard, 4 test hồi quy; sửa lỗi Items rỗng | Chạy lại 12 + 4, đều đạt | Kiểm thử cục bộ; không giả là lần gọi AWS mới |
| Read API trên AWS | Bản sửa triển khai 23/10; bảng rỗng thật trả missing/null; dọn bảng/Lambda/log dùng một lần | Hash nguồn trong repo khớp biên bản triển khai | Không tải lại ZIP AWS trong phiên 27/10 |
| Inventory/billing → DynamoDB → API | 23/10 có 10/10 hàng khớp; SigV4 200, không ký 403 | Mã/biên bản/ảnh còn đầy đủ | Mốc snapshot thuộc lần thu 23/10; cần kiểm tra lại trước quay |
| Dashboard S3 | Dữ liệu đủ, thiếu và JSON sai được kiểm tra trên trang S3 thật | JavaScript qua `node --check`; hash HTML khớp biên bản | Vẫn nạp JSON thủ công; chưa có đăng nhập trình duyệt/tự ký SigV4 |
| SNS chưa xác nhận | Vượt ngưỡng thử nhưng dừng trước Publish, published=false | Biên bản và ảnh tồn tại | Phép thử riêng ngày 23/10, không phải trạng thái subscription hôm nay |
| SNS đã xác nhận | alert_published, có MessageId; người nhận xác nhận email | Biên bản, ảnh và commit xác nhận còn đầy đủ | Không gửi email lại ngày 27/10 |
| Bảo mật | Hai bucket BPA/SSE-S3, API AWS_IAM, sáu Lambda LabRole, không Function URL | Đối chiếu biên bản và mã rà soát | Trạng thái AWS gần nhất xác minh ngày 23/10 |
| Giám sát | Bốn alarm sản phẩm, ba lịch ENABLED theo rà soát 23/10 | Biên bản còn đủ | OK/ENABLED không chứng minh lịch đã tự chạy; không có AlarmActions email |
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

Việc hash khớp biên bản không chứng minh tài nguyên AWS hôm nay không đổi. Muốn kết luận trạng thái đang chạy phải mở lại Learner Lab và kiểm tra trực tiếp.

## Chuẩn bị quay và bàn giao

Trước buổi quay cần mở phiên Lab hợp lệ, kiểm tra lại mã HTTP API, mốc snapshot và dashboard. Nếu snapshot đã cũ, freshness guard có thể từ chối đúng thiết kế; không sửa timestamp để làm dữ liệu có vẻ mới. Phép thử SNS ngày 23/10 đã phục hồi cấu hình và dọn bảng replay; không chạy lại máy móc cửa sổ 336 giờ của lần thử cũ.

Video đi theo [kịch bản có thao tác và lời thoại](11-demo-script.md). Sau khi quay, kiểm tra phụ thuộc và dọn tài nguyên không còn cần giữ. Báo cáo chỉ ghi dọn hoàn tất sau khi đã thực hiện và xác minh.

## Phần AI hỗ trợ lần đối chiếu này

LLM/AI ChatGPT trực tiếp đọc hồ sơ, chạy lại kiểm thử cục bộ, đối chiếu hash/URL, kiểm tra cấu trúc Word và soạn kịch bản video. Đây không phải bản ghi sinh viên đã trực tiếp thực hiện các thao tác trên AWS ngày 27/10; không cộng thời gian AI vào 10 giờ SV đã xác nhận.
