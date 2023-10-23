
var li = document.querySelectorAll(".cate_list > ul > li");
for(i = 1; i<li.length;i++){
    li[i].classList.remove("active");
};

var pas1 = document.querySelector(".body__main__taikhoan__infor__infor > table tr:nth-child(2) > td:nth-child(2) > div > i:nth-child(1)");
var pas2 = document.querySelector(".body__main__taikhoan__infor__infor > table tr:nth-child(2) > td:nth-child(2) > div > i:nth-child(2)");
var ip = document.querySelector("#pasw");
pas1.style.display ='none'
pas2.style.display ='block'
pas1.style.display ='none'
ip.type = 'password'
pas1.addEventListener('click', function(e){
    pas2.style.display ='block'
    pas1.style.display ='none'
    ip.type = 'password'
});
pas2.addEventListener('click', function(e){
    pas2.style.display ='none'
    pas1.style.display ='block'
    ip.type = 'text'
});

var l = document.querySelectorAll(".body__list__item > ul > li");
var hs = document.querySelector(".body__main__taikhoan");
var dh = document.querySelector(".body__main__donhang");
var lsmh = document.querySelector(".body__main__lichsu");
var yt = document.querySelector(".body__main__yeuthich");

var n = sessionStorage.getItem("chose");
if(n == 1){
    hs.style.display= "none"
    dh.style.display= "block"
    lsmh.style.display= "none"
    yt.style.display= "none"
}
if(n == 0){
    dh.style.display= "none"
    hs.style.display= "block"
    lsmh.style.display= "none"
    yt.style.display= "none"
}
if(n == 2){
    dh.style.display= "none"
    hs.style.display= "none"
    lsmh.style.display= "block"
    yt.style.display= "none"
}
if(n == 3){
    dh.style.display= "none"
    hs.style.display= "none"
    lsmh.style.display= "none"
    yt.style.display= "block"
}


l.forEach((i)=>{
    i.addEventListener('click', function(e){
        if (e.target == l[0] || e.target.parentNode == l[0]){
            hs.style.display= "block"
            dh.style.display= "none"
            lsmh.style.display= "none"
            yt.style.display= "none"
            sessionStorage.setItem("chose", "0");
        }
        if (e.target == l[1] || e.target.parentNode == l[1]){
            hs.style.display= "none"
            dh.style.display= "block"
            lsmh.style.display= "none"
            yt.style.display= "none"
            sessionStorage.setItem("chose", "1");
        }
        if (e.target == l[2] || e.target.parentNode == l[2]){
            hs.style.display= "none"
            dh.style.display= "none"
            lsmh.style.display= "block"
            yt.style.display= "none"
            sessionStorage.setItem("chose", "2");
        }
        if (e.target == l[3] || e.target.parentNode == l[3]){
            dh.style.display= "none"
            hs.style.display= "none"
            lsmh.style.display= "none"
            yt.style.display= "block"
            sessionStorage.setItem("chose", "3");
        }
    });
});

a = []
kq = []
var gia = document.querySelectorAll(".body__main__donhang__body .Ten p:nth-child(2)");
for (i=0;i<gia.length;i++){
    a[i] = gia[i].innerText.replace(".", "");
    a[i] = a[i].replace(".", "");
}
var sluong = document.querySelectorAll(".body__main__donhang__body .so_luong .amout_so");
var gt = document.querySelectorAll(".body__main__donhang__body .so_luong .gt");
var rs = document.querySelectorAll(".body__main__donhang__body .gia p:nth-child(2)");
if(sluong){
    for (i=0;i<sluong.length;i++){
        kq[i] = parseInt(sluong[i].value) * parseInt(a[i])
        rs[i].innerText = new Intl.NumberFormat().format(kq[i]) + "đ"
    }
}

sluong.forEach((i)=>{
    i.addEventListener("input", function(e){
        var c = parseInt(i.classList[1])
        for(ll = 0;ll<sluong.length;ll++){
            if(sluong[ll].classList[1] == c){
                if(!sluong[ll].value){
                    sluong[ll].value = 0
                }
                kq = parseInt(i.value) * parseInt(a[ll])
                rs[ll].innerText = new Intl.NumberFormat().format(kq) + "đ"
                break
            }
        }
    });
});

var bt_tru = document.querySelectorAll(".body__main__donhang__body .so_luong .tru");
var bt_cong = document.querySelectorAll(".body__main__donhang__body .so_luong .cong");
var soluo = document.querySelectorAll(".header .giohang .list .infor p span");
bt_tru.forEach((i)=>{
    i.addEventListener("click", function(e){
        n = parseInt(i.classList[1]);
        for(ll = 0;ll<bt_tru.length;ll++){
            if(bt_tru[ll].classList[1] == n){
                gtt = parseInt(sluong[ll].value)
                console.log(gtt)
                id_sp = gt[ll].value
                if(gtt>0){
                    sluong[ll].value = gtt - 1;
                }
                if(gtt<0){
                    sluong[ll].value = 0;
                }
                kq = parseInt(sluong[ll].value) * parseInt(a[ll])
                rs[ll].innerText = new Intl.NumberFormat().format(kq) + "đ"
                    fetch('/api/up_hang/'+id_sp, {
                        method: 'post',
                        body: JSON.stringify ({
                            'id': id_sp,
                            'sl': sluong[ll].value
                        }),
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    }).then(res => res.json()).then((data) => {
                        location.reload();
                    }).catch(function(err) {
                        console.error(err)
                    })
                }
            }
    });
});
bt_cong.forEach((i)=>{
    i.addEventListener("click", function(e){
        n = parseInt(i.classList[1]);
        for(ll = 0;ll<bt_tru.length;ll++){
            if(bt_tru[ll].classList[1] == n){
                gtt = parseInt(sluong[ll].value)
                id_sp = gt[ll].value
                sluong[ll].value = gtt + 1;
                kq = parseInt(sluong[ll].value) * parseInt(a[ll])
                rs[ll].innerText = new Intl.NumberFormat().format(kq) + "đ"
                    fetch('/api/up_hang/'+id_sp, {
                        method: 'post',
                        body: JSON.stringify ({
                            'id': id_sp,
                            'sl': sluong[ll].value
                        }),
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    }).then(res => res.json()).then((data) => {
                        location.reload();
                    }).catch(function(err) {
                        console.error(err)
                    })
                }
            }
    });
});

var sum = document.querySelectorAll(".body__main__taikhoan .tong p span");
var sum_sp = 0
var sum_tien = 0
for(ll = 0;ll<sluong.length;ll++){
    sum_sp = sum_sp + parseInt(sluong[ll].value)
    aa = rs[ll].innerText.replace(",", "");
    aa = aa.replace(",", "");
    sum_tien = sum_tien + parseInt(aa)
}
sum[0].innerText = sum_sp + " sản phẩm"
sum[1].innerText = new Intl.NumberFormat().format(sum_tien) + "đ"

var thanh_toan = document.querySelector(".xacnhan_thanhtoan .thongtin .btn a");
var ttcl = parseInt(thanh_toan.classList[1])
thanh_toan.addEventListener("click",function(){
    if(parseInt(sum[1].innerText) > 0){
        fetch('/api/thanh_toan/'+ttcl, {
            method: 'post',
            body: JSON.stringify ({
                'tg': sum[1].innerText
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(response => response.json()).then((data) => {
            location.reload();
        }).catch(function(err) {
            console.error(err)
        })
    }
});
var xntt = document.querySelector(".xacnhan_thanhtoan");
var xn = document.querySelector(".xacnhan_thanhtoan .xacnhan");
var thanh_toan = document.querySelector("body > div.container > div.body > form > div > div.body__main__donhang > div > div.tong > .thanh_toan");
console.log(thanh_toan)
xntt.addEventListener("click", function(){
    xn.classList.remove('slide')
    xntt.style.display = "none"
})
thanh_toan.addEventListener("click", function(){
    xntt.style.display = "block"
    xn.classList.add('slide')
    console.log("ok")
})

var xn_tsp = document.querySelector(".xacnhan_thanhtoan .thongtin .ssp p:nth-child(2)");
var xn_tt = document.querySelector(".xacnhan_thanhtoan .thongtin .ttien p:nth-child(2)");
xn_tsp.innerText = sum_sp + " sản phẩm"
xn_tt.innerText = new Intl.NumberFormat().format(sum_tien) + "đ"