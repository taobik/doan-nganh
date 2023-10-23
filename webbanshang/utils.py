from webbanshang import app, db
from webbanshang.models import Thich, BinhLuan, ThongTin, SanPham, Anh, Loai, TaiKhoan, ThongTinTaiKhoan, \
    GioHang, ChiTietGioHang, UserRole
from sqlalchemy import func, desc, update
import datetime
from flask_login import current_user
import hashlib


def load_cate(kw=None):
    loai = db.session.query(Loai.id, Loai.Ten)
    if kw:
        loai = loai.filter(Loai.Ten.contains(kw))
    return loai.all()


def load_sp(id=None, cate=None, max=None, id_cate=None, kw=None, trang=0):
    with app.app_context():
        m = db.session.query(func.min(Anh.id).label('id'), Anh.sanpham).group_by(Anh.sanpham).cte('m')
        sp = db.session.query(SanPham.id, SanPham.Ten, SanPham.GiaBan, SanPham.loai_id, Anh.Anh.label('Anh')) \
            .join(Anh, Anh.sanpham.__eq__(SanPham.id)).join(m, Anh.id == m.c.id) \
            .filter(SanPham.TinhTrang.__eq__(True))
        if id:
            sp = sp.filter(SanPham.id.__eq__(id))
        if cate:
            sp = sp.filter(SanPham.loai_id.__eq__(cate))
        if max:
            sp = sp.limit(max)
        if id_cate:
            x = sp.filter(SanPham.id.__eq__(id_cate))
            y = x[0][3]
            sp = sp.filter(SanPham.loai_id.__eq__(y))
        if kw:
            sp = sp.filter(SanPham.Ten.contains(kw))
        if trang:
            if trang > 0:
                sp = sp.limit(5).offset(trang*5-5)
        return sp.all()


def loc_sp(th=None, hdh=None, ram=None, dl=None, trang=0):
    with app.app_context():
        ttsp = db.session.query(ThongTin.id, ThongTin.ThuongHieu, ThongTin.HeDieuHanh, ThongTin.Ram, ThongTin.DungLuong) \
            .join(SanPham, SanPham.thongtin_id.__eq__(ThongTin.id)).filter(SanPham.TinhTrang.__eq__(True))
        if th:
            ttsp = ttsp.filter(ThongTin.ThuongHieu.contains(th))
        if hdh:
            ttsp = ttsp.filter(ThongTin.HeDieuHanh.contains(hdh))
        if ram:
            ttsp = ttsp.filter(ThongTin.Ram.contains(ram))
        if dl:
            ttsp = ttsp.filter(ThongTin.DungLuong.contains(dl))
        if trang:
            if trang > 0:
                ttsp = ttsp.limit(5).offset(trang * 5 - 5)
        li = []
        for i in ttsp:
            li.append(load_sp(id=i[0]))
        return li


def phantrang(x):
    n = len(x)
    trang = n // 5
    du = n - trang * 5
    if du > 0:
        trang = trang + 1
    return trang


def load_sp_id(id=None):
    sp = db.session.query(SanPham.id, SanPham.Ten, SanPham.GiaBan, SanPham.DaBan, ThongTin.MoTa,
                          ThongTin.ThuongHieu, ThongTin.ManHinh
                          , ThongTin.HeDieuHanh, ThongTin.Chip, ThongTin.Ram, ThongTin.DungLuong) \
        .join(ThongTin, SanPham.thongtin_id.__eq__(ThongTin.id), isouter=True).filter(SanPham.TinhTrang.__eq__(True))
    if id:
        sp = sp.filter(SanPham.id.__eq__(id))
    return sp.all()


def load_tim(user=None):
    m = db.session.query(func.min(Anh.id).label('id'), Anh.sanpham).group_by(Anh.sanpham).cte('m')
    tim = db.session.query(SanPham.id, SanPham.Ten, SanPham.GiaBan, Anh.Anh.label('Anh')) \
        .join(Anh, Anh.sanpham.__eq__(SanPham.id)).join(m, Anh.id == m.c.id).join(Thich,
                                                                                  Thich.sanpham.__eq__(SanPham.id)) \
        .filter(Thich.taikhoan.__eq__(user))
    return tim.all()


def load_tim_id(id=None, user=None):
    tim = db.session.query(Thich.taikhoan, Thich.sanpham).filter(Thich.sanpham.__eq__(id), Thich.taikhoan.__eq__(user)) \
        .first()
    return tim


def huy_tim(id=None, user=None):
    tim = Thich.query.filter_by(taikhoan=user, sanpham=id).first()
    if not tim:
        t = Thich(taikhoan=user, sanpham=id)
        db.session.add(t)
        db.session.commit()
    else:
        db.session.delete(tim)
        db.session.commit()


def load_binh_luan(id, max=None):
    bl = db.session.query(BinhLuan.id, BinhLuan.NgayTao, BinhLuan.NoiDung, BinhLuan.DanhGia,
                          TaiKhoan.AnhDaiDien, ThongTinTaiKhoan.Ho, ThongTinTaiKhoan.Ten,
                          BinhLuan.taikhoan.label('tkid')) \
        .filter(BinhLuan.sanpham.__eq__(id)) \
        .join(TaiKhoan, TaiKhoan.id.__eq__(BinhLuan.taikhoan)) \
        .join(ThongTinTaiKhoan, ThongTinTaiKhoan.id.__eq__(TaiKhoan.id)).order_by(desc(BinhLuan.NgayTao))

    if max:
        bl = bl.limit(max)
    return bl.all()


def add_dg(id_sp, user_id, danhgia, nd, id=None):
    if id:
        bl = BinhLuan.query.filter_by(id=id).first()
        bl.NgayTao = datetime.datetime.now()
        bl.NoiDung = nd
        bl.DanhGia = danhgia
        db.session.commit()
    else:
        bl = BinhLuan(NgayTao=datetime.datetime.now(), NoiDung=nd, DanhGia=danhgia, sanpham=id_sp, taikhoan=user_id)
        db.session.add(bl)
        db.session.commit()


def delete_dg(id):
    bl = BinhLuan.query.filter_by(id=id).first()
    db.session.delete(bl)
    db.session.commit()


def load_anh_sp(id=None):
    a = db.session.query(Anh.id, Anh.Anh)
    if id:
        a = a.filter(Anh.sanpham.__eq__(id))
    return a.all()


def get_tk_id(user_id):
    return TaiKhoan.query.get(user_id)


def user_check(user, password, role=None):
    if user and password:
        a = TaiKhoan.query.filter(TaiKhoan.TenDanhNhap.__eq__(user),
                                  TaiKhoan.Matkhau.__eq__(password),
                                  TaiKhoan.VaiTro.__eq__(role),
                                  TaiKhoan.TinhTrang.__eq__(True)).first()
    return a


def user_load_infor(id=None):
    a = db.session.query(TaiKhoan.TenDanhNhap, TaiKhoan.Matkhau, TaiKhoan.AnhDaiDien, ThongTinTaiKhoan.Ho,
                         ThongTinTaiKhoan.Ten,
                         ThongTinTaiKhoan.DiaChi, ThongTinTaiKhoan.Email, ThongTinTaiKhoan.SDT) \
        .join(ThongTinTaiKhoan, TaiKhoan.thongtintk.__eq__(ThongTinTaiKhoan.id), isouter=True) \
        .filter(TaiKhoan.id.__eq__(id)).first()
    return a


def user_add(user, password, Ho, Ten, DiaChi, Email, SDT):
    tttk = ThongTinTaiKhoan(Ho=Ho, Ten=Ten, DiaChi=DiaChi, Email=Email, SDT=SDT)
    db.session.add(tttk)
    db.session.commit()
    id = tttk.id
    tk = TaiKhoan(TenDanhNhap=user, Matkhau=password, VaiTro=UserRole.normal_user, thongtintk=id)
    db.session.add(tk)
    db.session.commit()


def user_update(id, password, Ho, Ten, DiaChi, Email, SDT, Anh):
    tk = TaiKhoan.query.filter_by(id=id).first()
    a = tk.AnhDaiDien
    tttk = ThongTinTaiKhoan.query.filter_by(id=id).first()
    tk.Matkhau = password
    if Anh:
        tk.AnhDaiDien = Anh
    else:
        tk.AnhDaiDien = a
    tttk.Ho = Ho
    tttk.Ten = Ten
    tttk.DiaChi = DiaChi
    tttk.Email = Email
    tttk.SDT = SDT
    db.session.commit()


def add_sp_to_gh(id_sp, id_user, sl, tt=0):
    gh = GioHang.query.filter_by(tk=id_user, DaTT=False).first()
    if gh:
        slct = ChiTietGioHang.query.filter_by(sanpham=id_sp, giohang=gh.id).first()
        if slct:
            if tt == 0:
                x = int(slct.SoLuong) + int(sl)
            else:
                x = int(sl)
            slct.SoLuong = x
            db.session.commit()
        else:
            ctgh = ChiTietGioHang(SoLuong=sl, sanpham=id_sp, giohang=gh.id)
            db.session.add(ctgh)
            db.session.commit()
    else:
        gh = GioHang(tk=id_user)
        db.session.add(gh)
        db.session.commit()
        gh = GioHang.query.filter_by(tk=id_user, DaTT=False).first()
        ctgh = ChiTietGioHang(SoLuong=sl, sanpham=id_sp, giohang=gh.id)
        db.session.add(ctgh)
        db.session.commit()


def delete_sp_to_gh(id_sp, id_user):
    gh = GioHang.query.filter_by(tk=id_user, DaTT=False).first()
    if gh:
        slct = ChiTietGioHang.query.filter_by(sanpham=id_sp, giohang=gh.id).first()
        if slct:
            db.session.delete(slct)
            db.session.commit()


def load_gh(id):
    gh = GioHang.query.filter_by(tk=id, DaTT=False).first()
    if gh:
        m = db.session.query(func.min(Anh.id).label('Aid'), Anh.sanpham).group_by(Anh.sanpham).cte('m')
        ctgh = db.session.query(ChiTietGioHang.id, ChiTietGioHang.Ngay, ChiTietGioHang.SoLuong,
                                ChiTietGioHang.sanpham, SanPham.Ten, Anh.Anh.label('Anh'), SanPham.GiaBan) \
            .filter(ChiTietGioHang.giohang.__eq__(gh.id)) \
            .join(SanPham, ChiTietGioHang.sanpham.__eq__(SanPham.id)) \
            .join(Anh, Anh.sanpham.__eq__(SanPham.id)).join(m, Anh.id == m.c.Aid)
        return ctgh.all()
    else:
        gh = GioHang(tk=id)
        db.session.add(gh)
        db.session.commit()
        load_gh(id)


def thanh_toan(user_id, tg):
    gh = GioHang.query.filter_by(tk=user_id, DaTT=False).first()
    if gh:
        gh.DaTT = True
        gh.TrangThai = True
        gh.TongGia = tg
        db.session.commit()


def lich_su(user_id):
    gh = db.session.query(GioHang.id, GioHang.NgayTao, GioHang.DaTT, GioHang.TrangThai, GioHang.TongGia).filter(
        GioHang.tk.__eq__(user_id)).filter(GioHang.TrangThai.__eq__(True))
    return gh.all()


def xoa_lich_su(id):
    gh = GioHang.query.filter_by(id=id).first()
    if gh:
        ctgh = ChiTietGioHang.query.filter_by(giohang=id).first()
        while ctgh:
            db.session.delete(ctgh)
            db.session.commit()
            ctgh = ChiTietGioHang.query.filter_by(giohang=id).first()
    db.session.delete(gh)
    db.session.commit()
