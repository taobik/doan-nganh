from webbanshang import app, db
from webbanshang.models import Thich, BinhLuan, ThongTin, SanPham, Anh, Loai, TaiKhoan, ThongTinTaiKhoan, \
    GioHang, ChiTietGioHang, UserRole
from sqlalchemy import func, desc, update
import datetime
from calendar import monthrange
from flask_login import current_user
import hashlib


def load_sp(kw=None, loai=None):
    m = db.session.query(func.min(Anh.id).label('id'), Anh.sanpham).group_by(Anh.sanpham).cte('m')
    sp = db.session.query(SanPham.id, SanPham.Ten, ThongTin.ThuongHieu, SanPham.GiaNhap, SanPham.GiaBan,
                          SanPham.SoLuong, SanPham.DaBan, SanPham.TinhTrang, Anh.Anh.label('Anh')) \
        .join(Anh, Anh.sanpham.__eq__(SanPham.id)).join(m, Anh.id == m.c.id) \
        .join(ThongTin, SanPham.thongtin_id.__eq__(ThongTin.id)) \
        .join(Loai, Loai.id.__eq__(SanPham.loai_id))
    if kw:
        sp = sp.filter(SanPham.Ten.contains(kw.strip()))
    if loai:
        sp = sp.filter(Loai.Ten.contains(loai.strip()))
    return sp.all()


def load_khach_hang():
    tk = db.session.query(TaiKhoan.id, TaiKhoan.TenDanhNhap, TaiKhoan.Matkhau, TaiKhoan.AnhDaiDien, TaiKhoan.VaiTro,
                          TaiKhoan.TinhTrang)
    return tk.all()


def load_sp_all(id=None):
    m = db.session.query(func.min(Anh.id).label('id'), Anh.sanpham).group_by(Anh.sanpham).cte('m')
    sp = db.session.query(SanPham.id, SanPham.Ten, SanPham.GiaNhap, SanPham.GiaBan, SanPham.SoLuong, SanPham.DaBan,
                          SanPham.TinhTrang, Anh.Anh.label('Anh'), ThongTin.MoTa, ThongTin.ThuongHieu,
                          ThongTin.ManHinh, ThongTin.HeDieuHanh, ThongTin.Chip, ThongTin.Ram, ThongTin.DungLuong) \
        .filter(SanPham.id.__eq__(id)) \
        .join(Anh, Anh.sanpham.__eq__(SanPham.id)).join(m, Anh.id == m.c.id) \
        .join(ThongTin, SanPham.thongtin_id.__eq__(ThongTin.id))
    return sp.all()


def load_khach_hang_all(id):
    tk = db.session.query(TaiKhoan.id, TaiKhoan.TenDanhNhap, TaiKhoan.Matkhau, TaiKhoan.AnhDaiDien, TaiKhoan.VaiTro,
                          TaiKhoan.TinhTrang, ThongTinTaiKhoan.id, ThongTinTaiKhoan.Ho, ThongTinTaiKhoan.Ten,
                          ThongTinTaiKhoan.DiaChi, ThongTinTaiKhoan.Email, ThongTinTaiKhoan.SDT) \
        .join(ThongTinTaiKhoan, ThongTinTaiKhoan.id.__eq__(TaiKhoan.thongtintk)) \
        .filter(TaiKhoan.id.__eq__(id))
    return tk.all()


def load_loai():
    loai = db.session.query(Loai.id, Loai.Ten)
    return loai.all()


def binh_luan(id):
    bl = db.session.query(BinhLuan.id, BinhLuan.NgayTao, BinhLuan.NoiDung, BinhLuan.DanhGia, BinhLuan.taikhoan,
                          ThongTinTaiKhoan.Ten, ThongTinTaiKhoan.Ho, TaiKhoan.AnhDaiDien) \
        .join(TaiKhoan, TaiKhoan.id.__eq__(BinhLuan.taikhoan)) \
        .join(ThongTinTaiKhoan, ThongTinTaiKhoan.id.__eq__(TaiKhoan.thongtintk)) \
        .filter(BinhLuan.sanpham.__eq__(id))
    return bl.all()


def binh_luan_khach(id):
    bl = db.session.query(BinhLuan.id, BinhLuan.NgayTao, BinhLuan.NoiDung, BinhLuan.DanhGia, BinhLuan.taikhoan,
                          ThongTinTaiKhoan.Ten, ThongTinTaiKhoan.Ho, TaiKhoan.AnhDaiDien,
                          BinhLuan.sanpham.label('id_sp')) \
        .join(TaiKhoan, TaiKhoan.id.__eq__(BinhLuan.taikhoan)) \
        .join(ThongTinTaiKhoan, ThongTinTaiKhoan.id.__eq__(TaiKhoan.thongtintk)) \
        .filter(TaiKhoan.id.__eq__(id))
    return bl.all()


def xoa_binh_luan(id):
    bl = BinhLuan.query.filter_by(id=id).first()
    db.session.delete(bl)
    db.session.commit()


def add_sp(ten_sp, loai, anh, gia_nhap, gia_ban, sl, mo_ta, th, mh, hdh, chip, ram, dluong, tt=0):
    with app.app_context():
        if tt == 0:
            ttsp = ThongTin(MoTa=mo_ta, ThuongHieu=th, ManHinh=mh, HeDieuHanh=hdh,
                            Chip=chip, Ram=ram, DungLuong=dluong)
            db.session.add(ttsp)
            db.session.commit()

            if loai:
                cate = Loai.query.filter_by(Ten=loai).first()
                if cate:
                    loai_id = cate.id
                else:
                    cate = Loai(Ten=loai)
                    db.session.add(cate)
                    db.session.commit()
                    loai_id = cate.id
            else:
                loai_id = 1

            sp = SanPham(Ten=ten_sp, GiaNhap=gia_nhap, GiaBan=gia_ban, SoLuong=sl,
                         DaBan=0, loai_id=loai_id, thongtin_id=ttsp.id)
            db.session.add(sp)
            db.session.commit()

            a = Anh(Anh=anh, sanpham=sp.id)
            db.session.add(a)
            db.session.commit()
        else:
            sp = SanPham.query.filter_by(id=tt).first()
            ttsp = ThongTin.query.filter_by(id=sp.thongtin_id).first()
            ttsp.MoTa = mo_ta
            ttsp.ThuongHieu = th
            ttsp.ManHinh = mh
            ttsp.HeDieuHanh = hdh
            ttsp.Chip = chip
            ttsp.Ram = ram
            ttsp.DungLuong = dluong
            db.session.commit()

            if loai:
                cate = Loai.query.filter_by(Ten=loai).first()
                if cate:
                    loai_id = cate.id
                else:
                    cate = Loai(Ten=loai)
                    db.session.add(cate)
                    db.session.commit()
                    loai_id = cate.id
            else:
                loai_id = sp.loai_id

            sp.Ten = ten_sp
            sp.GiaNhap = gia_nhap
            sp.GiaBan = gia_ban
            sp.SoLuong = sl
            sp.DaBan = 0
            sp.loai_id = loai_id
            sp.thongtin_id = ttsp.id
            db.session.commit()

            a = Anh.query.filter_by(sanpham=sp.id).first()
            a.Anh = anh
            db.session.commit()


def delete_sp(id):
    sp = SanPham.query.filter_by(id=id).first()
    ctdh = ChiTietGioHang.query.filter_by(sanpham=sp.id).first()
    while ctdh:
        db.session.delete(ctdh)
        db.session.commit()
        ctdh = ChiTietGioHang.query.filter_by(sanpham=sp.id).first()
    a = Anh.query.filter_by(sanpham=sp.id).first()
    while a:
        db.session.delete(a)
        db.session.commit()
        a = Anh.query.filter_by(sanpham=sp.id).first()
    bl = BinhLuan.query.filter_by(sanpham=sp.id).first()
    while bl:
        db.session.delete(bl)
        db.session.commit()
        bl = BinhLuan.query.filter_by(sanpham=sp.id).first()
    t = Thich.query.filter_by(sanpham=sp.id).first()
    while t:
        db.session.delete(t)
        db.session.commit()
        t = Thich.query.filter_by(sanpham=sp.id).first()
    sp_id = sp.thongtin_id
    db.session.delete(sp)
    db.session.commit()
    ttsp = ThongTin.query.filter_by(id=sp_id).first()
    db.session.delete(ttsp)
    db.session.commit()


def delete_kh(id):
    with app.app_context():
        tkoang = TaiKhoan.query.filter_by(id=id).first()
        tttk = ThongTinTaiKhoan.query.filter_by(id=tkoang.thongtintk).first()
        gh = GioHang.query.filter_by(tk=tkoang.id).first()
        while gh:
            ccgh = ChiTietGioHang.query.filter_by(giohang=gh.id).first()
            while ccgh:
                db.session.delete(ccgh)
                db.session.commit()
                ccgh = ChiTietGioHang.query.filter_by(giohang=gh.id).first()
            db.session.delete(gh)
            db.session.commit()
            gh = GioHang.query.filter_by(tk=tkoang.id).first()
        bl = BinhLuan.query.filter_by(taikhoan=tkoang.id).first()
        while bl:
            db.session.delete(bl)
            db.session.commit()
            bl = BinhLuan.query.filter_by(taikhoan=tkoang.id).first()

        t = Thich.query.filter_by(taikhoan=tkoang.id).first()
        while t:
            db.session.delete(t)
            db.session.commit()
            t = Thich.query.filter_by(taikhoan=tkoang.id).first()
        db.session.delete(tkoang)
        db.session.commit()
        db.session.delete(tttk)
        db.session.commit()


def hoat_dong(id):
    sp = SanPham.query.filter_by(id=id).first()
    active = sp.TinhTrang
    if active == True:
        sp.TinhTrang = False
        db.session.commit()
    else:
        sp.TinhTrang = True
        db.session.commit()


def hd_khach_hang(id):
    sp = TaiKhoan.query.filter_by(id=id).first()
    active = sp.TinhTrang
    if active == True:
        sp.TinhTrang = False
        db.session.commit()
    else:
        sp.TinhTrang = True
        db.session.commit()


def tinh_sp(id):
    li = []
    for i in range(12):
        i = i + 1
        n = monthrange(2023, i)
        dates = datetime.date(2023, i, 1)
        datee = datetime.date(2023, i, n[1])
        sp = db.session.query(func.count(ChiTietGioHang.id)).filter(ChiTietGioHang.sanpham.__eq__(id)) \
            .join(GioHang, ChiTietGioHang.giohang.__eq__(GioHang.id)).filter(GioHang.DaTT.__eq__(True)) \
            .filter(GioHang.NgayTao > dates).filter(GioHang.NgayTao < datee)
        li.append(sp[0][0])
    return li


def tinh_sp_trong_loai(id):
    with app.app_context():
        li = []
        th_sp = ThongTin.query.filter_by(id=id).first()
        th = th_sp.ThuongHieu
        sp = db.session.query(func.count(ChiTietGioHang.id)).filter(ChiTietGioHang.sanpham.__eq__(id)) \
            .join(GioHang, ChiTietGioHang.giohang.__eq__(GioHang.id)).filter(GioHang.DaTT.__eq__(True))
        li.append(sp[0][0])
        sp_all = db.session.query(func.count(ChiTietGioHang.id)) \
            .join(GioHang, ChiTietGioHang.giohang.__eq__(GioHang.id)).filter(GioHang.DaTT.__eq__(True)) \
            .join(SanPham, SanPham.id.__eq__(ChiTietGioHang.sanpham)) \
            .join(ThongTin, SanPham.id.__eq__(ThongTin.id)).filter(ThongTin.ThuongHieu.contains(th))
        n = sp[0][0] - li[0]
        li.append(n)
        return li


def tinh_sp_kh(id):
    li = []
    for i in range(12):
        i = i + 1
        n = monthrange(2023, i)
        dates = datetime.date(2023, i, 1)
        datee = datetime.date(2023, i, n[1])
        sp = db.session.query(func.count(ChiTietGioHang.id)).filter(GioHang.tk.__eq__(id)) \
            .join(GioHang, ChiTietGioHang.giohang.__eq__(GioHang.id)).filter(GioHang.DaTT.__eq__(True)) \
            .filter(GioHang.NgayTao > dates).filter(GioHang.NgayTao < datee)
        li.append(sp[0][0])
    return li


def doanhthu():
    kq = []
    li1 = []
    li2 = []
    li3 = []
    sp1 = db.session.query(ChiTietGioHang.SoLuong, ChiTietGioHang.giohang, ChiTietGioHang.sanpham, SanPham.GiaBan,
                           SanPham.GiaNhap) \
        .join(GioHang, GioHang.id.__eq__(ChiTietGioHang.giohang)) \
        .join(SanPham, SanPham.id.__eq__(ChiTietGioHang.sanpham)) \
        .filter(GioHang.DaTT.__eq__(True))
    for i in sp1:
        gn = i[4].replace(".", "")
        gb = i[3].replace(".", "")
        rs = int(gb) * int(i[0]) - int(gn) * int(i[0])
        li1.append(rs)
    rssum = sum(li1)
    kq.append(rssum)

    y = datetime.datetime.now().year
    dates = datetime.date(y, 1, 1)
    datee = datetime.date(y, 12, 31)
    sp2 = db.session.query(ChiTietGioHang.SoLuong, ChiTietGioHang.giohang, ChiTietGioHang.sanpham,
                           SanPham.GiaBan, SanPham.GiaNhap) \
        .join(GioHang, GioHang.id.__eq__(ChiTietGioHang.giohang)) \
        .join(SanPham, SanPham.id.__eq__(ChiTietGioHang.sanpham)) \
        .filter(GioHang.DaTT.__eq__(True)).filter(GioHang.NgayTao.between(dates, datee))
    for i in sp2:
        gn = i[4].replace(".", "")
        gb = i[3].replace(".", "")
        rs = int(gb) * int(i[0]) - int(gn) * int(i[0])
        li2.append(rs)
    rssum2 = sum(li2)
    kq.append(rssum2)

    y = datetime.datetime.now().year
    m = datetime.datetime.now().month
    d = monthrange(y, m)
    dates = datetime.date(y, m, 1)
    datee = datetime.date(y, m, d[1])
    sp3 = db.session.query(ChiTietGioHang.SoLuong, ChiTietGioHang.giohang, ChiTietGioHang.sanpham, SanPham.GiaBan,
                           SanPham.GiaNhap) \
        .join(GioHang, GioHang.id.__eq__(ChiTietGioHang.giohang)) \
        .join(SanPham, SanPham.id.__eq__(ChiTietGioHang.sanpham)) \
        .filter(GioHang.DaTT.__eq__(True)).filter(GioHang.NgayTao.between(dates, datee))
    for i in sp3:
        gn = i[4].replace(".", "")
        gb = i[3].replace(".", "")
        rs = int(gb) * int(i[0]) - int(gn) * int(i[0])
        li3.append(rs)
    rssum3 = sum(li2)
    kq.append(rssum3)
    return kq


def doanhthu_thang():
    li = []
    cate = []
    kq = []
    y = datetime.datetime.now().year
    dates = datetime.date(y, 1, 1)
    datee = datetime.date(y, 12, 31)
    loai = db.session.query(Loai.id,Loai.Ten)
    for l in loai:
        sp = db.session.query(ChiTietGioHang.SoLuong, ChiTietGioHang.giohang, ChiTietGioHang.sanpham,
                              SanPham.GiaBan, SanPham.GiaNhap) \
            .join(GioHang, GioHang.id.__eq__(ChiTietGioHang.giohang)) \
            .join(SanPham, SanPham.id.__eq__(ChiTietGioHang.sanpham)) \
            .join(ThongTin, SanPham.thongtin_id.__eq__(ThongTin.id)).filter(SanPham.loai_id.__eq__(l[0])) \
            .filter(GioHang.DaTT.__eq__(True)).filter(GioHang.NgayTao.between(dates, datee))
        li.append(str(l[1]))
        for i in sp:
            gn = i[4].replace(".", "")
            gb = i[3].replace(".", "")
            rs = int(gb) * int(i[0]) - int(gn) * int(i[0])
            cate.append(rs)
        while len(cate) > 1:
            cate[0] = int(cate[0]) + int(cate[1])
            cate.pop(1)
        if len(cate) > 0:
            li.append(cate[0])
        else:
            li.append(0)
        del cate[:]
    return li


def top_khachhang():
    with app.app_context():
        li = []
        cate = []
        kq = []
        tk = db.session.query(TaiKhoan.id,TaiKhoan.TenDanhNhap)
        for l in tk:
            sp = db.session.query(ChiTietGioHang.SoLuong, ChiTietGioHang.giohang, ChiTietGioHang.sanpham,
                                  SanPham.GiaBan, SanPham.GiaNhap, TaiKhoan.id) \
                .join(GioHang, GioHang.id.__eq__(ChiTietGioHang.giohang)) \
                .join(SanPham, SanPham.id.__eq__(ChiTietGioHang.sanpham)) \
                .join(ThongTin, SanPham.thongtin_id.__eq__(ThongTin.id))\
                .join(TaiKhoan, TaiKhoan.id.__eq__(GioHang.tk)).filter(GioHang.tk.__eq__(l[0])) \
                .filter(GioHang.DaTT.__eq__(True)).limit(10)
            li.append(l[0])
            li.append(l[1])
            for i in sp:
                gn = i[4].replace(".", "")
                gb = i[3].replace(".", "")
                rs = int(gb) * int(i[0]) - int(gn) * int(i[0])
                cate.append(rs)
            while len(cate) > 1:
                cate[0] = int(cate[0]) + int(cate[1])
                cate.pop(1)
            if len(cate) > 0:
                li.append(cate[0])
            else:
                li.append(0)
            del cate[:]
        while len(li) > 0:
            kq.append({
                'id': li[0],
                'ten': li[1],
                'dt': li[2]
            })
            li.pop(2)
            li.pop(1)
            li.pop(0)
        kq.sort(reverse=True,key=so)
        return kq


def top_sanpham():
    with app.app_context():
        li = []
        cate = []
        kq = []
        sp1 = db.session.query(SanPham.id,SanPham.Ten)
        for l in sp1:
            sp = db.session.query(ChiTietGioHang.SoLuong, ChiTietGioHang.giohang, ChiTietGioHang.sanpham,
                                  SanPham.GiaBan, SanPham.GiaNhap, SanPham.id) \
                .join(GioHang, GioHang.id.__eq__(ChiTietGioHang.giohang)) \
                .join(SanPham, SanPham.id.__eq__(ChiTietGioHang.sanpham)).filter(SanPham.id.__eq__(l[0])) \
                .filter(GioHang.DaTT.__eq__(True)).limit(10)
            li.append(l[0])
            li.append(l[1])
            for i in sp:
                gn = i[4].replace(".", "")
                gb = i[3].replace(".", "")
                rs = int(gb) * int(i[0]) - int(gn) * int(i[0])
                cate.append(rs)
            while len(cate) > 1:
                cate[0] = int(cate[0]) + int(cate[1])
                cate.pop(1)
            if len(cate) > 0:
                li.append(cate[0])
            else:
                li.append(0)
            del cate[:]
        while len(li) > 0:
            kq.append({
                'id': li[0],
                'ten': li[1],
                'dt': li[2]
            })
            li.pop(2)
            li.pop(1)
            li.pop(0)
        kq.sort(reverse=True,key=so)
        kq = kq[:5]
        return kq


def so(e):
  return e['dt']

















