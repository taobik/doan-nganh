var li = document.querySelectorAll(".cate_list > ul > li");
for(i = 1; i<li.length;i++){
    li[i].classList.remove("active");
};

var err = document.querySelector(".err");
setTimeout(function(){
    err.classList.add("errback")
}, 100)
setTimeout(function(){
    err.classList.remove("errback")
    err.style.display = "none"
}, 3000)