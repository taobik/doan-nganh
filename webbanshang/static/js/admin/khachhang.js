var cli = document.querySelectorAll(".body .list .list_item a")
for(i=0;i<cli.length; i++){
    cli[i].classList.remove('active')
}
cli[2].classList.add('active')

var check = document.querySelectorAll(".body td input")
check.forEach((i)=>{
    i.addEventListener("change", function(){
        n = parseInt(i.classList)
        fetch('/api/admin/khachhang/huy_hd',{
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