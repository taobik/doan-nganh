from webbanshang import app, controller, admin_controller, login, utils
from flask import render_template

app.add_url_rule("/", "home", controller.home)
app.add_url_rule("/sanpham", "sanpham_loc", controller.sanpham_loc)
app.add_url_rule("/sanpham/<int:cate>", "sanpham", controller.sanpham)
app.add_url_rule("/sanpham_tim", "tim_sp", controller.sanpham_tim, methods=['get', 'post'])
app.add_url_rule("/api/sanpham/loc", "loc_sp", controller.loc_sp, methods=['get', 'post'])
app.add_url_rule("/chitiet/<int:id>", "chitiet", controller.chitiet)
app.add_url_rule("/chitiet_tim/<int:id>", "tim", controller.tim, methods=['get', 'post'])
app.add_url_rule("/sanpham/phantrang", "phantrang", controller.phantrang, methods=['get', 'post'])
app.add_url_rule("/dangnhap", "dangnhap", controller.dangnhap, methods=['get', 'post'])
app.add_url_rule("/dangky", "dangky", controller.dangky, methods=['get', 'post'])
app.add_url_rule("/thongtintaikhoan", "thongtintaikhoan", controller.thongtintaikhoan, methods=['get', 'post'])
app.add_url_rule("/chitiet/dathang/<int:id>", "dathang", controller.dathang, methods=['get', 'post'])
app.add_url_rule("/chitiet/dathang_check", "dathang_check", controller.dathang_check, methods=['get', 'post'])
app.add_url_rule("/xoa_hang/<int:id_sp>", "xoa_hang", controller.xoa_hang)
app.add_url_rule("/thongtintaikhoan/<id_sp>", "xoa_ls", controller.xoa_ls)
app.add_url_rule("/dangxuat", "dangxuat", controller.dangxuat)
app.add_url_rule("/api/up_hang/<int:id>", "up_hang", controller.update_gio, methods=['get', 'post'])
app.add_url_rule("/api/sanpham/loc", "loc_sp", controller.loc_sp, methods=['get', 'post'])
app.add_url_rule("/api/thanh_toan/<int:user_id>", "thanh_toan", controller.thanh_toan, methods=['get', 'post'])
app.add_url_rule("/api/gui_danh_gia/<int:id>", "gui_danh_gia", controller.gui_danh_gia, methods=['get', 'post'])
app.add_url_rule("/api/xoa_danh_gia/<int:id>", "xoa_danh_gia", controller.xoa_danh_gia, methods=['get', 'post'])


app.add_url_rule("/admin", "admin", admin_controller.home)
app.add_url_rule("/admin_login", "admin_login", admin_controller.login, methods=['get', 'post'])
app.add_url_rule("/admin_dangxuat", "admin_dangxuat", admin_controller.dangxuat)
app.add_url_rule("/admin/sanpham", "admin_sanpham", admin_controller.sanpham)
app.add_url_rule("/admin/add_sanpham", "admin_add_sanpham", admin_controller.sanpham_add, methods=['get', 'post'])
app.add_url_rule("/admin/view_sanpham/<int:id>", "admin_view_sanpham", admin_controller.sanpham_view)
app.add_url_rule("/admin/edit_sanpham/<int:id>", "admin_edit_sanpham", admin_controller.sanpham_edit,
                 methods=['get', 'post'])
app.add_url_rule("/admin/delete_sanpham/<int:id>", "admin_delete_sanpham", admin_controller.sanpham_delete,
                 methods=['get', 'post'])
app.add_url_rule("/admin/khachhang", "admin_khachhang", admin_controller.khach_hang)
app.add_url_rule("/admin/view_khachhang/<int:id>", "admin_view_khachhang", admin_controller.khachhang_view)
app.add_url_rule("/admin/delete_khachhang/<int:id>", "admin_delete_khachhang", admin_controller.khachhang_delete,
                 methods=['get', 'post'])
app.add_url_rule("/api/admin/tim_sanpham", "tim_sanpham", admin_controller.tim_sanpham, methods=['get', 'post'])
app.add_url_rule("/api/admin/loc_sanpham", "loc_sanpham", admin_controller.tim_sanpham, methods=['get', 'post'])
app.add_url_rule("/api/admin/sanpham/huy_hd", "hoat_dong", admin_controller.hoat_dong, methods=['get', 'post'])
app.add_url_rule("/api/admin/khachhang/huy_hd", "khach_hang", admin_controller.hd_khach_hang, methods=['get', 'post'])
app.add_url_rule("/api/admin/xoa_binhluan/<int:id>", "xoa_binhluan", admin_controller.xoa_binhluan, methods=['get', 'post'])



@login.user_loader
def load_user(user_id):
    return utils.get_tk_id(user_id=user_id)


if __name__ == '__main__':
    app.run(debug=True)
