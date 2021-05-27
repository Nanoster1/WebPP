window.onload = function(){
    var button1 = document.getElementById("megalike");
    var button2 = document.getElementById("megadislike");
    button1.onclick = init3(button1,button2);

    button1.onclick = init4(button1,button2);
}
function init3(button1,button2)
{
    if(!button2?.style.color == 'rgb(3, 3, 3)')
    {
        if(button1?.style.color == 'rgb(3, 3, 3)')
        {
            button1?.style.color = "rgb(0, 0, 0)";
        }
        else
        {
            button1?.style.color = "rgb(3, 3, 3)";
        }
    }
}
function init4(button1,button2)
{
    if(!button1?.style.color == 'rgb(3, 3, 3)')
    {
        if(button2?.style.color == 'rgb(3, 3, 3)')
        {
            button2?.style.color = "rgb(0, 0, 0)";
        }
        else
        {
            button2?.style.color = "rgb(3, 3, 3)";
        }
    }
}
