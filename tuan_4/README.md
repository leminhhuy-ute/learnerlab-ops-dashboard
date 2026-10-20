# Kế hoạch dự kiến tuần 4 — Kiểm thử tổng thể và hoàn thiện bàn giao

**Sinh viên phụ trách:** Lê Minh Huy — MSSV 24110019
**Mã học phần:** CLCO332779
**Trạng thái:** Kế hoạch; các việc bên dưới chưa được tính là đã thực hiện.

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
- Chưa có kết quả AWS, ảnh chụp, số liệu chi phí hoặc worklog thực tế nào của tuần 4 được khẳng định trong tài liệu này.

## Tiêu chí kết thúc tuần 4

- Các kiểm thử hồi quy cần thiết có trạng thái và evidence đối chiếu được.
- Chi phí được trình bày theo đúng nguồn và kỳ dữ liệu; không gọi nhầm ước tính là hóa đơn cuối kỳ.
- Tài nguyên thử được giữ lại có lý do hoặc được dọn có kiểm soát; trạng thái trước/sau được ghi lại.
- Báo cáo tổng kết, repo và demo thống nhất với trạng thái thật trên AWS.
- Worklog phản ánh việc và giờ sinh viên xác nhận, đồng thời khai báo phần LLM/AI hỗ trợ riêng.

**Tham chiếu:** [Tổng hợp tuần 3](../tuan_3/README.md) · [Nguồn dữ liệu](../docs/data-sources.md) · [Repository](https://github.com/leminhhuy-ute/learnerlab-ops-dashboard).
