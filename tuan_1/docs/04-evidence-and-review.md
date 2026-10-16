# Minh chứng và tổng kết tuần 1

## Minh chứng đã thu

| Tệp | Nội dung đã đối chiếu |
|---|---|
| [01-lab-session-ready.jpg](../evidence/01-lab-session-ready.jpg) | Lab Ready; AWS Details cho Account ID `213858341631`, Region `us-east-1` ngày 07/10/2026 |
| [02-stack-complete.jpg](../evidence/02-stack-complete.jpg) | 08/10/2026: cùng Account/Region, stack `CREATE_COMPLETE`, output VPC/subnet/bucket, 10 tài nguyên |
| [03-network-check.jpg](../evidence/03-network-check.jpg) | VPC `10.20.0.0/16`, hai subnet khác AZ, auto public IPv4 tắt; route `0.0.0.0/0` tới IGW |
| [04-s3-private.jpg](../evidence/04-s3-private.jpg) | Bốn cờ chặn public đều bật; mã hóa `AES256`, BucketOwnerEnforced và tag Project/Owner/Environment |

Các ảnh CLI ghi Account ID, Region và thời gian do `date -Is` trong terminal Lab. Giờ trên ảnh là UTC−07:00; cộng 14 giờ để ra giờ Việt Nam. Không có credentials, bearer token hoặc URL ký trong ảnh.

## Kết quả thực tế

| Mục | Kết quả |
|---|---|
| Tài khoản / Region | `213858341631` / `us-east-1` |
| IAM | `arn:aws:iam::213858341631:role/LabRole` đã đọc bằng `GetRole`; không tạo role mới |
| Stack | `learnerlab-ops-week1`, `CREATE_COMPLETE`, 10/10 tài nguyên `CREATE_COMPLETE` |
| VPC | `vpc-0206a78d96a4b3a57`, `10.20.0.0/16` |
| Hai subnet | `subnet-0fe1f68d4d015130c` ở `us-east-1a`; `subnet-0a26fc106be139906` ở `us-east-1b` |
| Route | `rtb-0d686db1acc56489d` có `0.0.0.0/0` tới `igw-0998040b443aaa624`; gắn cả hai subnet |
| Bucket | `learnerlab-ops-week1-artifactbucket-u4t7cql7ngfo`; bucket riêng tư và mã hóa SSE-S3 |
| Tag | `Project=learnerlab-ops`, `Owner=24110019`, `Environment=learner-lab` trên tài nguyên hỗ trợ tag |
| Chi phí/tài nguyên chạy | Cổng Lab hiển thị `Used $0 of $50` lúc kiểm tra, có độ trễ; không thấy EC2 `running` hoặc NAT Gateway `available` ở hai Region được phép |
| Thời lượng của 24110019 | Sinh viên cung cấp tổng 8 giờ cho tuần 1; chưa có ghi chép phân bổ theo buổi/nhiệm vụ hoặc bằng chứng thời lượng độc lập. Cột giờ chi tiết trong worklog để trống. |
| Phần việc sinh viên xác nhận | Đọc tài liệu, tự sửa sơ đồ/template, chạy lệnh AWS, kiểm tra ảnh; chưa có bản ghi thời gian riêng cho các việc này |

Xem [biên bản triển khai và lệnh xác minh](07-deployment-record.md). Output `LabInstanceProfileName` trong template chỉ là tên tham khảo cho tuần sau, **chưa phải bằng chứng profile tồn tại**.

## Câu hỏi chuẩn bị vấn đáp

1. EventBridge và Lambda có vai trò gì? Vì sao không cần một EC2 chạy liên tục để kiểm kê?
2. Vì sao tách lịch kiểm kê tài nguyên khỏi lịch Cost Explorer? Request phân trang ảnh hưởng chi phí thế nào?
3. Cost Explorer có phải chi phí tức thời không? Khi thiếu quyền, dashboard nên hiển thị gì?
4. Vì sao DynamoDB lưu snapshot theo timestamp và service/region? Dữ liệu cũ/TTL xử lý thế nào?
5. VPC, subnet, route table và Internet Gateway khác nhau thế nào? Public route có tự cấp public IP không?
6. Vì sao collector hiện tại có thể hoạt động ngoài VPC của mình? Khi nào phải xem xét mạng VPC/NAT?
7. LabRole và LabInstanceProfile khác nhau thế nào? Vì sao template không tạo IAM role?
8. Vì sao bucket tuần 1 bật Block Public Access? URL presigned khác website endpoint thế nào?
9. CORS có thay thế xác thực API không? Token demo được bảo vệ và hết hạn thế nào?
10. Tag Project/Owner hỗ trợ việc kiểm kê và dọn tài nguyên ra sao? Xóa stack có xóa bucket Retain không?

## Ghi nhận AI hỗ trợ

Sinh viên xác nhận đã đọc tài liệu, sửa sơ đồ/template, chạy lệnh AWS và kiểm tra ảnh. LLM/AI (ChatGPT) hỗ trợ tham khảo tài liệu AWS, gợi ý kiến trúc, tạo bản nháp sơ đồ/template/script và biên soạn báo cáo. Trong phiên Learner Lab ngày 08/10/2026, công cụ còn trực tiếp triển khai stack, xác minh nền tảng và lưu ảnh CLI theo yêu cầu của sinh viên. Chưa có bản ghi riêng để đối chiếu các lệnh sinh viên tự chạy. Worklog để trống thời lượng cá nhân; không tính thời gian công cụ thao tác hoặc thời gian Lab chạy vào giờ sinh viên.

## Git

Các commit gốc và commit bổ sung tài liệu được liệt kê kèm ngày, nội dung và URL `/commit/<hash>` tại mục **Minh chứng commit** trong [báo cáo tuần 1](../README.md). Trong đó, commit `c54b76f` thêm `docs/data-sources.md`, commit `7d0290b` chuyển nội dung tuần 1 vào `tuan_1/`; commit `4bb8fd8` lưu nền tảng ban đầu ngày 08/10/2026.

Tài liệu, template và ảnh minh chứng được lưu ở [repository GitHub công khai](https://github.com/leminhhuy-ute/learnerlab-ops-dashboard). Trước khi công khai, các tệp văn bản trong repository và lịch sử commit đã được rà soát theo mẫu access key AWS, secret key, session token, GitHub token và private key; không phát hiện chuỗi khớp. Các ID tài khoản và tài nguyên trong ảnh/biên bản là dữ liệu nhận diện, không phải credentials.
