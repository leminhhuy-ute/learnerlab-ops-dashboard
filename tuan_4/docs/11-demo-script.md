# Kịch bản và lời thoại demo Learner Lab Ops Dashboard

**Sinh viên:** Lê Minh Huy — MSSV 24110019. **Thời lượng:** khoảng 9 phút, có khoảng đệm để tổng video không vượt 10 phút.

Kịch bản dùng cho video nộp riêng. Phần thao tác API và dashboard có thể quay trực tiếp khi Lab Ready. Hai nhánh SNS được trình bày bằng kết quả AWS đã lưu ngày 23/10/2026; nếu chỉ mở lại biên bản thì phải nói rõ đây là lần kiểm thử đã thực hiện, không gọi đó là email vừa gửi trong video.

## Chuẩn bị trước buổi quay

1. Mở Learner Lab, Start Lab đến Ready, mở AWS Console tại `us-east-1`. Kiểm tra phiên đăng nhập trước khi bật quay.
2. Mở sẵn repo, sơ đồ hệ thống, CloudFormation, Lambda read-api, DynamoDB, CloudShell, dashboard, SNS và CloudWatch. Đăng nhập và thời gian chờ trang không cần đưa vào video.
3. Trong CloudShell dạng trang đầy đủ, tải [chuan_bi_demo.py](../scripts/chuan_bi_demo.py) về máy rồi dùng **Actions → Upload file** để đưa vào home của CloudShell. Script chỉ đọc API và mốc snapshot, ghi tệp riêng trên ổ đĩa CloudShell; không sửa tài nguyên, không gọi Cost Explorer và không gửi SNS.
4. Chạy trước khi quay:

   ```bash
   python3 ~/chuan_bi_demo.py --preview
   ```

5. Chọn **Actions → Download file**, tải `/home/cloudshell-user/demo-24110019/summary.json` về máy. Đường dẫn thực tế cũng được script in ra.
6. Trước khi quay, chạy `cat ~/demo-24110019/dashboard-url-private.txt`, mở URL trong tab riêng rồi dùng `clear` để xóa URL khỏi phần màn hình CloudShell. URL xem S3 có thời hạn tối đa 15 phút, còn phụ thuộc hạn phiên Lab. Giữ URL và credentials ngoài khung hình.
7. Mở `summary.json` bằng Notepad để sẵn việc sao chép. Trong Lambda `learnerlab-ops-week2-read-api`, chuẩn bị sự kiện Test riêng tư tên `demo-summary`, JSON `{}`.
8. Quay thử 10 giây và nghe lại để kiểm tra micro. Trên Windows 11 có thể dùng Snipping Tool: **Windows + Shift + R**, chọn vùng quay, bật micro, Start; khi xong bấm Stop và lưu MP4.

**Điểm cần kiểm tra ngày quay:** lượt kiểm tra AWS sáng 27/10 cho thấy snapshot vẫn được thu ngày 23/10. Nếu dữ liệu chưa được cập nhật khi quay, hãy nói rõ đây là snapshot đã lưu, không nói là dữ liệu vừa thu. Guard sản phẩm dùng mặc định 48 giờ nên snapshot cũ có thể bị từ chối đúng thiết kế. Kiểm tra lại thời điểm trước buổi quay, không sửa timestamp hoặc số liệu trong JSON.

## 0:00–0:35 Giới thiệu đề tài và repo

**Thao tác:** mở trang repo, chỉ các thư mục `tuan_1`, `tuan_2`, `tuan_3`, `tuan_4`; mở [nguồn dữ liệu](../../docs/data-sources.md).

**Lời thoại:**

> Em là Lê Minh Huy, MSSV 24110019. Đề tài của em là bảng điều khiển vận hành cho AWS Learner Lab. Hệ thống đọc trạng thái tài nguyên và chi phí ước tính từ AWS API, lưu snapshot trong DynamoDB, cung cấp API có xác thực và cảnh báo qua SNS. Repo này có mã nguồn, nhật ký và minh chứng được chia theo bốn tuần.

## 0:35–1:10 Luồng xử lý tổng thể

**Thao tác:** mở sơ đồ hệ thống, di chuột lần lượt qua EventBridge, Lambda, DynamoDB, API/dashboard và SNS.

**Lời thoại:**

> EventBridge gọi các hàm thu thập. Kết quả kiểm kê và chi phí được lưu trong DynamoDB. Read API đọc snapshot để đưa lên giao diện. Nhánh cảnh báo kiểm tra dữ liệu còn mới hay không, so sánh ngưỡng và kiểm tra người nhận SNS đã xác nhận trước khi gửi. CloudWatch theo dõi log, metric và lỗi của các hàm, lịch chạy.

## 1:10–1:45 Nền tảng tuần 1

**Thao tác:** CloudFormation → stack `learnerlab-ops-week1`, chỉ trạng thái stack và tab Resources. Có thể chỉ VPC `10.20.0.0/16`, bucket/tag nếu đã mở sẵn.

**Lời thoại:**

> Tuần 1 dựng nền tảng bằng CloudFormation, gồm VPC, hai subnet, Internet Gateway, route và bucket S3. Biên bản triển khai ghi stack có 10 tài nguyên. Dự án dùng LabRole có sẵn và gắn Project, Owner để nhận diện tài nguyên. VPC là phần nền tảng Lab; các Lambda trong luồng serverless không được cấu hình chạy qua VPC này.

Đọc trạng thái stack đang hiển thị; không khẳng định `CREATE_COMPLETE` nếu console hiện trạng thái khác.

## 1:45–2:50 Đọc snapshot trên Lambda và đối chiếu DynamoDB

**Thao tác:**

1. Lambda → `learnerlab-ops-week2-read-api` → Test → chọn `demo-summary` → bấm Test với `{}`.
2. Mở phản hồi, chỉ `status`, một hàng `inventory` có `service`, `region`, `count`, `collectedAt`; chỉ `billing` và `estimated`.
3. DynamoDB → Tables → `learnerlab-ops-week2-snapshots` → Explore table items. Chọn Query với partition key `PK=INVENTORY#EC2#us-east-1`. Mở bản ghi có thời điểm trùng hàng API vừa xem, chỉ `PK`, `SK`, `count`, `collectedAt`.

**Lời thoại:**

> Đây là kết quả Lambda đọc các snapshot đã lưu. Mỗi hàng có dịch vụ, khu vực và thời điểm thu thập để đối chiếu với DynamoDB. Phạm vi kiểm kê là năm nhóm dịch vụ trên hai khu vực, nên có mười hàng. Count bằng 0 chỉ nói rằng không tìm thấy đối tượng trong phạm vi truy vấn tại thời điểm đó; không có nghĩa toàn tài khoản không phát sinh chi phí. Dữ liệu Cost Explorer có cờ estimated nên được trình bày là ước tính.

Nếu phản hồi có `missing` hoặc `partial`, nói theo kết quả thật và kiểm tra trước khi quay lại. Không thay dữ liệu thiếu thành 0.

## 2:50–3:40 API có và không có chữ ký

**Thao tác:** trong CloudShell chạy:

```bash
python3 ~/chuan_bi_demo.py
```

Chỉ hai dòng mã HTTP quan sát được. Có thể mở API Gateway → API `qvpnt8h5yh` → route `GET /summary` để chỉ `AWS_IAM`.

**Lời thoại, dùng khi đúng kết quả trên màn hình:**

> Với cùng route, request không ký bị từ chối bằng mã 403. Request ký SigV4 được chấp nhận bằng mã 200. API vẫn dùng AWS_IAM. Script này đọc API và snapshot đã có; không gọi thêm Cost Explorer, không thay đổi tài nguyên và không gửi email.

Nếu mã HTTP khác, dừng để kiểm tra phiên hoặc cấu hình, không đọc kết quả mong đợi như kết quả thực tế.

## 3:40–5:00 Dashboard và đầu vào sai định dạng

**Thao tác:**

1. Mở JSON thật vừa tải bằng Notepad, Ctrl+A, Ctrl+C.
2. Chuyển dashboard, dán vào ô **Nạp kết quả API đã xác thực**, bấm **Hiển thị dữ liệu**.
3. Chỉ thẻ tổng, chi phí và nhãn ước tính, bảng kiểm kê, thời điểm snapshot.
4. Thay nội dung ô bằng `{invalid-json`, bấm **Hiển thị dữ liệu**; chỉ lỗi và kết quả cũ đã được xóa.
5. Dán lại JSON thật và hiển thị lại. Nếu còn thời gian, mở S3 Permissions để chỉ Block Public Access và Properties để chỉ SSE-S3.

**Lời thoại:**

> Dashboard hiện dùng JSON lấy qua API đã xác thực và nạp thủ công. Giao diện chưa tự đăng nhập hoặc tự gọi API từ trình duyệt. Ở đây có kết quả kiểm kê, thời điểm và chi phí ước tính. Khi nhập JSON sai, trang báo lỗi và xóa kết quả trước đó. Trường hợp snapshot thiếu cũng được xử lý riêng, không đổi thành số 0. Bucket vẫn chặn truy cập công khai và dùng mã hóa SSE-S3.

JSON sai ở bước 4 là đầu vào cố ý để kiểm thử giao diện, không phải dữ liệu AWS. Minh chứng trường hợp snapshot thiếu có trong [kiểm thử dashboard](../evidence/10-dashboard-regression-2026-10-23.md).

## 5:00–7:00 Cảnh báo ngưỡng và hai trạng thái SNS

**Thao tác:**

1. Lambda → `learnerlab-ops-week2-threshold-alert` → Configuration → Environment variables. Chỉ `ALERT_THRESHOLD_USD=10`; xem mã nguồn để chỉ giá trị mặc định `MAX_SNAPSHOT_AGE_HOURS=48` nếu biến này không xuất hiện trong môi trường. Không sửa cấu hình.
2. SNS → topic `learnerlab-ops-week2-alerts` → Subscriptions, chỉ người nhận đã xác nhận nếu console hiện đúng như vậy.
3. Mở [biên bản SNS ngày 23/10](../evidence/08-sns-replay-2026-10-23.md). Cuộn đến kết quả trước và sau xác nhận cùng ảnh.
4. Nếu mở email đã nhận, chuẩn bị sẵn đúng email cảnh báo để chỉ nội dung cần thiết, không quay cả hộp thư.

**Lời thoại:**

> Hàm sản phẩm giữ ngưỡng 10 USD và tuổi snapshot tối đa 48 giờ. Theo gợi ý của thầy, ngày 23/10 đã có phép thử trên Lambda và topic riêng. Khi chi phí vượt ngưỡng thử nhưng subscription chưa xác nhận, kết quả là sns_subscription_pending_confirmation và published bằng false; hàm dừng trước Publish nên không có MessageId. Sau khi người nhận xác nhận, hàm trả alert_published, published bằng true và SNS cấp MessageId. Em cũng đã xác nhận nhận email của phép thử này.

> Phép thử dùng nguyên snapshot thật ngày 13/10, với ngưỡng thấp và cửa sổ thời gian riêng trên hàm thử. Đây là replay dữ liệu lịch sử, không phải chi phí hiện tại vừa vượt ngưỡng. Cấu hình sản phẩm không bị hạ ngưỡng. Sau phép thử, cấu hình thử được khôi phục và bảng replay đã xóa.

Không bấm Test tùy ý rồi chờ tái hiện kết quả cũ: bảng replay đã dọn. Cửa sổ thử 336 giờ là cấu hình dùng trong lần kiểm tra ngày 23/10, không bảo đảm snapshot 13/10 vẫn nằm trong cửa sổ đó ở ngày quay sau này. Nếu quay lại phép thử gửi email thật, phải chuẩn bị điều kiện riêng và kiểm tra dữ liệu/thời gian thực tế; không sửa timestamp hoặc hạ ngưỡng sản phẩm. Cờ `{"test":true}` kiểm tra tích hợp SNS riêng, không chứng minh nhánh so sánh ngưỡng đã chạy.

## 7:00–8:05 Giám sát và lịch chạy

**Thao tác:** CloudWatch → Alarms, lọc `learnerlab-ops`; chỉ các alarm sản phẩm đang có. EventBridge → Rules, lọc cùng prefix để chỉ các lịch. Nếu cần minh họa lịch sử chuyển trạng thái, mở [biên bản thử lỗi tuần 3](../../tuan_3/evidence/09-api-and-alarm-live-tests.md).

**Lời thoại:**

> CloudWatch theo dõi lỗi của Lambda và FailedInvocations của các lịch EventBridge. Lần rà soát ngày 23/10 ghi nhận bốn alarm sản phẩm và ba lịch đang bật. Hiện em đối chiếu lại trạng thái đang hiển thị trên console. Trạng thái OK hoặc ENABLED không tự chứng minh lịch đã chạy thành công. Lịch sử alarm chuyển sang In alarm rồi về OK trong phép thử lỗi có kiểm soát được lưu ở minh chứng tuần 3. Alarm hiện chưa gắn hành động email; cảnh báo chi phí được Lambda gửi qua SNS.

Không tìm alarm thử đã bị dọn ngày 22/10 rồi coi việc không thấy nó là lỗi triển khai; dùng biên bản đã lưu để trình bày lịch sử.

## 8:05–9:10 Tổng hợp kiểm thử, giới hạn và kết thúc

**Thao tác:** mở [rà soát cuối trên AWS ngày 23/10](../evidence/12-final-review-2026-10-23.md), sau đó [đối chiếu cục bộ ngày 27/10](12-completion-audit-2026-10-27.md). Chỉ liên kết mã nguồn, worklog và commit.

**Lời thoại:**

> Các chức năng và kết quả kiểm thử trên AWS được lưu trong biên bản ngày 23/10. Ngày 27/10, 12 kiểm thử cảnh báo và 4 kiểm thử hồi quy chạy cục bộ đều đạt; JavaScript của dashboard qua kiểm tra cú pháp. Lần kiểm tra AWS ngày 27/10 xác nhận API và cấu hình bảo mật, nhưng snapshot vẫn có thời điểm thu ngày 23/10. Dashboard hiện nạp JSON thủ công, chi phí là ước tính và các tài nguyên lõi được giữ đến khi hoàn tất trình bày.

> Trong quá trình thực hiện, em dùng LLM/AI ChatGPT hỗ trợ mã nguồn, kiểm thử và thao tác AWS. Phần hỗ trợ được khai riêng trong worklog. Em xin kết thúc phần demo.

## Lưu và kiểm tra video

- Lưu tên `Demo_LearnerLab_Ops_24110019.mp4`, giữ tổng thời lượng không quá 10 phút.
- Xem lại một lượt: nghe rõ giọng, đọc được kết quả, thao tác đúng thứ tự; không để credentials hoặc URL ký tạm lọt vào khung hình.
- Không nói “vừa chạy trên AWS” khi đang xem ảnh/biên bản cũ. Đọc số liệu và trạng thái theo lần quay thực tế.
- Sau khi quay xong, rà soát tài nguyên còn cần giữ và thực hiện việc dọn theo phạm vi đã xác định; đây là bước bàn giao còn lại, không ghi là đã hoàn tất trước khi thực hiện.
