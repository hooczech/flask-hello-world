$('#mainForm').submit(function () {
 send();
 return false;
});

let disabled = false

let replyHtml = `
        <div class="media w-75 mb-3"><img src="static/load.svg" alt="user" width="50" class="replyImg rounded-circle">
          <div class="media-body ml-3">
            <div class="bg-light rounded py-2 px-3 mb-2">
              <p class="replyClass text-small mb-0 text-muted">Přemýšlím, jsem pomalý, ale přesný, většinou odpovím do minuty</p>
            </div>
          </div>
        </div>
`;

let replyNoTextHtml = `
        <div class="media w-75 mb-3"><img src="static/avatar.svg" alt="user" width="50" class="rounded-circle">
          <div class="media-body ml-3">
            <div class="bg-light rounded py-2 px-3 mb-2">
              <p class="text-small mb-0 text-muted">Prosím, prvně napište otázku, na kterou mám odpovědět</p>
            </div>
          </div>
        </div>
`;


let questionHtml = `
        <div class="media w-50 ml-auto mb-3">
          <div class="media-body">
            <div class="bg-primary rounded py-2 px-3 mb-2">
              <p class="text-small mb-0 text-white">replaceMe</p>
            </div>
          </div>
        </div>
`;

function scrollMe(ele){
    let objDiv = document.getElementById(ele);
    objDiv.scrollTop = objDiv.scrollHeight;
}

function send(){
    if (disabled) return
    disabled = true
    console.log('called')

    let questionVal = $("#question").val();

    //dont process empty
    if (questionVal==''){
        $("#chatBox").append(replyNoTextHtml);
        scrollMe("chatBox")
        disabled = false
        return
    }

    htmlToAdd = questionHtml.replace('replaceMe', questionVal);
    $( "#chatBox" ).append(htmlToAdd);

    $("#fa").attr("class","fas fa-stroopwafel fa-spin");
    $("#question").val('');

    $( "#chatBox" ).append(replyHtml);
    scrollMe("chatBox")

    console.log('will send');
    let server_data = {"question": questionVal}
    $.ajax({
      type: "POST",
      url: "/q",
      data: JSON.stringify(server_data),
      contentType: "application/json",
      dataType: 'json',
      success: function(result) {
        console.log("Result:");
        console.log(result);
        $( ".replyClass" ).text(result.reply);
        $( ".replyClass" ).removeClass("replyClass");

        $( ".replyImg" ).attr("src","static/avatar.svg");
        $( ".replyImg" ).removeClass("replyImg");

        $("#fa").attr("class","fa fa-paper-plane");
        scrollMe("chatBox")
        disabled = false
      }
    });
}