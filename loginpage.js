




document.addEventListener("DOMContentLoaded", function() {
    // Select all <a> tags in the document
    const links = document.querySelectorAll('a');
    const closeModal = document.querySelector('.close-button');
    // Loop through each <a> element
    //links.forEach(link => {
      // Add the 'click' event listener
      //link.addEventListener('click', function(event) {
    modal.showModal();
        // If you want to perform other actions (e.g., tracking, preventing default behavior), do it here.
    //});
   // });
    closeModal.addEventListener('click', () => {
    modal.close();
    
    
  });
  });
  