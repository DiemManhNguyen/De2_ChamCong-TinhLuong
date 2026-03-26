<h2 align="center">
    <a href="https://dainam.edu.vn/vi/khoa-cong-nghe-thong-tin">
    🎓 Faculty of Information Technology (DaiNam University)
    </a>
</h2>
<h2 align="center">
    PLATFORM ERP
</h2>
<div align="center">
    <p align="center">
        <img src="docs/logo/aiotlab_logo.png" alt="AIoTLab Logo" width="170"/>
        <img src="docs/logo/fitdnu_logo.png" alt="AIoTLab Logo" width="180"/>
        <img src="docs/logo/dnu_logo.png" alt="DaiNam University Logo" width="200"/>
    </p>

[![AIoTLab](https://img.shields.io/badge/AIoTLab-green?style=for-the-badge)](https://www.facebook.com/DNUAIoTLab)
[![Faculty of Information Technology](https://img.shields.io/badge/Faculty%20of%20Information%20Technology-blue?style=for-the-badge)](https://dainam.edu.vn/vi/khoa-cong-nghe-thong-tin)
[![DaiNam University](https://img.shields.io/badge/DaiNam%20University-orange?style=for-the-badge)](https://dainam.edu.vn)

</div>

## 📖 1. Giới thiệu
Platform ERP được áp dụng vào học phần Thực tập doanh nghiệp dựa trên mã nguồn mở Odoo. 

## 🔧 2. Các công nghệ được sử dụng
<div align="center">

### Hệ điều hành
[![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)](https://ubuntu.com/)
### Công nghệ chính
[![Odoo](https://img.shields.io/badge/Odoo-714B67?style=for-the-badge&logo=odoo&logoColor=white)](https://www.odoo.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![XML](https://img.shields.io/badge/XML-FF6600?style=for-the-badge&logo=codeforces&logoColor=white)](https://www.w3.org/XML/)
### Cơ sở dữ liệu
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
</div>

## 🧪 3. Phát triển bởi AIoTLabs & FIT-DNU
Dự án được xây dựng và tối ưu hóa bởi Đội ngũ kỹ thuật thuộc **AIoTLab** - Khoa Công nghệ Thông tin, Trường Đại học Đại Nam. Mục tiêu là phát triển giải pháp ERP thông minh, tích hợp các công nghệ hiện đại như **Trí tuệ Nhân tạo (AI)** và **Internet vạn vật (IoT)** vào quản trị doanh nghiệp thực tế.
## ⚙️ 4. Cài đặt

### 4.1. Cài đặt công cụ, môi trường và các thư viện cần thiết

#### 4.1.1. Tải project.
```
git clone https://github.com/FIT-DNU/Business-Internship.git
```
#### 4.1.2. Cài đặt các thư viện cần thiết
Người sử dụng thực thi các lệnh sau đề cài đặt các thư viện cần thiết

```
sudo apt-get install libxml2-dev libxslt-dev libldap2-dev libsasl2-dev libssl-dev python3.10-distutils python3.10-dev build-essential libssl-dev libffi-dev zlib1g-dev python3.10-venv libpq-dev
```
#### 4.1.3. Khởi tạo môi trường ảo.
- Khởi tạo môi trường ảo
```
python3.10 -m venv ./venv
```
- Thay đổi trình thông dịch sang môi trường ảo
```
source venv/bin/activate
```
- Chạy requirements.txt để cài đặt tiếp các thư viện được yêu cầu
```
pip3 install -r requirements.txt
```
### 4.2. Setup database

Khởi tạo database trên docker bằng việc thực thi file dockercompose.yml.
```
sudo docker-compose up -d
```
### 4.3. Setup tham số chạy cho hệ thống
Tạo tệp **odoo.conf** có nội dung như sau:
```
[options]
addons_path = addons
db_host = localhost
db_password = odoo
db_user = odoo
db_port = 5431
xmlrpc_port = 8069
```
Có thể kế thừa từ file **odoo.conf.template**
### 4.4. Chạy hệ thống và cài đặt các ứng dụng cần thiết
Lệnh chạy
```
python3 odoo-bin.py -c odoo.conf -u all
```
Người sử dụng truy cập theo đường dẫn _http://localhost:8069/_ để đăng nhập vào hệ thống.

## 📝 5. License

© 2024 AIoTLab, Faculty of Information Technology, DaiNam University. All rights reserved.


---

## 🚀 Dự án Chấm công & Tính lương (Đề số 2)

Dự án này tập trung vào việc chuyển đổi các module từ khóa K15 thành một hệ thống ERP thống nhất tích hợp Nhân sự, Chấm công và Lương, có tích hợp **Trí tuệ Nhân tạo (Gemini AI)**. 

- **Business Flow**: Luồng nghiệp vụ mô tả từ khâu tuyển dụng, ký hợp đồng tại `btl_hr`, đăng ký ca làm tại `btl_attendance`, chấm công thực tế hàng ngày cho đến khi tổng hợp và tính lương tự động tại `btl_payroll`.
- **Tính năng AI**: Tích hợp **Google Gemini Pro** để tự động phân tích hiệu suất làm việc, kỷ luật và đề xuất khen thưởng dựa trên dữ liệu thật của nhân viên.
- **Luồng dữ liệu**: `btl_hr` (Dữ liệu gốc) -> `btl_attendance` (Dữ liệu công) -> `btl_payroll` (Dữ liệu tiền lương + Gemini AI).

Xem chi tiết sơ đồ nghiệp vụ tại: [docs/business_flow/Nhom02_BusinessFlow_ChamCongTinhLuong.png](docs/business_flow/Nhom02_BusinessFlow_ChamCongTinhLuong.png)

*Người thực hiện: Nhóm 02 - Antigravity AI*
