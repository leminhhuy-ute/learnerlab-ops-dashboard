# Phân công và thời lượng tuần 3

**Sinh viên:** Lê Minh Huy — MSSV 24110019

**Mã học phần:** CLCO332779

**Đề tài:** Bảng điều khiển vận hành cho AWS Learner Lab

## 1. Phân công

Nhóm có một sinh viên. Lê Minh Huy xác nhận phạm vi công việc và thời lượng của mình, yêu cầu triển khai các hạng mục tuần 3, đồng ý dùng email trường để kiểm thử trường hợp SNS subscription chưa xác nhận và theo dõi kết quả. Sinh viên cho biết đã tìm hiểu tài liệu liên quan đến đề tài ngoài hệ thống vào ngày 19 và 20/10. Chưa có bản ghi chi tiết để phân bổ 3 giờ làm dự án mỗi ngày cho từng chức năng.

LLM/AI (ChatGPT) hỗ trợ soạn mã, kiểm thử và tài liệu. Những thao tác AWS do ChatGPT trực tiếp thực hiện được ghi riêng trong [worklog](../worklog.csv), không tính thành giờ sinh viên. Kết quả kỹ thuật, phép thử và giới hạn thực tế được trình bày trong [README tuần 3](../README.md) cùng các file minh chứng tại thư mục [evidence](../evidence/).

## 2. Thời lượng sinh viên xác nhận

| Ngày | Làm dự án tuần 3 | Tìm hiểu ngoài hệ thống | Tổng ngày |
|---|---:|---:|---:|
| 19/10/2026 | 3 giờ | 1 giờ | 4 giờ |
| 20/10/2026 | 3 giờ | 1 giờ | 4 giờ |
| **Tổng tuần 3** | **6 giờ** | **2 giờ** | **8 giờ** |

Số giờ là thông tin sinh viên tự xác nhận; phần 2 giờ tìm hiểu ngoài hệ thống được xác nhận bổ sung ngày 21/10/2026. Worklog không có mốc bắt đầu/kết thúc, bảng chấm công hay minh chứng độc lập cho thời lượng này. Thời điểm trên AWS và Git dùng để đối chiếu sự kiện kỹ thuật, không dùng để suy ra giờ làm của sinh viên.

## 3. Kết quả liên quan

- [Mã Lambda kiểm tra ngưỡng, SNS subscription và độ mới snapshot](../src/threshold-alert/lambda_function.py)
- [Kiểm thử đơn vị 12/12](../tests/test_threshold_alert.py)
- [Kiểm thử SNS subscription chưa xác nhận](../evidence/01-live-sns-check.md)
- [Triển khai freshness guard trên AWS](../evidence/05-live-freshness-guard.md)
- [Kiểm thử API và CloudWatch alarm](../evidence/09-api-and-alarm-live-tests.md)

Các link trên chứng minh mã và kết quả kiểm thử được ghi nhận; chúng không xác minh số giờ sinh viên học hoặc thao tác.
