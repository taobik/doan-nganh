
var left1 = document.querySelector(".banner-top > .left");
var right1 = document.querySelector(".banner-top > .right");
var image1 = document.querySelectorAll(".banner-top > .banner-top-item > .image");
var banner_top = 0;
right1.addEventListener('click', function (e) {
    if(banner_top>-200){
        banner_top = banner_top - 100
    }
    else{
        banner_top = 0
    }
    for (i = 0; i < image1.length; i++){
        image1[i].style.transform = 'translateX(' + banner_top + '%)';
    }
});
left1.addEventListener('click', function (e) {
    if(banner_top<0){
        banner_top = banner_top + 100
    }
    else{
        banner_top = -200
    }
    for (i = 0; i < image1.length; i++){
        image1[i].style.transform = 'translateX(' + banner_top + '%)';
    }
});
setInterval(function(){
  if(banner_top>-200){
        banner_top = banner_top - 100
    }
    else{
        banner_top = 0
    }
    for (i = 0; i < image1.length; i++){
        image1[i].style.transform = 'translateX(' + banner_top + '%)';
    }
}, 5000);



var left2 = document.querySelector(".san_pham_moi > .left");
var right2 = document.querySelector(".san_pham_moi > .right");
var image2 = document.querySelectorAll(".san_pham_moi > .san_pham_list > a");
var sp_moi = 0;
right2.addEventListener('click', function (e) {
    if(sp_moi>-100){
        sp_moi = sp_moi - 100
    }
    else{
        sp_moi = 0
    }
    for (i = 0; i < image2.length; i++){
        image2[i].style.transform = 'translateX(' + sp_moi + '%)';
    }

});
left2.addEventListener('click', function (e) {
    var image2 = document.querySelectorAll(".san_pham_moi > .san_pham_list > a");
    if(sp_moi<0){
        sp_moi = sp_moi + 100
    }
    else{
        sp_moi = -100
    }
    for (i = 0; i < image2.length; i++){
        image2[i].style.transform = 'translateX(' + sp_moi + '%)';
    }
});

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

const color = ["#eaedf1","#0262d2", "#2e0158", "#db239b"]
var tab = document.querySelectorAll(".tab_sp > .tab > li");
tab = Array.from(tab)
var sp = document.querySelectorAll(".tab_sp > .sp > .sp_list");
for(i=0;i<sp.length;i++){
    sp[i].style.display = 'none'
}

tab[0].style.backgroundColor = color[1]
sp[0].style.backgroundColor = color[1]
sp[0].style.display = 'block'
tab.forEach((i)=>{
    i.addEventListener('click', function(e){
        for(j=0;j<tab.length;j++){
            tab[j].style.backgroundColor = color[0]
            sp[j].style.backgroundColor = color[0]
        }
        console.log(i)
        console.log(tab.indexOf(i))
        if(e.target.parentNode == i){
            var io = tab.indexOf(i)
            tab[io].style.backgroundColor = color[io+1]
            sp[io].style.backgroundColor = color[io+1]
            for(l=0;l<sp.length;l++){
                sp[l].style.display = 'none'
            }
            sp[io].style.display = 'block'
        }
    });
})

var bn_item = document.querySelectorAll(".hot > .banner > a");
var bn_item_value = 0;
setInterval(function(){
  if(bn_item_value>-100){
        bn_item_value = bn_item_value - 105
    }
    else{
        bn_item_value = 0
    }
    for (i = 0; i < bn_item.length; i++){
        bn_item[i].style.transform = 'translateX(' + bn_item_value + '%)';
    }
}, 5000);


