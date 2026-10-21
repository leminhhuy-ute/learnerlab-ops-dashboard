# Rà soát điều kiện hoàn tất tuần 3

**Ngày rà soát:** 21/10/2026  
**Môi trường:** AWS Learner Lab, account `213858341631`, Region `us-east-1`  
**Mã nguồn:** [Repository tuần 3](https://github.com/leminhhuy-ute/learnerlab-ops-dashboard/tree/main/tuan_3)

Tài liệu này đối chiếu kết quả đã có với checklist ở [kế hoạch tuần 3](https://github.com/leminhhuy-ute/learnerlab-ops-dashboard/blob/main/tuan_2/docs/09-week3-plan.md). Trạng thái chỉ phản ánh phép thử/cấu hình có bằng chứng; unit test không được tính thay cho kiểm thử AWS.

| Hạng mục | Bằng chứng và kết quả | Trạng thái |
|---|---|---|
| Guard trạng thái SNS | Lambda thử riêng đọc subscription đang `PendingConfirmation`, trả `sns_subscription_pending_confirmation`, `published=false`; không gọi SNS Publish. | Đạt — AWS thật trên tài nguyên thử |
| Guard freshness | Lambda thử từ chối snapshot lịch sử là `stale_billing_snapshot`, `published=false`. | Đạt — AWS thật trên tài nguyên thử |
| Nhánh dưới ngưỡng của Lambda sản phẩm | Handler tuần 3 được triển khai lên `learnerlab-ops-week2-threshold-alert`; lần gọi trả HTTP invocation 200, `FunctionError=null`, `below_threshold`, `published=false`. Ngưỡng sản phẩm giữ ở 10 USD. | Đạt — AWS thật |
| Nhánh vượt ngưỡng / email cảnh báo sản phẩm | Kiểm thử đơn vị xác nhận nhánh có subscriber đã xác nhận gọi Publish; chưa chủ động tạo dữ liệu chi phí giả hoặc gửi email thử từ Lambda sản phẩm. | Chưa kiểm thử trực tiếp trên AWS |
| API `GET /summary` | Request không ký bị `Forbidden`; SigV4 trả HTTP 200. Các trường inventory và billing được chọn khớp snapshot DynamoDB tại lần đối chiếu. | Đạt — AWS thật |
| Bảo vệ dashboard và API | Bucket dashboard bật Block Public Access/SSE-S3; `GET /summary` giữ `AWS_IAM`, không đưa credentials vào JavaScript. | Đạt — AWS Console |
| CloudWatch log retention | Log group của Lambda thử có retention 7 ngày. | Đạt — chỉ Lambda thử |
| CloudWatch alarm Lambda | Alarm `learnerlab-ops-week3-test-lambda-errors` đã chuyển `OK → In alarm → OK` theo metric Errors thật của Lambda thử; không gắn action gửi thông báo. | Đạt — chỉ Lambda thử |
| CloudWatch cho Lambda sản phẩm và lịch EventBridge | Chưa có bằng chứng alarm theo dõi `learnerlab-ops-week2-threshold-alert` và `FailedInvocations` của ba rule tuần 2. | Chưa đạt checklist giám sát |
| Rà soát LabRole | Một số API đọc policy bị explicit deny `voc-cancel-cred`; không tìm cách vòng qua quyền. | Bị giới hạn bởi policy Learner Lab |
| IaC giám sát bổ sung | Không tạo stack giám sát mới để tránh trùng tài nguyên; IaC bổ sung là tùy chọn trong đề. | Không bắt buộc |
| Kiểm thử mã | Bộ `tuan_3/tests` chạy thành công **12/12**. | Đạt — kiểm thử cục bộ |

## Kết luận trung thực

Mã guard đã được triển khai lên Lambda sản phẩm và các kiểm tra tích hợp/bảo mật có bằng chứng. Tuy nhiên, nếu áp dụng đúng checklist giám sát trong kế hoạch, **chưa thể ghi tuần 3 hoàn tất 100%** cho đến khi CloudWatch bao phủ Lambda sản phẩm và ba lịch EventBridge, rồi xác minh cấu hình/trạng thái trên AWS. Lần rà soát này không thể thực hiện thao tác tiếp trong CloudShell; vì vậy không ghi nhận thay đổi AWS mới.

Không thêm giờ sinh viên vào worklog cho lượt rà soát này. Worklog chỉ giữ các giờ sinh viên đã xác nhận; việc chạy test và cập nhật tài liệu do LLM/AI thực hiện không được cộng vào thời lượng sinh viên.

## Bằng chứng liên quan

- [Triển khai Lambda sản phẩm và kết quả gọi thật](10-product-alert-deployment.md)
- [SNS PendingConfirmation và lịch sử CloudWatch](11-additional-live-results.md)
- [API SigV4 và CloudWatch alarm](09-api-and-alarm-live-tests.md)
- [Kết quả 12 unit tests](https://github.com/leminhhuy-ute/learnerlab-ops-dashboard/blob/main/tuan_3/tests/test_threshold_alert.py)
- [Mã Lambda tuần 3](https://github.com/leminhhuy-ute/learnerlab-ops-dashboard/blob/main/tuan_3/src/threshold-alert/lambda_function.py)
