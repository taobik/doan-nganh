//console.log(sticky)
var li = document.querySelectorAll(".cate_list > ul > li");
for(i = 1; i<li.length;i++){
    li[i].classList.remove("active");
};
li[1].classList.add("active");


var header = document.querySelector(".header");
var y = header.offsetTop;

window.onscroll = function() {
  if (window.pageYOffset > y) {
    header.classList.add("follow");
  } else {
    header.classList.remove("follow");
  }
};

var gh = document.querySelector(".header a .click")
var par_gh = gh.parentNode
par_gh.addEventListener('click', function(e){
    sessionStorage.setItem("chose", "1");
});

var tttk = document.querySelector(".user_droplist a > .tttk")
if(tttk){
    var tttk_gh = tttk.parentNode
    tttk_gh.addEventListener('click', function(e){
    sessionStorage.setItem("chose", "0");
});
}


var dh = document.querySelector(".user_droplist a > .dh")
if(dh){
var dh_gh = dh.parentNode
dh_gh.addEventListener('click', function(e){
    sessionStorage.setItem("chose", "1");
});
}

var soluo = document.querySelectorAll(".header .giohang .list .infor p span");
var so = document.querySelector(".header .giohang .num .so_luong");
if(so){
    var num =parseInt(so.innerText);
    for (i=0;i<soluo.length;i++){
        num = num + parseInt(soluo[i].innerText)
    }
    if(!num){
        num = 0
    }
    so.innerText = num
}





