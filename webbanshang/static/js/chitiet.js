var li = document.querySelectorAll(".cate_list > ul > li");
for(i = 1; i<li.length;i++){
    li[i].classList.remove("active");
};

var err = document.querySelector(".err");
if(err != null){
setTimeout(function(){
    err.classList.add("errback")
}, 100)
setTimeout(function(){
    err.classList.remove("errback")
    err.remove()
}, 3000)
}

var image = document.querySelectorAll(".chitiet > .ttgioithieu > .thongtin > .anh > .phu > .anh_phu");
var main = document.querySelectorAll(".chitiet > .ttgioithieu > .thongtin > .anh > .chinh > .anh_chinh")
var x = 0,y=0,p = 0;
image[0].classList.add("chosen")
image.forEach((i) => {
    i.addEventListener("click", function(e){
    var chose = document.querySelector(".chitiet > .ttgioithieu > .thongtin > .anh > .phu > .chosen");
    for(i=0;i<image.length;i++){
        if (image[i].style.backgroundImage == chose.style.backgroundImage){
            y = i;
        }
        image[i].classList.remove("chosen")
        if (image[i].style.backgroundImage == e.target.style.backgroundImage){
            x = i
        }
    }
    e.target.classList.add("chosen")
    if (x>y){
        p = p-(x-y)*100
    }
    else{
        p = p+(x-y)*-100
    }
    for(i=0;i<main.length;i++){
        main[i].style.transform = 'translateX(' + p + '%)';
    }
    });
});
var bt = document.querySelectorAll(".chitiet > .ttgioithieu > .thongtin > .coban .so_luong > div");
bt[0].addEventListener("click", function(e){
    var so = document.querySelector(".chitiet >.ttgioithieu > .thongtin > .coban .so_luong input");
    console.log(so)
    n = so.value;
    if(parseInt(n)>0){
        so.value = parseInt(n)-1;
    }
});
bt[1].addEventListener("click", function(e){
    var so = document.querySelector(".chitiet >.ttgioithieu > .thongtin > .coban .so_luong input");
    n = so.value;
    so.value = parseInt(n)+1;
});

var dathang1 = document.querySelector(".chitiet >.ttgioithieu > .thongtin > .coban .button > .dathang:nth-child(1)");
console.log(dathang1)
var dathang2 = document.querySelector(".chitiet >.ttgioithieu > .thongtin > .coban .button > .dathang:nth-child(2)");
var sl = document.querySelector(".chitiet >.ttgioithieu > .thongtin > .coban .form .so");

if(dathang1){
    dathang1.addEventListener('click', function(){
        fetch('/chitiet/dathang/'+dathang1.classList[1], {
            method: 'post',
            body: JSON.stringify ({
                'id': dathang1.classList[1],
                'sl': sl.value
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(response => response.json()).then((data) => {
            location.reload();
        }).catch(function(err) {
            console.error(err)
        })
    })
}

if(dathang2){
    dathang2.addEventListener('click', function(){
        fetch('/chitiet/dathang/'+dathang2.classList[1], {
            method: 'post',
            body: JSON.stringify ({
                'id': dathang2.classList[1],
                'sl': sl.value
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(response => response.json()).then((data) => {

        }).catch(function(err) {
            console.error(err)
        })
        location.reload()
    })
}




var tab = document.querySelectorAll(".chitiet >.ttgioithieu > .danhgia > .tabs > .tab");
var inf = document.querySelectorAll(".chitiet >.ttgioithieu > .danhgia > .infor");
tab[0].classList.remove("tab_chose");
inf[0].classList.remove("tab_active");
tab[1].classList.add("tab_chose");
inf[1].classList.add("tab_active");
tab.forEach((p)=>{
    p.addEventListener("click", function(e){
    for(i=0;i<tab.length;i++){
        tab[i].classList.remove("tab_chose");
    }
    for(i=0;i<inf.length;i++){
        inf[i].classList.remove("tab_active");
    }
    var id = e.target.id;
    tab[id-1].classList.add("tab_chose");
    inf[id-1].classList.add("tab_active");
});
})


var thoi_gian = document.querySelectorAll(".chitiet .ttgioithieu .danhgia .comment .items .thich .thoi_gian");
var danh_gia = document.querySelectorAll(".chitiet .ttgioithieu .danhgia .comment .items .noi_dung .danh_gia");
for (i = 0; i < danh_gia.length; i++){
    dg = parseInt(danh_gia[i].classList[1])
    dg_child = danh_gia[i].childNodes
    for (j = 0; j < dg_child.length; j++){
        if (dg_child[j].tagName == "SPAN" && dg>0){
            dg_child[j].innerHTML = "<i style=\"color: #efb84f\" class=\"fa-solid fa-star\"></i>"
            dg = dg - 1
        }
    }
}
for(tl=0;tl<thoi_gian.length;tl++)
{
    hien_tai = Date.now();
    time_ht = (hien_tai - Date.parse(thoi_gian[tl].innerText))/1000
    if (time_ht<=1){
        thoi_gian[tl].innerText = "Khoảng 1 phút trước"
    }
    if (time_ht>1){
        time_ht = time_ht/60
        thoi_gian[tl].innerText = "Khoảng " + Math.floor(time_ht) + " phút trước"
    }
    if (time_ht>60){
        time_ht = time_ht/60
        thoi_gian[tl].innerText = "Khoảng " + Math.floor(time_ht) + " giờ trước"
    }
    if (time_ht>24){
        time_ht = time_ht/24
        thoi_gian[tl].innerText = "Khoảng " + Math.floor(time_ht) + " ngày trước"
    }
    if (time_ht>30){
        time_ht = time_ht/30
        thoi_gian[tl].innerText = "Khoảng " + Math.floor(time_ht) + " tháng trước"
    }
}
var back = document.querySelector(".chitiet .ttgioithieu .danhgia .comment .o_viet_bl");
var ifor = document.querySelector(".chitiet .ttgioithieu .danhgia .comment >.infor");
var inn = document.querySelector(".chitiet .ttgioithieu .danhgia .comment .viet_binhluan .viet_bl");
var dagia = document.querySelectorAll(".chitiet .ttgioithieu .danhgia .comment > .infor .danh_gia span");
var viet = document.querySelector(".chitiet .ttgioithieu .danhgia .comment > .infor .viet");
back.style.display = "none"
ifor.style.display = "none"
back.addEventListener("click", function(){
    back.style.display = "none"
    ifor.style.display = "none"
    viet.style.display = "none"
})
inn.addEventListener("click", function(){
    event.preventDefault()
    back.style.display = "block"
    ifor.style.display = "block"
    for(i = 0; i < dagia.length; i++){
        dagia[i].innerHTML = "<i style=\"color: #efb84f\" class=\"fa-regular fa-star\"></i>"
    }
})

function sao(n){
    viet.style.display = "block"
    sessionStorage.setItem('sao', n)
    for(j = 0; j < 5; j++){
        if(j < n){
            dagia[j].innerHTML = "<i style=\"color: #efb84f\" class=\"fa-solid fa-star\"></i>"
        }else{
            dagia[j].innerHTML = "<i style=\"color: #efb84f\" class=\"fa-regular fa-star\"></i>"
        }
    }
}
dagia.forEach((i)=>{
    i.addEventListener("click", function(){
        sao(i.classList)
    })
})


var textarea = document.querySelector(".chitiet .ttgioithieu .danhgia .comment > .infor .viet textarea");
var dem = document.querySelector(".chitiet .ttgioithieu .danhgia .comment > .infor .viet .dem span");
textarea.value = ""
textarea.addEventListener("input", function(){
    n = textarea.value.length
    if(n<250){
        dem.innerText = n
    }else{
        dem.innerText = "Tối đa"

    }
})

var guidagia = document.querySelector(".chitiet .ttgioithieu .danhgia .comment > .infor .gui");
id_sp = parseInt(guidagia.classList[1])
var bl = document.querySelectorAll(".chitiet .ttgioithieu .danhgia .comment > .items .text");
var load_dg = document.querySelectorAll(".chitiet .ttgioithieu .danhgia .comment .items .noi_dung .danh_gia");

guidagia.addEventListener("click", function(){
    danhgia(id_sp)
})

var suadagia = document.querySelectorAll(".chitiet .ttgioithieu .danhgia .comment .items .thich .sua");
suadagia.forEach((i) => {
    i.addEventListener("click", function(){
        back.style.display = "block"
        ifor.style.display = "block"
        viet.style.display = "block"
        id = parseInt(i.classList[1])
        sessionStorage.setItem('id', id)
        for(j=0;j<bl.length;j++){
            if (bl[j].classList[1] == id){
                textarea.value = bl[j].childNodes[1].innerText
                break
            }
        }
        for(j=0;j<load_dg.length;j++){
            if (load_dg[j].classList[2] == id){
                sao(load_dg[j].classList[1])
                break
            }
        }
        n = textarea.value.length
        dem.innerText = n
        guidagia.childNodes[1].innerText="Sửa đánh giá"
    })
})

function danhgia(id_sp){
    back.style.display = "none"
    ifor.style.display = "none"
    dg = textarea.value
    id = sessionStorage.getItem('id')
    fetch('/api/gui_danh_gia/'+id_sp, {
        method: 'post',
        body: JSON.stringify ({
            'id': id,
            'id_sp': id_sp,
            'sao': sessionStorage.getItem('sao'),
            'dg': dg
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(response => response.json()).then((data) => {
        sessionStorage.removeItem('id')
        location.reload();
    }).catch(function(err) {
        console.error(err)
    })
}

var xoadagia = document.querySelectorAll(".chitiet .ttgioithieu .danhgia .comment .items .thich .xoa");
xoadagia.forEach((i) => {
    i.addEventListener("click", function(){
        n = i.classList[1]
        fetch('/api/xoa_danh_gia/'+n, {
            method: 'post',
            body: JSON.stringify ({
                'id': n
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(response => response.json()).then((data) => {
            location.reload();
        }).catch(function(err) {
            console.error(err)
        })
    })
})

var thich = document.querySelector(".ttgioithieu > .thongtin > .coban > .form > .button > .thich")
var thich_i = thich.childNodes[1]
console.log(thich.id)
thich.addEventListener("click", function(){
    n = parseInt(thich.classList[1])
    if (thich.id == "tim2"){
        fetch('/chitiet_tim/'+n, {
            method: 'post',
            body: JSON.stringify ({
                'id': n
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(response => response.json()).then((data) => {
            thich.innerHTML = "<i class=\"fa-regular fa-heart\"></i>"
            location.reload();
        }).catch(function(err) {
            console.error(err)
        })
    }else{
        fetch('/chitiet_tim/'+n, {
            method: 'post',
            body: JSON.stringify ({
                'id': n
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(response => response.json()).then((data) => {
            thich.innerHTML = "<i class=\"fa-solid fa-heart\"></i>"
            location.reload();
        }).catch(function(err) {
            console.error(err)
        })
    }
})