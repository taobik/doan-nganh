from flask import render_template, request, redirect, session, jsonify, url_for
from webbanshang import admin_utils, utils
from flask_login import login_user, logout_user, login_required, current_user
from webbanshang.models import UserRole
from datetime import datetime
import cloudinary.uploader


def home():
    if not current_user.is_authenticated or current_user.VaiTro != UserRole.admin:
        return redirect(url_for('admin_login'))
    else:
        kq = admin_utils.doanhthu()
        cate = admin_utils.load_loai()
        dtthl = admin_utils.doanhthu_thang()[0::2]
        dtthdt = admin_utils.doanhthu_thang()[1::2]
        top_kh = admin_utils.top_khachhang()
        top_sp = admin_utils.top_sanpham()
    return render_template("admin/index.html",
                           kq=kq, cate=cate, dtthl=dtthl, dtthdt=dtthdt, top_kh=top_kh, top_sp=top_sp)


def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['passw']
        user = utils.user_check(user=username, password=password, role=UserRole.admin)
        if user:
            login_user(user)
            return redirect(url_for('admin'))
    return render_template("admin/login.html")


def dangxuat():
    logout_user()
    return redirect(url_for('admin_login'))


def sanpham():
    loai = admin_utils.load_loai()
    kw = session.get('kw')
    loaijs = session.get('loai')
    sp = admin_utils.load_sp(kw, loaijs)
    session['kw'] = None
    session['loai'] = None

    return render_template("admin/sanpham.html",
                           sp=sp, loai=loai)


def tim_sanpham(kw=None, loai=None):
    data = request.get_json()
    kwjs = data['kw']
    loaijs = data['loai']
    if kwjs:
        kw = kwjs
    if loaijs:
        loai = loaijs
    session['kw'] = kw
    session['loai'] = loai
    return jsonify(data)


def sanpham_add():
    loai = admin_utils.load_loai()
    if request.method == 'POST':
        ten_sp = request.form['ten_sp']
        loai = request.form.get('loai_select')
        if request.form['loai']:
            loai = request.form['loai']
        a = request.files.get('anh')
        if a:
            res = cloudinary.uploader.upload(a)
            anh = res['secure_url']
        gia_nhap = request.form['gia_nhap']
        gia_ban = request.form['gia_ban']
        sl = request.form['so_luong']
        mo_ta = request.form['mo_ta']
        th = request.form['thuong_hieu']
        mh = request.form['man_hinh']
        hdh = request.form['hdh']
        chip = request.form['chip']
        ram = request.form['ram']
        dluong = request.form['duong_luong']
        admin_utils.add_sp(ten_sp, loai, anh, gia_nhap, gia_ban, sl, mo_ta, th, mh, hdh, chip, ram, dluong)
        return redirect(url_for('admin_sanpham'))
    return render_template("admin/sanpham_add_edit.html",
                           loai=loai)


def sanpham_view(id):
    sp = admin_utils.load_sp_all(id)
    bl = admin_utils.binh_luan(id)
    mua = admin_utils.tinh_sp(id)
    mua_loai = admin_utils.tinh_sp_trong_loai(id)
    return render_template("admin/sanpham_view.html",
                           sp=sp, bl=bl, mua=mua, mua_loai=mua_loai)


def xoa_binhluan(id):
    data = request.get_json()
    id = data['id']
    admin_utils.xoa_binh_luan(id)
    return jsonify(data)


def sanpham_edit(id):
    loai = admin_utils.load_loai()
    if request.method == 'POST':
        ten_sp = request.form['ten_sp']
        loai = request.form.get('loai_select')
        if request.form['loai']:
            loai = request.form['loai']
        a = request.files.get('anh')
        anh = request.files.get('anh_cu')
        if a:
            res = cloudinary.uploader.upload(a)
            anh = res['secure_url']
        gia_nhap = request.form['gia_nhap']
        gia_ban = request.form['gia_ban']
        sl = request.form['so_luong']
        mo_ta = request.form['mo_ta']
        th = request.form['thuong_hieu']
        mh = request.form['man_hinh']
        hdh = request.form['hdh']
        chip = request.form['chip']
        ram = request.form['ram']
        dluong = request.form['duong_luong']
        admin_utils.add_sp(ten_sp, loai, anh, gia_nhap, gia_ban, sl, mo_ta, th, mh, hdh, chip, ram, dluong, tt=id)
        return redirect(url_for('admin_sanpham'))
    sp_edit = admin_utils.load_sp_all(id)
    return render_template("admin/sanpham_add_edit.html",
                           loai=loai, sp_edit=sp_edit)


def sanpham_delete(id):
    admin_utils.delete_sp(id)
    return redirect(url_for('admin_sanpham'))


def hoat_dong():
    data = request.get_json()
    id = data['id']
    admin_utils.hoat_dong(id)
    return jsonify(data)


def khach_hang():
    kh = admin_utils.load_khach_hang()
    return render_template("admin/khachhang.html",
                           kh=kh)


def khachhang_view(id):
    kh = admin_utils.load_khach_hang_all(id)
    bl = admin_utils.binh_luan_khach(id)
    mua = admin_utils.tinh_sp_kh(id)
    return render_template("admin/khachhang_view.html",
                           kh=kh, bl=bl, mua=mua)


def khachhang_delete(id):
    admin_utils.delete_kh(id)
    return redirect(url_for('admin_khachhang'))


def hd_khach_hang():
    data = request.get_json()
    id = data['id']
    admin_utils.hd_khach_hang(id)
    return jsonify(data)
