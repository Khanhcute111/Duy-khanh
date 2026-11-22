# DK Site

Website AI làm nét ảnh trên Cloud, giao diện tối ưu cho điện thoại. Backend FastAPI gọi Replicate Real-ESRGAN 4x; API token chỉ nằm trong biến môi trường máy chủ.

## Deploy trên Render
1. Mở https://dashboard.render.com/ và chọn **New > Blueprint**.
2. Chọn repository `Khanhcute111/Duy-khanh` và nhánh `main`.
3. Khi Render yêu cầu, thêm biến môi trường `REPLICATE_API_TOKEN` bằng token mới tạo tại https://replicate.com/account/api-tokens.
4. Deploy. Render sẽ tạo web service theo `render.yaml`.
5. Mở URL `https://dk-site.onrender.com` (hoặc URL Render cấp nếu tên đã được dùng).

## Lưu ý
- Không commit API token vào GitHub hoặc gửi token trong chat. Token đã từng được dán công khai cần thu hồi và thay mới.
- Replicate là dịch vụ tính phí theo mức sử dụng/tài khoản; không cam kết miễn phí vô hạn.
- Model: `cjwbw/real-esrgan`, scale 4x.
- Health check: `/api/health`.
