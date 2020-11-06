var config, editor;

config = {
    lineNumbers: true,
    mode: "text/x-python",
    theme: "shadowfox",
    indentWithTabs: true,
    // readOnly: true
    screenReaderLabel: "Code",
    smartIndent: true,
    addModeClass: true,
    lineWrapping: false,
    autoCloseBrackets: true,
    scrollbarStyle: "simple",
    gutters: ["CodeMirror-lint-markers"],
    lint: true
};

editor = CodeMirror.fromTextArea(document.getElementById("code"), config);
editor.setSize(null, 500)

// function selectTheme() {
//     editor.setOption("theme", "solarized dark");
// }
// setTimeout(selectTheme, 5000);

function showCode() {
    console.log(editor.getValue().split("\n"));
}

let languages = ['JAVA', 'C', 'C++', 'Python', '']


function changeCode() {
    let mode = "text/x-csrc";
    let lang = document.getElementById("languages").value;
    if (lang == "C++") {

        mode = "text/x-c++src"
    } else if (lang == "Java") {
        mode = "text/x-java"
    } else if (lang == "Python") {
        mode = "text/x-python"
    } else if (lang == "C") {
        mode = "text/x-csrc"
    }
    // document.getElementById("language-label").innerText = "Language (" + lang + ")"
    editor.setOption("mode", mode)
}

function changeCodeOnLoad(lang) {
    let mode = "text/x-csrc";
    console.log(mode)
    if (lang === "C++") {
        mode = "text/x-c++src"
    } else if (lang === "Java") {
        mode = "text/x-java"
    } else if (lang === "Python") {
        mode = "text/x-python"
    } else if (lang === "C") {
        mode = "text/x-csrc"
    }
    // document.getElementById("language-label").innerText = "Language (" + lang + ")"
    editor.setOption("mode", mode)
    editor.setOption("readOnly", "nocursor")
}

function validateinput() {
    var cinput = document.getElementById("custominput").value
    if (cinput == "") {
        document.getElementById("custominput-label").innerText = "Custom Input (Invalid)"
        document.getElementById("custominput-label").style.color = "red"
    } else {
        document.getElementById("custominput-label").innerText = "Custom Input"
        document.getElementById("custominput-label").style.color = "black"
    }
}

function validateName() {
    let c_input = document.getElementById("codename").value
    if (c_input === "") {
        document.getElementById("codenamelabel").innerText = " Name can't be empty"
        document.getElementById("codenamelabel").style.color = "red"
    } else {
        document.getElementById("codenamelabel").innerText = ""
        document.getElementById("codenamelabel").style.color = "white"
    }
}

function toggleinput() {
    var cb = document.getElementById("custominput-check")
    if (cb.checked) {
        document.getElementById("custominput").disabled = false
    } else {
        document.getElementById("custominput").disabled = true
        document.getElementById("custominput-label").innerText = "Custom Input"
        document.getElementById("custominput-label").style.color = "black"
    }
}

function copyCode() {
    navigator.clipboard.writeText(editor.getValue()).then(function () {
        console.log('Async: Copying to clipboard was successful!');
    }, function (err) {
        console.error('Async: Could not copy text: ', err);
    });
}

function enableOrDisablePin() {
    if (document.getElementById("customSwitch1").checked === true) {
        document.getElementById("PIN").disabled = false;
        document.getElementById("PIN").required = true;
    } else {
        document.getElementById("PIN").disabled = true;
        document.getElementById("PIN").required = false;
    }
}

function toggleExecutable() {
    if (document.getElementById("customSwitch2").checked === true) {
        document.getElementById("execution").hidden = false
        document.getElementById("executebutton").disabled=false
    } else {
        document.getElementById("execution").hidden = true
        document.getElementById("executebutton").disabled=true
    }
}

function copyLink(baseurl) {
    let copyText = document.getElementById("link").value;
    let input = document.createElement('input');
    input.setAttribute('value', copyText);
    document.body.appendChild(input);
    input.select();
    let result = document.execCommand('copy');
    document.body.removeChild(input);
    document.getElementById("copybutton").innerText = "Copied!"
}


function executeCode(baseurl) {
    let url = baseurl + 'execute'
    let http = new XMLHttpRequest();
    let params = 'code=';
    params += editor.getValue() + '&language='
    params += document.getElementById('languages').value + '&input='
    params += document.getElementById('input').value
    // const params={
    //     code:editor.getValue(),
    //     language:document.getElementById('languages').value,
    //     input:document.getElementById('input').value
    // }
    http.open('POST', url, true);
    http.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

    http.onreadystatechange = function () {//Call a function when the state changes.
        if (http.readyState == 4 && http.status == 200) {
            document.getElementById("output").innerHTML = http.responseText
        }
        else
        {
            document.getElementById("output").innerHTML = 'Server Error Try Again Later'
        }
    }

    // http.send(JSON.stringify(params));
    http.send(params);

}