# LTW_TaskManagement

## Mô tả

LTW_TaskManagement là một ứng dụng quản lý công việc được xây dựng bằng Flask. Ứng dụng cho phép người dùng tạo, chỉnh sửa, xóa và quản lý các công việc và dự án. Ứng dụng hỗ trợ xác thực người dùng và cung cấp một giao diện thân thiện để quản lý công việc và dự án.

## Cấu trúc Thư mục

```plaintext
The repository has the following structure:
LTW_TaskManagement/
├── __pycache__/           # Compiled Python files
├── .gitignore             # Git ignore file
├── .idea/                 # IDE-specific files
├── app.py                 # Main entry point of the application
├── README.md              # Project description and instructions
├── requirements.txt       # List of dependencies
├── task_management/       # Main application code
│   ├── __init__.py        # Initializes the Flask application and its extensions
│   ├── db/                # Database files
│   ├── forms.py           # Defines the forms used in the application
│   ├── models.py          # Defines the database models
│   ├── project/           # Project-related views and templates
│   │   ├── __init__.py    # Initializes the project module
│   │   ├── forms.py       # Project-specific forms
│   │   ├── templates/     # Project-specific HTML templates
│   │   ├── views.py       # Defines the views for managing projects
│   ├── routes.py          # Defines the routes for the application
│   ├── static/            # Static files such as CSS, images, and JavaScript
│   ├── task/              # Task-related views and templates
│   ├── user/              # User-related views and templates
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
