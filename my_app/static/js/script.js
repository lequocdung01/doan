//<!-- Script for Slide Show: Change picture every three seconds -->
document.addEventListener('DOMContentLoaded', function() {
var index = 0;
   change();

   function change() {

       //Collect all images with class 'slides'
       var x = document.getElementsByClassName('slides');

       //Set all the images display to 'none' (invisible)
       for(var i = 0; i < x.length; i++) { 
           x[i].style.display = "none"; 
       }

       //Increment index variable
       index++;

       //Set index to 1 if it's greater than the amount of images
       if(index > x.length) { 
           index = 1; 
       }

       //set image display to 'block' (visible)
       x[index - 1].style.display = "block";

       //set loop to change image every 5000 milliseconds (5 seconds)
       setTimeout(change, 3000);
    }
},false);
document.addEventListener('DOMContentLoaded', function() {
var index1 = 0;
         change1();
      
         function change1() {
      
             //Collect all images with class 'slides'
             var x1 = document.getElementsByClassName('clads');
      
             //Set all the images display to 'none' (invisible)
             for(var i = 0; i < x1.length; i++) { 
                 x1[i].style.display = "none"; 
             }
      
             //Increment index variable
             index1++;
      
             //Set index to 1 if it's greater than the amount of images
             if(index1 > x1.length) { 
                 index1 = 1; 
             }
      
             //set image display to 'block' (visible)
             x1[index1 - 1].style.display = "block";
      
             //set loop to change image every 5000 milliseconds (5 seconds)
             setTimeout(change1, 3000);
          }
        },false);
