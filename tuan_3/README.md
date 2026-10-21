# Tuần 3 — Tích hợp, bảo mật và giám sát

**Sinh viên:** Lê Minh Huy — MSSV 24110019

**Mã học phần:** CLCO332779

**Môi trường:** AWS Learner Lab, account `213858341631`, Region `us-east-1`

> **Đối chiếu trước khi nộp:** Mã tuần 3 đã được triển khai lên Lambda cảnh báo sản phẩm và các test chính có kết quả cục bộ/AWS. Tuy vậy, theo checklist đã lập, tuần 3 **chưa thể xác nhận hoàn tất 100%**: CloudWatch alarm mới theo dõi Lambda thử, chưa bao phủ Lambda sản phẩm và ba lịch EventBridge. Bảng đối chiếu từng mục, bằng chứng và việc còn thiếu nằm trong [rà soát hoàn tất tuần 3](evidence/14-final-completion-review.md). Không trình bày các mục còn thiếu như đã triển khai.

## Kết quả

Các hạng mục tuần 3 gồm kiểm tra tuổi snapshot trước khi cảnh báo, xử lý SNS chưa xác nhận, xác thực API và giám sát CloudWatch đã được triển khai/kiểm thử trên AWS. Ngày 21/10, cùng handler tuần 3 được cập nhật lên **Lambda cảnh báo sản phẩm** `learnerlab-ops-week2-threshold-alert`; topic, bảng snapshot, ngưỡng 10 USD và trigger EventBridge được giữ nguyên. Topic/Lambda thử vẫn tách riêng cho các phép thử tiêu cực. Xem [biên bản triển khai sản phẩm và ảnh kết quả](evidence/10-product-alert-deployment.md).

### Mã và kiểm thử cục bộ

Handler [`src/threshold-alert/lambda_function.py`](src/threshold-alert/lambda_function.py) từ chối snapshot không an toàn trước khi phát cảnh báo:

- Subscription SNS đang `PendingConfirmation`: `sns_subscription_pending_confirmation`, `published=false`; không gọi `Publish`.
- Không có subscriber đã xác nhận: `sns_no_confirmed_subscribers`, `published=false`.
- Snapshot cũ, thiếu/sai `collectedAt` hoặc có thời gian tương lai: trả trạng thái riêng, `published=false`.
- Snapshot hợp lệ dưới ngưỡng: `below_threshold`, `published=false`.

Chạy kiểm thử:

```powershell
python -m unittest discover -s tuan_3/tests -v
```

**12/12 unit tests đạt.** Bao gồm subscription chờ xác nhận/đã xác nhận/hỗn hợp, phân trang, lỗi quyền SNS, chi phí dưới ngưỡng và các trường hợp freshness. Mã được triển khai trước trên Lambda thử, rồi lên Lambda sản phẩm ngày 21/10. Chi tiết từng lần gọi nằm trong [evidence SNS](evidence/01-live-sns-check.md), [evidence freshness](evidence/05-live-freshness-guard.md), [evidence API/CloudWatch](evidence/09-api-and-alarm-live-tests.md) và [evidence sản phẩm](evidence/10-product-alert-deployment.md).

## Kết quả kiểm thử AWS

| Hạng mục | Kết quả đã quan sát |
|---|---|
| SNS chưa xác nhận | Topic thử có 1 email subscription `PendingConfirmation`; Lambda trả `sns_subscription_pending_confirmation`, `published=false`, không gửi email. |
| Freshness guard | Snapshot lịch sử `SNAPSHOT#20261013T020042Z` bị từ chối là cũ; Lambda trả `stale_billing_snapshot`, `published=false`. |
| API Gateway `GET /summary` | Request không ký nhận `Forbidden`; request SigV4 trả HTTP 200. Đã đối chiếu các trường inventory EC2 và billing được chọn với snapshot DynamoDB mới nhất; cả hai khớp (`True`). Chỉ lưu kết quả đối chiếu, không ghi giá trị chi phí/tài nguyên vào evidence. |
| CloudWatch | Log group và alarm `Errors > 0` của Lambda thử được kiểm tra; alarm chuyển `OK → In alarm → OK` theo metric thật. Chưa có alarm cho Lambda sản phẩm và ba lịch EventBridge. Không có notification action. |
| Bảo mật S3/API | Bucket dashboard vẫn bật Block Public Access, SSE-S3 và tag; API vẫn dùng `IAM (built-in)`. Dashboard tĩnh tiếp tục nhận JSON thủ công theo quyết định giữ AWS_IAM, không nhúng credentials vào trình duyệt. |
| EventBridge | Ba lịch tuần 2 được ghi nhận `ENABLED` trong lần rà soát CloudWatch. |
| Lambda sản phẩm | Mã tuần 3 cập nhật thành công ngày 21/10; gọi `{}` với snapshot mới trả `StatusCode=200`, `FunctionError=null`, `below_threshold`, `published=false`; giữ ngưỡng 10 USD. |

Biên bản đầy đủ về trạng thái, lệnh và giới hạn của từng phép thử: [API SigV4 và alarm](evidence/09-api-and-alarm-live-tests.md), [retention/alarm](evidence/08-cloudwatch-retention-alarm.md), [rà soát quyền](evidence/06-current-lab-permission-block.md), [bảo mật](evidence/07-security-review.md).

Ảnh AWS thật được đặt ngay tại phần kết quả tương ứng: [Lambda sản phẩm](evidence/10-product-alert-deployment.md), [SNS chưa xác nhận và CloudWatch History](evidence/11-additional-live-results.md), [freshness guard trên Lambda thử](evidence/05-live-freshness-guard.md).

## Phạm vi và giới hạn

- Mã cảnh báo tuần 3 đã chạy trên Lambda sản phẩm; kiểm thử ứng dụng, API và phần giám sát Lambda thử có bằng chứng. Tuy nhiên, mục giám sát trong kế hoạch chưa bao phủ Lambda sản phẩm/EventBridge, nên chưa kết luận tuần 3 hoàn tất 100% theo checklist.
- IaC bổ sung là tùy chọn theo yêu cầu đề tài; không tạo stack giám sát trùng với tài nguyên đã cấu hình trực tiếp.
- `GET /summary` đã kiểm thử bằng SigV4 từ CloudShell; không tự nối dashboard S3 vì dashboard tĩnh không có cơ chế ký request an toàn và người học đã chọn giữ AWS_IAM.
- Trong phiên 20/10, một số truy vấn chỉ đọc (`logs:DescribeLogGroups`, `cloudwatch:DescribeAlarms`, `lambda:GetFunctionConfiguration`, `events:ListRules`) bị explicit deny bởi `voc-cancel-cred`; không tìm cách vòng qua policy. Phiên 21/10 đã gọi được `lambda:GetFunctionConfiguration` cho hàm sản phẩm để đối chiếu gói mã/cấu hình. Chưa khẳng định các quyền bị từ chối khác đã thay đổi.
- Snapshot ngày 13/10 dùng cho phép thử freshness là dữ liệu lịch sử/ước tính. Snapshot ngày 21/10 dùng cho lần gọi Lambda sản phẩm là dữ liệu mới tại thời điểm đó; không suy ra chi phí tương lai từ nó.

## Worklog và AI

Sinh viên xác nhận 8 giờ cho tuần 3: ngày 19/10 có 3 giờ làm dự án và 1 giờ tìm hiểu ngoài hệ thống; ngày 20/10 cũng có 3 giờ làm dự án và 1 giờ tìm hiểu ngoài hệ thống. Hai giờ tìm hiểu được xác nhận bổ sung ngày 21/10. Đây là thời lượng sinh viên tự xác nhận, chưa có mốc bắt đầu/kết thúc hay minh chứng độc lập để kiểm tra độ dài từng buổi. Worklog phân biệt thời lượng này với thao tác của **LLM/AI (ChatGPT)**. Lượt rà soát, gọi API và thử alarm do AI thực hiện không được cộng vào giờ sinh viên. Xem [phân công và thời lượng tuần 3](docs/10-week3-assignment-and-time.md) và [worklog.csv](worklog.csv).

Kế hoạch và tiêu chí tuần 3: [09-week3-plan.md](../tuan_2/docs/09-week3-plan.md).

Kế hoạch tiếp theo (chưa thực hiện): [dự kiến tuần 4](../tuan_4/README.md).
