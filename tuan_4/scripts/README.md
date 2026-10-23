# Script triển khai và kiểm thử tuần 4

Các script được dùng trong AWS CloudShell với credentials tạm của phiên Learner Lab đang Ready. Account được kiểm tra là `213858341631`; không tạo IAM role mới. Chạy từ gốc repository. Mỗi script thay đổi AWS đều có mục đích kiểm thử cụ thể; xem biên bản trong [evidence](../evidence/) trước khi chạy lại.

| Script | Công việc |
|---|---|
| [deploy_read_api.py](deploy_read_api.py) | Sao lưu ZIP/cấu hình, cập nhật read-api bằng RevisionId, đối chiếu nguồn; tạo bảng/Lambda rỗng dùng một lần, kiểm thử và dọn; đối chiếu API với DynamoDB. |
| [refresh_final_snapshots.py](refresh_final_snapshots.py) | Gọi inventory và billing có giới hạn, thử guard sản phẩm rồi đối chiếu API. Dừng nếu đã có receipt billing để tránh gọi lặp Cost Explorer. |
| [deploy_dashboard.py](deploy_dashboard.py) | Sao lưu HTML, cập nhật S3, đối chiếu nội dung và giữ BPA/SSE-S3; lưu riêng URL tạm và JSON API để kiểm thử giao diện. |
| [test_alert_delivery.py](test_alert_delivery.py) | Chuẩn bị replay dữ liệu lịch sử trên tài nguyên riêng, thử subscription pending/confirmed và phục hồi cấu hình thử. |
| [review_security.py](review_security.py) | Chỉ đọc bảo mật bucket/API/Lambda, lịch, topic, alarm và log; không in email hoặc số tiền. |

Ví dụ các lệnh triển khai đã dùng (đường dẫn nguồn có thể được truyền rõ):

```bash
python3 tuan_4/scripts/deploy_read_api.py --source tuan_2/src/lambdas/read-api/index.py
python3 tuan_4/scripts/refresh_final_snapshots.py
python3 tuan_4/scripts/deploy_dashboard.py --source tuan_2/src/dashboard/index.html
python3 tuan_4/scripts/review_security.py
```

Kiểm thử SNS cần thực hiện từng bước; chỉ tiếp tục khi điều kiện thật đã đạt:

```bash
python3 tuan_4/scripts/test_alert_delivery.py prepare --source tuan_3/src/threshold-alert/lambda_function.py
python3 tuan_4/scripts/test_alert_delivery.py pending
# Người nhận tự bấm Confirm subscription sau khi đã lưu kết quả pending.
python3 tuan_4/scripts/test_alert_delivery.py positive
python3 tuan_4/scripts/test_alert_delivery.py restore
```

`prepare` nhập email bằng getpass, sao chép nguyên snapshot thật sang bảng replay và đặt cấu hình riêng cho Lambda thử. Snapshot 13/10 đã quá cửa sổ sản phẩm 48 giờ, nên replay dùng cửa sổ 336 giờ; không sửa timestamp để giả dữ liệu mới. `restore` đưa cấu hình thử về 10 USD/48 giờ và bảng snapshot gốc, rồi xóa đúng bảng replay có tag Purpose/Owner phù hợp. Không có bước tự xác nhận email.

Kết quả và bản sao lưu của phiên 23/10 được lưu ở `~/week4-final-20261023`. Script cố ý từ chối một số thao tác lặp nếu đã có bản sao lưu/receipt/kết quả. Khi gặp điều kiện này, đọc kết quả đã lưu và kiểm tra trạng thái AWS; không bỏ chặn bằng cách xóa bằng chứng để chạy lại. ZIP cũ, biến môi trường thử, JSON billing và URL S3 ký tạm là tài liệu riêng, không đưa lên GitHub.
