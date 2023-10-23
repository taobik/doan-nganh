var cli = document.querySelectorAll(".body .list .list_item a")
for(i=0;i<cli.length; i++){
    cli[i].classList.remove('active')
}
cli[0].classList.add('active')

function chart1(labels,data,color){
    const ctx = document.querySelector('#bieu_do1');

    new Chart(ctx, {
    type: 'bar',
    data: {
         labels: labels,
         datasets: [{
            label: 'Doanh thu sản phẩm trong tháng',
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