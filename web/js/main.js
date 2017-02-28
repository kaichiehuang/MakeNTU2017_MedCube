"use strict";
let pic_list = []
$(function()
    {
    
    $('#fileSelector').change(function(evt)
        {
            let files = evt.target.files;
            for (let i = 0; i < files.length; i++)
            {
                console.log(files[i].name);
                pic_list.push(files[i].name);
            }
        // hide the pink bottom after pushed in
        // $('#fileBtn').hide();
        });
    /*
    $('#drawBtn').click(function()
        {
            console.log(pic_list);
            if (pic_list.length != 0)
            {
                let chosen = Math.floor(Math.random() * pic_list.length);
                console.log(chosen);
                $('#chosenPic').attr("src", "pic/" + pic_list[chosen]);
                pic_list.splice(chosen, 1);
                console.log(pic_list);
            }
            else
            {
                console.error("No Pictures Left!");
                $('#chosenPic').attr("src", "img/question.png");
            }
        });*/
    $('#writeBtn').click(function()
        {
            //get the temp value in text

        });
    $('#regBtn').click(function()
        {
            //stroe information in files
            
        });
    });






