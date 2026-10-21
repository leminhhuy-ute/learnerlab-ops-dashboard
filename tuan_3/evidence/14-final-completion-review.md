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
| CloudWatch cho Lambda sản phẩm và lịch EventBridge | Đã tạo alarm `learnerlab-ops-week3-product-alert-errors` cho Lambda sản phẩm và ba alarm `FailedInvocations` cho các rule `alert-daily`, `billing-daily`, `inventory-6h`. Sau chu kỳ đánh giá, cả bốn ở `OK`; alarm billing ghi rõ không nhận datapoint trong một kỳ và xử lý datapoint thiếu theo `notBreaching`. Không gắn notification action. Trạng thái `OK` không chứng minh rule/target chạy thành công. | Đạt về cấu hình; cần datapoint để chứng minh lần chạy lịch billing |
| Rà soát LabRole | Một số API đọc policy bị explicit deny `voc-cancel-cred`; không tìm cách vòng qua quyền. | Bị giới hạn bởi policy Learner Lab |
| IaC giám sát bổ sung | Không tạo stack giám sát mới để tránh trùng tài nguyên; IaC bổ sung là tùy chọn trong đề. | Không bắt buộc |
| Kiểm thử mã | Bộ `tuan_3/tests` chạy thành công **12/12**. | Đạt — kiểm thử cục bộ |

## Kết luận trung thực

Mã guard đã được triển khai lên Lambda sản phẩm; kiểm tra tích hợp, bảo mật, cấu hình alarm và unit test có bằng chứng. Bốn alarm bổ sung đã được tạo và xác minh trên AWS. Alarm billing hiện `OK` nhờ chính sách thiếu datapoint `notBreaching`, nhưng chưa có datapoint để xác nhận lần chạy lịch. Nhánh vượt ngưỡng của Lambda sản phẩm chưa được gọi trực tiếp trên AWS vì không tạo chi phí giả hoặc cảnh báo giả. Báo cáo không mô tả hai điểm này như đã kiểm thử thành công.

Không thêm giờ sinh viên vào worklog cho lượt rà soát này. Worklog chỉ giữ các giờ sinh viên đã xác nhận; việc chạy test và cập nhật tài liệu do LLM/AI thực hiện không được cộng vào thời lượng sinh viên.

## Bằng chứng liên quan

- [Triển khai Lambda sản phẩm và kết quả gọi thật](10-product-alert-deployment.md)
- [SNS PendingConfirmation và lịch sử CloudWatch](11-additional-live-results.md)
- [Bốn alarm CloudWatch cho Lambda sản phẩm và lịch EventBridge](15-cloudwatch-alarm-coverage.md)
- [API SigV4 và CloudWatch alarm](09-api-and-alarm-live-tests.md)
- [Kết quả 12 unit tests](https://github.com/leminhhuy-ute/learnerlab-ops-dashboard/blob/main/tuan_3/tests/test_threshold_alert.py)
- [Mã Lambda tuần 3](https://github.com/leminhhuy-ute/learnerlab-ops-dashboard/blob/main/tuan_3/src/threshold-alert/lambda_function.py)
