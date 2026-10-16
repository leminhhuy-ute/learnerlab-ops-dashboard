# Tuần 1 — Tìm hiểu dịch vụ và chốt yêu cầu

Ngày chuẩn bị: 07/10/2026 (Asia/Ho_Chi_Minh). Tài liệu này là thiết kế và hướng dẫn học; chưa phải minh chứng đã triển khai thành công trên AWS.

Thành viên đã xác nhận: **Lê Minh Huy — MSSV 24110019** (tối thiểu 8 giờ/tuần). Cấu hình dự án: `Project=learnerlab-ops`, `Owner=24110019`, triển khai `us-east-1`, kiểm kê hai vùng được phép. Nền tảng VPC/S3 đã triển khai thật trên tài khoản Learner Lab `213858341631` ngày 08/10/2026; quyền của các dịch vụ pipeline tuần 2–3 chưa được xác minh. Xem [biên bản AWS](07-deployment-record.md).

## 1. Mục tiêu và phạm vi

Xây dựng dashboard giúp sinh viên biết tài nguyên nào đang hoạt động, chi phí billing đã ghi nhận đến thời điểm gần nhất và các cảnh báo cần xử lý trong AWS Learner Lab.

Đầu ra tuần 1: bản yêu cầu, bảng dịch vụ, sơ đồ kiến trúc, quyết định thiết kế, kiểm tra quyền của phiên Learner Lab, nền tảng S3/VPC phù hợp, quy ước tag và nhật ký công việc. Lambda thu thập dữ liệu, API, biểu đồ và SNS hoạt động đầy đủ thuộc tuần 2–3.

Các giới hạn dưới đây lấy từ ảnh đề bài do người dùng cung cấp. Chúng là yêu cầu của bài tập, không phải quota mặc định của AWS:

| Ràng buộc | Cách áp dụng trong dự án |
|---|---|
| Tối đa 2 sinh viên, mỗi người ≥ 8 giờ/tuần; thời gian 4 tuần | Nhật ký ghi người thực hiện, công việc, thời gian thực tế, sản phẩm/minh chứng |
| Chỉ `us-east-1` và `us-west-2` | Đặt vùng triển khai chính `us-east-1`; kiểm kê hai vùng, không triển khai ở vùng khác |
| Dùng `LabRole` / `LabInstanceProfile`; không tạo IAM user/role | Xác minh ARN role có sẵn, dùng role đó khi tạo Lambda; không sửa trust policy để né giới hạn |
| EC2 nano → large; ≤ 9 instance và ≤ 32 vCPU đồng thời mỗi Region | Dashboard ghi trạng thái và số lượng; kiểm tra cả loại máy và tổng vCPU khi thử nghiệm |
| EBS ≤ 100 GB, chỉ gp2/gp3 | Kiểm kê EBS và trạng thái volume; không tự tạo volume cho dashboard |
| Tag `Project` và `Owner` | Tag các tài nguyên do nhóm tạo; không đổi tag tài nguyên của nhóm khác |
| Dừng/xóa tài nguyên sau mỗi buổi | Tắt lịch thu thập khi không dùng; kiểm tra tài nguyên còn tính phí trước khi kết thúc phiên |
| Hạ tầng và demo phải chạy thật trên Learner Lab | Dữ liệu mẫu chỉ dùng để phát triển; ghi nhãn rõ và không dùng làm minh chứng triển khai |
| Cho phép AI hỗ trợ nhưng sinh viên phải giải thích mã/cấu hình | Worklog và báo cáo ghi phần được AI hỗ trợ; tự kiểm tra và diễn giải lại |
| Minh chứng có Account ID, Region, thời gian; mã/template trên Git | Lưu ảnh console/CLI thực tế, sơ đồ, báo cáo, video demo ≤ 10 phút |

## 2. Dịch vụ phải hiểu

| Dịch vụ | Nhiệm vụ trong hệ thống | Nội dung học và kết quả cần kiểm tra |
|---|---|---|
| AWS Lambda | Chạy collector tài nguyên, collector billing, API đọc và authorizer | Handler/event, execution role, timeout, environment variable, log, lỗi từng nguồn; dùng `LabRole` có sẵn |
| Amazon EventBridge | Kích hoạt collector theo lịch | Hai lịch độc lập: kiểm kê 15 phút/lần, billing 2 lần/ngày; dùng scheduled rule và permission của Lambda |
| Amazon DynamoDB | Lưu snapshot, trạng thái nguồn và trạng thái cảnh báo | Khóa partition/sort, Query thay vì Scan, on-demand, thời gian thu thập và TTL |
| Amazon API Gateway HTTP API | Cung cấp JSON cho dashboard | Route GET, Lambda integration, CORS chính xác, authorizer; không kích hoạt collector từ thao tác tải trang |
| Amazon S3 | Lưu frontend tĩnh và artifact tuần 1 | Bucket private, Block Public Access, mã hóa mặc định, tag, upload/download, URL HTTPS tạm thời |
| AWS Cost Explorer | Lấy dữ liệu chi phí billing theo ngày/dịch vụ | Quyền `ce:GetCostAndUsage`, khoảng ngày, phân trang, dữ liệu trễ, chi phí API và giới hạn số request |
| Amazon SNS | Gửi cảnh báo vượt ngưỡng | Standard topic, Publish, email subscription và xác nhận của người nhận |
| Amazon CloudWatch | Theo dõi Lambda và lỗi vận hành | Log có request ID/status/duration; không ghi secret/token; đặt retention và theo dõi Errors/Throttles |
| VPC / IAM | Nền tảng mạng và quyền | Collector đọc AWS API không cần vào VPC của tài khoản; xem quyền thực tế của `LabRole`, không giả định được toàn quyền |

DynamoDB on-demand tính phí theo request, vẫn có chi phí lưu trữ. Đây là lựa chọn thiết kế cho lưu lượng demo nhỏ, không phải cam kết miễn phí. TTL xóa bất đồng bộ, nên API phải loại item hết hạn khỏi kết quả thay vì chờ dữ liệu biến mất. [On-demand capacity](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/on-demand-capacity-mode.html), [DynamoDB TTL](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html).

Scheduled rule được AWS gọi là cơ chế legacy. Dự án chọn nó vì có thể gọi Lambda bằng resource policy mà không tạo execution role mới; EventBridge Scheduler cần execution role phù hợp. Cần kiểm tra quyền tạo rule và `lambda:AddPermission` trong lab. [Scheduled rules](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-create-rule-schedule.html), [Target resource policies](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-use-resource-based.html), [Scheduler execution role](https://docs.aws.amazon.com/lambda/latest/dg/with-eventbridge-scheduler.html).

Email chỉ nhận được cảnh báo sau khi người nhận xác nhận subscription. Tuần 1 chuẩn bị địa chỉ người nhận và ngưỡng, chưa gửi email cảnh báo thật. [SNS email subscriptions](https://docs.aws.amazon.com/sns/latest/dg/sns-email-notifications.html).

## 3. Tài nguyên cần kiểm kê

Các API đều phải đọc hết các trang. Lỗi của một dịch vụ/vùng không được làm mất snapshot của những nguồn đã đọc thành công.

| Nguồn | API/nhóm API dự kiến | Dữ liệu hiển thị tối thiểu | Giới hạn phải giải thích |
|---|---|---|---|
| EC2 | `DescribeInstances`, `DescribeVolumes`, `DescribeInstanceTypes` | ID, Region, instance type, state, vCPU, Project/Owner; EBS loại/dung lượng/trạng thái | EC2 stopped không đồng nghĩa toàn bộ chi phí đã dừng; volume còn tồn tại cần được kiểm tra riêng |
| RDS | `DescribeDBInstances`, thêm `DescribeDBClusters` để đủ phạm vi đã chốt | ID, engine, class, status, storage, Region | Không đăng nhập database; phân biệt DB instance và cluster, không cộng chi phí trùng |
| SageMaker | `ListNotebookInstances`, `ListEndpoints`, `ListTrainingJobs`; xem xét `ListApps` cho Studio | Nhóm tài nguyên, tên, trạng thái, loại máy nếu API trả về, Region | Notebook không đại diện toàn bộ SageMaker. Mỗi adapter phải có trạng thái riêng; Studio/app thiếu quyền hiển thị chưa khả dụng |
| EKS | `ListClusters`, `DescribeCluster`; nodegroup nếu cần và được phép | Tên cluster, status, version, Region | Đây là kiểm kê control plane. Không cần truy cập Kubernetes API; worker EC2 đã được tính trong EC2 |
| Billing | `GetCostAndUsage`, `Granularity=DAILY`, metric `UnblendedCost`, group `SERVICE` | Tổng tháng, chuỗi theo ngày/dịch vụ, unit, Estimated, collectedAt, phạm vi ngày | Không coi là dữ liệu thời gian thực hoặc hóa đơn cuối cùng |

EC2 API có eventual consistency và yêu cầu xử lý phân trang; instance vừa terminated có thể còn xuất hiện tạm thời. [DescribeInstances](https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeInstances.html). RDS `DescribeDBInstances` cũng có phân trang và có thể trả cả Neptune/DocumentDB; adapter cần giới hạn engine/phạm vi hỗ trợ. [DescribeDBInstances](https://docs.aws.amazon.com/AmazonRDS/latest/APIReference/API_DescribeDBInstances.html).

Notebook API trả các instance trong từng Region. EKS cần `ListClusters` rồi `DescribeCluster`; không lấy certificate/endpoint rồi suy ra quyền truy cập Kubernetes. [ListNotebookInstances](https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_ListNotebookInstances.html), [ListClusters](https://docs.aws.amazon.com/eks/latest/APIReference/API_ListClusters.html), [DescribeCluster](https://docs.aws.amazon.com/eks/latest/APIReference/API_DescribeCluster.html).

## 4. Hai loại số liệu chi phí

**Billing đã ghi nhận:** Cost Explorer cập nhật ít nhất mỗi 24 giờ, có thể trễ hơn. Đánh dấu thời điểm lấy dữ liệu và cờ `Estimated`; dữ liệu chưa ổn định không được gọi là hóa đơn đã chốt. Mỗi request có phân trang tính phí 0,01 USD. [Cost Explorer overview](https://docs.aws.amazon.com/cost-management/latest/userguide/ce-what-is.html).

**Ước tính từ tài nguyên:** tùy chọn giai đoạn sau, tính từ loại tài nguyên, thời gian quan sát và bảng giá đã xác minh theo Region. Gắn nhãn “ước tính”, ghi phạm vi bao phủ; không cộng số này vào tổng billing. Snapshot 15 phút chỉ cho biết trạng thái tại thời điểm lấy, không xác định chính xác thời lượng chạy giữa hai snapshot. Nếu thiếu giá hoặc nguồn dữ liệu, trả `null`/“chưa đủ dữ liệu”, không trả 0 USD.

Không suy ra số tiền Learner Lab còn lại từ Cost Explorer. Ngân sách/credit và thời gian phiên hiển thị trong cổng Learner Lab cần ghi nhận riêng; API billing có thể bị giới hạn trong tài khoản đào tạo.

Thiết kế billing: 2 lượt/ngày, tối đa **4 HTTP request Cost Explorer thực tế/ngày UTC**, bao gồm trang tiếp theo và retry. Dùng counter/lock bền vững trong DynamoDB trước khi gọi, không chỉ đếm invocation Lambda. Khi hết ngân sách request mà còn trang, đánh dấu `partial`, giữ snapshot thành công cũ và ngừng gọi. Nhịp này tối đa 1,12 USD cho 28 ngày chỉ cho CE API, chưa gồm các dịch vụ khác; đây là trần tính theo thiết kế, không phải báo giá toàn dự án.

Frontend chỉ đọc snapshot; bấm refresh hoặc mở nhiều tab không được gọi Cost Explorer. `GetCostAndUsage` sử dụng mốc Start bao gồm và End không bao gồm; adapter lưu nguyên khoảng truy vấn và unit. [GetCostAndUsage](https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_GetCostAndUsage.html).

## 5. Quyền, mạng và an toàn dữ liệu

Phiên CLI dùng credentials tạm thời từ Learner Lab ở môi trường người dùng hoặc profile cục bộ đã được cấu hình. Không chép access key/secret/session token vào Git, HTML, ảnh minh chứng hoặc worklog. `LabInstanceProfile` chỉ cần nếu sau này thật sự dùng EC2; dashboard serverless không cần tạo EC2.

Chỉ kiểm tra quyền đang có của `LabRole`. Không tạo IAM user/role, không tự gắn policy mới vào role hoặc sửa trust policy. `AccessDenied` phải được lưu thành nguồn chưa khả dụng, báo trong báo cáo và trao đổi với giảng viên về phạm vi cho phép.

Lambda đọc metadata qua AWS service API, không kết nối SQL/Kubernetes private endpoint. Vì vậy chọn Lambda **không gắn VPC của tài khoản**. Gắn Lambda vào public subnet không tự cho internet; gắn VPC có thể cần NAT/endpoint và quyền mạng bổ sung. [Lambda VPC internet access](https://docs.aws.amazon.com/lambda/latest/dg/configuration-vpc-internet.html).

Nếu bài tập yêu cầu minh chứng VPC: xem default VPC hoặc tạo VPC nền tảng có tag trong vùng chính. Template nền tảng dự kiến có hai subnet, route tới Internet Gateway, tắt tự cấp public IPv4; không NAT Gateway, không Elastic IP, không EC2, RDS, SageMaker endpoint hoặc EKS để phục vụ dashboard. Đây là bài học mạng riêng; không phải dependency của Lambda collector.

S3 website endpoint chỉ hỗ trợ HTTP và nội dung public. Dashboard có thông tin vận hành không nên truyền token bằng trang HTTP. Thiết kế demo chính dùng bucket private và frontend HTML tự chứa qua presigned URL HTTPS; URL có thể hết hạn sớm khi credentials của phiên lab hết hạn. [S3 website endpoints](https://docs.aws.amazon.com/AmazonS3/latest/userguide/WebsiteEndpoints.html), [Presigned URLs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-presigned-url.html).

## 6. Yêu cầu chức năng và tiêu chí nghiệm thu

| Mã | Yêu cầu | Điều kiện kiểm tra ở tuần 2–4 |
|---|---|---|
| F01 | Danh sách EC2, RDS, SageMaker, EKS theo hai Region | Đối chiếu API/console thực tế, gồm trường hợp không có tài nguyên |
| F02 | Phân biệt thành công, lỗi quyền và dữ liệu cũ | Nguồn `unavailable` không có số lượng/chi phí giả bằng 0; có collectedAt và trạng thái |
| F03 | Chi phí tháng và biểu đồ ngày/dịch vụ | Nhãn billing, đơn vị tiền, khoảng dữ liệu, Estimated; cache độc lập với inventory |
| F04 | SNS khi vượt ngưỡng | Email đã xác nhận; có mã sự kiện và tránh gửi lặp trong mỗi chu kỳ thu thập |
| F05 | Tag và nhận diện tài nguyên do nhóm tạo | Project/Owner xuất hiện trong metadata và minh chứng |
| N01 | API bảo vệ trước khi trả dữ liệu thật | Thiếu/sai/hết hạn token bị từ chối; token không nằm trong frontend/Git/log |
| N02 | Khống chế chi phí collector | Mở trang nhiều lần không tăng request CE; thử phân trang/retry không vượt cap ngày |
| N03 | Không tự dừng/xóa tài nguyên được kiểm kê | Dashboard đọc và cảnh báo; cleanup chỉ áp dụng tài nguyên của nhóm theo manifest |
| N04 | Hệ thống giải thích được | Sinh viên diễn giải luồng dữ liệu, quyền, lỗi, chi phí, giới hạn lab và phần AI hỗ trợ |

## 7. Quyết định còn cần dữ liệu thật

- ARN và quyền thực tế của `LabRole`; quyền read từng dịch vụ, CE, tạo S3/VPC, Lambda và resource permission.
- CE đã có dữ liệu và được phép truy cập trong lab hay chưa. Không tự bật dịch vụ hoặc đổi IAM để vượt hạn chế.
- Ngân sách/tháng, ngưỡng cảnh báo và email của người nhận; Project/Owner và người thực hiện đã chốt ở đầu tài liệu.
- Phạm vi SageMaker Studio/endpoint/training jobs và RDS clusters theo tài nguyên thật/quyền lab.
- Có yêu cầu bắt buộc public website endpoint hay không. Nếu có, thống nhất HTTPS frontend bằng CloudFront/private S3 khi lab cho phép; nếu không được, cần giảng viên chấp nhận demo HTTPS tạm thời trên S3. Không mặc định bỏ xác thực để đạt URL public.
- Chính sách giữ tài nguyên giữa các buổi và thời gian lưu snapshot/minh chứng; chỉ tick hoàn thành phần AWS sau khi có output/ảnh thực tế.
