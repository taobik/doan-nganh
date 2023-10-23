
<p>Hướng dẫn chạy code đồ án ngành:</p>
<p>Bước 1: cài đặt PyCharm bằng link "https://download.com.vn/download/pycharm-151429".</p>
<p>Bước 2: Mở PyCharm và chọn open Project hoặc File >> Open và trỏ tới nơi lưu trữ của đồ án .</p>
<p>Bước 3: Vào Terminal</p>
<p>      - Nếu phía trước đường dẫn lưu trữ không có (venv) thì vào File >> Settings >> Tools >> Terminal, sửa Shell path thành "C:\Windows\system32\cmd.exe" và khởi động lại PyCharm.</p>
<p>Bước 4: Vào Terminal nếu chưa thấy (venv) thì thực hiện lại bước 3. Nếu đã hiện (venv) thì nhập "pip install -r requirements.txt" và Enter.</p>
<p>Bước 5: Mở MySQL và tạo schema có tên là "banhang" với Charset/Collation "utf8mb4" và "utf8mb4_unicode_ci"</p>
<p>Bước 6: Vào Project và chyạ file "models.py" để tạo cơ sở dữ liệu</p>
<p>Bước 7: Chạy file "index.py" và link vào "http://127.0.0.1:5000" để chạy Project</p>
