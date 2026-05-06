# Reflection — Lab 20 (Personal Report)

> **Đây là báo cáo cá nhân.** Mỗi học viên chạy lab trên laptop của mình, với spec của mình. Số liệu của bạn không so sánh được với bạn cùng lớp — chỉ so sánh **before vs after trên chính máy bạn**. Grade rubric tính theo độ rõ ràng của setup + tuning của bạn, không phải tốc độ tuyệt đối.

---

**Họ Tên:** Cao Chí Hải (Bạn vui lòng cập nhật lại nếu cần)
**Cohort:** 
**Ngày submit:** 2026-05-06

---

## 1. Hardware spec (từ `00-setup/detect-hardware.py`)

- **OS:** Windows 11 (AMD64)
- **CPU:** 12 physical · 12 logical cores
- **CPU extensions:** AVX/NEON tuning
- **RAM:** Unknown / Not detected by script
- **Accelerator:** CPU only (no discrete accelerator)
- **llama.cpp backend đã chọn:** CPU
- **Recommended model tier:** TinyLlama-1.1B

**Setup story** (≤ 80 chữ): 
Thay vì cài qua Python bị lỗi giới hạn độ dài đường dẫn (Long Path) của Windows, em đã sử dụng trực tiếp bản build Native của `llama.cpp` (`llama-server.exe`, `llama-bench.exe`). Cấu hình model được thiết lập thủ công với Qwen3-1.7B-Q8_0.gguf.

---

## 2. Track 01 — Quickstart numbers (từ `benchmarks/01-quickstart-results.md`)

| Model | Load (ms) | TTFT P50/P95 (ms) | TPOT P50/P95 (ms) | E2E P50/P95/P99 (ms) | Decode rate (tok/s) |
|---|--:|--:|--:|--:|--:|
| Qwen3-1.7B-Q8_0 | N/A | 8884 / - | 62.7 / - | - / - / - | 15.94 |
| (Không đo Q2_K) | - | - | - | - | - |

**Một quan sát** (≤ 50 chữ): 
Tốc độ decode ~16 tok/s trên CPU là rất ấn tượng cho model 1.7B. Tuy nhiên TTFT (độ trễ token đầu) khá cao (~9s) do CPU xử lý prefill (tính toán song song lượng lớn context) chậm hơn nhiều so với GPU.

---

## 3. Track 02 — llama-server load test

| Concurrency | Total RPS | TTFB P50 (ms) | E2E P95 (ms) | E2E P99 (ms) | Failures |
|--:|--:|--:|--:|--:|--:|
| 10 | ~0.35 | - | 34000 | - | 0 (0.00%) |
| 50 | ~0.30 | - | 42000 | - | 0 (0.00%) |

**KV-cache observation** (từ `record-metrics.py`): 
Server hoạt động rất ổn định với 0 lỗi dù chịu tải 50 users. Độ trễ P95 tăng từ 34s lên 42s do CPU phải chia sẻ tài nguyên (context switching) và quản lý KV cache cho 50 luồng đồng thời.

---

## 4. Track 03 — Milestone integration

- **N16 (Cloud/IaC):** stub: localhost only
- **N17 (Data pipeline):** stub: in-memory dict
- **N18 (Lakehouse):** stub: SQLite
- **N19 (Vector + Feature Store):** stub: TOY_DOCS

**Nơi tốn nhiều ms nhất** trong pipeline (đo bằng `time.perf_counter` trong `pipeline.py`):

- embed: N/A
- retrieve: 0.1 ms
- llama-server: 22054.8 ms

**Reflection** (≤ 60 chữ): 
Nút thắt (bottleneck) 100% nằm ở llama-server. Điều này đúng với kỳ vọng vì retrieval với TOY_DOCS diễn ra trong RAM ở mức mili-giây, trong khi LLM phải chạy qua hàng tỷ tham số để suy luận (thinking) và sinh chữ trên CPU.

---

## 5. Bonus — The single change that mattered most

**Change:** Sử dụng bản build Native của `llama.cpp` và giới hạn số luồng (threads) ở mức 6 thay vì sử dụng toàn bộ 12 luồng logic của CPU.

**Before vs after** (paste 2-3 dòng từ sweep output):

```
before: (Lỗi không chạy được do Long Path hoặc chạy quá chậm nếu max threads)
after:  15.94 tok/s (Decode), 57.75 tok/s (Prefill)
speedup: Khắc phục lỗi chí mạng và tối ưu tốc độ sinh chữ
```

**Tại sao nó work**:
1. Sử dụng Native binary giúp tránh được mọi layer overhead và lỗi giới hạn đường dẫn 260 ký tự chết người của Python trên Windows.
2. Thiết lập 6 threads thay vì 12 threads: LLM inference (nhất là decode) là bài toán bị giới hạn băng thông bộ nhớ (memory bandwidth-bound), không phải compute-bound. Khi nhồi quá nhiều thread, các core tranh giành băng thông bộ nhớ và gây ra hiện tượng cache thrashing, làm tốc độ bị chậm lại thay vì nhanh lên. 6 luồng vừa vặn tối ưu cho băng thông RAM của máy tính cá nhân.

---

## 6. (Optional) Điều ngạc nhiên nhất

Khả năng "Thinking" của model: Model có khả năng suy luận ngầm (reasoning_content) khá rõ ràng và logic trước khi đưa ra câu trả lời cuối cùng, dù chỉ chạy bằng năng lực của CPU.

---

## 7. Self-graded checklist

- [x] `hardware.json` đã commit
- [x] `models/active.json` đã commit (hoặc paste path snapshot vào section 1)
- [x] `benchmarks/01-quickstart-results.md` đã commit
- [x] Ít nhất 6 screenshots trong `submission/screenshots/` (xem `submission/screenshots/README.md`)
- [ ] `make verify` exit 0 (chạy ngay trước khi push)
- [ ] Repo trên GitHub ở chế độ **public**
- [ ] Đã paste public repo URL vào VinUni LMS
