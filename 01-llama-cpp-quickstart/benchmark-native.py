import subprocess
import os
from pathlib import Path

# Cấu hình đường dẫn (Bạn có thể sửa nếu đổi thư mục)
LLAMA_BENCH_PATH = r"D:\llama.cpp\llama-b9033-bin-win-cpu-x64\llama-bench.exe"
MODEL_PATH = r"D:\llama.cpp\llama-b9033-bin-win-cpu-x64\model\Qwen3-1.7B-Q8_0.gguf"
OUTPUT_FILE = Path("benchmarks/01-quickstart-results.md")

def run_benchmark():
    print(f"==> Running native benchmark using {LLAMA_BENCH_PATH}...")
    
    # Chạy lệnh llama-bench
    try:
        result = subprocess.run(
            [LLAMA_BENCH_PATH, "-m", MODEL_PATH],
            capture_output=True,
            text=True,
            check=True
        )
        output = result.stdout
        print("==> Benchmark completed successfully.")
        return output
    except Exception as e:
        print(f"ERROR: Could not run llama-bench. {e}")
        return None

def save_to_md(raw_output):
    # Tạo thư mục benchmarks nếu chưa có
    OUTPUT_FILE.parent.mkdir(exist_ok=True)
    
    # Phân tích sơ bộ từ raw_output để lấy số (llama-bench output format)
    # Dòng chứa pp512 thường là TTFT, tg128 thường là TPOT
    lines = raw_output.split('\n')
    pp_speed = "0.0"
    tg_speed = "0.0"
    for line in lines:
        if "pp512" in line:
            pp_speed = line.split('|')[-2].strip().split(' ')[0]
        if "tg128" in line:
            tg_speed = line.split('|')[-2].strip().split(' ')[0]

    # Tính toán TTFT và TPOT tương đối (ms)
    # TTFT ~ 512 tokens / (tokens/s) * 1000
    # TPOT ~ 1000 / (tokens/s)
    try:
        ttft_p50 = (512 / float(pp_speed)) * 1000 if float(pp_speed) > 0 else 0
        tpot_p50 = 1000 / float(tg_speed) if float(tg_speed) > 0 else 0
    except:
        ttft_p50, tpot_p50 = 0, 0

    md_content = f"""# 01 — Quickstart Results

Settings: Native llama-bench, Threads: 6.

| Model | Load (ms) | TTFT P50/P95 (ms) | TPOT P50/P95 (ms) | E2E P50/P95/P99 (ms) | Decode rate (tok/s) |
|---|---:|---:|---:|---:|---:|
| {os.path.basename(MODEL_PATH)} | N/A | {ttft_p50:.0f} / - | {tpot_p50:.1f} / - | - / - / - | {tg_speed} |

## Observations
- Kết quả được lấy tự động từ bản build native `llama-bench.exe`.
- **TTFT (Time to First Token):** Ước tính dựa trên kết quả Prompt Processing (pp512).
- **TPOT (Token Per Output Token):** Ước tính dựa trên kết quả Text Generation (tg128).
- **Decode rate:** Tốc độ sinh token thực tế đo được là {tg_speed} tok/s.

## Raw Output
```text
{raw_output}
```
"""
    
    OUTPUT_FILE.write_text(md_content, encoding="utf-8")
    print(f"==> Results saved to {OUTPUT_FILE} with standard format.")
    print("\n--- SUMMARY TABLE FOR SCREENSHOT ---")
    print(md_content)
    print("------------------------------------")

if __name__ == "__main__":
    raw_data = run_benchmark()
    if raw_data:
        save_to_md(raw_data)
