# Hướng dẫn Lab 20 (Dành cho bản Native Binaries - D:\llama.cpp)

Chào bạn! Bạn đang sử dụng bản build sẵn của `llama.cpp` tại `D:\llama.cpp\llama-b9033-bin-win-cpu-x64`. Hướng dẫn này đã được tối ưu để bạn sử dụng trực tiếp các file `.exe` của mình.

---

## 🚀 Các bước thực hiện

### 1. Chuẩn bị môi trường Python (Bắt buộc để test)
Dù dùng bản Native, bạn vẫn cần Python để chạy các bài test tự động (Locust, Smoke test):
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
# Lưu ý: Nếu cài llama-cpp-python bị lỗi, BỎ QUA NÓ. Chỉ cần các thư viện khác.
python -m pip install httpx locust psutil
```

### 2. Kiểm tra phần cứng (Track 00)
Tạo file `hardware.json` để nộp bài:
```powershell
python 00-setup/detect-hardware.py
```
**Yêu cầu:** Chụp ảnh kết quả và lưu vào `submission/screenshots/01-hardware-probe.png`.

### 3. Benchmarking (Track 01) - ĐÃ HOÀN THÀNH ✅
Bạn đã chạy lệnh này và tôi đã cập nhật kết quả vào file `benchmarks/01-quickstart-results.md`:
```powershell
D:\llama.cpp\llama-b9033-bin-win-cpu-x64\llama-bench.exe -m "D:\llama.cpp\llama-b9033-bin-win-cpu-x64\model\Qwen3-1.7B-Q8_0.gguf"
```

### 4. Chạy Model Server (Track 02)
Mở một cửa sổ Terminal mới, kích hoạt `.venv` và chạy server:
```powershell
D:\llama.cpp\llama-b9033-bin-win-cpu-x64\llama-server.exe -m "D:\llama.cpp\llama-b9033-bin-win-cpu-x64\model\Qwen3-1.7B-Q8_0.gguf" --port 8080
```
*Giữ cửa sổ này chạy xuyên suốt các bước sau.*

**Thực hiện các bài test:**
- **Smoke test:** `python 02-llama-cpp-server/smoke-test.py`
- **Load test (10 users):** `locust -f 02-llama-cpp-server/load-test.py --headless -u 10 -r 1 -t 1m --host http://localhost:8080`
- **Chụp ảnh:** Chụp màn hình lúc server đang log các yêu cầu từ Locust.

### 5. Tích hợp RAG Pipeline (Track 03)
Khi server vẫn đang chạy, chạy script tích hợp:
```powershell
python 03-milestone-integration/pipeline.py
```

---

## 📝 Yêu cầu nộp bài (Submission)

1.  **Screenshots:** Lưu đầy đủ ảnh vào `submission/screenshots/`.
2.  **REFLECTION.md:** Điền thông tin vào `submission/REFLECTION.md`. 
    *   *Mẹo:* Ở phần tối ưu hóa, hãy ghi rõ bạn dùng bản build Native và công cụ `llama-bench.exe` để có kết quả chính xác nhất.
3.  **Kiểm tra cuối cùng:** 
    ```powershell
    python scripts/verify.py
    ```
4.  **Push bài:** Đẩy code lên GitHub Public và nộp URL.

---
*Lưu ý: Bạn không cần cài llama-cpp-python vì chúng ta dùng trực tiếp file .exe để benchmark và chạy server.*

