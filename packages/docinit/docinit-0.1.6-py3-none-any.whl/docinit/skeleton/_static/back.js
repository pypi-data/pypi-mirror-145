$(document).ready(function() {

let menu = document.querySelectorAll('.wy-menu')[0];
menu.innerHTML = '<ul><li class="toctree-l1"><a class="reference internal fa fa-arrow-left" href="/"> Back to main project</a></li></ul>' + menu.innerHTML;
document.querySelectorAll('.icon-home')[0].href='/';

});