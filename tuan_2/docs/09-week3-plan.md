# Kế hoạch tuần 3

**Sinh viên phụ trách:** Lê Minh Huy — MSSV 24110019.

**Mã học phần:** CLCO332779.

**Đề tài:** Bảng điều khiển vận hành cho AWS Learner Lab.

## Mục tiêu

Tích hợp các thành phần tuần 2 thành luồng vận hành có thể kiểm tra, rà soát bảo mật, bổ sung giám sát CloudWatch và cân nhắc IaC nếu phù hợp với quyền Learner Lab. Kế hoạch ban đầu được giữ để đối chiếu; phần cập nhật cuối tài liệu ghi kết quả đã chạy trên AWS.

## Thứ tự công việc

| Thứ tự | Công việc | Cách kiểm tra | Đầu ra |
|---|---|---|---|
| 1 | Rà soát luồng inventory/billing → DynamoDB → Lambda đọc → API Gateway; xác nhận tên bảng, khóa, khoảng thời gian và cách nhận biết snapshot lỗi hoặc cũ. | Gọi API có SigV4, so sánh phản hồi với bản ghi DynamoDB tương ứng; kiểm tra trường thời gian, trạng thái và nguồn dữ liệu. | Hoàn tất: API HTTP 200; các trường inventory EC2 và billing được chọn khớp snapshot DynamoDB mới nhất. Kết quả chỉ ghi cờ khớp, không ghi số tiền/tài nguyên. |
| 2 | Đánh giá cách kết nối dashboard S3 với GET /summary đang bảo vệ bằng AWS_IAM. | Xác định phương án xác thực phù hợp Learner Lab; kiểm tra luồng trong trình duyệt mà không đưa credentials tạm thời vào HTML, JavaScript, Git hoặc ảnh. | Quyết định kiến trúc và kiểm thử. Nếu chưa có cách an toàn, giữ xác thực AWS_IAM và ghi rõ thao tác nạp JSON thủ công hiện tại. |
| 3 | Thiết lập giám sát CloudWatch cho các Lambda và lịch EventBridge. | Kiểm tra log, Errors, Throttles, Duration, Invocations và trạng thái target; tạo thử cảnh báo trong điều kiện kiểm soát nếu quyền Lab cho phép. Không gửi cảnh báo vượt ngưỡng giả như thể là dữ liệu thật. | Log group và cấu hình metric/alarm phù hợp, ảnh kết quả kiểm tra. |
| 4 | Rà soát bảo mật và quyền truy cập. | Xác nhận S3 vẫn riêng tư, Block Public Access và SSE-S3 còn bật; API vẫn yêu cầu SigV4; rà soát quyền hiện có của LabRole, không tạo IAM user/role mới. | Bảng kiểm soát bảo mật và các điểm cần điều chỉnh nếu phát hiện. |
| 5 | Chuẩn bị tự động hóa/IaC cho các tài nguyên phù hợp với quyền Learner Lab. | Đối chiếu template với tài nguyên đang chạy, tag Project/Owner, Region và cấu hình; thử kiểm tra template trước khi cập nhật stack. Không ghi nhận triển khai nếu lệnh bị thiếu quyền hoặc chưa chạy thành công. | Template/runbook có thể kiểm tra lại và biên bản kết quả triển khai hoặc giới hạn quyền. |
| 6 | Chạy kiểm thử hồi quy, lưu minh chứng và rà soát chi phí. | Lặp lại các kiểm tra inventory, snapshot, billing theo hạn mức Cost Explorer, API có/không có chữ ký, SNS subscription và lịch chạy; xác minh không còn dữ liệu thử hoặc tài nguyên tạm không cần thiết. | Bảng test case–kết quả, ảnh Console/CLI có Region và thời gian, worklog và danh sách dọn dẹp. |

## Phân công và cách ghi worklog

Sinh viên phụ trách đọc yêu cầu, xác định thứ tự triển khai, kiểm tra kết quả trên Learner Lab, giải thích cấu hình và lưu minh chứng. Nếu LLM/AI (ChatGPT) hỗ trợ viết mã, template, phân tích log hoặc chạy lệnh, worklog cần ghi riêng chính xác phần đó; không cộng thời gian AI vào thời lượng sinh viên.

Ghi số giờ thực tế theo từng ngày sau khi sinh viên xác nhận. Không tự chia tổng giờ thành các buổi hoặc gán giờ cho một tác vụ nếu không có ghi chép. Tài liệu đối chiếu tuần 2 hiện tại: [worklog](https://github.com/leminhhuy-ute/learnerlab-ops-dashboard/blob/main/tuan_2/worklog.csv) và [phân công, thời lượng tuần 2](https://github.com/leminhhuy-ute/learnerlab-ops-dashboard/blob/main/tuan_2/docs/10-week2-assignment-and-time.md).

## Điều kiện hoàn tất

- Luồng đọc được kiểm tra bằng request SigV4 tới API; request không ký bị từ chối.
- Các nhánh SNS `PendingConfirmation`, freshness và dưới ngưỡng có kết quả AWS; unit tests hồi quy đạt.
- S3 riêng tư, SSE-S3 và AWS_IAM được giữ nguyên; dashboard không nhận credentials.
- Log group có retention, alarm CloudWatch được kiểm tra cả trạng thái `ALARM` và trạng thái phục hồi `OK` bằng metric thật trên Lambda thử.
- Evidence/worklog phân biệt rõ thao tác LLM/AI với giờ sinh viên; không ghi giờ AI thành giờ SV.
- IaC bổ sung là tùy chọn theo yêu cầu đề tài. Không tạo stack giám sát trùng với tài nguyên đã cấu hình.

[Báo cáo tuần 2](https://github.com/leminhhuy-ute/learnerlab-ops-dashboard/blob/main/tuan_2/README.md) · [Phân công và thời lượng tuần 2](https://github.com/leminhhuy-ute/learnerlab-ops-dashboard/blob/main/tuan_2/docs/10-week2-assignment-and-time.md).

## Cập nhật tiến độ thực tế — 20/10/2026

| Hạng mục | Trạng thái đã xác minh | Việc còn lại / giới hạn |
|---|---|---|
| Nhánh cảnh báo SNS subscription chưa xác nhận | Lambda thử riêng trả `sns_subscription_pending_confirmation`, `published=false`; không phát cảnh báo chi phí. | Không thay Lambda tuần 2; không cần gửi lại email xác nhận. |
| Snapshot billing và freshness guard | Snapshot thật `SNAPSHOT#20261013T020042Z` được xử lý là cũ; Lambda thử trả `stale_billing_snapshot`, `published=false`. | Dữ liệu mới nhất quan sát là bản ghi lịch sử, không đại diện chi phí hiện tại. |
| Bảo mật dashboard/API | S3 bật Block Public Access, SSE-S3 và tag; route `GET /summary` dùng `IAM (built-in)`. Không ký bị `Forbidden`; SigV4 trả HTTP 200 với JSON `billing`, `inventory`, `status`. | Dashboard giữ cách nạp JSON thủ công theo quyết định AWS_IAM; không đưa credentials vào trình duyệt. |
| Đối chiếu nguồn dữ liệu API | Inventory EC2 `us-east-1` và các trường billing được chọn trong phản hồi SigV4 đều khớp bản ghi snapshot DynamoDB mới nhất (`True`). | Chỉ lưu kết quả khớp/không khớp và trạng thái; không công khai giá trị chi phí hoặc danh sách tài nguyên. |
| Giám sát CloudWatch | Log group thử retention 7 ngày. Alarm `Errors > 0`/1 phút chuyển `OK → In alarm` sau một fault-injection có chủ đích và trở lại `OK` sau lần gọi an toàn; không có action gửi email. | Alarm theo dõi riêng Lambda thử, không phải mọi Lambda của tài khoản. |
| Kiểm thử mã và tích hợp | 12/12 unit tests đạt; SNS pending, below-threshold, freshness guard và GET SigV4 đã được kiểm tra. | Snapshot billing dùng trong các test trước là lịch sử/ước tính, không phải chi phí hiện tại. |
| Quyền và IaC | Quyền cần thiết cho các nhánh Lambda đã được xác nhận qua kết quả chạy; CloudFormation nền tảng tuần 1 và lịch EventBridge tuần 2 tồn tại. IaC giám sát bổ sung là tùy chọn. | Không đọc được đầy đủ policy LabRole do explicit deny `voc-cancel-cred` cho một số API chỉ đọc; không thử vượt policy. Không tạo stack trùng. |

Chi tiết kiểm thử API SigV4 và hai lần chuyển trạng thái alarm: [evidence API/alarm](https://github.com/leminhhuy-ute/learnerlab-ops-dashboard/blob/main/tuan_3/evidence/09-api-and-alarm-live-tests.md). Cấu hình CloudWatch: [retention/alarm](https://github.com/leminhhuy-ute/learnerlab-ops-dashboard/blob/main/tuan_3/evidence/08-cloudwatch-retention-alarm.md). Tổng hợp tuần 3: [README](https://github.com/leminhhuy-ute/learnerlab-ops-dashboard/blob/main/tuan_3/README.md).

## Đối chiếu cuối — 21/10/2026

| Checklist | Trạng thái cuối | Bằng chứng / việc còn lại |
|---|---|---|
| Tích hợp API, DynamoDB và guard cảnh báo | Handler tuần 3 đã triển khai lên Lambda sản phẩm; invocation dưới ngưỡng trả `below_threshold`, `published=false`. API SigV4 trả HTTP 200, không ký bị `Forbidden`. | [Lambda sản phẩm](../../tuan_3/evidence/10-product-alert-deployment.md), [API/alarm](../../tuan_3/evidence/09-api-and-alarm-live-tests.md). Nhánh cảnh báo vượt ngưỡng của sản phẩm chưa phát thử email trên AWS. |
| SNS PendingConfirmation và freshness guard | Có kết quả AWS trên Lambda/topic thử tách riêng; cả hai nhánh đều không publish. | [Kết quả bổ sung](../../tuan_3/evidence/11-additional-live-results.md), [freshness](../../tuan_3/evidence/05-live-freshness-guard.md). |
| Bảo mật S3/API | Block Public Access, SSE-S3 và AWS_IAM được giữ. | [Rà soát bảo mật](../../tuan_3/evidence/07-security-review.md). Policy LabRole chỉ đọc được một phần do explicit deny. |
| Giám sát CloudWatch | Log retention 7 ngày và alarm đã được kiểm tra trên Lambda thử; alarm ghi nhận `OK → In alarm → OK`. | Chưa có alarm cho Lambda sản phẩm và ba lịch EventBridge; xem [rà soát cuối](../../tuan_3/evidence/14-final-completion-review.md). |
| Kiểm thử mã | 12/12 unit tests đạt. | Kiểm thử cục bộ bổ trợ, không thay cho kiểm thử AWS. |
| IaC bổ sung | Không tạo stack giám sát mới; IaC là tùy chọn và tránh tạo tài nguyên trùng. | Các tài nguyên tuần 1/2 đã có cấu hình trực tiếp. |

**Kết luận:** Tuần 3 đã triển khai mã guard lên Lambda sản phẩm và có bằng chứng tích hợp/bảo mật/kiểm thử. Theo checklist giám sát đã ghi ở kế hoạch, tuần 3 **chưa được xác nhận hoàn tất 100%** vì alarm hiện chỉ bao phủ Lambda thử, chưa có alarm cho Lambda sản phẩm và các lịch EventBridge. Một số thao tác đọc policy `LabRole` bị explicit deny; không tìm cách vòng qua policy.
