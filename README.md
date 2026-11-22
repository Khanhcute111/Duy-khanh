# DK Site

Website tĩnh độc lập chạy bằng GitHub Pages. Không có backend, không cần Render, Termux hay API key.

## Cách hoạt động
- Giao diện chạy trong trình duyệt.
- AI nâng cấp ảnh dùng UpscalerJS + ESRGAN 2x chạy trên thiết bị.
- Thư viện và trọng số mô hình được tải từ CDN khi cần; ảnh được chọn không gửi đến máy chủ DK Site.
- Hiệu năng phụ thuộc thiết bị, RAM và trình duyệt.

## Bật GitHub Pages
1. Mở Settings của repository.
2. Chọn Pages.
3. Trong Build and deployment, chọn Source là GitHub Actions.
4. Lưu lại. Workflow tự triển khai khi có commit vào nhánh main.

Sau khi workflow thành công, URL thường có dạng:
https://khanhcute111.github.io/Duy-khanh/
