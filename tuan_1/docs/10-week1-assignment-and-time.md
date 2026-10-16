# Phân công và thời lượng tuần 1

**Sinh viên:** Lê Minh Huy — MSSV 24110019.  
**Đề tài:** Bảng điều khiển vận hành cho AWS Learner Lab.  
**Tổng thời lượng tuần 1 do sinh viên cung cấp:** 8 giờ.

Tài liệu tổng hợp phân công, các mốc công việc có nguồn đối chiếu và thời lượng sinh viên đã cung cấp. Thời gian trong các bảng dưới đây được ghi theo giờ Việt Nam (UTC+07:00).

## 1. Phân công nhiệm vụ

| Nhóm việc | Người phụ trách | Nội dung và phần việc sinh viên đã xác nhận | Sản phẩm đối chiếu |
|---|---|---|---|
| Tìm hiểu dịch vụ và yêu cầu | Lê Minh Huy | Đọc tài liệu; tìm hiểu vai trò các dịch vụ trong đề tài, giới hạn Learner Lab và nguồn dữ liệu dự kiến. | [Ghi chú dịch vụ](01-services-and-requirements.md), [nguồn dữ liệu](../../docs/data-sources.md). |
| Thiết kế kiến trúc, sơ đồ và template | Lê Minh Huy | Sinh viên xác nhận đã chỉnh sửa sơ đồ/template; rà soát luồng thu thập, lưu snapshot, đọc dữ liệu và cảnh báo. | [Thiết kế kiến trúc](02-architecture.md), [sơ đồ](../diagrams/architecture-week1-simple.png), [template](../infra/week1-foundation.yaml). |
| Dựng nền tảng AWS | Lê Minh Huy | Phụ trách nền tảng VPC/LabRole/S3; sinh viên xác nhận đã chạy lệnh AWS. Việc triển khai và các lệnh công cụ trực tiếp thực thi được ghi trong biên bản. | [Biên bản triển khai](07-deployment-record.md), [ảnh stack](../evidence/02-stack-complete.jpg). |
| Kiểm tra cấu hình, tag và minh chứng | Lê Minh Huy | Sinh viên xác nhận đã kiểm tra ảnh; nội dung đối chiếu gồm mạng VPC/subnet/route, cấu hình bảo vệ S3 và tag Project/Owner. | [Ảnh mạng](../evidence/03-network-check.jpg), [ảnh S3](../evidence/04-s3-private.jpg), [bảng tổng kết](04-evidence-and-review.md). |

## 2. Các mốc triển khai AWS ngày 08/10/2026

Các mốc API được tổng hợp từ [worklog tuần 1](worklog.csv) và bảng sự kiện trong [tài liệu đối chiếu CloudTrail](08-cloudtrail-audit.md). Riêng mốc stack hoàn tất lấy từ [biên bản triển khai](07-deployment-record.md).

| Ngày | Giờ (UTC+07) | Sự kiện | Nội dung ghi nhận |
|---|---|---|---|
| 08/10/2026 | 12:38:11 | `ConsoleLogin` | AWS ghi nhận đăng nhập Console bằng định danh Learner Lab gắn với mã sinh viên 24110019. |
| 08/10/2026 | 12:47:24 | `CreateChangeSet` | Tạo change set cho stack `learnerlab-ops-week1`. |
| 08/10/2026 | 12:47:29 | `ExecuteChangeSet` | Thực thi change set để triển khai nền tảng. |
| 08/10/2026 | 12:47:32 | `CreateVpc`, `CreateInternetGateway` | Tạo VPC và Internet Gateway của dự án. |
| 08/10/2026 | 12:47:34 | `CreateBucket` và các lệnh cấu hình S3 | Tạo bucket; ghi nhận cấu hình mã hóa, Block Public Access và lifecycle. |
| 08/10/2026 | 12:47:43 | `ModifyVpcAttribute` | Hai sự kiện cấu hình thuộc tính VPC. |
| 08/10/2026 | 12:47:46 | `CreateSubnet`, `CreateRouteTable` | Tạo hai subnet và route table. |
| 08/10/2026 | 12:47:47 | `AttachInternetGateway` | Gắn Internet Gateway vào VPC. |
| 08/10/2026 | 12:47:50 | `AssociateRouteTable` | Gắn hai subnet với route table. |
| 08/10/2026 | 12:47:58 | `CreateRoute` | Tạo tuyến Internet trong route table. |
| 08/10/2026 | 12:52:18 | Kiểm tra kết quả CloudFormation | Biên bản ghi stack đạt `CREATE_COMPLETE`, 10/10 tài nguyên hoàn tất. |

Biên bản còn ghi việc đọc lại `LabRole`, kiểm tra mạng, bảo mật S3, tag Project/Owner và kết thúc phiên Lab sau kiểm tra. Các việc này chưa có mốc giờ riêng trong worklog nên không được gán thêm giờ bắt đầu hoặc kết thúc.

## 3. Các mốc chuẩn bị, lưu tài liệu và rà soát

Bảng này bổ sung các mốc có trong tài liệu và lịch sử Git. Thời điểm commit cho biết lúc phiên bản được lưu vào Git.

| Ngày, giờ (UTC+07) | Nội dung | Nguồn đối chiếu |
|---|---|---|
| 07/10/2026 — chưa có giờ cụ thể | Tài liệu kế hoạch ghi ngày chuẩn bị; danh mục ảnh minh chứng ghi nhận phiên Lab Ready trong ngày. | [Kế hoạch tuần 1](00-plan.md), [danh mục minh chứng](04-evidence-and-review.md). |
| 08/10/2026 13:02:45 | Lưu phiên bản nền tảng đầu tiên gồm template, tài liệu thiết kế, biên bản triển khai và ảnh AWS. Khi đó các file nằm trong cấu trúc thư mục cũ. | [Commit 4bb8fd8](https://github.com/leminhhuy-ute/learnerlab-ops-dashboard/commit/4bb8fd84ba471d9fd4c3e727f632e8bcd4818dfc). |
| 10/10/2026 13:44:40 | Bổ sung mã tạo báo cáo tuần 1 và sơ đồ kiến trúc đơn sắc. | [Commit ee85b7f](https://github.com/leminhhuy-ute/learnerlab-ops-dashboard/commit/ee85b7f799c1ae878bedbe69af6981324410c6d7). |
| 10/10/2026 14:50:36 | Cập nhật sơ đồ kiến trúc tuần 1 và các file liên quan. | [Commit 51042ed](https://github.com/leminhhuy-ute/learnerlab-ops-dashboard/commit/51042edd9ac01cd2dc34d2ac2726f149846bfe32). |
| 10/10/2026 — chưa có giờ cụ thể | Đối chiếu CloudTrail, kiểm tra EC2 ở hai Region, kiểm tra trạng thái ngân sách hiển thị và kết thúc phiên Lab. | [Biên bản rà soát CloudTrail](08-cloudtrail-audit.md). |

## 4. Tổng hợp thời lượng

| Sinh viên | Tổng thời lượng tuần 1 được sinh viên cung cấp | Giờ chi tiết từng nhiệm vụ/buổi |
|---|---|---|
| Lê Minh Huy — 24110019 | 8 giờ | Chưa có ghi chép phân bổ; giữ trống trong worklog. |

Số 8 giờ lấy từ thông tin sinh viên đã cung cấp trong quá trình thực hiện dự án. Worklog hiện chưa có giờ bắt đầu, kết thúc hoặc số giờ riêng cho từng nhiệm vụ. Vì vậy, các mốc AWS và Git ở trên được dùng để đối chiếu công việc; không lấy khoảng cách giữa các mốc để tính hoặc chia tổng 8 giờ. Tổng thời lượng này chưa có bằng chứng thời lượng độc lập.

## 5. Phần có LLM/AI (ChatGPT) hỗ trợ

LLM/AI (ChatGPT) hỗ trợ tham khảo tài liệu, gợi ý kiến trúc, tạo bản nháp sơ đồ/template/script và biên soạn nội dung. Theo biên bản triển khai, công cụ còn trực tiếp thực thi một số lệnh tạo stack, kiểm tra cấu hình và lưu ảnh CLI. Sinh viên xác nhận đã đọc tài liệu, sửa sơ đồ/template, chạy lệnh AWS và kiểm tra ảnh; chưa có bản ghi riêng để đối chiếu từng lệnh sinh viên tự chạy. Chi tiết phần hỗ trợ được giữ trong cột `ai_ho_tro` của [worklog](worklog.csv).

[Trở về báo cáo tuần 1](../README.md) · [Kế hoạch tuần 2](09-week2-plan.md).
