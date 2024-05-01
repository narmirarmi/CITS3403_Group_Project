var newPollModal = document.getElementById('newPollModal')
newPollModal.addEventListener('show.bs.modal', function (event) {

  // Button that triggered the modal
  var button = event.relatedTarget;

  // get the function identifier
  var recfunction = button.getAttribute('data-bs-whatever');

  // TODO: Perform a check to see if the user is logged in and update modal accordingly
  if(getLoginState()){
    var modalTitle = newPollModal.querySelector('.modal-title');
    var modalBodyInput = newPollModal.querySelector('.modal-body input');
    var modalImageInput = newPollModal.getElementById('product-image-file');
    modalImageInput.style.height = getComputedStyle(modalImageInput).width;
  }

  // TODO: redirect if user is not logged in

  // TODO: data validation and visual cleanup

})

//check client to see if user is logged in
function getLoginState(){
  return true;
}
