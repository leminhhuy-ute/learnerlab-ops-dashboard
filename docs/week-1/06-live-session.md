# Ghi nhận phiên Learner Lab thật

Nguồn: [Launch AWS Academy Learner Lab](https://awsacademy.instructure.com/courses/192433/modules/items/19043634), khóa học 192433 của người dùng.

Kiểm tra lúc **16:16 ngày 07/10/2026 (giờ Việt Nam)** bằng công cụ trình duyệt, không lấy từ dữ liệu mẫu.

| Nội dung quan sát | Kết quả |
|---|---|
| Trạng thái môi trường | AWS Status: Ready; Lab environment ready |
| AWSAccountId trong AWS Details | 213858341631 |
| Region trong AWS Details | us-east-1 |
| Ngân sách cổng Lab hiển thị lúc kiểm tra | Used $0 of $50; đây là thông tin portal tại thời điểm quan sát, không phải lời xác nhận chi phí tức thời |
| Phiên bắt đầu theo AWS Details | 07/10/2026 16:06:48 giờ Việt Nam (nguồn hiển thị 2026-10-07T02:06:48-0700) |
| Phiên dự kiến kết thúc theo AWS Details | 07/10/2026 20:06:48 giờ Việt Nam (thời gian này có thể đổi nếu gia hạn phiên) |
| LabRole / LabInstanceProfile | Chưa mở được IAM để kiểm tra |
| Stack learnerlab-ops-week1 / VPC / S3 | Chưa triển khai |

Minh chứng: [01-lab-session-ready.jpg](../../evidence/week-1/01-lab-session-ready.jpg).

## Phiên triển khai ngày 08/10/2026

Phiên Lab mới ở trạng thái Ready lúc khoảng 12:36 giờ Việt Nam, AWS Details tiếp tục hiển thị Account ID `213858341631`, Region `us-east-1`. Nút AWS vẫn không mở Console trong trình duyệt điều khiển. Terminal nhúng truy cập được nhưng mặc định dùng role `runserver` của tài khoản vận hành Vocareum; các lệnh AWS ban đầu bị `AccessDenied` vì **không phải** tài khoản Learner Lab. Sau khi người dùng đồng ý để Codex tự chọn cách thao tác, credentials AWS CLI tạm thời từ AWS Details được dùng trong terminal Lab. STS xác nhận đúng tài khoản `213858341631` trước khi triển khai.

CloudFormation `ValidateTemplate` thành công, stack `learnerlab-ops-week1` đạt `CREATE_COMPLETE` lúc 12:52 giờ Việt Nam. Xem [biên bản](07-deployment-record.md) và [ảnh minh chứng](../../evidence/week-1/README.md). Tệp credentials tạm và bản sao template ở `/tmp` đã xóa lúc khoảng 12:56 giờ Việt Nam; lịch sử lệnh shell được xóa. Không lưu credentials trong repository. Sau khi kiểm tra tài nguyên tốn phí, Codex bấm **End Lab**; trạng thái chuyển sang **Terminated** lúc khoảng 13:00 giờ Việt Nam. Stack và bucket được giữ cho tuần 2.

## Trở ngại của công cụ trong phiên 07/10 (đã khắc phục ngày 08/10)

Nút AWS trong khung Lab chưa tạo được tab AWS Console mà công cụ điều khiển nhận diện. Điều khiển terminal lồng trong iframe bị từ chối; mở terminal riêng hiển thị Connection Closed. Không có lệnh AWS triển khai nào được thực thi và không đọc/copy credentials.

Phiên đó không đổi cấu hình tài khoản hoặc reset môi trường. Sang ngày 08/10, terminal đã điều khiển được và triển khai qua CLI bằng credentials tạm thời của đúng tài khoản Lab.
