# Thực hành buổi 1: Python MQTT

Ba bài thực hành gồm gửi/nhận thông điệp, mô phỏng cảm biến và điều khiển đèn thông minh. Sáu file `*_bai*.py` tương ứng với sáu chương trình được yêu cầu; `mqtt_common.py` chứa cấu hình broker và hàm dùng chung.

## Chuẩn bị

Yêu cầu Python 3.9+ và một MQTT broker. Cài thư viện:

```powershell
python -m pip install -r requirements.txt
```

**Broker mặc định:** `localhost:1883` (Mosquitto chạy trên chính máy bạn). Nếu dùng cách này, không cần đặt `MQTT_HOST`, `MQTT_PORT`, tài khoản hay TLS trong PowerShell. Cần cài và chạy broker trước khi chạy các chương trình Python.

### Chạy broker trên Windows

Kiểm tra broker trong PowerShell:

```powershell
Test-NetConnection localhost -Port 1883
```

Nếu `TcpTestSucceeded : False`, máy chưa có broker đang nghe ở cổng này. Tải bản Windows x64 tại [trang tải Mosquitto chính thức](https://mosquitto.org/download/) và cài đặt. Nếu cài xong mà cổng vẫn chưa mở, chạy broker trong một cửa sổ PowerShell riêng:

```powershell
& "C:\Program Files\mosquitto\mosquitto.exe" -v
```

Giữ cửa sổ đó mở trong lúc làm bài. Nếu bạn chọn thư mục cài khác, thay đường dẫn cho đúng. Nếu installer đã bật dịch vụ Mosquitto và `TcpTestSucceeded : True`, **không chạy thêm `mosquitto.exe -v`**: hai broker không thể cùng dùng cổng 1883. Chạy Mosquitto không kèm file cấu hình chỉ cho kết nối trên chính máy đó và cho phép kết nối không cần tài khoản.

Nếu trước đó bạn đã thử IP ví dụ hoặc nhập tài khoản mẫu, đặt lại cấu hình **trong từng terminal sẽ chạy Python**:

```powershell
$env:MQTT_HOST = "localhost"
$env:MQTT_PORT = "1883"
Remove-Item Env:MQTT_USERNAME -ErrorAction SilentlyContinue
Remove-Item Env:MQTT_PASSWORD -ErrorAction SilentlyContinue
Remove-Item Env:MQTT_TLS -ErrorAction SilentlyContinue
```

Nếu lỗi kết nối ghi một IP khác `localhost` (ví dụ `192.168.1.10`), `MQTT_HOST` trong terminal đó vẫn trỏ tới IP cũ. Chạy lại khối lệnh trên rồi chạy file Python trong **cùng terminal**.

### Dùng broker khác

Nếu broker ở máy khác, lấy địa chỉ, cổng và tài khoản (nếu có) từ người quản lý broker. Đặt `MQTT_HOST` thành địa chỉ **thật** và `MQTT_PORT` thành cổng **thật** trong PowerShell trước khi chạy chương trình. Chỉ đặt `MQTT_USERNAME` và `MQTT_PASSWORD` nếu broker yêu cầu đăng nhập; chỉ đặt `MQTT_TLS=1` nếu broker yêu cầu TLS. Khi bật TLS mà không đặt `MQTT_PORT`, chương trình dùng cổng `8883`.

Publisher và subscriber phải dùng cùng một broker. Biến `$env:...` chỉ áp dụng cho terminal hiện tại; nếu mở hai terminal, hãy cấu hình ở cả hai.

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

Mở hai terminal. Ở terminal thứ nhất, chạy monitor:

```powershell
python monitor_subscriber_bai2.py
```

Ở terminal thứ hai, chạy sensor:

```powershell
python sensor_publisher_bai2.py
```

Sensor gửi JSON lên `iot/lab/sensor01/data` mỗi 3 giây. Dùng `--count 5` để gửi đúng năm mẫu, hoặc `--interval 1` để đổi chu kỳ. Monitor in dữ liệu và cảnh báo khi nhiệt độ **> 35°C** hoặc độ ẩm **< 40%**. Giá trị sinh ngẫu nhiên trong khoảng 20–40°C và 30–80%.

## Bài 3: Điều khiển đèn thông minh

Mở hai terminal. Ở terminal thứ nhất, chạy thiết bị:

```powershell
python device_bai3.py
```

Ở terminal thứ hai, chạy bộ điều khiển:

```powershell
python controller_bai3.py
```

Nhập `ON`, `OFF` hoặc `EXIT`. Controller gửi lệnh lên `iot/lab/light01/cmd`; thiết bị nhận lệnh hợp lệ và trả JSON trạng thái lên `iot/lab/light01/status`; controller hiển thị phản hồi. Lệnh khác được báo lỗi hoặc bỏ qua. Cần giữ `device_bai3.py` đang chạy để nhận phản hồi.

## Kết quả cần thấy

- Bài 1: subscriber nhận đúng lời chào kèm mã sinh viên và họ tên.
- Bài 2: monitor hiển thị `device_id`, nhiệt độ, độ ẩm và cảnh báo đúng ngưỡng.
- Bài 3: nhập `ON`/`OFF` thì nhận JSON như `{"device_id":"light01","status":"ON"}`.

Các chương trình gửi với MQTT QoS 1. Nếu không kết nối được, kiểm tra broker đang chạy, địa chỉ, cổng, tài khoản và cấu hình TLS.
