# Tuần 4 — Kiểm thử tổng thể và hoàn thiện bàn giao

**Sinh viên phụ trách:** Lê Minh Huy — MSSV 24110019
**Mã học phần:** CLCO332779
**Trạng thái:** Các nhóm công việc kỹ thuật tuần 4 có minh chứng AWS đến 23/10/2026. Ngày 27/10 chạy lại 16/16 kiểm thử cục bộ đều đạt; bản Word tổng kết đã hoàn tất. Video chưa được ghi nhận hoàn thành; tài nguyên lõi và một số tài nguyên thử đang giữ cần được rà soát/dọn sau buổi quay.

**Đối chiếu ngày 27/10:** [Bảng kiểm tra mức độ hoàn tất](docs/12-completion-audit-2026-10-27.md) ghi kết quả kiểm thử cục bộ và kiểm tra trực tiếp AWS sau khi Lab Ready. API và cấu hình bảo mật đã được đối chiếu; snapshot kiểm kê và chi phí vẫn thu ngày 23/10. [Kịch bản demo](docs/11-demo-script.md) có từng thao tác, lời thoại và thời lượng khoảng 9 phút.

## Tiến độ ngày 21/10/2026 — buổi 1 (25%)

Đã chạy 12/12 unit tests của guard tuần 3 và 3/3 kiểm thử hồi quy cục bộ cho Lambda đọc snapshot. Kiểm thử mới phát hiện và sửa lỗi `IndexError` khi DynamoDB trả `Items` rỗng. Bản sửa nằm trong repo cục bộ, **chưa triển khai lên Lambda AWS**.

Learner Lab đã Ready; lần kiểm tra AWS lúc 13:46 ICT xác nhận account `213858341631`, Region `us-east-1`. Bảng DynamoDB `learnerlab-ops-week2-snapshots` ở trạng thái `ACTIVE`, PAY_PER_REQUEST, có 78 item. Lambda `learnerlab-ops-week2-read-api` được gọi trực tiếp và trả `StatusCode=200`; response có trạng thái `ok`, 10/10 hàng inventory đều `ok`, không thiếu snapshot; billing `ok`, `estimated=true`, kỳ dữ liệu `2026-10-01` đến trước `2026-10-22`. API `GET /summary` trả HTTP 200 khi ký SigV4 và HTTP 403 khi không xác thực; đối chiếu trực tiếp với DynamoDB cho kết quả 10/10 snapshot inventory khớp và snapshot billing khớp. Năm alarm CloudWatch đang `OK`, ba lịch EventBridge đang `ENABLED`, SNS có email subscription đã xác nhận. Chi tiết lệnh, kết quả và giới hạn nằm trong [biên bản kiểm thử](evidence/01-regression-2026-10-21.md).

Theo kế hoạch 4 buổi, buổi 1 tương ứng 25% tổng thời lượng dự kiến. Worklog ghi 2 giờ do sinh viên tự xác nhận, không có mốc giờ độc lập; thời gian và các thao tác do LLM/AI (ChatGPT) thực hiện được khai riêng, không cộng vào giờ sinh viên.

## Tiến độ ngày 22/10/2026 — buổi 2 (50% lũy kế)

Đã rà soát snapshot billing, tài nguyên có khả năng phát sinh chi phí và trạng thái tag trong hai Region được phép. Snapshot billing mới nhất được tìm thấy có `collectedAt=20261021T020041Z` (09:00:41 ICT ngày 21/10), `periodStart=2026-10-01`, `periodEndExclusive=2026-10-22`, `estimated=true`; snapshot không bao gồm ngày 22/10. Buổi này không gọi Cost Explorer, không ghi giá trị tiền và không coi số liệu ước tính là hóa đơn chốt.

Trong các dịch vụ đã kiểm tra, không thấy EC2 instance, EBS volume, NAT Gateway hoặc Elastic IP đang tồn tại ở `us-east-1`/`us-west-2`; cũng không thấy RDS, SageMaker endpoint/notebook, EKS, ELBv2 hoặc EFS. Redshift provisioned cluster, serverless workgroup và namespace đều không có ở `us-east-1`. Các kết quả này không chứng minh tài khoản không phát sinh phí: Lambda, DynamoDB, S3, CloudWatch và các dịch vụ khác vẫn có thể phát sinh phí.

Resource Groups Tagging API trả 22 tài nguyên mang tag `Project=learnerlab-ops` ở `us-east-1`, tất cả có `Owner=24110019`; không có tài nguyên mang tag Project này ở `us-west-2`. API này chỉ liệt kê tài nguyên có ít nhất một tag và có thể hỗ trợ khác nhau theo dịch vụ, nên không dùng nó để khẳng định mọi tài nguyên chưa gắn tag đều đã được phát hiện. Bucket dashboard được xác minh có đủ bốn cờ S3 Block Public Access bật, mã hóa SSE-S3/AES256 và các tag `Project`, `Environment`, `Owner`.

Rà soát phát hiện bốn CloudWatch alarm tuần 3 thuộc dự án thiếu `Project`/`Owner`. Đã gắn hai tag này cho bốn alarm và kiểm tra lại: cả năm alarm tuần 3 hiện đều có `Project` và `Owner`. Đây là thay đổi cấu hình duy nhất của buổi rà soát; không tạo/xóa tài nguyên. Chi tiết thời điểm, phạm vi lệnh, kết quả và giới hạn nằm trong [biên bản rà soát chi phí, tài nguyên và tag](evidence/02-cost-resource-review-2026-10-22.md).

Worklog ghi **3 giờ** do sinh viên tự xác nhận cho ngày 22/10/2026; không có mốc bắt đầu/kết thúc hay phân chia theo từng thao tác để kiểm chứng độc lập. CloudShell/AWS API được LLM/AI (ChatGPT) dùng để đọc trạng thái, gắn tag cho bốn alarm và xác minh sau thay đổi; thời gian AI khai riêng, không cộng vào giờ sinh viên.

## Tiến độ ngày 22/10/2026 — buổi 3 (75% lũy kế)

Đã kiểm tra trực tiếp hai bucket của dự án: đủ bốn cờ Block Public Access, SSE-S3/AES256, không có ACL công khai và có tag Project/Owner. API `GET /summary` vẫn dùng `AWS_IAM`; sau dọn dẹp, request không ký trả **403**, request SigV4 trả **200**, `status=ok`, có 10 hàng inventory và billing `status=ok`. Sáu Lambda dự án tại `us-east-1` đều dùng `LabRole`, không có Function URL; không thấy Lambda mang prefix dự án tại `us-west-2`.

Đã lưu cấu hình, tags và **4** bản ghi lịch sử của alarm thử `learnerlab-ops-week3-test-lambda-errors`, tải bản sao về máy, đối chiếu hash và kiểm tra không có composite alarm phụ thuộc. Sau đó dọn riêng alarm này. Bốn alarm sản phẩm vẫn còn, tham số cấu hình khớp trước/sau; ba rule EventBridge vẫn `ENABLED`. Lambda/topic thử và log retention 7 ngày được giữ để phục vụ phép thử gửi email thật và demo ở buổi cuối. Tại lần rà soát 22/10, topic thử chưa còn subscription; ngày 27/10 kiểm tra lại thấy cả topic thử và topic sản phẩm đều có một subscription đã xác nhận.

Chi tiết và ảnh AWS nằm trong [biên bản bảo mật/dọn dẹp](evidence/03-security-cleanup-2026-10-22.md); cấu hình và lịch sử alarm thử nằm ở [bản lưu trước dọn](evidence/04-test-alarm-archive-2026-10-22.md). [Script rà soát](scripts/review_security.py) chỉ đọc các trường cần kiểm tra và đã chạy trên CloudShell; SHA-256 nguồn khớp repo.

Buổi 3 ghi **thêm 2 giờ** theo xác nhận của sinh viên, giữ nguyên 3 giờ buổi 2 cùng ngày. [Worklog tuần 4](worklog.csv) hiện tổng **7 giờ**: 21/10 có 2 giờ, 22/10 có 3 + 2 giờ. LLM/AI ChatGPT trực tiếp chạy truy vấn, lưu/dọn alarm thử, kiểm tra API và thu ảnh; phần hỗ trợ được ghi riêng, không cộng vào giờ sinh viên.

## Tiến độ ngày 23/10/2026 — buổi 4

- Đã triển khai bản sửa `Items=[]` lên Lambda read-api sản phẩm, tải ZIP để đối chiếu nguồn; thử cùng mã trên bảng DynamoDB rỗng thật, nhận `missing/null` rồi dọn tài nguyên dùng một lần.
- Đã thu inventory và billing mới, chạy guard sản phẩm ở ngưỡng 10 USD/48 giờ; API SigV4 trả 200, unsigned 403; 10/10 hàng inventory và billing khớp DynamoDB. Billing gọi thêm một lần, bộ đếm ngày là 1/4, kết quả vẫn là ước tính.
- Đã sửa và triển khai dashboard lên S3; kiểm tra dữ liệu đủ, thiếu snapshot và JSON lỗi ngay trên trang thật. Dữ liệu thiếu được phân biệt với số lượng 0.
- Đã kiểm thử lại nhánh SNS chưa xác nhận bằng snapshot lịch sử thật và cấu hình replay riêng; nhánh xác nhận cũng đã trả `alert_published`, có messageId và người nhận xác nhận đã nhận email. Đã trả cấu hình thử về 10 USD/48 giờ và dọn bảng replay.
- **16/16 unit tests đạt**. Worklog ngày 23/10 bổ sung **3 giờ**, tổng tuần **10 giờ**; phần LLM/AI ChatGPT trực tiếp thao tác được khai riêng.

| Tài liệu | Nội dung |
|---|---|
| [Triển khai read-api và hồi quy luồng](evidence/06-read-api-deployment-2026-10-23.md) | Bảng rỗng, nguồn trên AWS, snapshot mới, API/DynamoDB và ảnh |
| [Kiểm thử SNS](evidence/08-sns-replay-2026-10-23.md) | Dữ liệu lịch sử 13/10, cửa sổ thử 336 giờ; trạng thái từng nhánh và giới hạn |
| [Giao diện và ảnh kết quả](evidence/10-dashboard-regression-2026-10-23.md) | Triển khai S3, ba trường hợp kiểm thử trên trình duyệt |
| [Rà soát cuối tuần](evidence/12-final-review-2026-10-23.md) | Checklist, cấu hình bảo mật và tài nguyên giữ cho demo |
| [Phân công và thời lượng](docs/10-week4-assignment-and-time.md) | Bốn buổi, tổng 10 giờ; [worklog CSV](worklog.csv) |

Bản Word tổng kết **toàn bộ dự án** đã hoàn tất sau buổi kỹ thuật cuối. Video được nộp riêng và còn phải quay; tỷ lệ hoàn tất kỹ thuật không có nghĩa toàn bộ việc bàn giao, gồm video và dọn tài nguyên còn giữ, đã kết thúc.

## Mục tiêu

Kiểm thử lại luồng dashboard từ nguồn dữ liệu đến API, rà soát chi phí và cấu hình bảo mật, dọn tài nguyên thử không còn cần thiết, sau đó hoàn thiện repository và chuẩn bị cho Word tổng kết/video demo ở bước tiếp theo. Mọi kết quả trong báo cáo sẽ dựa trên lần kiểm tra thực tế của tuần 4; số liệu cũ được ghi rõ ngày và không trình bày như số liệu hiện tại.

## Thứ tự công việc dự kiến

| Buổi | Thời lượng dự kiến | Công việc | Cách xác nhận hoàn tất |
|---|---:|---|---|
| 1 | 2 giờ | Chạy kiểm thử hồi quy inventory, billing snapshot, freshness guard, SNS, API Gateway và CloudWatch alarm. Kiểm tra request API có SigV4 và request không xác thực; đối chiếu phản hồi đọc với snapshot DynamoDB tương ứng. | Bảng test case ghi điều kiện, kết quả quan sát, thời điểm và đường dẫn evidence. Không thay dữ liệu thật bằng kết quả giả lập. |
| 2 | 2 giờ | Rà soát chi phí và tài nguyên trong các Region được phép. Đọc snapshot Cost Explorer hiện có; nếu cần gọi Cost Explorer thì giới hạn vài request trong ngày. Kiểm tra các tài nguyên có thể phát sinh phí và trạng thái tag. | Bảng tổng hợp ghi rõ kỳ dữ liệu, nguồn, thời điểm và việc số liệu là ước tính hay dữ liệu đã chốt. Không tạo EC2/RDS/SageMaker/EKS mới chỉ để làm demo. |
| 3 | 2 giờ | Rà soát bảo mật và dọn tài nguyên thử tuần 3 nếu đã lưu đủ minh chứng, không còn phụ thuộc và quyền Lab cho phép. Kiểm tra lại S3 Block Public Access/SSE-S3, API AWS_IAM, tag và giới hạn Region. | Checklist trước/sau dọn dẹp; chỉ xóa đúng tài nguyên thử đã xác định, kiểm tra phụ thuộc trước khi thao tác. Nếu quyền bị từ chối thì ghi lại, không tìm cách vượt quyền. |
| 4 | 2 giờ | Chốt bản sửa Lambda đọc API, kiểm thử nhánh gửi cảnh báo thật trên topic thử nếu đủ điều kiện; hoàn thiện nội dung tổng kết, liên kết mã nguồn/evidence/commit, kịch bản demo tối đa 10 phút và kiểm tra repository. | Báo cáo và demo khớp trạng thái AWS đã quan sát; link Git mở được; không chứa credentials, URL ký tạm thời hoặc thông tin nhạy cảm. |

**Tổng thời lượng dự kiến: 8 giờ.** Đây là phân bổ kế hoạch theo yêu cầu học phần, không phải worklog đã làm. Worklog tuần 4 sẽ chỉ ghi thời gian và phần việc sinh viên xác nhận sau từng buổi; thời gian LLM/AI (ChatGPT) hỗ trợ sẽ được ghi riêng, không cộng vào giờ sinh viên.

## Điều kiện và giới hạn

- Chỉ làm trong `us-east-1` hoặc `us-west-2`, dùng `LabRole`/`LabInstanceProfile` có sẵn; không tạo IAM user/role.
- Nếu cần tạo tài nguyên kiểm thử, tuân thủ giới hạn EC2, vCPU và EBS của học phần; gắn tag `Project` và `Owner`.
- Không gọi Cost Explorer liên tục; API có tính phí theo request. Ưu tiên snapshot đã có và chỉ gọi thêm khi cần xác minh.
- Lưu ảnh/log minh chứng trước khi dọn tài nguyên thử. Không xóa VPC, bucket dữ liệu, bảng DynamoDB hoặc tài nguyên lõi trước khi kiểm tra phụ thuộc và xác nhận chúng không cần cho demo/bàn giao.
- Không đưa credentials vào repo hoặc trình duyệt. Nếu LabRole tiếp tục bị explicit deny, ghi rõ phạm vi không thể kiểm tra thay vì suy đoán.
- Kết quả billing trong buổi 1 là snapshot ước tính (`estimated=true`), không phải hóa đơn chốt. Không lưu giá trị tiền hoặc địa chỉ email vào evidence.
- Bản sửa `Items=[]` đã triển khai và kiểm thử AWS ngày 23/10; các đoạn ghi “chưa triển khai” ở buổi 1 là trạng thái lịch sử ngày 21/10.

## Tiêu chí kết thúc tuần 4

- Các kiểm thử hồi quy cần thiết có trạng thái và evidence đối chiếu được.
- Chi phí được trình bày theo đúng nguồn và kỳ dữ liệu; không gọi nhầm ước tính là hóa đơn cuối kỳ.
- Tài nguyên thử được giữ lại có lý do hoặc được dọn có kiểm soát; trạng thái trước/sau được ghi lại.
- Repository và minh chứng thống nhất với trạng thái AWS; Word tổng kết toàn dự án và video demo được hoàn thiện ở bước tiếp theo.
- Worklog phản ánh việc và giờ sinh viên xác nhận, đồng thời khai báo phần LLM/AI hỗ trợ riêng.

**Tham chiếu:** [Tổng hợp tuần 3](../tuan_3/README.md) · [Nguồn dữ liệu](../docs/data-sources.md) · [Repository](https://github.com/leminhhuy-ute/learnerlab-ops-dashboard).
