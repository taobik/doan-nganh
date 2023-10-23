var cli = document.querySelectorAll(".body .list .list_item a")
for(i=0;i<cli.length; i++){
    cli[i].classList.remove('active')
}
cli[1].classList.add('active')


var image_dp = document.querySelector(".sp .tt_hang > .form-group .img_display")
var image = document.querySelector(".sp .tt_hang > .form-group .form-control")
image.addEventListener("input", function(){
    image_dp.src = URL.createObjectURL(image.files[0]);
})

var textarea = document.querySelector(".sp .tt_chitiet > .form-group textarea");
var dem = document.querySelector(".sp .tt_chitiet > .form-group .num span");
textarea.value = ""
textarea.addEventListener("input", function(){
    n = textarea.value.length
    if(n<250){
        dem.innerText = n
    }else{
        dem.innerText = "Tối đa"
    }
})

