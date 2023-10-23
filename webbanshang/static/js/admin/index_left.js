var cli = document.querySelectorAll(".body .list .list_item a")
for(i=0;i<cli.length; i++){
    cli[i].classList.remove('active')
}
cli[0].classList.add('active')

cli.forEach((e)=>{
    e.addEventListener("click", function(){
        for(i=0;i<cli.length; i++){
            cli[i].classList.remove('active')
        }
        e.classList.add('active')
    })
})