# Đối chiếu CloudTrail cho worklog tuần 1

## Phạm vi kiểm tra

Ngày 10/10/2026, AWS CloudTrail Event history được mở trong phiên AWS Academy Learner Lab của tài khoản `213858341631`, Region `us-east-1`. Thời gian trong bảng là giờ Việt Nam (UTC+07:00). CloudTrail hiển thị định danh người dùng Learner Lab gắn với mã sinh viên 24110019.

CloudTrail lưu thời điểm các API được gọi. Nhật ký không đo thời gian đọc tài liệu, thiết kế sơ đồ, trao đổi nhóm hay thời gian làm việc tổng cộng. Nhật ký cũng không xác định người nào đã trực tiếp bấm phím trong phiên. Biên bản triển khai `07-deployment-record.md` ghi rõ LLM/AI (ChatGPT) trực tiếp thực thi lệnh triển khai và kiểm tra; vì vậy những mốc API dưới đây không được quy thành giờ làm riêng của sinh viên.

Trong lần xác minh trực tiếp ngày 10/10/2026 theo yêu cầu của sinh viên, Learner Lab hiển thị `Used $0 of $50`; console EC2 không có instance tại `us-east-1` và `us-west-2`. Sau khi kiểm tra CloudTrail và EC2, phiên Lab được kết thúc; giao diện chuyển sang `Terminated`. Đây là lần kiểm tra trạng thái sau triển khai, không phải thời lượng làm việc tuần 1 của sinh viên.

## Các sự kiện nhìn thấy trong Event history

| Ngày, giờ (UTC+07) | Sự kiện AWS | Tài nguyên liên quan |
|---|---|---|
| 08/10/2026 12:38:11 | `ConsoleLogin` | Phiên AWS Console của Learner Lab |
| 08/10/2026 12:47:24 | `CreateChangeSet` | Stack `learnerlab-ops-week1` |
| 08/10/2026 12:47:29 | `ExecuteChangeSet` | Stack `learnerlab-ops-week1` |
| 08/10/2026 12:47:32 | `CreateVpc`, `CreateInternetGateway` | VPC `vpc-0206a78d96a4b3a57`; IGW `igw-0998040b443aaa624` |
| 08/10/2026 12:47:34 | `CreateBucket`, `PutBucketEncryption`, `PutBucketPublicAccessBlock`, `PutBucketLifecycle` | Bucket `learnerlab-ops-week1-artifactbucket-u4t7cql7ngfo` |
| 08/10/2026 12:47:43 | `ModifyVpcAttribute` (2 sự kiện) | VPC `vpc-0206a78d96a4b3a57` |
| 08/10/2026 12:47:46 | `CreateSubnet` (2 sự kiện), `CreateRouteTable` | Hai subnet và route table của VPC tuần 1 |
| 08/10/2026 12:47:47 | `AttachInternetGateway` | IGW `igw-0998040b443aaa624` gắn vào VPC |
| 08/10/2026 12:47:50 | `AssociateRouteTable` (2 sự kiện) | Hai subnet và route table `rtb-0d686db1acc56489d` |
| 08/10/2026 12:47:58 | `CreateRoute` | Route table `rtb-0d686db1acc56489d` |

Biên bản CloudFormation đã lưu trước đó ghi stack chuyển sang `CREATE_COMPLETE` lúc 12:52:18 và có 10/10 tài nguyên ở trạng thái `CREATE_COMPLETE`. Mốc này đến từ lần gọi API kiểm tra stack, không phải một sự kiện tạo tài nguyên trong bảng CloudTrail.

## Giới hạn và cách dùng trong worklog

Event history hiển thị cảnh báo `AccessDeniedException` cho một phần thao tác console, dù các sự kiện nêu trong bảng vẫn xuất hiện. Bảng này chỉ ghi những sự kiện đã nhìn thấy, không khẳng định là bản xuất đầy đủ của mọi thao tác trong tài khoản.

Các sự kiện xác nhận môi trường AWS đã nhận các lệnh và thời điểm thực thi. Chúng không cho phép tính số giờ sinh viên tự học. Vì vậy, cột `gio_thuc_te` trong `worklog.csv` được để trống; thời lượng chỉ nên điền khi có nguồn ghi nhận riêng phù hợp với cá nhân.
