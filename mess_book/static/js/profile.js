document.addEventListener('DOMContentLoaded', function () {
    const updateBtn = document.getElementById('update-btn');
    const updatePassBtn = document.getElementById('update-password-btn');
    const modal = document.getElementById('update-modal');
    const pass_modal = document.getElementById('update-password-modal');
    const closeBtn = document.getElementsByClassName('close')[0];
    const closePassBtn = document.getElementsByClassName('close_btn')[0];
     
    
    updateBtn.onclick = function () {
        modal.style.display = 'block';
    }

    updatePassBtn.onclick = function () {
        pass_modal.style.display = 'block';
    }

    closeBtn.onclick = function () {
        modal.style.display = 'none';
    }

    closePassBtn.onclick = function () {
        pass_modal.style.display = 'none';
    }

    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
        else if(event.target == pass_modal){
            pass_modal.style.display = 'none'
        }
    }
});
