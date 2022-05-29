// Gets bot response
function getBotResponse(usermsg) {
    let botResponse = summariseWeb(usermsg);
    let botHtml = '<p class="bot-msg"><span>' + botResponse + '</span></p>';
    $("#texts").append(botHtml);

    document.getElementById("chat-bar-bottom").scrollIntoView(true);
}

//Gets the text text from the input box and processes it
function getResponse() {
    console.log("function ran")
    let usermsg = $("#msg").val();

    // if (usermsg == "") {
    //     usermsg = "";
    // }

    botMsg = getBotResponse(usermsg)

    let userHtml = '<p class="usermsg"><span>' + usermsg + '</span></p>';

    $("#msg").val("");
    $("#texts").append(userHtml);
    document.getElementById("chat-bar-bottom").scrollIntoView(true);
}

function summariseWeb() {
    return "Here's the summary!"
}