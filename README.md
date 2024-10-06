# LTW_TaskManagement

## Mô tả

LTW_TaskManagement là một ứng dụng quản lý công việc được xây dựng bằng Flask. Ứng dụng cho phép người dùng tạo, chỉnh sửa, xóa và quản lý các công việc và dự án. Ứng dụng hỗ trợ xác thực người dùng và cung cấp một giao diện thân thiện để quản lý công việc và dự án.

## Cấu trúc Thư mục

```plaintext
Kho chứa có cấu trúc sau:
LTW_TaskManagement/
├── __pycache__/           # Các tệp Python đã được biên dịch
├── .gitignore             # Tệp gitignore
├── .idea/                 # Các tệp dành riêng cho IDE
├── app.py                 # Điểm đầu vào chính của ứng dụng
├── README.md              # Mô tả và hướng dẫn dự án
├── requirements.txt       # Danh sách các phụ thuộc
├── task_management/       # Mã chính của ứng dụng
│   ├── __init__.py        # Khởi tạo ứng dụng Flask và các phần mở rộng
│   ├── db/                # Các tệp cơ sở dữ liệu
│   ├── forms.py           # Định nghĩa các biểu mẫu được sử dụng trong ứng dụng
│   ├── models.py          # Định nghĩa các mô hình cơ sở dữ liệu
│   ├── project/           # Các view và template liên quan đến dự án
│   │   ├── __init__.py    # Khởi tạo module dự án
│   │   ├── forms.py       # Các biểu mẫu liên quan đến dự án
│   │   ├── templates/     # Các template HTML dành riêng cho dự án
│   │   ├── views.py       # Định nghĩa các view để quản lý dự án
│   ├── routes.py          # Định nghĩa các tuyến đường của ứng dụng
│   ├── static/            # Các tệp tĩnh như CSS, hình ảnh và JavaScript
│   ├── task/              # Các view và template liên quan đến công việc
│   ├── user/              # Các view và template liên quan đến người dùng
```

### Các tệp và thư mục chính

- [app.py]: Điểm đầu vào chính của ứng dụng.
- [requirements.txt]: Liệt kê các phụ thuộc cần thiết để chạy ứng dụng.
- [task_management/]: Chứa mã chính của ứng dụng.
  - [__init__.py]: Khởi tạo ứng dụng Flask và các phần mở rộng.
  - [db/]: Chứa các tệp cơ sở dữ liệu.
  - [forms.py]: Định nghĩa các biểu mẫu được sử dụng trong ứng dụng.
  - [models.py]: Định nghĩa các mô hình cơ sở dữ liệu.
  - [project/]: Chứa các view và template liên quan đến dự án.
  - [views.py]: Định nghĩa các view để quản lý dự án.
  - [routes.py]: Định nghĩa các tuyến đường của ứng dụng.
  - static/: Chứa các tệp tĩnh như CSS, hình ảnh và JavaScript.
  - [task/]: Chứa các view và template liên quan đến công việc.
  - [user/]: Chứa các view và template liên quan đến người dùng.
