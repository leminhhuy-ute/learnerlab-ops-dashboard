# Kết quả kiểm tra cục bộ

Ngày: 07/10/2026. **Không có thao tác AWS thật trong các kiểm tra dưới đây.**

| Kiểm tra | Kết quả |
|---|---|
| Đọc YAML và kiểm tra 10 tài nguyên nền tảng | PASS |
| Chỉ hai Region us-east-1/us-west-2; Owner bắt buộc; tag tài nguyên hỗ trợ tag | PASS |
| CIDR/subnet không chồng lấn; route IGW; auto public IPv4 tắt | PASS |
| S3 mã hóa, riêng tư, Retain; không tự hết hạn object người dùng | PASS |
| Không tạo compute/NAT/EIP/IAM user/role | PASS |
| PowerShell parser cho check-aws-session.ps1/deploy-week1.ps1 | PASS, 0 lỗi cú pháp |
| Validator từ chối sáu cấu hình sai: public S3, Region thừa, thiếu Owner, subnet chồng lấn, IAM role mới, expiration object | PASS |
| Thiếu CLI/vùng không được phép bị từ chối trước khi triển khai | PASS |
| Mock CLI: đường xem change set và triển khai, chuyển tham số/tag, kiểm tra S3 sau triển khai | PASS — mô phỏng, không gọi AWS |
| Sơ đồ PNG đã được mở và kiểm tra bố cục | PASS |

Đây là bảng kiểm tra **cục bộ ngày 07/10**, trước triển khai. AWS ValidateTemplate, LabRole, CloudFormation `CREATE_COMPLETE` và VPC/S3 thật sau đó đã được xác minh ngày 08/10; xem [biên bản AWS](07-deployment-record.md). Cost Explorer và các API nguồn của pipeline tuần 2–3 chưa được kiểm tra. Phần việc sinh viên xác nhận được ghi riêng ở [worklog](worklog.csv); giờ cá nhân chưa có chứng cứ thời gian để điền.

Lặp lại kiểm tra cấu hình cục bộ:

```powershell
python .\scripts\validate_week1.py
```
