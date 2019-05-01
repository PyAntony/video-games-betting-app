
window.onload = function() {
    console.log('hiii')
    function thisID(id) {
        return document.getElementById(id)
    }

    function showHide(id, id2='', type="block") {

        // toggle visibility

        var e = thisID(id);
        var e2 = thisID(id2);

        if (e.style.display === type) {
            e.style.display = "none";
        } else {
            e.style.display = type;
            e2.style.display = "none";
        }
    }

    thisID('delBtn').onclick =
        function() {showHide('areyousure', 'createGameForm', "inline")};

    thisID('sure-no').onclick =
            function() {showHide('areyousure', 'areyousure')};

    thisID('createBtn').onclick =
        function() {showHide('createGameForm', 'areyousure')};
};
