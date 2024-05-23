<<<<<<< HEAD
// /* link den web thong tin cua may hut bui */
// {% extends 'html/base.html' %}
// {% load static %}
// function Produce_1() {
//     location.href = "{% url 'detail' %}";
// }
// /* link den web thong tin cua ti vi */
// function Produce_2() {
//     location.href = "";
// }
// /* link den web thong tin cua bep tu */
// function Produce_3() {
//     location.href = "";
// }
// /* link den web thong tin cua lo nuong */
// function Produce_4() {
//     location.href = "";
// }
// /* link den web thong tin cua may giat */
// function Produce_5() {
//     location.href = "";
// }
=======
let star = document.querySelectorAll('input');
let showValue = document.querySelector('#rating-value');
for (let i = 0; i < star.length; i++) {
    star[i].addEventListener('click',function() {
        i = this.value;
        showValue.innerHTML = i + "cua 5";
    })
}
>>>>>>> c741b029281df892a6277e3955dcc9aecfe973b7
