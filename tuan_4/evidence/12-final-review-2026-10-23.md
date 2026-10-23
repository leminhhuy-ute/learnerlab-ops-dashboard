# Rà soát cuối tuần 4 — 23/10/2026

## Phạm vi đã kiểm tra

| Hạng mục | Kết quả | Minh chứng |
|---|---|---|
| Mã cảnh báo và read-api | 16/16 unit tests đạt; bản sửa đọc bảng rỗng đã chạy trên Lambda AWS thật | [Triển khai và hồi quy](06-read-api-deployment-2026-10-23.md) |
| Luồng inventory/billing → DynamoDB → API | Snapshot mới 23/10; API 200 với SigV4, 403 khi không ký; 10/10 dòng và billing khớp DynamoDB | [Kết quả luồng dữ liệu](06-read-api-deployment-2026-10-23.md) |
| Giao diện S3 | Khớp JSON thật; xử lý missing và JSON lỗi đạt | [Ba phép thử giao diện và ảnh](10-dashboard-regression-2026-10-23.md) |
| Chi phí và tài nguyên | Đã rà soát hai Region, bổ sung tag thiếu; buổi cuối gọi collector billing thêm một lần | [Rà soát 22/10](02-cost-resource-review-2026-10-22.md) |
| Bảo mật | Hai bucket chặn công khai, SSE-S3, không ACL public; route AWS_IAM; 6 Lambda dùng LabRole, không Function URL | Kết quả rà soát chỉ đọc bên dưới |
| Giám sát/lịch | Bốn alarm sản phẩm tồn tại; ba rule ENABLED; test Lambda không có rule hay event source mapping | Kết quả rà soát chỉ đọc bên dưới |
| Dọn dẹp | Alarm thử đã lưu rồi dọn ngày 22/10; Lambda/bảng/log rỗng dùng một lần đã dọn ngày 23/10 | [Lưu alarm thử](04-test-alarm-archive-2026-10-22.md), [dọn test rỗng](06-read-api-deployment-2026-10-23.md) |
| Phân công/thời lượng | 23/10 thêm 3 giờ, tổng 10 giờ tuần 4; phần AI khai riêng | [Phân công và thời lượng](../docs/10-week4-assignment-and-time.md), [worklog CSV](../worklog.csv) |

## Cảnh báo SNS nâng cao

Nhánh PendingConfirmation đã đạt; nhánh gửi sau xác nhận còn chờ người nhận bấm liên kết xác nhận email. Bảng replay và Lambda thử đang được giữ tạm để tiếp tục. Chưa ghi hoàn thành 100% toàn bộ checklist kỹ thuật. Xem [điều kiện và kết quả SNS](08-sns-replay-2026-10-23.md).

## Giới hạn và tài nguyên giữ lại

- Số Cost Explorer có thể trễ và đang `estimated=true`; snapshot mới không phải hóa đơn cuối kỳ. Không lấy dữ liệu lịch sử 13/10 làm chi phí hiện tại.
- Trạng thái alarm `OK` và rule `ENABLED` không chứng minh lịch đã tự chạy; phép thử luồng 23/10 là gọi Lambda trực tiếp có kiểm soát. Bốn alarm hiện không gắn AlarmActions gửi email; cảnh báo chi phí do Lambda phát SNS riêng.
- Bucket/API tiếp tục được bảo vệ. Trình duyệt dùng JSON đã xác thực nạp thủ công; chưa có đăng nhập và tự gọi API.
- Giữ nền tảng, dữ liệu, Lambda/API/S3, lịch và alarm sản phẩm cho video demo. Topic/Lambda thử và log retention 7 ngày được giữ để trình bày hai nhánh SNS. Giữ tài nguyên có thể còn phát sinh chi phí; dọn phần lõi sau khi quay demo và hoàn tất bàn giao.
- **Video demo thực tế (tối đa 10 phút) làm sau. Báo cáo Word là báo cáo tổng kết toàn bộ dự án 4 tuần, thực hiện ở bước tiếp theo; không tạo Word/PDF tuần 4 trong buổi này.** Không ghi hai sản phẩm này là đã nộp hoặc đã hoàn tất.

Nguồn script: [review_security.py](../scripts/review_security.py), chỉ đọc các trường cần kiểm tra. Thời điểm và cấu hình thực tế nằm dưới đây; địa chỉ email, tiền, credentials và URL ký tạm không được đưa vào repo.


<details>
<summary>Kết quả lệnh đã lưu (chỉ các trường công khai)</summary>

```json
{
  "security-final.json": {
    "checkedAtUtc": "2026-10-23T00:56:47.157640+00:00",
    "account": "213858341631",
    "buckets": [
      {
        "name": "learnerlab-ops-week1-artifactbucket-u4t7cql7ngfo",
        "region": "us-east-1",
        "publicAccessBlock": {
          "BlockPublicAcls": true,
          "IgnorePublicAcls": true,
          "BlockPublicPolicy": true,
          "RestrictPublicBuckets": true
        },
        "encryption": [
          "AES256"
        ],
        "isPublicPolicy": false,
        "hasBucketPolicy": false,
        "publicAclGrantCount": 0,
        "tags": {
          "Project": "learnerlab-ops",
          "Owner": "24110019",
          "Environment": "learner-lab"
        }
      },
      {
        "name": "learnerlab-ops-week2-dashboard-213858341631",
        "region": "us-east-1",
        "publicAccessBlock": {
          "BlockPublicAcls": true,
          "IgnorePublicAcls": true,
          "BlockPublicPolicy": true,
          "RestrictPublicBuckets": true
        },
        "encryption": [
          "AES256"
        ],
        "isPublicPolicy": false,
        "hasBucketPolicy": false,
        "publicAclGrantCount": 0,
        "tags": {
          "Project": "learnerlab-ops",
          "Environment": "learner-lab",
          "Owner": "24110019"
        }
      }
    ],
    "apiRoutes": [
      {
        "RouteKey": "GET /summary",
        "AuthorizationType": "AWS_IAM",
        "Target": "integrations/gr1j2oa"
      }
    ],
    "apiStages": [
      {
        "StageName": "$default",
        "AutoDeploy": true
      }
    ],
    "functions": [
      {
        "name": "learnerlab-ops-week2-billing-collector",
        "role": "LabRole",
        "functionUrlCount": 0,
        "functionUrlAuthTypes": [],
        "invokePolicy": [
          {
            "Effect": "Allow",
            "Principal": {
              "Service": "events.amazonaws.com"
            },
            "Action": "lambda:InvokeFunction",
            "Condition": {
              "ArnLike": {
                "AWS:SourceArn": "arn:aws:events:us-east-1:213858341631:rule/learnerlab-ops-week2-billing-daily"
              }
            }
          }
        ]
      },
      {
        "name": "learnerlab-ops-week2-read-api",
        "role": "LabRole",
        "functionUrlCount": 0,
        "functionUrlAuthTypes": [],
        "invokePolicy": [
          {
            "Effect": "Allow",
            "Principal": {
              "Service": "apigateway.amazonaws.com"
            },
            "Action": "lambda:InvokeFunction",
            "Condition": {
              "ArnLike": {
                "AWS:SourceArn": "arn:aws:execute-api:us-east-1:213858341631:qvpnt8h5yh/*/GET/summary"
              }
            }
          }
        ]
      },
      {
        "name": "learnerlab-ops-week2-ec2-collector",
        "role": "LabRole",
        "functionUrlCount": 0,
        "functionUrlAuthTypes": [],
        "invokePolicy": []
      },
      {
        "name": "learnerlab-ops-week2-inventory-core",
        "role": "LabRole",
        "functionUrlCount": 0,
        "functionUrlAuthTypes": [],
        "invokePolicy": [
          {
            "Effect": "Allow",
            "Principal": {
              "Service": "events.amazonaws.com"
            },
            "Action": "lambda:InvokeFunction",
            "Condition": {
              "ArnLike": {
                "AWS:SourceArn": "arn:aws:events:us-east-1:213858341631:rule/learnerlab-ops-week2-inventory-6h"
              }
            }
          }
        ]
      },
      {
        "name": "learnerlab-ops-week3-threshold-negative-test",
        "role": "LabRole",
        "functionUrlCount": 0,
        "functionUrlAuthTypes": [],
        "invokePolicy": []
      },
      {
        "name": "learnerlab-ops-week2-threshold-alert",
        "role": "LabRole",
        "functionUrlCount": 0,
        "functionUrlAuthTypes": [],
        "invokePolicy": [
          {
            "Effect": "Allow",
            "Principal": {
              "Service": "events.amazonaws.com"
            },
            "Action": "lambda:InvokeFunction",
            "Condition": {
              "ArnLike": {
                "AWS:SourceArn": "arn:aws:events:us-east-1:213858341631:rule/learnerlab-ops-week2-alert-daily"
              }
            }
          }
        ]
      }
    ],
    "rules": [
      {
        "name": "learnerlab-ops-week2-alert-daily",
        "state": "ENABLED",
        "targetArns": [
          "arn:aws:lambda:us-east-1:213858341631:function:learnerlab-ops-week2-threshold-alert"
        ]
      },
      {
        "name": "learnerlab-ops-week2-billing-daily",
        "state": "ENABLED",
        "targetArns": [
          "arn:aws:lambda:us-east-1:213858341631:function:learnerlab-ops-week2-billing-collector"
        ]
      },
      {
        "name": "learnerlab-ops-week2-inventory-6h",
        "state": "ENABLED",
        "targetArns": [
          "arn:aws:lambda:us-east-1:213858341631:function:learnerlab-ops-week2-inventory-core"
        ]
      }
    ],
    "testEventSourceMappings": [],
    "topics": [
      {
        "name": "learnerlab-ops-week2-alerts",
        "confirmed": 1,
        "pending": 0,
        "policy": [
          {
            "Effect": "Allow",
            "Principal": {
              "AWS": "*"
            },
            "Action": [
              "SNS:GetTopicAttributes",
              "SNS:SetTopicAttributes",
              "SNS:AddPermission",
              "SNS:RemovePermission",
              "SNS:DeleteTopic",
              "SNS:Subscribe",
              "SNS:ListSubscriptionsByTopic",
              "SNS:Publish"
            ],
            "Condition": {
              "StringEquals": {
                "AWS:SourceOwner": "213858341631"
              }
            }
          }
        ]
      },
      {
        "name": "learnerlab-ops-week3-negative-test",
        "confirmed": 0,
        "pending": 1,
        "policy": [
          {
            "Effect": "Allow",
            "Principal": {
              "AWS": "*"
            },
            "Action": [
              "SNS:GetTopicAttributes",
              "SNS:SetTopicAttributes",
              "SNS:AddPermission",
              "SNS:RemovePermission",
              "SNS:DeleteTopic",
              "SNS:Subscribe",
              "SNS:ListSubscriptionsByTopic",
              "SNS:Publish"
            ],
            "Condition": {
              "StringEquals": {
                "AWS:SourceOwner": "213858341631"
              }
            }
          }
        ]
      }
    ],
    "alarms": [
      {
        "AlarmName": "learnerlab-ops-week3-alert-rule-failures",
        "StateValue": "OK",
        "AlarmActions": [],
        "OKActions": [],
        "InsufficientDataActions": [],
        "Dimensions": [
          {
            "Name": "RuleName",
            "Value": "learnerlab-ops-week2-alert-daily"
          }
        ]
      },
      {
        "AlarmName": "learnerlab-ops-week3-billing-rule-failures",
        "StateValue": "OK",
        "AlarmActions": [],
        "OKActions": [],
        "InsufficientDataActions": [],
        "Dimensions": [
          {
            "Name": "RuleName",
            "Value": "learnerlab-ops-week2-billing-daily"
          }
        ]
      },
      {
        "AlarmName": "learnerlab-ops-week3-inventory-rule-failures",
        "StateValue": "OK",
        "AlarmActions": [],
        "OKActions": [],
        "InsufficientDataActions": [],
        "Dimensions": [
          {
            "Name": "RuleName",
            "Value": "learnerlab-ops-week2-inventory-6h"
          }
        ]
      },
      {
        "AlarmName": "learnerlab-ops-week3-product-alert-errors",
        "StateValue": "OK",
        "AlarmActions": [],
        "OKActions": [],
        "InsufficientDataActions": [],
        "Dimensions": [
          {
            "Name": "FunctionName",
            "Value": "learnerlab-ops-week2-threshold-alert"
          }
        ]
      }
    ],
    "testLogGroups": [
      {
        "logGroupName": "/aws/lambda/learnerlab-ops-week3-threshold-negative-test",
        "retentionInDays": 7,
        "storedBytes": 4396
      }
    ],
    "west2ProjectFunctionCount": 0
  }
}
```

</details>
