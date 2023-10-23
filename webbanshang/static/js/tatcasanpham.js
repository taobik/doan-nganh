var li = document.querySelectorAll(".cate_list > ul > li");
for(i = 1; i<li.length;i++){
    li[i].classList.remove("active");
};
li[2].classList.add("active")


var thieu = document.querySelector(".body > .san_pham > .loc  > .loc_list #thieu");
var hdhanh = document.querySelector(".body > .san_pham > .loc  > .loc_list #hdh");
var ram = document.querySelector(".body > .san_pham > .loc  > .loc_list #ram");
var dluong = document.querySelector(".body > .san_pham > .loc  > .loc_list #dungluong");
var btloc = document.querySelector(".body > .san_pham > .loc  > .loc_list .loc_button");

if(sessionStorage.getItem('thieu')){
    thieu.value = sessionStorage.getItem('thieu')
}
if(sessionStorage.getItem('hdhanh')){
    hdhanh.value = sessionStorage.getItem('hdhanh')
}
if(sessionStorage.getItem('ram')){
    ram.value = sessionStorage.getItem('ram')
}
if(sessionStorage.getItem('dluong')){
    dluong.value = sessionStorage.getItem('dluong')
}

function check(){
    var th = sessionStorage.getItem('thieu')
    var hdh = sessionStorage.getItem('hdhanh')
    var r = sessionStorage.getItem('ram')
    var dl = sessionStorage.getItem('dluong')
    fetch('/api/sanpham/loc', {
        method: 'post',
        body: JSON.stringify ({
            'th': th,
            'hdh': hdh,
            'r': r,
            'dl': dl
        }),
        headers: {
            'Content-Type': "application/json"
        }
    }).then(res => res.json()).then((data) => {
    }).catch(function(err) {
        console.log(err)
    })
}
check()
thieu.addEventListener("change", function() {
    sessionStorage.setItem('thieu', thieu.value)
    check()
});
hdhanh.addEventListener("change", function() {
    sessionStorage.setItem('hdhanh', hdhanh.value)
    check()
});
ram.addEventListener("change", function() {
    sessionStorage.setItem('ram', ram.value)
    check()
});
dluong.addEventListener("change", function() {
    sessionStorage.setItem('dluong', dluong.value)
    check()
});
var trang = document.querySelectorAll(".san_pham > .trang .num p");
t = sessionStorage.getItem('mau')
if (t && trang.length > 1){
    trang[t-1].classList.add('mau')
}else{
    trang[0].classList.add('mau')
    sessionStorage.setItem('mau', 1)
}
trang.forEach((i)=>{
    i.addEventListener("click", function(){
        for(j = 0; j< trang.length; j++){
            trang[j].classList.remove('mau')
        }
        i.classList.add('mau')
        n = parseInt(i.innerText)
        sessionStorage.setItem('mau', n)
        fetch('/sanpham/phantrang', {
            method: 'post',
            body: JSON.stringify ({
                'tr': n
            }),
            headers: {
                'Content-Type': "application/json"
            }
        }).then(res => res.json()).then((data) => {
            location.reload();
        }).catch(function(err) {
            console.log(err)
        })
        })
})