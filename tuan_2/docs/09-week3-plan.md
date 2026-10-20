# Kế hoạch tuần 3

**Sinh viên phụ trách:** Lê Minh Huy — MSSV 24110019.

**Mã học phần:** CLCO332779.

**Đề tài:** Bảng điều khiển vận hành cho AWS Learner Lab.

## Mục tiêu

Tích hợp các thành phần tuần 2 thành luồng vận hành có thể kiểm tra, rà soát bảo mật, bổ sung giám sát CloudWatch và tự động hóa/IaC nếu quyền Learner Lab cho phép. Tuần 3 là kế hoạch; chưa được tính là công việc đã triển khai.

## Thứ tự công việc

| Thứ tự | Công việc | Cách kiểm tra | Đầu ra |
|---|---|---|---|
| 1 | Rà soát luồng inventory/billing → DynamoDB → Lambda đọc → API Gateway; xác nhận tên bảng, khóa, khoảng thời gian và cách nhận biết snapshot lỗi hoặc cũ. | Gọi API có SigV4, so sánh phản hồi với bản ghi DynamoDB tương ứng; kiểm tra trường thời gian, trạng thái và nguồn dữ liệu. | Sơ đồ luồng cập nhật, checklist đầu vào/đầu ra và kết quả đối chiếu. |
| 2 | Đánh giá cách kết nối dashboard S3 với GET /summary đang bảo vệ bằng AWS_IAM. | Xác định phương án xác thực phù hợp Learner Lab; kiểm tra luồng trong trình duyệt mà không đưa credentials tạm thời vào HTML, JavaScript, Git hoặc ảnh. | Quyết định kiến trúc và kiểm thử. Nếu chưa có cách an toàn, giữ xác thực AWS_IAM và ghi rõ thao tác nạp JSON thủ công hiện tại. |
| 3 | Thiết lập giám sát CloudWatch cho các Lambda và lịch EventBridge. | Kiểm tra log, Errors, Throttles, Duration, Invocations và trạng thái target; tạo thử cảnh báo trong điều kiện kiểm soát nếu quyền Lab cho phép. Không gửi cảnh báo vượt ngưỡng giả như thể là dữ liệu thật. | Log group và cấu hình metric/alarm phù hợp, ảnh kết quả kiểm tra. |
| 4 | Rà soát bảo mật và quyền truy cập. | Xác nhận S3 vẫn riêng tư, Block Public Access và SSE-S3 còn bật; API vẫn yêu cầu SigV4; rà soát quyền hiện có của LabRole, không tạo IAM user/role mới. | Bảng kiểm soát bảo mật và các điểm cần điều chỉnh nếu phát hiện. |
| 5 | Chuẩn bị tự động hóa/IaC cho các tài nguyên phù hợp với quyền Learner Lab. | Đối chiếu template với tài nguyên đang chạy, tag Project/Owner, Region và cấu hình; thử kiểm tra template trước khi cập nhật stack. Không ghi nhận triển khai nếu lệnh bị thiếu quyền hoặc chưa chạy thành công. | Template/runbook có thể kiểm tra lại và biên bản kết quả triển khai hoặc giới hạn quyền. |
| 6 | Chạy kiểm thử hồi quy, lưu minh chứng và rà soát chi phí. | Lặp lại các kiểm tra inventory, snapshot, billing theo hạn mức Cost Explorer, API có/không có chữ ký, SNS subscription và lịch chạy; xác minh không còn dữ liệu thử hoặc tài nguyên tạm không cần thiết. | Bảng test case–kết quả, ảnh Console/CLI có Region và thời gian, worklog và danh sách dọn dẹp. |

## Phân công và cách ghi worklog

Sinh viên phụ trách đọc yêu cầu, xác định thứ tự triển khai, kiểm tra kết quả trên Learner Lab, giải thích cấu hình và lưu minh chứng. Nếu LLM/AI (ChatGPT) hỗ trợ viết mã, template, phân tích log hoặc chạy lệnh, worklog cần ghi riêng chính xác phần đó; không cộng thời gian AI vào thời lượng sinh viên.

Ghi số giờ thực tế theo từng ngày sau khi sinh viên xác nhận. Không tự chia tổng giờ thành các buổi hoặc gán giờ cho một tác vụ nếu không có ghi chép. Tài liệu đối chiếu tuần 2 hiện tại: [worklog](https://github.com/leminhhuy-ute/learnerlab-ops-dashboard/blob/main/tuan_2/worklog.csv) và [phân công, thời lượng tuần 2](https://github.com/leminhhuy-ute/learnerlab-ops-dashboard/blob/main/tuan_2/docs/10-week2-assignment-and-time.md).

## Điều kiện hoàn tất

- Các luồng dữ liệu chính được kiểm tra từ collector đến API và snapshot lưu trữ.
- Kết quả kiểm thử ghi rõ điều kiện chạy, phản hồi thực tế và ảnh minh chứng.
- Chính sách AWS_IAM, quyền LabRole và cấu hình riêng tư của S3 được rà soát.
- CloudWatch có log và chỉ số cần thiết; cảnh báo chỉ được đánh dấu đã thử khi có kết quả thật.
- Template và worklog khớp với tài nguyên, lệnh và kết quả thực tế.
- Tài nguyên thử không cần thiết được dừng hoặc xóa theo quy định Learner Lab.

[Báo cáo tuần 2](https://github.com/leminhhuy-ute/learnerlab-ops-dashboard/blob/main/tuan_2/README.md) · [Phân công và thời lượng tuần 2](https://github.com/leminhhuy-ute/learnerlab-ops-dashboard/blob/main/tuan_2/docs/10-week2-assignment-and-time.md).

## Cập nhật tiến độ thực tế — 20/10/2026

| Hạng mục | Trạng thái đã xác minh | Việc còn lại / giới hạn |
|---|---|---|
| Nhánh cảnh báo SNS subscription chưa xác nhận | Lambda thử riêng trả `sns_subscription_pending_confirmation`, `published=false`; không phát cảnh báo chi phí. | Không thay Lambda tuần 2; không cần gửi lại email xác nhận. |
| Snapshot billing và freshness guard | Snapshot thật `SNAPSHOT#20261013T020042Z` được xử lý là cũ; Lambda thử trả `stale_billing_snapshot`, `published=false`. | Dữ liệu mới nhất quan sát là bản ghi lịch sử, không đại diện chi phí hiện tại. |
| Bảo mật dashboard/API | S3 bật Block Public Access, SSE-S3 và tag; `GET /summary` vẫn dùng `IAM (built-in)`. | Dashboard chưa gọi API tự động do giữ AWS_IAM theo quyết định đã chọn; không đưa credentials vào trình duyệt. |
| Giám sát CloudWatch | Log group Lambda thử có retention 1 tuần; alarm metric `Errors > 0`/1 phút chuyển sang `OK` khi nhận `Errors=0`. | Chưa có datapoint lỗi để kiểm thử chuyển sang `ALARM`; alarm không có notification action. |
| Kiểm thử mã | 12/12 unit tests cục bộ đạt; các test live SNS, below-threshold và freshness guard có kết quả AWS được ghi trong evidence. | Chưa có kiểm thử API end-to-end có SigV4 trong lần rà soát này. |
| Quyền và IaC | Nền tảng tuần 1 có CloudFormation stack đã xác minh. | CloudShell bị explicit deny cho các thao tác đọc CloudWatch/Lambda/EventBridge; chưa rà soát đầy đủ quyền LabRole hoặc triển khai IaC tuần 3. Không thử vòng qua policy. |

Chi tiết cấu hình CloudWatch và trạng thái alarm: [evidence tuần 3](https://github.com/leminhhuy-ute/learnerlab-ops-dashboard/blob/main/tuan_3/evidence/08-cloudwatch-retention-alarm.md). Tổng hợp triển khai, kiểm thử và giới hạn: [README tuần 3](https://github.com/leminhhuy-ute/learnerlab-ops-dashboard/blob/main/tuan_3/README.md).
