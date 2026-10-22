# Lưu cấu hình và lịch sử alarm thử trước khi dọn — 22/10/2026

**Phạm vi:** chỉ alarm `learnerlab-ops-week3-test-lambda-errors` tại account `213858341631`, Region `us-east-1`.

Bản sao được lấy trực tiếp từ CloudWatch trước khi dọn, gồm tham số tạo lại alarm, tags, bốn bản ghi lịch sử và cấu hình của bốn alarm sản phẩm để đối chiếu sau thao tác. Tệp JSON gốc đã tải về máy và đối chiếu SHA-256; không chứa credentials, email hay giá trị billing.

- Thời điểm sao lưu UTC: `2026-10-22T12:00:37.762940+00:00`.
- SHA-256 tệp JSON gốc: `837d72549a0676bd941e2544a7785187ab2a26d9e7f6fdf073875c1323293a47`.
- Số bản ghi lịch sử: **4**.
- Kiểm tra toàn bộ composite alarm không tìm thấy tham chiếu tới alarm thử.
- `AlarmActions`, `OKActions`, `InsufficientDataActions` đều rỗng; dimension chỉ trỏ tới Lambda thử tuần 3.

## Tham số khôi phục cấu hình

Nếu cần dùng lại alarm này, lưu JSON dưới đây thành `test-alarm-restore.json`, xác nhận đang ở đúng account Learner Lab rồi chạy `aws cloudwatch put-metric-alarm --region us-east-1 --cli-input-json file://test-alarm-restore.json`. Chưa chạy lệnh khôi phục trong buổi này. Lệnh tạo lại cấu hình, không phục hồi lịch sử/state cũ vào CloudWatch; lịch sử gốc được lưu riêng ở mục tiếp theo.

```json
{
  "AlarmName": "learnerlab-ops-week3-test-lambda-errors",
  "AlarmDescription": "Theo doi metric AWS/Lambda Errors cua ham thu tuan 3. 1 loi trong 1 phut se vao ALARM; khong gan SNS/Lambda action de tranh gui thong bao trong qua trinh kiem thu.",
  "ActionsEnabled": true,
  "OKActions": [],
  "AlarmActions": [],
  "InsufficientDataActions": [],
  "MetricName": "Errors",
  "Namespace": "AWS/Lambda",
  "Statistic": "Sum",
  "Dimensions": [
    {
      "Name": "FunctionName",
      "Value": "learnerlab-ops-week3-threshold-negative-test"
    }
  ],
  "Period": 60,
  "EvaluationPeriods": 1,
  "DatapointsToAlarm": 1,
  "Threshold": 0.0,
  "ComparisonOperator": "GreaterThanThreshold",
  "TreatMissingData": "notBreaching",
  "Tags": [
    {
      "Key": "Project",
      "Value": "learnerlab-ops"
    },
    {
      "Key": "Owner",
      "Value": "24110019"
    }
  ]
}
```

## Bốn bản ghi lịch sử thật

Đây là toàn bộ `AlarmHistoryItems` mà AWS trả về trong lần sao lưu. `HistoryData` là dữ liệu JSON do CloudWatch cung cấp; không bổ sung sự kiện mô phỏng.

```json
[
  {
    "AlarmName": "learnerlab-ops-week3-test-lambda-errors",
    "AlarmType": "MetricAlarm",
    "Timestamp": "2026-10-20 15:55:26.078000+00:00",
    "HistoryItemType": "StateUpdate",
    "HistorySummary": "Alarm updated from ALARM to OK",
    "HistoryData": "{\"version\":\"1.0\",\"oldState\":{\"stateValue\":\"ALARM\",\"stateReason\":\"Threshold Crossed: 1 out of the last 1 datapoints [1.0 (20/10/26 15:51:00)] was greater than the threshold (0.0) (minimum 1 datapoint for OK -> ALARM transition).\",\"stateReasonData\":{\"version\":\"1.0\",\"queryDate\":\"2026-10-20T15:52:26.071+0000\",\"startDate\":\"2026-10-20T15:51:00.000+0000\",\"statistic\":\"Sum\",\"period\":60,\"recentDatapoints\":[1.0],\"threshold\":0.0,\"evaluatedDatapoints\":[{\"timestamp\":\"2026-10-20T15:51:00.000+0000\",\"sampleCount\":1.0,\"value\":1.0}]}},\"newState\":{\"stateValue\":\"OK\",\"stateReason\":\"Threshold Crossed: 1 out of the last 1 datapoints [0.0 (20/10/26 15:54:00)] was not greater than the threshold (0.0) (minimum 1 datapoint for ALARM -> OK transition).\",\"stateReasonData\":{\"version\":\"1.0\",\"queryDate\":\"2026-10-20T15:55:26.075+0000\",\"startDate\":\"2026-10-20T15:54:00.000+0000\",\"statistic\":\"Sum\",\"period\":60,\"recentDatapoints\":[0.0],\"threshold\":0.0,\"evaluatedDatapoints\":[{\"timestamp\":\"2026-10-20T15:54:00.000+0000\",\"sampleCount\":1.0,\"value\":0.0}]}}}"
  },
  {
    "AlarmName": "learnerlab-ops-week3-test-lambda-errors",
    "AlarmType": "MetricAlarm",
    "Timestamp": "2026-10-20 15:52:26.072000+00:00",
    "HistoryItemType": "StateUpdate",
    "HistorySummary": "Alarm updated from OK to ALARM",
    "HistoryData": "{\"version\":\"1.0\",\"oldState\":{\"stateValue\":\"OK\",\"stateReason\":\"Threshold Crossed: no datapoints were received for 1 period and 1 missing datapoint was treated as [NonBreaching].\",\"stateReasonData\":{\"version\":\"1.0\",\"queryDate\":\"2026-10-20T14:46:26.102+0000\",\"statistic\":\"Sum\",\"period\":60,\"recentDatapoints\":[],\"threshold\":0.0,\"evaluatedDatapoints\":[{\"timestamp\":\"2026-10-20T14:45:00.000+0000\"}]}},\"newState\":{\"stateValue\":\"ALARM\",\"stateReason\":\"Threshold Crossed: 1 out of the last 1 datapoints [1.0 (20/10/26 15:51:00)] was greater than the threshold (0.0) (minimum 1 datapoint for OK -> ALARM transition).\",\"stateReasonData\":{\"version\":\"1.0\",\"queryDate\":\"2026-10-20T15:52:26.071+0000\",\"startDate\":\"2026-10-20T15:51:00.000+0000\",\"statistic\":\"Sum\",\"period\":60,\"recentDatapoints\":[1.0],\"threshold\":0.0,\"evaluatedDatapoints\":[{\"timestamp\":\"2026-10-20T15:51:00.000+0000\",\"sampleCount\":1.0,\"value\":1.0}]}}}"
  },
  {
    "AlarmName": "learnerlab-ops-week3-test-lambda-errors",
    "AlarmType": "MetricAlarm",
    "Timestamp": "2026-10-20 14:46:26.103000+00:00",
    "HistoryItemType": "StateUpdate",
    "HistorySummary": "Alarm updated from INSUFFICIENT_DATA to OK",
    "HistoryData": "{\"version\":\"1.0\",\"oldState\":{\"stateValue\":\"INSUFFICIENT_DATA\",\"stateReason\":\"Unchecked: Initial alarm creation\"},\"newState\":{\"stateValue\":\"OK\",\"stateReason\":\"Threshold Crossed: no datapoints were received for 1 period and 1 missing datapoint was treated as [NonBreaching].\",\"stateReasonData\":{\"version\":\"1.0\",\"queryDate\":\"2026-10-20T14:46:26.102+0000\",\"statistic\":\"Sum\",\"period\":60,\"recentDatapoints\":[],\"threshold\":0.0,\"evaluatedDatapoints\":[{\"timestamp\":\"2026-10-20T14:45:00.000+0000\"}]}}}"
  },
  {
    "AlarmName": "learnerlab-ops-week3-test-lambda-errors",
    "AlarmType": "MetricAlarm",
    "Timestamp": "2026-10-20 14:45:19.662000+00:00",
    "HistoryItemType": "ConfigurationUpdate",
    "HistorySummary": "Alarm \"learnerlab-ops-week3-test-lambda-errors\" created",
    "HistoryData": "{\"version\":\"1.0\",\"type\":\"Create\",\"createdAlarm\":{\"alarmName\":\"learnerlab-ops-week3-test-lambda-errors\",\"alarmDescription\":\"Theo doi metric AWS/Lambda Errors cua ham thu tuan 3. 1 loi trong 1 phut se vao ALARM; khong gan SNS/Lambda action de tranh gui thong bao trong qua trinh kiem thu.\",\"alarmArn\":\"arn:aws:cloudwatch:us-east-1:213858341631:alarm:learnerlab-ops-week3-test-lambda-errors\",\"alarmConfigurationUpdatedTimestamp\":\"2026-10-20T14:45:19.661+0000\",\"namespace\":\"AWS/Lambda\",\"metricName\":\"Errors\",\"extendedStatistic\":\"SUM\",\"period\":60,\"dimensions\":[{\"value\":\"learnerlab-ops-week3-threshold-negative-test\",\"name\":\"FunctionName\"}],\"threshold\":0.0,\"comparisonOperator\":\"GreaterThanThreshold\",\"evaluationPeriods\":1,\"datapointsToAlarm\":1,\"treatMissingData\":\"notBreaching\",\"stateValue\":\"INSUFFICIENT_DATA\",\"stateUpdatedTimestamp\":\"2026-10-20T14:45:19.661+0000\",\"actionsEnabled\":true,\"alarmActions\":[],\"insufficientDataActions\":[],\"okactions\":[]}}"
  }
]
```

Các ảnh của phép thử tuần 3 và diễn biến `OK → ALARM → OK` vẫn được giữ tại [minh chứng tuần 3](../../tuan_3/evidence/11-additional-live-results.md). Kết quả dọn và kiểm tra lại sản phẩm nằm trong [biên bản buổi 3](03-security-cleanup-2026-10-22.md).
