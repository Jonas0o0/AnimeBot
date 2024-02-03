texte = new Array();
texte[0] = "Anime World at Your Fingertips !";
texte[1] = "Your Anime Adventure Awaits !";
texte[2] = "Dive into Anime Magic !";
texte[3] = "Unleash Anime Wonders !";
texte[4] = "Explore the Anime Universe !";
nb=-1;
function change(){
    if(nb==texte.length-1)
    {nb=0;}else
    {nb++;}
    document.getElementsByClassName("swap")[0].innerHTML=texte[nb];
}
setInterval("change()",5000);



var burger = document.getElementsByClassName('burguer')[0];
var bar1 = document.getElementsByClassName('up')[0];
var bar2 = document.getElementsByClassName('mid')[0];
var bar3 = document.getElementsByClassName('down')[0];
var link = document.getElementsByClassName('link')[0];

burger.addEventListener('click', swap);

function swap(){
    bar1.classList.toggle('active');
    bar2.classList.toggle('active');
    bar3.classList.toggle('active');
    link.classList.toggle('active');
}