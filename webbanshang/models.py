from sqlalchemy import Column, Integer, String, Float, Boolean, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from webbanshang import db, app
from datetime import datetime
from enum import Enum as userenum
from flask_login import UserMixin


class UserRole(userenum):
    admin = 0
    normal_user = 1


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class SanPham(BaseModel):
    __tablename__ = 'SanPham'

    Ten = Column(String(255), nullable=False)
    GiaNhap = Column(String(50), nullable=False)
    GiaBan = Column(String(50), nullable=False)
    SoLuong = Column(String(50), nullable=False)
    DaBan = Column(String(50), nullable=False)
    TinhTrang = Column(Boolean, default=True)
    loai_id = Column(Integer, ForeignKey('Loai.id'), nullable=False)
    thongtin_id = Column(Integer, ForeignKey('ThongTin.id'), nullable=False)
    anh = relationship('Anh', backref='SanPham', lazy=True)
    chitietgh = relationship('ChiTietGioHang', backref='SanPham', lazy=True)
    binhluan = relationship('BinhLuan', backref='SanPham', lazy=True)

    def __str__(self):
        return self.name


class Loai(BaseModel):
    __tablename__ = 'Loai'

    Ten = Column(String(50), nullable=False)
    sanpham = relationship('SanPham', backref='Loai', lazy=True)

    def __str__(self):
        return self.name


class Anh(BaseModel):
    __tablename__ = 'Anh'

    Anh = Column(String(255), nullable=False)
    sanpham = Column(Integer, ForeignKey('SanPham.id'), nullable=False)

    def __str__(self):
        return self.name


class ThongTin(BaseModel):
    __tablename__ = 'ThongTin'

    MoTa = Column(String(255), nullable=False)
    ThuongHieu = Column(String(50), nullable=False)
    ManHinh = Column(String(255), nullable=False)
    HeDieuHanh = Column(String(255), nullable=False)
    Chip = Column(String(255), nullable=False)
    Ram = Column(String(255), nullable=False)
    DungLuong = Column(String(255), nullable=False)
    sanpham = relationship('SanPham', backref='ThongTin', lazy=True)

    def __str__(self):
        return self.name


class TaiKhoan(BaseModel, UserMixin):
    __tablename__ = 'TaiKhoan'

    TenDanhNhap = Column(String(255), nullable=False)
    Matkhau = Column(String(50), nullable=False)
    AnhDaiDien = Column(String(255),
                        default='https://res.cloudinary.com/dascseee2/image/upload/v1695288828/images_wszd7i.png')
    VaiTro = Column(Enum(UserRole), default=UserRole.normal_user)
    TinhTrang = Column(Boolean, default=True)
    thongtintk = Column(Integer, ForeignKey('ThongTinTaiKhoan.id'), nullable=False)
    giohang = relationship('GioHang', backref='TaiKhoan', lazy=True)
    binhluan = relationship('BinhLuan', backref='TaiKhoan', lazy=True)
    thich = relationship('Thich', backref='TaiKhoan', lazy=True)

    def __str__(self):
        return self.name


class Thich(BaseModel):
    __tablename__ = 'Thich'

    taikhoan = Column(Integer, ForeignKey('TaiKhoan.id'), nullable=False)
    sanpham = Column(Integer, ForeignKey('SanPham.id'), nullable=False)

    def __str__(self):
        return self.name


class BinhLuan(BaseModel):
    __tablename__ = 'BinhLuan'

    NgayTao = Column(DateTime, default=datetime.now())
    NoiDung = Column(String(255), nullable=False)
    DanhGia = Column(Integer, default=0)
    taikhoan = Column(Integer, ForeignKey('TaiKhoan.id'), nullable=False)
    sanpham = Column(Integer, ForeignKey('SanPham.id'), nullable=False)

    def __str__(self):
        return self.name


class ThongTinTaiKhoan(BaseModel):
    __tablename__ = 'ThongTinTaiKhoan'

    Ho = Column(String(50), nullable=False)
    Ten = Column(String(50), nullable=False)
    DiaChi = Column(String(50), nullable=False)
    Email = Column(String(50), nullable=False)
    SDT = Column(String(50), nullable=False)
    taikhoan = relationship('TaiKhoan', backref='ThongTinTaiKhoan', lazy=True)

    def __str__(self):
        return self.name


class GioHang(BaseModel):
    __tablename__ = 'GioHang'

    NgayTao = Column(DateTime, default=datetime.now())
    DaTT = Column(Boolean, default=False)
    TongGia = Column(String(50), default=0)
    TrangThai = Column(Boolean, default=False)
    tk = Column(Integer, ForeignKey('TaiKhoan.id'), nullable=False)
    chitietgh = relationship('ChiTietGioHang', backref='GioHang', lazy=True)

    def __str__(self):
        return self.name


class ChiTietGioHang(BaseModel):
    __tablename__ = 'ChiTietGioHang'

    Ngay = Column(DateTime, default=datetime.now())
    SoLuong = Column(Integer, nullable=False)
    sanpham = Column(Integer, ForeignKey('SanPham.id'), nullable=False)
    giohang = Column(Integer, ForeignKey('GioHang.id'), nullable=False)

    def __str__(self):
        return self.name


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        l1 = Loai(Ten='Điện thoại')
        l2 = Loai(Ten='LapTop')
        l3 = Loai(Ten='Máy tính bảng')
        l4 = Loai(Ten='Đồng hồ')

        db.session.add_all([l1, l2, l3, l4])
        db.session.commit()

        tt1 = ThongTin(
            MoTa='Samsung Galaxy A53 5G 128GB trình làng với một thiết kế hiện đại, hiệu năng ổn định cùng một màn hình hiển thị sắc nét hay thỏa mãn đam mê nhiếp ảnh trong bạn '
                 'nhờ trang bị camera có độ phân giải cao', ThuongHieu='Samsung', ManHinh='Super AMOLED6.5"Full HD+',
            HeDieuHanh='Android 12',
            Chip='Exynos 1280', Ram='8GB', DungLuong='128GB')
        sp1 = SanPham(Ten='Điện thoại Samsung Galaxy A53 5G 128GB', GiaNhap='3.500.000', GiaBan='5.150.000',
                      SoLuong='100', DaBan='50', loai_id=1, thongtin_id=1)
        a11 = Anh(
            Anh='https://res.cloudinary.com/dascseee2/image/upload/v1695480428/1689349344792_galaxy_a23_didongviet_1_hpmme3.webp',
            sanpham=1)
        a12 = Anh(
            Anh='https://res.cloudinary.com/dascseee2/image/upload/v1695480728/samsung-galaxy-a23-5g-mau-cam-didongviet_lztauf.webp',
            sanpham=1)
        a13 = Anh(
            Anh='https://res.cloudinary.com/dascseee2/image/upload/v1695480729/samsung-galaxy-a23-5g-mau-den-didongviet_1_c3oknb.webp',
            sanpham=1)

        db.session.add_all([tt1, sp1, a11, a12, a13])
        db.session.commit()

        tt2 = ThongTin(
            MoTa='Tại sự kiện Samsung Unpacked thường niên, Samsung Galaxy Z Fold4 256GB chính thức được trình làng thị trường công nghệ, mang trên mình nhiều cải tiến đáng giá giúp Galaxy Z Fold '
                 'trở thành dòng điện thoại gập đã tốt nay càng tốt hơn', ThuongHieu='Samsung',
            ManHinh='Quad HD+ (2K+)',
            HeDieuHanh='Android 12', Chip='Snapdragon 8+ Gen 1', Ram='12GB', DungLuong='256GB')
        sp2 = SanPham(Ten='Điện thoại Samsung Galaxy Z Fold4 5G 256GB', GiaNhap='15.000.000', GiaBan='17.150.000',
                      SoLuong='200', DaBan='165', loai_id=1, thongtin_id=2)
        a21 = Anh(
            Anh='https://res.cloudinary.com/dascseee2/image/upload/v1695482280/samsung-galaxy-z-fold-4-256gb-1_apzpjw.jpg',
            sanpham=2)
        a22 = Anh(
            Anh='https://res.cloudinary.com/dascseee2/image/upload/v1695482280/samsung-galaxy-z-fold4-256gb-1_bfqkuc.jpg',
            sanpham=2)
        a23 = Anh(
            Anh='https://res.cloudinary.com/dascseee2/image/upload/v1695482280/samsung-galaxy-z-flod-4-den-1_kj1bkd.jpg',
            sanpham=2)

        db.session.add_all([tt2, sp2, a21, a22, a23])
        db.session.commit()

        tt3 = ThongTin(
            MoTa='Laptop MSI Gaming GF63 Thin 11UC i7 11800H (1228VN) được trang bị bộ vi xử lý Intel Core i7 dòng H hiệu năng cao và card đồ họa NVIDIA mạnh mẽ, đáp ứng mọi nhu cầu của game thủ và người dùng làm trong ngành sáng tạo nội dung',
            ThuongHieu='MSI', ManHinh='15.6" FHD (1920 x 1080) 60Hz, 72% NTSC, IPS-Level, close to 100%sRGB',
            HeDieuHanh='Windows 11 Home SL',
            Chip='i7-11800H-2.30 GHz', Ram='8GB-DDR4 2 khe (1 khe 8 GB + 1 khe rời)-3200 MHz',
            DungLuong='512GB SSD NVMe PCIe-Hỗ trợ khe cắm SATA 2.5 inch mở rộng '
                      '(nâng cấp SSD hoặc HDD đều được)')
        sp3 = SanPham(Ten='Laptop MSI Gaming GF63 Thin 11UC i7 11800H/8GB/512GB/4GB RTX3050/144Hz/Win11 (1228VN)',
                      GiaNhap='14.500.000', GiaBan='17.790.000', SoLuong='70', DaBan='35', loai_id=2, thongtin_id=3)
        a31 = Anh(
            Anh='https://res.cloudinary.com/dascseee2/image/upload/v1695524029/441vn_72d2775d07e74d7485727dcc9b1164e5_31502463832b4e8192b24c2036a577fa_grande_a6kyu1.webp',
            sanpham=3)
        a32 = Anh(
            Anh='https://res.cloudinary.com/dascseee2/image/upload/v1695524029/29565a03a14e61a556ec86cd10d8a0_master_96d8aa661ed24c7f82501adb3e4f0fb3_8ce2cd7dfb264b3cb9b3e2589f3d12ad_1024x1024_mf2fk3.webp',
            sanpham=3)
        a33 = Anh(
            Anh='https://res.cloudinary.com/dascseee2/image/upload/v1695524029/2771297576488f8763063f659d2a01_master_6b7792c7a28840218fe042c363a7d141_60479c1da95f4b4e95a1da5c6c6d11da_1024x1024_eupajs.webp',
            sanpham=3)

        db.session.add_all([tt3, sp3, a31, a32, a33])
        db.session.commit()

        tt4 = ThongTin(
            MoTa='iPad mini 6 WiFi 256GB được trình làng với cấu hình mạnh mẽ từ chip Apple A15 Bionic, cho bạn những trải nghiệm tuyệt vời trên màn hình sắc nét vượt trội, Apple Pen thỏa sức sáng tạo, và camera thông minh tuyệt vời không thua kém so với smartphone ',
            ThuongHieu='Apple', ManHinh='LED-backlit IPS LCD', HeDieuHanh='iPadOS 15', Chip='Apple A15 Bionic',
            Ram='4GB',
            DungLuong='256GB')
        sp4 = SanPham(Ten='Máy tính bảng iPad mini 6 WiFi 256GB', GiaNhap='10.500.000', GiaBan='14.150.000',
                      SoLuong='100', DaBan='25', loai_id=3, thongtin_id=4)
        a41 = Anh(
            Anh='https://res.cloudinary.com/dascseee2/image/upload/v1695524759/0001078_space-gray_550_dlqals.webp',
            sanpham=4)
        a42 = Anh(
            Anh='https://res.cloudinary.com/dascseee2/image/upload/v1695524759/0001079_space-gray_550_uwykq1.webp',
            sanpham=4)
        a43 = Anh(
            Anh='https://res.cloudinary.com/dascseee2/image/upload/v1695524759/0001080_space-gray_550_rv6wrq.webp',
            sanpham=4)

        db.session.add_all([tt4, sp4, a41, a42, a43])
        db.session.commit()

        tt5 = ThongTin(
            MoTa='Một bước tiến cấu hình vượt bật được Acer ưu ái trên chiếc laptop Acer Nitro 5 Tiger AN515 58 52SP i5 (NH.QFHSV.001) khi trang bị bộ vi xử lý Intel Gen 12 đầy mạnh mẽ cùng phong cách thiết kế đậm chất “mãnh hổ”',
            ThuongHieu='Acer', ManHinh='15.6 Inch FHD (1920 x 1080) IPS 144Hz', HeDieuHanh='Windows 11 Home SL',
            Chip='i5-12500H-2.5GHz', Ram='32GB-DDR4 2 khe (1 khe 8 GB + 1 khe rời)-3200 MHz',
            DungLuong='512GB SSD NVMe PCIe-Hỗ trợ khe cắm SATA 2.5 inch mở rộng (nâng cấp SSD hoặc HDD đều được)')
        sp5 = SanPham(
            Ten='Laptop Acer Nitro 5 Tiger AN515 58 52SP i5 2500H/8GB/512GB/4GB RTX3050/144Hz/Win11 (NH.QFHSV.001)',
            GiaNhap='17.500.000', GiaBan='20.150.000', SoLuong='200', DaBan='78', loai_id=2, thongtin_id=5)
        a51 = Anh(
            Anh='https://res.cloudinary.com/dascseee2/image/upload/v1695580558/acer-nitro-5-tiger-an515-58-52sp-i5-nhqfhsv001-abc-2_lajtme.jpg',
            sanpham=5)
        a52 = Anh(
            Anh='https://res.cloudinary.com/dascseee2/image/upload/v1695580558/acer-nitro-5-tiger-an515-58-52sp-i5-nhqfhsv001-abc-1_bc3rzb.jpg',
            sanpham=5)
        a53 = Anh(
            Anh='https://res.cloudinary.com/dascseee2/image/upload/v1695580559/acer-nitro-5-tiger-an515-58-52sp-i5-nhqfhsv001-abc-3_awlwa9.jpg',
            sanpham=5)

        db.session.add_all([tt5, sp5, a51, a52, a53])
        db.session.commit()

        tt6 = ThongTin(
            MoTa='Samsung Galaxy Tab A7 Lite là dòng máy tính bảng nằm trong phân khúc tầm trung của nhà Samsung. Sản phẩm phù hợp với những người dùng có nhu cầu vừa phải, được trang bị nhiều tính năng hiện đại',
            ThuongHieu='Samsung', ManHinh='TFT LCD', HeDieuHanh='Android 11',
            Chip='Mediatek MT8768T Helio P22T (12 nm)',
            Ram='4GB', DungLuong='32GB')
        sp6 = SanPham(Ten='Samsung Galaxy Tab A7 Lite', GiaNhap='1.500.000', GiaBan='2.150.000',
                      SoLuong='200', DaBan='78', loai_id=3, thongtin_id=6)
        a61 = Anh(
            Anh='https://res.cloudinary.com/dascseee2/image/upload/v1695614946/samsung-galaxy-tab-a8_1_mppfcs.jpg',
            sanpham=6)
        a62 = Anh(
            Anh='https://res.cloudinary.com/dascseee2/image/upload/v1695614946/samsung-galaxy-tab-a8_2_qxuggk.jpg',
            sanpham=6)

        db.session.add_all([tt6, sp6, a61, a62])
        db.session.commit()

        tt7 = ThongTin(
            MoTa='Samsung Galaxy Z Fold5 là mẫu điện thoại cao cấp được ra mắt vào tháng 07/2023 với nhiều điểm đáng chú ý như thiết kế gập độc đáo, hiệu năng mạnh mẽ cùng camera quay chụp tốt',
            ThuongHieu='Samsung', ManHinh='Dynamic AMOLED 2X, Chính 7.6" & Phụ 6.2", Quad HD+ (2K+)',
            HeDieuHanh='Android 13',
            Chip='Snapdragon 8 Gen 2 for Galaxy', Ram='16GB', DungLuong='256GB')
        sp7 = SanPham(Ten='Điện thoại Samsung Galaxy Z Fold5 5G 256GB ', GiaNhap='30.500.000', GiaBan='34.150.000',
                      SoLuong='100', DaBan='32', loai_id=1, thongtin_id=7)
        a71 = Anh(
            Anh='https://res.cloudinary.com/dascseee2/image/upload/v1695616953/samsung-galaxy-zfold5-kem-256gb-1-1_pp4vc4.jpg',
            sanpham=7)
        a72 = Anh(
            Anh='https://res.cloudinary.com/dascseee2/image/upload/v1695616954/samsung-galaxy-zfold5-xanh-256gb-1-1_ty1cmx.jpg',
            sanpham=7)
        a73 = Anh(
            Anh='https://res.cloudinary.com/dascseee2/image/upload/v1695616954/samsung-galaxy-zfold5-den-256gb-1_ckysep.jpg',
            sanpham=7)

        db.session.add_all([tt7, sp7, a71, a72, a73])
        db.session.commit()

        tt8 = ThongTin(
            MoTa='BeFit B4 mang ngôn ngữ thiết kế tối giản, đem đến sự thời thượng cho người sử dụng, được trang bị nhiều tính năng hỗ trợ sức khỏe và rèn luyện thể thao chỉ với mức giá chưa đến 1 triệu đồng.',
            ThuongHieu='BeFit', ManHinh='TFT,169 inch',
            HeDieuHanh='Kết nối được với Android 4.4 trở lên, iOS 8 trở lên',
            Chip='Hãng không công bố', Ram='Hãng không công bố', DungLuong='Hãng không công bố')
        sp8 = SanPham(Ten='Đồng hồ thông minh BeFit B4 44mm ', GiaNhap='150.000', GiaBan='200.000',
                      SoLuong='300', DaBan='124', loai_id=4, thongtin_id=8)
        a81 = Anh(
            Anh='https://res.cloudinary.com/dascseee2/image/upload/v1696086710/befit-beu-b4-hong-1_mdefk2.jpg',
            sanpham=8)
        a82 = Anh(
            Anh='https://res.cloudinary.com/dascseee2/image/upload/v1696086708/befit-beu-b4-hong-2_aqqttx.jpg',
            sanpham=8)
        a83 = Anh(
            Anh='https://res.cloudinary.com/dascseee2/image/upload/v1696086733/befit-beu-b4-hong-3_iria2w.jpg',
            sanpham=8)

        db.session.add_all([tt8, sp8, a81, a82, a83])
        db.session.commit()

        tt9 = ThongTin(
            MoTa='Samsung Galaxy Watch 4 LTE Classic 46mm mang nét sang trọng, hiện đại cùng với bộ khung viền thép không gỉ cứng cáp, màn hình SUPER AMOLED được bao bọc bởi lớp kính cường lực Gorrilla Glass Dx+ bền bỉ, chịu lực tốt.',
            ThuongHieu='Samsung', ManHinh='SUPER AMOLED,1.4 inch',
            HeDieuHanh='Wear OS được tùy biến bởi Samsung, Kết nối được với Android 6.0 trở lên dùng Google Mobile Service',
            Chip='Exynos W920', Ram='Hãng không công bố', DungLuong='16GB')
        sp9 = SanPham(Ten='Đồng hồ thông minh Samsung Galaxy Watch4 LTE Classic 46mm Đen', GiaNhap='5.000.000',
                      GiaBan='6.990.000',
                      SoLuong='150', DaBan='68', loai_id=4, thongtin_id=9)
        a91 = Anh(
            Anh='https://res.cloudinary.com/dascseee2/image/upload/v1696087179/samsung-galaxy-watch-4-lte-classic-46mm1-org_sykrn6.jpg',
            sanpham=9)
        a92 = Anh(
            Anh='https://res.cloudinary.com/dascseee2/image/upload/v1696087178/samsung-galaxy-watch-4-lte-classic-46mm2-org_bjysze.jpg',
            sanpham=9)
        a93 = Anh(
            Anh='https://res.cloudinary.com/dascseee2/image/upload/v1696087178/samsung-galaxy-watch-4-lte-classic-46mm3-org_yzl06y.jpg',
            sanpham=9)

        db.session.add_all([tt9, sp9, a91, a92, a93])
        db.session.commit()

        tk1 = TaiKhoan(TenDanhNhap='linh1', Matkhau='123', VaiTro=UserRole.admin, thongtintk=1)
        tttk1 = ThongTinTaiKhoan(Ho='Truong1', Ten='Linh', DiaChi='Phu Yen', Email='123@gmail.com', SDT='234567890')

        tk2 = TaiKhoan(TenDanhNhap='linh2', Matkhau='123', thongtintk=2)
        tttk2 = ThongTinTaiKhoan(Ho='nguyen2', Ten='Linh', DiaChi='Phu Yen', Email='123@gmail.com', SDT='234567890')

        tk3 = TaiKhoan(TenDanhNhap='linh3', Matkhau='123', thongtintk=3)
        tttk3 = ThongTinTaiKhoan(Ho='pham3', Ten='Linh', DiaChi='Phu Yen', Email='123@gmail.com', SDT='234567890')

        db.session.add_all([tk1, tttk1, tk2, tttk2, tk3, tttk3])
        db.session.commit()

        gh1 = GioHang(tk=2)
        ctgh11 = ChiTietGioHang(SoLuong=3, sanpham=1, giohang=1)
        ctgh12 = ChiTietGioHang(SoLuong=3, sanpham=2, giohang=1)
        ctgh13 = ChiTietGioHang(SoLuong=3, sanpham=5, giohang=1)

        db.session.add_all([gh1, ctgh11, ctgh12, ctgh13])
        db.session.commit()

        gh2 = GioHang(tk=3)
        ctgh21 = ChiTietGioHang(SoLuong=3, sanpham=1, giohang=2)
        ctgh22 = ChiTietGioHang(SoLuong=3, sanpham=2, giohang=2)
        ctgh23 = ChiTietGioHang(SoLuong=3, sanpham=5, giohang=2)

        db.session.add_all([gh2, ctgh21, ctgh22, ctgh23])
        db.session.commit()

        gh3 = GioHang(tk=2, DaTT=True, TongGia="20.000.000")
        ctgh31 = ChiTietGioHang(SoLuong=3, sanpham=1, giohang=3)
        ctgh32 = ChiTietGioHang(SoLuong=3, sanpham=2, giohang=3)
        ctgh33 = ChiTietGioHang(SoLuong=3, sanpham=5, giohang=3)

        db.session.add_all([gh3, ctgh31, ctgh32, ctgh33])
        db.session.commit()

        bl1 = BinhLuan(NoiDung="san pham kha tot1", DanhGia=3, taikhoan=2, sanpham=1)
        bl2 = BinhLuan(NoiDung="san pham kha tot2", DanhGia=5, taikhoan=3, sanpham=1)
        bl3 = BinhLuan(NoiDung="san pham kha tot3", DanhGia=5, taikhoan=2, sanpham=2)

        db.session.add_all([bl1, bl2, bl3])
        db.session.commit()

        t1 = Thich(taikhoan=2, sanpham=1)
        db.session.add_all([t1])
        db.session.commit()