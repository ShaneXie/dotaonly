/**
 * Created by An on 12/25/2014.
 */

$(document).ready(function() {
    var streamHeight = $(".streamContainer").height();
    $(".streamObj").height(streamHeight);

    pageInit();
    //$('#streamList').load('ajax/getStreamList/001/');
    //loadFirstDouyuStream();
});

$(window).resize(function() {
    var streamHeight = $(".streamContainer").height();
    $(".streamObj").height(streamHeight);
});

function hideLeftPanel(){
    $('#leftPanel').hide('slide', {direction: 'left'}, 300);
    $('#leftPanelSwitchIcon').html("<span class='glyphicon glyphicon-step-forward' aria-hidden='true'></span>");
    $('#leftPanelSwitch').css("background-color","#44B78B");
    $('#mainDiv').css("margin-left","15px");
    $('#leftPanelFlag').text("off");
}

function showLeftPanel(){
    $('#leftPanel').show('slide', {direction: 'left'}, 300);
    $('#leftPanelSwitchIcon').html("<span class='glyphicon glyphicon-step-backward' aria-hidden='true'></span>");
    $('#leftPanelSwitch').css("background-color","#0C4B33");
    $('#mainDiv').css("margin-left","265px");
    $('#leftPanelFlag').text("on");
}

function loadFirstDouyuStream(){
    var streamInfo=$('.streamItem')[0].id;
    var info = streamInfo.split('_');
    var html = "<div id=\"streamTopLeft\" class=\"streamContainerMain\"><object  type=\"application/x-shockwave-flash\" data=\"http://staticlive.douyutv.com/common/share/play.swf?room_id="+info[2]+"\" width=\"100%\" height=\"100%\" allowscriptaccess=\"always\" allowfullscreen=\"true\" allowfullscreeninteractive=\"true\"></object> </div> "
    $('#mainDivContent').html(html);
}

function clearScreen(){
    var counter = 0;
    var allScreen = $('.streamContainer');
    for(i=0;i<allScreen.length;i++){
        if(allScreen.eq(i).html() == ""){
            counter++;
        }
    }
    if(counter == 3) {
        for (i = 0; i < allScreen.length; i++) {
            if (allScreen.eq(i).html() == "") {
                allScreen.eq(i).remove();
            }
            else{
                allScreen.eq(i).removeClass("streamContainer").addClass("streamContainerMain mainScreen");
            }
        }
    }
}

function dragStart(){
    if($('.streamContainerMain').length == 1){
        $('.streamContainerMain').removeClass("streamContainerMain").addClass("streamContainer mainScreen");
        var qHtml = "<div class=\"streamContainer subScreen\" ></div>"
        $('#mainDivContent').append(qHtml);
        $('#mainDivContent').append(qHtml);
        $('#mainDivContent').append(qHtml);
    }

    $('.streamContainer').droppable({
        hoverClass: "screenHover",
        drop:function(event, ui){
            //info idx 0='stream' 1=site 2=id 3=/link
            info = ui.draggable.prop('id').split('_');

            if(info[1]=='Douyu'){
                html = "<object  type=\"application/x-shockwave-flash\" data=\"http://staticlive.douyutv.com/common/share/play.swf?room_id="+info[2]+"\" width=\"100%\" height=\"100%\" allowscriptaccess=\"always\" allowfullscreen=\"true\" allowfullscreeninteractive=\"true\" allowfullscreen=\"true\"></object>"
                $(this).html(html);
            }
            if(info[1]=='Zhanqi'){
                html = "<iframe width=\"100%\" height=\"100%\" src=\"http://www.zhanqi.tv/live/embed?roomId="+info[2]+"\" frameborder=\"0\" allowfullscreen=\"true\" allowfullscreen=\"true\"></iframe>";
                $(this).html(html);
            }
            if(info[1]=='Huomao'){
                html = "<iframe height=\"100%\" width=\"100%\" src=\"http://www.huomaotv.com/index.php?c=outplayer&amp;live_id="+info[2]+"\" frameborder=\"0\" allowfullscreen=\"true\" allowfullscreen=\"true\"></iframe>";
                $(this).html(html);
            }
            if(info[1]=='Huya'){
                html = "<embed src=\"http://yy.com/s/"+info[2]+"/mini.swf\" quality=\"high\" width=\"100%\" height=\"100%\" align=\"middle\" allowscriptaccess=\"never\" allowfullscreen=\"true\" wmode=\"transparent\" type=\"application/x-shockwave-flash\">";
                $(this).html(html);
            }
            if(info[1]=='Twitch'){
                html = "<iframe src=\""+info[2]+"/embed\" frameborder=\"0\" scrolling=\"no\" height=\"100%\" width=\"100%\"></iframe>";
                $(this).html(html);
            }
            clearScreen();
        }
    });

    //$('.streamContainer').addClass('screenHover');
}

function streamListAjax(code){
    if(code == '000'){
        siteCode = '001';
    }else{
        siteCode = code;
    }
    $.ajax({
      url: 'ajax/getStreamList/'+siteCode+'/',
      cache: false,
      success: function(html){
          $('#streamList').html(html);

          $('.streamItem').draggable({
              stack: ".streamItem",
              containment: "#mainDivContent #streamList",
              revert: 'invalid',
              helper: "clone",
              scroll: false,
              start: function() {
                dragStart();
              },
              drag: function() {

              },
              stop: function() {
                //$('.streamContainer').removeClass('screenHover');
                clearScreen();
              }
          });
            /*

          */

      },

      complete: function(){
          //$('#loading-image').hide();
          if(code == '000') {
              loadFirstDouyuStream();
          }
      }
    });
};

function pageInit(){
    //$('#loading-image').show();
    streamListAjax('000');
}

$('#leftPanelSwitch').click(function(){
    var flag = $('#leftPanelFlag').text();
    if(flag == 'on'){
        hideLeftPanel();
    }else{
        showLeftPanel();
    }
})

$('#streamBtn').click(function(){
   $('#sitePicker').fadeIn(1000);
})
$('#bookmarkBtn').click(function(){
   $('#sitePicker').fadeOut(1000);
})

$('#getDouyuList').click(function(){
    streamListAjax('001');
})

$('#getZhanqiList').click(function(){
    streamListAjax('002');
})
$('#getHuomaoList').click(function(){
    streamListAjax('003');
})
$('#getHuyaList').click(function(){
    streamListAjax('004');
})
$('#getTwitchList').click(function(){
    streamListAjax('005');
})