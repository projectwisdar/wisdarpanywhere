


$(document).ready(function () {

     
     TweenMax.from("preloader", 1, {
          y: 1000,
          opacity:1,
         
     });


     TweenMax.to("preloader", 2, {

          y: -1500,
          opacity: 1,
          ease: Power2.easeInOut,

     });

     TweenMax.to("preloader", 2, {

          delay: 2,
          visibility: 'hidden',
     });


     TweenMax.from(".preloadertitle1", 1, {
          x: -200,
          delay: 0.5,
          opacity: 1
          

     });

     TweenMax.from(".preloadertitle1", 1, {
          y: -200,
          delay: 1,
          opacity: 1

     });


     TweenMax.to(".preloadertitle1", 2, {


          opacity: 1,
          ease: Power2.easeInOut
     });

     TweenMax.from(".preloadertitle2", 1, {
          x: 200,
          opacity: 1

     });
     TweenMax.from(".preloadertitle2", 1, {
          y: 200,
          delay: 1,
          opacity: 1

     });


     TweenMax.to(".preloadertitle2", 2, {


          opacity: 1,
          ease: Power2.easeInOut
     });
     TweenMax.to(".preloadertitle2", 2, {

          delay: 2,
          opacity: 0,
          ease: Power2.easeInOut
     });
     TweenMax.to(".preloadertitle1", 2, {

          delay: 2,
          opacity: 0,
          ease: Power2.easeInOut
     });
     TweenMax.to("#gridbg", 2, {

          delay: 1.5,
          opacity: 0,
          ease: Power2.easeInOut,

     });
     TweenMax.to("#gridbg", 2.5, {
          delay: 3.5,
          visibility: 'hidden',

     });



     TweenMax.from(".logolink", 1, {
          visibility: 'hidden',
          opacity: 0,
          delay: 3,
     });

     TweenMax.to(".logolink", 1, {
          delay: 3,
          opacity:1,
          ease: Expo.easeInOut
     });

     TweenMax.from(".btmlogo", 1, {
          visibility: 'hidden',
          opacity: 0,
          delay: 3,
     });

     TweenMax.to(".btmlogo", 1, {
          delay: 3,
          opacity:1,
          ease: Expo.easeInOut
     });
     TweenMax.from(".arrow", 0, {
          visibility: 'hidden',
          opacity: 0,
          delay: 4,
     });

     TweenMax.to(".arrow", 1, {
          delay: 3,
          opacity:1,
          ease: Expo.easeInOut
     });



     TweenMax.from("#primary", 1, {
          x: -200,
          opacity: 0,
          delay: 3,
     });

     TweenMax.to("#primary", 1, {
          delay: 3,
          ease: Expo.easeInOut
     });
     TweenMax.from(".toggler", 1, {
          visibility: 'hidden',
          opacity: 0,
          delay: 3,
     });

     TweenMax.to(".toggler", 1, {
          delay: 3,
          ease: Expo.easeInOut
     });
     TweenMax.from(".menu-wrap", 0, {
          visibility: 'hidden',
          opacity: 0,
          delay: 4,
     });

     TweenMax.to(".menu-wrap", 1, {
          delay: 3,
          opacity: 1,
          ease: Expo.easeInOut
     });
 
     TweenMax.from(".language", 1, {
          visibility: 'hidden',
          opacity: 0,
          delay: 3,
     });

     TweenMax.to(".language", 1, {
          delay: 3,
          opacity: 1,
          ease: Expo.easeInOut
     });
 


     intro();
     introtxt();
     function introtxt() {

          var tltxt = new TimelineMax({
               delay: 4,
               repeat: -1, repeatDelay: 0
          });



          tltxt.to("#titles", 0, {
           
               opacity: 1,



          });
          tltxt.from(".digitalcontenttitle", 0.5, {
               delay: 1.8,
               y: 30,
               display: 'none',
               ease: Power4.ease,
               opacity: 0,



          });
          tltxt.to(".digitalcontenttitle", 0.5, {
               delay: 1.8,
               y: 30,
               display: 'none',
               ease: Power4.ease,
               opacity: 0,



          });
          tltxt.from(".digitalplatformstitle", 0.5, {
               delay: 1.8,
               y: 30,
               display: 'none',
               ease: Power4.ease,
               opacity: 0,



          });
          tltxt.to(".digitalplatformstitle", 0.5, {
               delay: 1.8,
               y: 30,
               display: 'none',
               ease: Power4.ease,
               opacity: 0,



          });
          tltxt.from(".fintechtitle", 0.5, {
               delay: 1.8,
               y: 30,
               display: 'none',
               ease: Power4.ease,
               opacity: 0,



          });
          tltxt.to(".fintechtitle", 0.5, {
               delay: 1.8,
               y: 30,
               display: 'none',
               ease: Power4.ease,
               opacity: 0,



          });
          tltxt.from(".energysolutionstitle", 0.5, {
               delay: 1.8,
               y: 30,
               display: 'none',
               ease: Power4.ease,
               opacity: 0,



          });
          tltxt.to(".energysolutionstitle", 0.5, {
               delay: 1.8,
               y: 30,
               display: 'none',
               ease: Power4.ease,
               opacity: 0,



          });


     }
     function intro() {
        
          var tl = new TimelineMax({
               delay: 4, yoyo: true,
               repeat: -1, repeatDelay: 0.5
          });

           

          tl.to(".svgintro", 0, {

            

               opacity: 1

          });
          tl.from("#wisdar1", 0.2, {

               scaleY: 0,

               opacity: 1

          });

          tl.from("#wisdar2", 0.2, {
               scaleX: 0,
               transformOrigin: "100% 0%",


               opacity: 1

          });
          tl.from("#wisdar3", 0.2, {
               scaleY: 0,
               transformOrigin: "0% bottom",


               opacity: 1

          });
          tl.from("#wisdar4", 0.2, {
               scaleX: 0,
               transformOrigin: "0% 100%",


               opacity: 1

          });
          tl.from("#wisdar5", 0.2, {

               scaleY: 0,

               opacity: 1

          });
          tl.from("#wisdar6", 0.2, {
               scaleX: 0,
               transformOrigin: "100% 0%",


               opacity: 1

          });
          tl.from("#wisdar7", 0.2, {

               scaleY: 0,

               opacity: 1

          });
          tl.from("#wisdar8", 0.2, {
               scaleX: 0,
               transformOrigin: "100% 0%",


               opacity: 1

          });
          tl.from("#wisdar9", 0.2, {
               scaleY: 0,
               transformOrigin: "0% bottom",


               opacity: 1

          });



     }


});
