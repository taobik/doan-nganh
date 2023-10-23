var cli = document.querySelectorAll(".body .list .list_item a")
for(i=0;i<cli.length; i++){
    cli[i].classList.remove('active')
}
cli[1].classList.add('active')

var check = document.querySelectorAll(".body td input")
check.forEach((i)=>{
    i.addEventListener("change", function(){
        n = parseInt(i.classList)
        fetch('/api/admin/sanpham/huy_hd',{
            method: 'post',
            body: JSON.stringify ({
                'id': n,
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
sessionStorage.removeItem('loai')
var loai = document.querySelector(".body .loc .loai")
loai.addEventListener("change", function(){
    loain = loai.value
    sessionStorage.setItem('loai', loain)
    kw = sessionStorage.getItem('kw')
    fetch('/api/admin/loc_sanpham', {
        method: 'post',
        body: JSON.stringify ({
            'kw': kw,
            'loai': loain
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






















