var cli = document.querySelectorAll(".body .list .list_item a")
for(i=0;i<cli.length; i++){
    cli[i].classList.remove('active')
}
cli[1].classList.add('active')

var tab = document.querySelectorAll(".main .tab .tab_item")
var body_tab = document.querySelectorAll(".main .body_tab_list")
for(i=0;i<tab.length; i++){
    tab[i].classList.remove('chose')
    body_tab[i].style.display = "none"
}
n = sessionStorage.getItem('stt')
if(n){
    tab[n].classList.add('chose')
    body_tab[n].style.display = "block"
}else{
    tab[0].classList.add('chose')
    body_tab[0].style.display = "block"
}


tab.forEach((e)=>{
    e.addEventListener("click", function(){
        n = parseInt(e.classList[1])
        for(i=0;i<tab.length; i++){
            tab[i].classList.remove('chose')
            body_tab[i].style.display = "none"
        }
        e.classList.add('chose')
        body_tab[n-1].style.display = "block"
        sessionStorage.setItem('stt', n-1)
    })
})

var danh_gia = document.querySelectorAll(".main .body_tab .body_tab_list .comment .items .danh_gia")
var thoi_gian = document.querySelectorAll(".main .body_tab .body_tab_list .comment .items .thich .thoi_gian");
function sao(n){
    viet.style.display = "block"
    for(j = 0; j < 5; j++){
        if(j < n){
            dagia[j].innerHTML = "<i style=\"color: #efb84f\" class=\"fa-solid fa-star\"></i>"
        }else{
            dagia[j].innerHTML = "<i style=\"color: #efb84f\" class=\"fa-regular fa-star\"></i>"
        }
    }
}

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
var danh_gia = document.querySelectorAll(".main .body_tab .body_tab_list .comment .items .xoa")
danh_gia.forEach((e)=>{
    e.addEventListener("click",function(){
        n = e.classList[1]
        fetch('/api/admin/xoa_binhluan/'+n, {
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

function chart1(labels,data,color){
    const ctx = document.querySelector('#bieu_do1');

    new Chart(ctx, {
    type: 'bar',
    data: {
         labels: labels,
         datasets: [{
            label: 'Doanh thu sản phẩm trong năm',
            data: data,
            backgroundColor: color,
            borderColor: color,
            borderWidth: 1
          }]
        },
        options: {
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }
    });
}
function chart2(labels,data,color){
    const ctx = document.querySelector('#bieu_do2');

    new Chart(ctx, {
    type: 'pie',
    data: {
         labels: labels,
         datasets: [{
            label: 'Doanh thu sản phẩm so với sản phẩm cùng loại',
            data: data,
            backgroundColor: color,
            borderColor: color,
            borderWidth: 1
          }]
        },
        options: {
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }
    });
}
















