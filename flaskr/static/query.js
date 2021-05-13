hoverarea.addEventListener('mouseover', function() {
   document.getElementById("hoverarea").getElementsByTagName("img")[0].style.filter = 'opacity(100%)';
});

hoverarea.addEventListener('mouseout', function() {
    document.getElementById("hoverarea").getElementsByTagName("img")[0].style.filter = 'opacity(75%)';
 });
 
let div = document.getElementById("hoverarea");
let height = div.offsetHeight;
let div_iframe = document.getElementById('playlist');
div_iframe.style.height = height;
let iframe = div_iframe.getElementsByTagName('iframe')[0];
iframe.style.height = height;

search.addEventListener('click', function() {
   document.getElementById("searchTerm").style.display = 'inline-flex';
});
document.querySelectorAll('.hoverareaResult').forEach(item => {
      item.addEventListener('mouseover', function() {
       item.style.filter = 'opacity(100%)';
    });
})

document.querySelectorAll('.hoverareaResult').forEach(item => {
      item.addEventListener('mouseout', function() {
       item.style.filter = 'opacity(50%)';
    });
})
