# Phân công và thời lượng tuần 2

**Sinh viên:** Lê Minh Huy — MSSV 24110019.

**Mã học phần:** CLCO332779.

**Đề tài:** Bảng điều khiển vận hành cho AWS Learner Lab.

**Tổng thời lượng tuần 2 do sinh viên xác nhận:** 11 giờ.

Tài liệu này tách riêng phần phân công và thời lượng theo góp ý của giảng viên. Giờ ngày 11/10 và 13/10 được sinh viên xác nhận bổ sung vào ngày 16/10/2026. Worklog không có giờ bắt đầu/kết thúc hay phân chia số giờ theo từng tác vụ; vì vậy tài liệu chỉ ghi tổng giờ theo ngày, không tự chia nhỏ hoặc lấy thời gian AWS/Git để tính.

## 1. Phân công nhiệm vụ

| Hạng mục | Phần việc sinh viên được ghi nhận | Phần có LLM/AI (ChatGPT) hỗ trợ hoặc thực hiện | Kết quả đối chiếu |
|---|---|---|---|
| Bảng snapshot DynamoDB | Xác nhận thời lượng buổi 10/10 và phạm vi làm việc; worklog không tách riêng thao tác AWS của sinh viên theo lệnh. | Tạo bảng snapshot, chạy PutItem/GetItem/Query/DeleteItem và kiểm tra bản ghi sau khi xóa. | Bảng ở trạng thái ACTIVE, PAY_PER_REQUEST; các thao tác CRUD trả HTTP 200, GetItem sau xóa không còn bản ghi. |
| Kiểm kê tài nguyên | Đăng nhập Learner Lab và giới hạn phạm vi buổi 11/10; xác nhận thời lượng ngày này bổ sung vào 16/10. | Viết, triển khai và gọi thử Lambda kiểm kê; sau đó triển khai inventory-core cho EC2, RDS, SageMaker endpoint/notebook và EKS tại hai Region. | 10 tổ hợp dịch vụ/Region trả status=ok và count=0 ở lần kiểm tra được lưu. Kết quả bằng 0 nghĩa là không tìm thấy tài nguyên thuộc phạm vi, không phải lỗi API. |
| Thu thập chi phí và API đọc | Xác nhận tổng thời lượng ngày 12/10; worklog không có phân bổ giờ theo từng thao tác. | Triển khai billing-collector, read-api và API Gateway GET /summary; gọi Cost Explorer theo giới hạn và kiểm tra xác thực SigV4. | API có chữ ký trả HTTP 200; request không ký trả HTTP 403. Snapshot Cost Explorer ghi 0.0000000001 USD và estimated=true. |
| Lịch chạy, cảnh báo và dashboard | Chọn phạm vi công việc ngày 13/10; xác nhận subscription SNS và đã nhận thư thử; xác nhận bổ sung tổng 3 giờ ngày 13/10 vào 16/10. | Tạo threshold-alert, ba lịch EventBridge, SNS topic và dashboard tĩnh trên S3; chạy các kiểm tra cấu hình và luồng dữ liệu. | Ba lịch được bật, có Lambda target và không ghi nhận failed entry; lịch billing tạo snapshot. Email thử đã được sinh viên xác nhận nhận. Dữ liệu thật thấp hơn ngưỡng 10 USD nên chưa có lần cảnh báo vượt ngưỡng. |

Thông tin kỹ thuật và ảnh theo từng thành phần nằm trong [báo cáo triển khai và kiểm thử tuần 2](https://github.com/leminhhuy-ute/learnerlab-ops-dashboard/blob/main/tuan_2/README.md). Bảng nguồn được xác định tại [docs/data-sources.md](https://github.com/leminhhuy-ute/learnerlab-ops-dashboard/blob/main/docs/data-sources.md).

## 2. Nhật ký theo ngày

Thời lượng trong bảng là số giờ sinh viên tự xác nhận. Các ghi nhận AWS và Git dùng để đối chiếu sự kiện kỹ thuật, không dùng để suy ra giờ học hoặc thời gian thao tác cá nhân.

| Ngày | Giờ sinh viên xác nhận | Công việc sinh viên được ghi nhận | Công việc có LLM/AI (ChatGPT) hỗ trợ hoặc trực tiếp thực hiện |
|---|---:|---|---|
| 10/10/2026 | 2 giờ | Xác nhận tổng thời lượng của buổi; worklog ban đầu ghi nhận sinh viên tự đọc, kiểm tra hoặc thao tác AWS nhưng chưa có phân bổ theo việc. | Tạo bảng DynamoDB snapshots và chạy kiểm thử CRUD. |
| 11/10/2026 | 3 giờ | Sinh viên xác nhận bổ sung tổng 3 giờ vào ngày 16/10. Worklog ghi nhận sinh viên đăng nhập Learner Lab và giới hạn phạm vi buổi; không có mốc giờ hay phân bổ theo tác vụ. | Tạo mã và triển khai EC2 collector; chạy invocation đồng bộ một lần, kiểm tra kết quả status=ok, resourceCount=0 và snapshot DynamoDB. |
| 12/10/2026 | 3 giờ | Xác nhận tổng thời lượng ngày 12/10; chưa có giờ bắt đầu/kết thúc hoặc phân bổ 3 giờ theo từng đầu việc. | Triển khai và kiểm thử inventory-core, billing-collector, read-api và API Gateway AWS_IAM; thực hiện hai lượt gọi Cost Explorer được ghi trong worklog. |
| 13/10/2026 | 3 giờ | Sinh viên xác nhận bổ sung tổng 3 giờ vào ngày 16/10. Worklog ghi nhận sinh viên chọn phạm vi, bấm xác nhận email subscription SNS và báo đã nhận thư thử; không có mốc giờ hay phân bổ theo tác vụ. | Tạo SNS, threshold-alert, lịch EventBridge và dashboard S3; kiểm tra API, snapshot, lịch billing và thư thử. |
| **Tổng** | **11 giờ** | **2 + 3 + 3 + 3 giờ theo xác nhận của sinh viên.** | Thời gian LLM/AI thao tác không cộng vào tổng giờ sinh viên. |

### Cách ghi nhận giờ bổ sung

Worklog ngày 11/10 và 13/10 được cập nhật lên 3 giờ/ngày theo xác nhận của sinh viên ngày 16/10/2026. Hai số giờ này là khai báo bổ sung của sinh viên; worklog không có mốc bắt đầu/kết thúc, bảng chấm công hay phân bổ theo tác vụ để đối chiếu độc lập. CloudTrail, thời điểm Lambda chạy và thời lượng phiên Learner Lab chỉ chứng minh một số sự kiện kỹ thuật, không xác minh được tổng giờ học của sinh viên.

Tổng 11 giờ vượt mức tối thiểu 8 giờ/tuần theo yêu cầu học phần nếu tính theo số giờ sinh viên tự xác nhận. Báo cáo phân biệt rõ phần việc của sinh viên với lệnh triển khai/kiểm thử do LLM/AI (ChatGPT) trực tiếp thực hiện như worklog ghi nhận.

## 3. Mã nguồn, dữ liệu và minh chứng

- [Worklog tuần 2](https://github.com/leminhhuy-ute/learnerlab-ops-dashboard/blob/main/tuan_2/worklog.csv)
- [Nguồn dữ liệu và giới hạn phạm vi](https://github.com/leminhhuy-ute/learnerlab-ops-dashboard/blob/main/docs/data-sources.md)
- [Mã Lambda kiểm kê](https://github.com/leminhhuy-ute/learnerlab-ops-dashboard/blob/main/tuan_2/src/lambdas/inventory-core/index.py)
- [Mã Lambda thu thập chi phí](https://github.com/leminhhuy-ute/learnerlab-ops-dashboard/blob/main/tuan_2/src/lambdas/billing-collector/index.py)
- [Mã Lambda đọc snapshot](https://github.com/leminhhuy-ute/learnerlab-ops-dashboard/blob/main/tuan_2/src/lambdas/read-api/index.py)
- [Mã Lambda cảnh báo](https://github.com/leminhhuy-ute/learnerlab-ops-dashboard/blob/main/tuan_2/src/lambdas/threshold-alert/lambda_function.py)
- [Mã giao diện dashboard](https://github.com/leminhhuy-ute/learnerlab-ops-dashboard/blob/main/tuan_2/src/dashboard/index.html)
- [Ảnh kiểm thử Lambda kiểm kê](https://github.com/leminhhuy-ute/learnerlab-ops-dashboard/blob/main/tuan_2/evidence/02-inventory.jpg)
- [Ảnh kiểm thử xác thực API](https://github.com/leminhhuy-ute/learnerlab-ops-dashboard/blob/main/tuan_2/evidence/03-api-authentication.jpg)
- [Ảnh kiểm tra bảo mật S3](https://github.com/leminhhuy-ute/learnerlab-ops-dashboard/blob/main/tuan_2/evidence/05-s3-dashboard-security.jpg)
- [Ảnh đối chiếu snapshot chi phí](https://github.com/leminhhuy-ute/learnerlab-ops-dashboard/blob/main/tuan_2/evidence/06-billing-snapshot.jpg)
- [Ảnh dashboard sau khi nạp JSON](https://github.com/leminhhuy-ute/learnerlab-ops-dashboard/blob/main/tuan_2/evidence/07-dashboard-render.jpg)
- [Ảnh kiểm thử CRUD DynamoDB](https://github.com/leminhhuy-ute/learnerlab-ops-dashboard/blob/main/tuan_2/evidence/08-dynamodb-crud.jpg)
- [Commit mã nguồn tuần 2](https://github.com/leminhhuy-ute/learnerlab-ops-dashboard/commit/6e3d034762b3ece2706a2341955364f64ec2202b)

## 4. Khai báo LLM/AI (ChatGPT)

LLM/AI (ChatGPT) hỗ trợ tham khảo tài liệu và biên soạn tài liệu. Theo worklog, ChatGPT trực tiếp soạn/triển khai một số mã Lambda, tạo tài nguyên AWS và chạy các lệnh kiểm thử đã liệt kê. Sinh viên xác nhận phạm vi, thời lượng theo ngày và thao tác xác nhận subscription email SNS. Số giờ sinh viên tự xác nhận không bao gồm thời gian ChatGPT thao tác.

[Báo cáo tuần 2](https://github.com/leminhhuy-ute/learnerlab-ops-dashboard/blob/main/tuan_2/README.md) · [Kế hoạch tuần 3](https://github.com/leminhhuy-ute/learnerlab-ops-dashboard/blob/main/tuan_2/docs/09-week3-plan.md).
