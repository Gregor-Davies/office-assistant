function darkMode() {
    var element = document.body;
    element.classList.toggle("dark-mode");
}

function activePerson() {
    var personer = document.getElementById("person");
    personer.classList.toggle('active');
}

function activeLine() {
    var linear = document.getElementById("line");
    linear.classList.toggle('active');
}

function activeStop() {
    var stopping = document.getElementById("stop");
    stopping.classList.toggle('active');
}

function checkIfDisabled() {
    var check = document.getElementById("line")

    if (check.disabled) {
        check.disabled = false
    }
    else {
        check.disabled = true
    }

}

function checkIfDisabledPerson() {
    var check = document.getElementById("person")

    if (check.disabled) {
        check.disabled = false
    }
    else {
        check.disabled = true
    }

}

function checkIfDisabledStop() {
    var check = document.getElementById("line")
    var linech = document.getElementById("person")

    if (check.disabled || linech.disabled) {
        check.disabled = false
        linech.disabled = false
    }
    else {
        check.disabled = true
        linech.disabled = true
    }

}

var btnName = function() {
    $.get('/stop_button',
      function(x) {
          $("#resBtnHere").html(x);
      }
    )
}

var lineButton = function() {
    $.get('/stop_button',
    function(x) {
        $('#resBtnHere').html(x);
    }
    )
}