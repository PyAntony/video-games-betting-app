
window.onload = function() {

    function thisID(id) {
        return document.getElementById(id)
    }

    function ifActionFoundDisplayBlock(action, block_id, id='action') {

        if (thisID(id).value.includes(action)) {
            thisID(block_id).style.display = "block";
        }
    }

    function showHide(id, id2='invisibleBlock') {

        // toggles an element's display property
        // hides second element if passed

        var e = thisID(id);
        var e2 = thisID(id2);

        if (e.style.display === "block") {
            e.style.display = "none";
        } else {
            e.style.display = "block";
            e2.style.display = "none";
        }
    }

    ifActionFoundDisplayBlock('register-error', 'registerForm')
    ifActionFoundDisplayBlock('login-error', 'loginForm')
    ifActionFoundDisplayBlock('create_room-error', 'createRoomForm')
    ifActionFoundDisplayBlock('welcome-g', 'command-center')
    ifActionFoundDisplayBlock('show-login', 'loginForm')

    if (thisID('signBtn')) {
        thisID('signBtn').onclick =
            function() { showHide('registerForm', 'loginForm') };
    }

    if (thisID('logBtn')) {
        thisID('logBtn').onclick =
            function() { showHide('loginForm', 'registerForm') };
    }

    if (thisID('createRoomBtn')) {

        thisID('createRoomBtn').onclick = function() {

            showHide('createRoomForm');
            if (thisID('myRoomsDiv'))
                { thisID('myRoomsDiv').style.display = "none" };
            if (thisID('myGamesDiv'))
                { thisID('myGamesDiv').style.display = "none" };
        };
    }
};
