document.addEventListener('DOMContentLoaded', (event) => {
    let deferredPrompt;
    const installButton = document.getElementById('installButton');
  
    if (installButton) {
      window.addEventListener('beforeinstallprompt', (e) => {
        e.preventDefault();
        deferredPrompt = e;
        installButton.style.display = 'block';
  
        installButton.addEventListener('click', () => {
          installButton.style.display = 'none';
          deferredPrompt.prompt();
          deferredPrompt.userChoice.then((choiceResult) => {
            if (choiceResult.outcome === 'accepted') {
              console.log('User accepted the A2HS prompt');
            } else {
              console.log('User dismissed the A2HS prompt');
            }
            deferredPrompt = null;
          });
        });
      });
    } else {
      console.error('Install button not found');
    }
  });
