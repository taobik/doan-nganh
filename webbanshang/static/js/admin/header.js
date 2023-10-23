var list = document.querySelector(".header .list .list_item:nth-child(1)")
var lct = document.querySelector(".left_contan")
n = sessionStorage.getItem("slide")
if(n == 0){
    lct.classList.remove("slide")
}else{
    lct.classList.add("slide")
}
list.addEventListener("click", function(){
    event.preventDefault()
    if(lct.classList[1]){
        lct.classList.remove("slide")
        sessionStorage.setItem("slide", 0)
    }else{
        lct.classList.add("slide")
        sessionStorage.setItem("slide", 1)
    }
})

sessionStorage.removeItem('kw')
var input = document.querySelector(".header .list .list_item input")
input.addEventListener("input",function(){
    n = input.value
    sessionStorage.setItem('kw', n)
    loain = sessionStorage.getItem('loai')
    fetch('/api/admin/tim_sanpham', {
        method: 'post',
        body: JSON.stringify ({
            'kw': n,
            'loai': loain
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(response => response.json()).then((data) => {
    }).catch(function(err) {
        console.error(err)
    })
})



















