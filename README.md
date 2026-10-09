# Thực hành buổi 1: Python MQTT

Ba bài thực hành gồm gửi/nhận thông điệp, mô phỏng cảm biến và điều khiển đèn thông minh. Sáu file `*_bai*.py` tương ứng với sáu chương trình được yêu cầu; `mqtt_common.py` chứa cấu hình broker và hàm dùng chung.

## Chuẩn bị

Yêu cầu Python 3.9+ và một MQTT broker. Cài thư viện:

```powershell
python -m pip install -r requirements.txt
```

**Broker mặc định:** Mosquitto chạy trên máy cá nhân tại `localhost:1883`. Bạn cần cài và khởi động broker trước khi chạy các chương trình Python.

### Chạy broker trên Windows

Nếu lệnh `Test-NetConnection localhost -Port 1883` báo `TcpTestSucceeded : False`, máy chưa có broker đang nghe ở cổng này. Tải bản Windows x64 tại [trang tải Mosquitto chính thức](https://mosquitto.org/download/) và cài đặt. Sau khi cài, mở một cửa sổ PowerShell riêng để chạy broker:

```powershell
& "C:\Program Files\mosquitto\mosquitto.exe" -v
```

Giữ cửa sổ này mở trong lúc làm bài. Nếu bạn chọn thư mục cài khác, thay đường dẫn cho đúng. Nếu installer đã bật dịch vụ Mosquitto và cổng 1883 đã hoạt động, không cần chạy thêm lệnh trên. Kiểm tra lại trong PowerShell khác:

```powershell
Test-NetConnection localhost -Port 1883
```

Khi thấy `TcpTestSucceeded : True`, các chương trình trong repo có thể dùng cấu hình mặc định. Chạy Mosquitto không kèm file cấu hình chỉ cho kết nối trên chính máy đó và cho phép kết nối không cần tài khoản. **Không nhập** các giá trị mẫu `ten_dang_nhap` và `mat_khau` ở ví dụ bên dưới nếu bạn dùng cách này.

### Dùng broker khác

Nếu broker ở máy khác hoặc có cổng khác, đặt các biến môi trường trước khi chạy **mọi** chương trình, sao cho publisher và subscriber dùng cùng một broker:

```powershell
$env:MQTT_HOST = "localhost"  # Đổi thành địa chỉ broker của bạn nếu cần
$env:MQTT_PORT = "1883"
# Nếu broker yêu cầu tài khoản:
$env:MQTT_USERNAME = "ten_dang_nhap"
$env:MQTT_PASSWORD = "mat_khau"
# Nếu broker dùng TLS: đặt MQTT_TLS = "1" và cổng phù hợp (thường là 8883).
```

Không cần khai báo tài khoản và TLS cho broker Mosquitto nội bộ không bật xác thực. Nếu đặt `MQTT_TLS=1` mà không đặt `MQTT_PORT`, cổng mặc định là `8883`. Các biến môi trường được đọc riêng cho từng tiến trình; mở nhiều cửa sổ terminal thì cấu hình ở từng cửa sổ.

## Bài 1: Publisher và subscriber

Mở hai terminal. Chạy subscriber trước:

```powershell
python subscriber_bai1.py
```

Ở terminal kia, thay thông tin sinh viên bằng **thông tin thật** và gửi thông điệp:

```powershell
python publisher_bai1.py --name "Nguyen Van A" --student-id "B23DCCN001"
```

Có thể thêm `--count 3 --interval 1` để gửi ba lần. Có thể dùng biến `STUDENT_NAME` và `STUDENT_ID` thay cho hai tham số. Subscriber in topic `iot/lab/message`, nội dung và thời điểm nhận. Nhấn `Ctrl+C` để dừng.

## Bài 2: Cảm biến nhiệt độ, độ ẩm

Mở hai terminal, chạy monitor trước rồi chạy sensor:

```powershell
python monitor_subscriber_bai2.py
python sensor_publisher_bai2.py
```

Sensor gửi JSON lên `iot/lab/sensor01/data` mỗi 3 giây. Dùng `--count 5` để gửi đúng năm mẫu, hoặc `--interval 1` để đổi chu kỳ. Monitor in dữ liệu và cảnh báo khi nhiệt độ **> 35°C** hoặc độ ẩm **< 40%**. Giá trị sinh ngẫu nhiên trong khoảng 20–40°C và 30–80%.

## Bài 3: Điều khiển đèn thông minh

Mở hai terminal, chạy thiết bị trước rồi chạy bộ điều khiển:

```powershell
python device_bai3.py
python controller_bai3.py
```

Nhập `ON`, `OFF` hoặc `EXIT`. Controller gửi lệnh lên `iot/lab/light01/cmd`; thiết bị nhận lệnh hợp lệ và trả JSON trạng thái lên `iot/lab/light01/status`; controller hiển thị phản hồi. Lệnh khác được báo lỗi hoặc bỏ qua. Cần giữ `device_bai3.py` đang chạy để nhận phản hồi.

## Kết quả cần thấy

- Bài 1: subscriber nhận đúng lời chào kèm mã sinh viên và họ tên.
- Bài 2: monitor hiển thị `device_id`, nhiệt độ, độ ẩm và cảnh báo đúng ngưỡng.
- Bài 3: nhập `ON`/`OFF` thì nhận JSON như `{"device_id":"light01","status":"ON"}`.

Các chương trình gửi với MQTT QoS 1. Nếu không kết nối được, kiểm tra broker đang chạy, địa chỉ, cổng, tài khoản và cấu hình TLS.
