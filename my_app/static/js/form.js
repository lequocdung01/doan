let options = document.querySelectorAll('.option-content');
let form = document.getElementById('form');
let bg = document.getElementById('option-background')

options.forEach(val => {
    val.addEventListener('click', function(event){
        form.classList.remove('login');
        form.classList.remove('regester');
        form.classList.add(this.id);
        bg.style.left = this.offsetLeft + 'px';
    })
})