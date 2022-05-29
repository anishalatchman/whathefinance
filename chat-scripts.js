// Gets bot response
async function getBotResponse(usermsg) {
    // we will add more later
    keywords = new Set(['Interest', 'Inflation', 'Sanction', 'Bitcoin', 'Optimus Prime'])

    let bot_wordz = ""
    keywords.forEach(keyword => {
        if(usermsg.includes(keyword)) {
            bot_wordz = bot_wordz.concat(`${keyword}-`)
        }
    })

    // we don't own a server!!!
    let api_url = 'http://127.0.0.1:5000'

    // for now we assume chrome because everything is on fire
    let user_browser = "Chrome"

    // this is a string. Grab it and convert it to a dictionary.
    // this way of formatting requests is messy and bad but we don't got time for best practices
    let url = `${api_url}/${user_browser}/${bot_wordz}`
    console.log(`Our JSON url is: ${url}`)
    let json_response = await $.getJSON(url)
    console.log(`Response done! ${url}`)

    for (key in json_response){
        console.log(`key is ${key}, and the summary is ${json_response[key]} \n`)
        let botResponse = `Here is a link: ${key}. \n. Also here's a summary of that article that I just made: ${json_response[key]}`
        // let botHtml = '<p class="bot-msg"><span>' + botResponse + '</span></p>';
        var tag = document.createElement('p')
        tag.className = 'bot-msg'
        var kid = document.createElement("span")
        var text = document.createTextNode(botResponse)
        kid.appendChild(text)
        tag.appendChild(kid)
        $("#texts").append(tag);
    }


    document.getElementById("chat-bar-bottom").scrollIntoView(true);
}
//Gets the text text from the input box and processes it

function getResponse() {
    try {
        console.log("function ran! We'll try something out, won't we!")
        let usermsg = $("#msg").val();

        // if (usermsg == "") {
        //     usermsg = "";
        // }

        botMsg = getBotResponse(usermsg)

        let userHtml = '<p class="user-msg"><span>' + usermsg + '</span></p>';

        $("#msg").val("");
        $("#texts").append(userHtml);
        document.getElementById("chat-bar-bottom").scrollIntoView(true);
    } catch (e) {
        console.log("Something definitely broke in getResponse.")
    }
}

function summariseWeb() {
    return "Here's the summary!"
}