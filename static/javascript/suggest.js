let suggestions =[];
"use strict";
fetch("./static/javascript/insname.json").then(function(resp){
    return resp.json();
}).then(function(data){
    suggestions=data;
})