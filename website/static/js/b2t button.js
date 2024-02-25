let mysBtn = document 
    .getElementById('scrollbuttonid'); 
  
window.addEventListener('scroll', function () { 
    if (document.body.scrollTop > 1000 
        || document.documentElement.scrollTop > 1000) { 
        mysBtn.style.display = 'block'; 
    } else { 
        mysBtn.style.display = 'none'; 
    } 
}); 