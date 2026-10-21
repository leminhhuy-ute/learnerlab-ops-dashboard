# Kế hoạch dự kiến tuần 4 — Kiểm thử tổng thể và hoàn thiện bàn giao

**Sinh viên phụ trách:** Lê Minh Huy — MSSV 24110019
**Mã học phần:** CLCO332779
**Trạng thái:** Hoàn thành buổi kiểm thử đầu tiên ngày 21/10/2026 (25% kế hoạch tuần 4); phần rà soát, dọn dẹp và tổng kết tiếp tục ở các buổi sau.

## Tiến độ ngày 21/10/2026 — buổi 1 (25%)

Đã chạy 12/12 unit tests của guard tuần 3 và 3/3 kiểm thử hồi quy cục bộ cho Lambda đọc snapshot. Kiểm thử mới phát hiện và sửa lỗi `IndexError` khi DynamoDB trả `Items` rỗng. Bản sửa nằm trong repo cục bộ, **chưa triển khai lên Lambda AWS**.

Learner Lab đã Ready; lần kiểm tra AWS lúc 13:46 ICT xác nhận account `213858341631`, Region `us-east-1`. Bảng DynamoDB `learnerlab-ops-week2-snapshots` ở trạng thái `ACTIVE`, PAY_PER_REQUEST, có 78 item. Lambda `learnerlab-ops-week2-read-api` được gọi trực tiếp và trả `StatusCode=200`; response có trạng thái `ok`, 10/10 hàng inventory đều `ok`, không thiếu snapshot; billing `ok`, `estimated=true`, kỳ dữ liệu `2026-10-01` đến trước `2026-10-22`. API `GET /summary` trả HTTP 200 khi ký SigV4 và HTTP 403 khi không xác thực; đối chiếu trực tiếp với DynamoDB cho kết quả 10/10 snapshot inventory khớp và snapshot billing khớp. Năm alarm CloudWatch đang `OK`, ba lịch EventBridge đang `ENABLED`, SNS có email subscription đã xác nhận. Chi tiết lệnh, kết quả và giới hạn nằm trong [biên bản kiểm thử](evidence/01-regression-2026-10-21.md).

Theo kế hoạch 4 buổi, buổi 1 tương ứng 25% tổng thời lượng dự kiến. Worklog ghi 2 giờ do sinh viên tự xác nhận, không có mốc giờ độc lập; thời gian và các thao tác do LLM/AI (ChatGPT) thực hiện được khai riêng, không cộng vào giờ sinh viên.

## Mục tiêu

Kiểm thử lại luồng dashboard từ nguồn dữ liệu đến API, rà soát chi phí và cấu hình bảo mật, dọn tài nguyên thử không còn cần thiết, sau đó hoàn thiện báo cáo và bản demo. Mọi kết quả trong báo cáo sẽ dựa trên lần kiểm tra thực tế của tuần 4; số liệu cũ được ghi rõ ngày và không trình bày như số liệu hiện tại.

## Thứ tự công việc dự kiến

| Buổi | Thời lượng dự kiến | Công việc | Cách xác nhận hoàn tất |
|---|---:|---|---|
| 1 | 2 giờ | Chạy kiểm thử hồi quy inventory, billing snapshot, freshness guard, SNS, API Gateway và CloudWatch alarm. Kiểm tra request API có SigV4 và request không xác thực; đối chiếu phản hồi đọc với snapshot DynamoDB tương ứng. | Bảng test case ghi điều kiện, kết quả quan sát, thời điểm và đường dẫn evidence. Không thay dữ liệu thật bằng kết quả giả lập. |
| 2 | 2 giờ | Rà soát chi phí và tài nguyên trong các Region được phép. Đọc snapshot Cost Explorer hiện có; nếu cần gọi Cost Explorer thì giới hạn vài request trong ngày. Kiểm tra các tài nguyên có thể phát sinh phí và trạng thái tag. | Bảng tổng hợp ghi rõ kỳ dữ liệu, nguồn, thời điểm và việc số liệu là ước tính hay dữ liệu đã chốt. Không tạo EC2/RDS/SageMaker/EKS mới chỉ để làm demo. |
| 3 | 2 giờ | Rà soát bảo mật và dọn tài nguyên thử tuần 3 nếu đã lưu đủ minh chứng, không còn phụ thuộc và quyền Lab cho phép. Kiểm tra lại S3 Block Public Access/SSE-S3, API AWS_IAM, tag và giới hạn Region. | Checklist trước/sau dọn dẹp; chỉ xóa đúng tài nguyên thử đã xác định, kiểm tra phụ thuộc trước khi thao tác. Nếu quyền bị từ chối thì ghi lại, không tìm cách vượt quyền. |
| 4 | 2 giờ | Hoàn thiện nội dung báo cáo tổng kết, liên kết đến mã nguồn/evidence/commit, chuẩn bị kịch bản demo tối đa 10 phút và kiểm tra repository. | Báo cáo và demo khớp trạng thái AWS đã quan sát; link Git mở được; không chứa credentials, URL ký tạm thời hoặc thông tin nhạy cảm. |

**Tổng thời lượng dự kiến: 8 giờ.** Đây là phân bổ kế hoạch theo yêu cầu học phần, không phải worklog đã làm. Worklog tuần 4 sẽ chỉ ghi thời gian và phần việc sinh viên xác nhận sau từng buổi; thời gian LLM/AI (ChatGPT) hỗ trợ sẽ được ghi riêng, không cộng vào giờ sinh viên.

## Điều kiện và giới hạn

- Chỉ làm trong `us-east-1` hoặc `us-west-2`, dùng `LabRole`/`LabInstanceProfile` có sẵn; không tạo IAM user/role.
- Nếu cần tạo tài nguyên kiểm thử, tuân thủ giới hạn EC2, vCPU và EBS của học phần; gắn tag `Project` và `Owner`.
- Không gọi Cost Explorer liên tục; API có tính phí theo request. Ưu tiên snapshot đã có và chỉ gọi thêm khi cần xác minh.
- Lưu ảnh/log minh chứng trước khi dọn tài nguyên thử. Không xóa VPC, bucket dữ liệu, bảng DynamoDB hoặc tài nguyên lõi trước khi kiểm tra phụ thuộc và xác nhận chúng không cần cho demo/bàn giao.
- Không đưa credentials vào repo hoặc trình duyệt. Nếu LabRole tiếp tục bị explicit deny, ghi rõ phạm vi không thể kiểm tra thay vì suy đoán.
- Kết quả billing trong buổi 1 là snapshot ước tính (`estimated=true`), không phải hóa đơn chốt. Không lưu giá trị tiền hoặc địa chỉ email vào evidence.
- Bản sửa `Items=[]` mới vượt qua kiểm thử hồi quy cục bộ; Lambda sản phẩm trên AWS vẫn là phiên bản triển khai trước đó. Chưa kết luận lỗi biên này đã được khắc phục trên AWS.

## Tiêu chí kết thúc tuần 4

- Các kiểm thử hồi quy cần thiết có trạng thái và evidence đối chiếu được.
- Chi phí được trình bày theo đúng nguồn và kỳ dữ liệu; không gọi nhầm ước tính là hóa đơn cuối kỳ.
- Tài nguyên thử được giữ lại có lý do hoặc được dọn có kiểm soát; trạng thái trước/sau được ghi lại.
- Báo cáo tổng kết, repo và demo thống nhất với trạng thái thật trên AWS.
- Worklog phản ánh việc và giờ sinh viên xác nhận, đồng thời khai báo phần LLM/AI hỗ trợ riêng.

**Tham chiếu:** [Tổng hợp tuần 3](../tuan_3/README.md) · [Nguồn dữ liệu](../docs/data-sources.md) · [Repository](https://github.com/leminhhuy-ute/learnerlab-ops-dashboard).
