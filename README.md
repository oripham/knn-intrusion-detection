# Dự án ATTBMTT

## Giới thiệu

Dự án ATTBMTT là hệ thống quản lý với nhiều thành phần:
- **Frontend (fe):** Giao diện người dùng, sử dụng React + Vite.
- **Backend:** (Nếu có) Xử lý logic nghiệp vụ, API, kết nối cơ sở dữ liệu.
- **Docker:** Hỗ trợ triển khai nhanh toàn bộ hệ thống.
- **Các thành phần khác:** (Nếu có) như tài liệu, scripts, v.v.

## Cấu trúc thư mục

- `fe/`: Mã nguồn frontend (React + Vite)
- `backend/`: Mã nguồn backend (nếu có)
- `docs/`: Tài liệu dự án (nếu có)
- `docker-compose.yml`: File cấu hình Docker Compose
- `README.md`: Hướng dẫn tổng quan dự án

## Hướng dẫn cài đặt & chạy

### Chạy bằng Docker

Yêu cầu: Đã cài đặt [Docker](https://www.docker.com/) và Docker Compose.

```bash
docker-compose up --build
```

### Chạy thủ công

#### Frontend

```bash
cd fe
npm install
npm run dev
```

#### Backend

```bash
cd backend
# Cài đặt các package cần thiết
npm install
# Chạy server backend (ví dụ với Node.js/Express)
npm run dev
```
> Tham khảo thêm hướng dẫn chi tiết trong file `be/README.md`.


