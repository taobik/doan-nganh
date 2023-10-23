from flask import render_template, request, redirect, session, jsonify, url_for
from webbanshang import utils
from flask_login import login_user, logout_user, login_required, current_user
from webbanshang.models import UserRole
from webbanshang import app
from datetime import datetime
import cloudinary.uploader


def home():
    session['trangnow'] = 1
    dh = None
    if current_user.is_authenticated:
        user_id = current_user.id
        dh = utils.load_gh(user_id)
    err_msg = request.args.get('err_msg')
    loai = utils.load_cate()
    sp = utils.load_sp(max=7)
    sp1 = utils.load_sp(cate=1, max=5)
    sp2 = utils.load_sp(cate=2, max=5)
    sp3 = utils.load_sp(cate=3, max=5)
    sp4 = utils.load_sp(cate=4, max=5)
    return render_template("index.html",
                           loai=loai,
                           sp=sp,
                           sp1=sp1, sp2=sp2, sp3=sp3, sp4=sp4,
                           err_msg=err_msg, dh=dh)


def phantrang():
    data = request.get_json()
    tr = data['tr']
    session['trangnow'] = int(tr)
    if not session.get('trangnow'):
        session['trangnow'] = 0
    return jsonify(data)


def sanpham(cate):
    dh = None
    loai = utils.load_cate()
    sp = utils.load_sp(cate=cate)
    li = utils.phantrang(sp)
    n = session.get('trangnow')
    if not n:
        n = 1
    sp = utils.load_sp(cate=cate, trang=n)
    session.pop("trangnow", default=1)
    if current_user.is_authenticated:
        user_id = current_user.id
        dh = utils.load_gh(user_id)
    return render_template("tatcasanpham.html",
                           loai=loai,
                           sp=sp, dh=dh, li=li)


def sanpham_loc():
    dh = None
    spl = None
    sp=None
    loai = utils.load_cate()
    data = session.get('loc')
    if request.method == 'POST':
        kw = request.form['kw']
        if kw:
            print("0")
            spl = utils.load_sp(kw=kw)
            li = utils.phantrang(spl)
            n = session.get('trangnow')
            if not n:
                n = 1
            spl = utils.load_sp(kw=kw, trang=n)
            session.pop("trangnow", default=1)
    if data:
        spl = utils.loc_sp(th=data['th'], hdh=data['hdh'], ram=data['r'], dl=data['dl'])
        print("1")
        li = utils.phantrang(spl)
        n = session.get('trangnow')
        if not n:
            n = 1
        spl = utils.loc_sp(th=data['th'], hdh=data['hdh'], ram=data['r'], dl=data['dl'], trang=n)
        session.pop("trangnow", default=1)
    else:
        sp = utils.load_sp()
        li = utils.phantrang(sp)
        n = session.get('trangnow')
        if not n:
            n = 1
        sp = utils.load_sp(trang=n)
        session.pop("trangnow", default=1)
        # li = 1
        # # n = session.get('trangnow')
        # # spl = utils.loc_sp(trang=n)
        # session['trangnow'] = 1
        # spl = []
    if current_user.is_authenticated:
        user_id = current_user.id
        dh = utils.load_gh(user_id)
    return render_template("tatcasanpham.html",
                           loai=loai,
                           spl=spl, dh=dh, li=li, sp=sp)


def sanpham_tim():
    dh = None
    sp = None
    li = 1
    print("tim")
    loai = utils.load_cate()
    if request.method == 'POST':
        kw = request.form['kw']
        if kw:
            sp = utils.load_sp(kw=kw)
            li = utils.phantrang(sp)
            n = session.get('trangnow')
            if not n:
                n = 1
            sp = utils.load_sp(kw=kw, trang=n)
            session.pop("trangnow", default=1)
        else:
            sp = utils.load_sp()
            li = utils.phantrang(sp)
            n = session.get('trangnow')
            if not n:
                n = 1
            sp = utils.load_sp(kw=kw, trang=n)
            session.pop("trangnow", default=1)
    if current_user.is_authenticated:
        user_id = current_user.id
        dh = utils.load_gh(user_id)
    return render_template("tatcasanpham.html",
                           loai=loai,
                           sp=sp, dh=dh, li=li)


def loc_sp():
    session['loc'] = 0
    data = request.get_json()
    th = data['th']
    hdh = data['hdh']
    r = data['r']
    dl = data['dl']
    c = utils.loc_sp(th=th, hdh=hdh, ram=r, dl=dl)
    if c:
        session['loc'] = data
    else:
        session['loc'] = []
        # session.pop('loc', default=None)
    return jsonify(data)


def chitiet(id):
    tim = None
    bl = utils.load_binh_luan(id, max=10)
    err_msg = session.get('errmsg')
    color = session.get('color')
    loai = utils.load_cate()
    a = utils.load_anh_sp(id)
    sp = utils.load_sp_id(id)
    bl = utils.load_binh_luan(id, max=10)
    sp_cate = utils.load_sp(id_cate=id)
    dh = None
    if current_user.is_authenticated:
        user_id = current_user.id
        dh = utils.load_gh(user_id)
        tim = utils.load_tim_id(id=id, user=user_id)
    session.pop('color', default=None)
    session.pop('errmsg', default=None)
    return render_template("chitiet.html",
                           loai=loai,
                           anh=a,
                           sp=sp, bl=bl,
                           sp_cate=sp_cate,
                           err_msg=err_msg, color=color, dh=dh, tim=tim)


def tim(id):
    data = request.get_json()
    id = data['id']
    if current_user.is_authenticated:
        user_id = current_user.id
    utils.huy_tim(id=id, user=user_id)
    return jsonify(data)


def gui_danh_gia(id):
    data = request.get_json()
    c = None
    id = data['id']
    id_sp = data['id_sp']
    tk = current_user.id
    danhgia = data['sao']
    nd = data['dg']
    if id:
        utils.add_dg(id_sp=id_sp, user_id=tk, danhgia=danhgia, nd=nd, id=id)
    else:
        utils.add_dg(id_sp=id_sp, user_id=tk, danhgia=danhgia, nd=nd)
    return jsonify(data)


def xoa_danh_gia(id):
    data = request.get_json()
    id = data['id']
    utils.delete_dg(id)
    return jsonify(data)


def dangnhap():
    err_msg = request.args.get('err_msg')
    color = request.args.get('color')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['passw']
        user = utils.user_check(user=username, password=password, role=UserRole.normal_user)
        if user:
            err_msg = "Đăng nhập thành công"
            login_user(user)
            color = "green"
            return redirect(url_for('home', err_msg=err_msg, color=color))
        else:
            err_msg = "Đăng nhập thất bại!! Hãy thử lại sau"
            color = "red"
    return render_template("dangnhap.html", err_msg=err_msg, color=color)


def dangky():
    err_msg = request.args.get('err_msg')
    color = request.args.get('color')
    if request.method == 'POST':
        username = request.form['username']
        Ho = request.form['Ho']
        Ten = request.form['Ten']
        DiaChi = request.form['DiaChi']
        Email = request.form['Email']
        SDT = request.form['SDT']
        pas = request.form['pas']

        user = utils.user_check(user=username, password=pas)
        if user:
            err_msg = "Đăng ký thất bại!! Tên tài khoản đã tồn tại"
            color = "red"
            return redirect(url_for('dangky', err_msg=err_msg, color=color))
        else:
            utils.user_add(username, pas, Ho, Ten, DiaChi, Email, SDT)
            err_msg = "Đăng ký thành công"
            color = "green"
            return redirect(url_for('dangnhap', err_msg=err_msg, color=color))
    # return render_template("index.css", err_msg=err_msg)
    return render_template("dangky.html", err_msg=err_msg, color=color)


def thongtintaikhoan():
    id = current_user.id
    loai = utils.load_cate()
    dh = None
    lsdh = None
    if current_user.is_authenticated:
        user_id = current_user.id
        dh = utils.load_gh(user_id)
        lsdh = utils.lich_su(user_id)
        tim = utils.load_tim(user_id)
    if request.method == 'POST':
        pas = request.form['pasw']
        Ho = request.form['Ho']
        Ten = request.form['Ten']
        DiaChi = request.form['DiaChi']
        Email = request.form['Email']
        SDT = request.form['SDT']
        Anh = request.files.get('avatar')
        if Anh:
            res = cloudinary.uploader.upload(Anh)
            link = res['secure_url']
            utils.user_update(id, pas, Ho, Ten, DiaChi, Email, SDT, Anh=link)
        else:
            utils.user_update(id, pas, Ho, Ten, DiaChi, Email, SDT, Anh=None)
    user = utils.user_load_infor(id)
    return render_template("thongtintaikhoan.html", user=user, loai=loai, dh=dh, lsdh=lsdh, tim=tim)


def dathang(id):
    err_msg = request.args.get('errmsg')
    data = request.get_json()
    id = data['id']
    sl = data['sl']
    user_id = current_user.id
    if current_user.is_authenticated:
        utils.add_sp_to_gh(id_sp=id, id_user=user_id, sl=sl)
        err_msg = "Đặt hàng thành công"
        color = "green"
        session['errmsg'] = err_msg
        session['color'] = "green"
    else:
        err_msg = "Bạn cần đăng nhập để đặt hàng"
        color = "red"
        session['errmsg'] = err_msg
        session['color'] = "red"
    return jsonify(data)


def dathang_check():
    err_msg = "Bạn cần đăng nhập để đặt hàng"
    color = "red"
    return redirect(url_for('dangnhap', err_msg=err_msg, color=color))


def update_gio(id):
    data = request.get_json()
    sl = data['sl']
    user_id = current_user.id
    c = utils.add_sp_to_gh(id_sp=id, id_user=user_id, sl=sl, tt=1)
    return jsonify(c)


def xoa_hang(id_sp):
    id = current_user.id
    loai = utils.load_cate()
    user = utils.user_load_infor(id)
    utils.delete_sp_to_gh(id_sp, id)
    dh = None
    if current_user.is_authenticated:
        user_id = current_user.id
        dh = utils.load_gh(user_id)
    return render_template("thongtintaikhoan.html", user=user, loai=loai, dh=dh)


def xoa_ls(id_sp):
    utils.xoa_lich_su(id_sp)
    return redirect(url_for('thongtintaikhoan'))


def thanh_toan(user_id):
    data = request.get_json()
    tg = data['tg']
    c = utils.thanh_toan(user_id=user_id, tg=tg)
    return jsonify(c)


def dangxuat():
    logout_user()
    return redirect(url_for('home'))


def admin_use():
    return redirect('/admin')
