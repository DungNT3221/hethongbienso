FROM nginx:alpine

# Sao chép các file tĩnh vào thư mục mặc định của Nginx
COPY . /usr/share/nginx/html

# Sao chép file cấu hình Nginx tùy chỉnh (nếu cần)
# COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Khởi động Nginx
CMD ["nginx", "-g", "daemon off;"]
