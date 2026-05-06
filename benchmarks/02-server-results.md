# Track 02 — Server Results

Kết quả đo đạc từ Locust load test (Headless mode).

## 10 Users Concurrency
- **Total Requests:** 21
- **Failures:** 0 (0.00%)
- **Median Response Time:** 23000 ms
- **95% Percentile:** 34000 ms
- **Average RPS:** ~0.35

## 50 Users Concurrency
- **Total Requests:** 17
- **Failures:** 0 (0.00%)
- **Median Response Time:** 31000 ms
- **95% Percentile:** 42000 ms
- **Average RPS:** ~0.30

## Observations
- Server Native `llama-server.exe` chạy rất ổn định trên Windows.
- Không xảy ra lỗi (Failures = 0) dù ở mức tải cao 50 users.
- Độ trễ tăng theo quy luật khi số lượng user tăng do giới hạn tài nguyên CPU.
