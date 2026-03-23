# Báo cáo Đánh giá Hiện trạng & Phân tích sự khác biệt (Audit & Gap Analysis)

## 1. Đánh giá hiện trạng (Audit Code)
Kiểm thử mã nguồn cũ (`nhan_su` và `cham_cong` K15 Group 5):

| Chức năng | Trạng thái | Lỗi/Tồn đọng | Hướng xử lý |
| :--- | :--- | :--- | :--- |
| **Quản lý Nhân viên** | Hoạt động | Dùng model tự chế `nhan_vien` không chuẩn Odoo. | Refactor sang `hr.employee`. |
| **Chấm công** | Hoạt động | Định nghĩa ca làm việc (Selection) không linh hoạt. | Dùng `resource.calendar`. |
| **Đơn từ** | Tốt | Tên biến chưa chuẩn PEP8. | Chuẩn hóa Naming. |
| **Tính lương** | Thiếu | Chưa có module tính lương. | Phát triển mới `btl_payroll`. |

## 2. Phân tích sự khác biệt (Gap Analysis)
- **Phần kế thừa**: Thuật toán tính toán số phút đi muộn, về sớm và logic trừ thời gian khi có đơn từ được phê duyệt.
- **Phần phát triển mới**: 
    - Module `btl_hr`: Quản lý hợp đồng (`hr.contract`), bảo hiểm, cấp bậc nhân sự.
    - Module `btl_attendance`: Cơ chế đăng ký ca và tích hợp lịch làm việc linh hoạt.
    - Module `btl_payroll`: Hệ thống Payslip tự động kết nối với Attendance.

---
*Ngày báo cáo: 17/03/2026*
