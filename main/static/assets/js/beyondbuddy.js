(function() {
    document.addEventListener('DOMContentLoaded', function() {
        console.log("Document loaded, initializing chat widget...");

        // Create the widget container
        var C = document.createElement('div');
        C.id = 'beyondbuddy-chat-widget';
        C.className = 'beyondbuddy-chat-widget';
        C.style.width = '64px';
        C.style.height = '64px';
        C.style.position = 'fixed';
        C.style.bottom = '20px';
        C.style.left = '15px'; // Position the widget on the left side
        C.style.zIndex = '999999'; // Ensure it's on top of everything
        C.style.backgroundImage = 'url("/static/img/widget-icon.gif")';
        C.style.backgroundSize = 'cover';
        C.style.backgroundRepeat = 'no-repeat';
        C.style.backgroundPosition = 'center';
        C.style.pointerEvents = 'auto'; // Ensure it is clickable

        console.log("Widget container created:", C);

        // Add a click event listener to expand the widget
        C.addEventListener('click', function() {
            console.log("Widget clicked!");
            C.style.width = '400px';
            C.style.height = '500px';
            C.style.backgroundImage = 'none';
            D.style.display = 'block';
        });

        // Create the iframe for the chat
        var D = document.createElement('iframe');
        D.style.display = 'none'; // Initially hidden
        D.style.width = '100%';
        D.style.height = '100%';
        D.style.border = 'none';
        D.src = '/static/react-chatbot/index.html'; // Ensure this path is correct

        C.appendChild(D);
        document.body.appendChild(C);
        console.log("Iframe created and appended:", D);

        // Add styles to the document
        var aC = document.createElement('style');
        aC.innerHTML = `
            .beyondbuddy-chat-widget {
                border-radius: 35px;
                transition: opacity .35s ease-in, border-radius 0.55s cubic-bezier(.26,1.18,.78,1), height 0.55s cubic-bezier(.26,1.18,.78,1), width 0.45s cubic-bezier(.26,1.18,.78,1);
                box-shadow: rgba(0, 0, 0, 0.1) 0px 10px 15px -3px, rgba(0, 0, 0, 0.1) 0px 4px 6px -4px;
                color: rgb(255, 255, 255);
                overflow: hidden;
                opacity: 0;
                pointer-events: auto; /* Ensure it is clickable */
            }

            .beyondbuddy-chat-widget.loaded {
                opacity: 1;
            }

            .beyondbuddy-chat-widget.light-mode {
                border: 1px solid #e5e7eb;
                background: #fff;
            }

            .beyondbuddy-chat-widget.dark-mode {
                background: #171717;
            }

            .beyondbuddy-chat-widget.widget-opened {
                border-radius: 26px;
            }
        `;
        document.head.appendChild(aC);
        console.log("Styles added to document head");

        // Simulate loading complete by adding loaded class
        setTimeout(() => {
            C.classList.add('loaded');
            console.log("Widget loaded class added");
        }, 1000);
    });
})();
