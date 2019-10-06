# Đồ án Trí Tuệ Nhân Tạo - Robot Tìm Đường

## Khởi tạo môi trường phát triển

#### Git

Clone project về với lệnh

```
    git clone https://github.com/remtori/pathfinding-robot.git
```

#### Python

Python 3.5 trở lên, bao gồm công cụ cài đặt __pip__

#### Virtualenv

- Windows:

```
    pip install virtualenv
```

- Linux/Unix:

```
    python3 -m pip install virtualenv
```

#### Cài đặt môi trường

__Bước 1:__ Trong thư mục chứa mã nguồn, tạo môi trường độc lập cho ứng dụng

- Windows:

```
    virtualenv env
```

- Linux/Unix:

```
    python3 -m virtualenv env
```

__Bước 2:__ Kích hoạt môi trường

- Windows:

```
    env\Scripts\activate
```

- Linux/Unix:

```
    source env/bin/activate
```

__Bước 3:__ Cài các thư viện cần sử dụng.


```
    pip install -r requirements.txt
```

## Chương trình

Chạy chương trình bằng lệnh

- Windows:

```
python src/main.py
```

- Linux/Unix:

```
python3 src/main.py
```

