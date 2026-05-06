# 01 — Quickstart Results

Settings: Native llama-bench, Threads: 6.

| Model | Load (ms) | TTFT P50/P95 (ms) | TPOT P50/P95 (ms) | E2E P50/P95/P99 (ms) | Decode rate (tok/s) |
|---|---:|---:|---:|---:|---:|
| Qwen3-1.7B-Q8_0.gguf | N/A | 7678 / - | 54.2 / - | - / - / - | 18.46 |

## Observations
- Kết quả được lấy tự động từ bản build native `llama-bench.exe`.
- **TTFT (Time to First Token):** Ước tính dựa trên kết quả Prompt Processing (pp512).
- **TPOT (Token Per Output Token):** Ước tính dựa trên kết quả Text Generation (tg128).
- **Decode rate:** Tốc độ sinh token thực tế đo được là 18.46 tok/s.

## Raw Output
```text
| model                          |       size |     params | backend    | threads |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | ------: | --------------: | -------------------: |
| qwen3 1.7B Q8_0                |   1.70 GiB |     1.72 B | CPU        |       6 |           pp512 |         66.68 Â± 6.00 |
| qwen3 1.7B Q8_0                |   1.70 GiB |     1.72 B | CPU        |       6 |           tg128 |         18.46 Â± 0.17 |

build: 70a830911 (9033)

```
