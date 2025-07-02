# Magentic-UI Docker Setup

Tài liệu này hướng dẫn cách sử dụng Docker để chạy Magentic-UI.

## 🚀 Chạy nhanh

### Sử dụng Docker Compose (Khuyến nghị)

1. **Thiết lập biến môi trường:**
   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   # Hoặc cho Azure:
   export AZURE_OPENAI_API_KEY="your-azure-api-key"
   export AZURE_OPENAI_ENDPOINT="your-azure-endpoint"
   ```

2. **Chạy ứng dụng:**
   ```bash
   docker-compose up -d
   ```

3. **Truy cập ứng dụng:**
   Mở trình duyệt và truy cập: http://localhost:8081

### Sử dụng Docker trực tiếp

1. **Build image:**
   ```bash
   docker build -t magentic-ui:latest .
   ```

2. **Chạy container:**
   ```bash
   ./docker-run.sh
   ```

## 📋 Các lệnh hữu ích

### Xem logs
```bash
docker-compose logs -f magentic-ui
# hoặc
docker logs -f magentic-ui
```

### Dừng ứng dụng
```bash
docker-compose down
# hoặc
docker stop magentic-ui
```

### Restart ứng dụng
```bash
docker-compose restart
# hoặc
docker restart magentic-ui
```

### Xóa container và volume
```bash
docker-compose down -v
# hoặc
docker rm magentic-ui
docker volume rm magentic_data
```

## 🔧 Cấu hình

### Biến môi trường

Các biến môi trường quan trọng:

- `OPENAI_API_KEY`: API key của OpenAI
- `AZURE_OPENAI_API_KEY`: API key của Azure OpenAI
- `AZURE_OPENAI_ENDPOINT`: Endpoint của Azure OpenAI

### Volumes

- `magentic_data`: Lưu trữ dữ liệu persistent của ứng dụng
- `/var/run/docker.sock`: Cho phép container quản lý Docker (Docker-in-Docker)

### Ports

- `8081`: Port chính của ứng dụng web

## 🛠️ Development

### Build development image
```bash
docker build -t magentic-ui:dev .
```

### Chạy với volume mount cho development
```bash
docker run -it --rm \
  -p 8081:8081 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v $(pwd):/app \
  --privileged \
  magentic-ui:dev
```

## 🐛 Troubleshooting

### Container không khởi động được
1. Kiểm tra logs: `docker logs magentic-ui`
2. Đảm bảo port 8081 không bị chiếm dụng
3. Kiểm tra Docker daemon đang chạy

### Không thể truy cập ứng dụng
1. Kiểm tra container đang chạy: `docker ps`
2. Kiểm tra health check: `docker inspect magentic-ui`
3. Kiểm tra firewall settings

### Lỗi permission với Docker socket
```bash
sudo chown $USER:docker /var/run/docker.sock
```

## 📝 Lưu ý

- Container cần quyền `privileged` để chạy Docker-in-Docker
- Đảm bảo có đủ RAM (khuyến nghị tối thiểu 4GB)
- Lần đầu chạy có thể mất thời gian do cần download Playwright browsers
