var text1_maxchars=3000;
var mce_editor_0_undobuffer="";
var mce_editor_1_undobuffer="";


function myCustomOnInit(){
    tinyMCE_timer1=setTimeout("countchars('comment_form',tinyMCE.selectedInstance.editorId,text1_maxchars,'msgCounter')",1000);
}

function myCustomOnChangeHandler(inst){
    tinyMCE_timer1=setTimeout("countchars('comment_form',tinyMCE.selectedInstance.editorId,text1_maxchars,'msgCounter')",250);
}

function myHandleEvent(e){
    if(e.type=="keyup"){
        clearTimeout(tinyMCE_timer1);
        countchars('comment_form',tinyMCE.selectedInstance.editorId,text1_maxchars,'msgCounter')
    }
    return true;
}

function getHTML_TinyMCE(editor_id){
    obj=document.getElementById(editor_id);
    if(obj.contentDocument){
        content=obj.contentDocument.body.innerHTML;
    }else{
        content=top.frames[editor_id].document.body.innerHTML;
    }
    return content;
}

function countchars_TinyMCE(editor_id){
    content=getHTML_TinyMCE(editor_id);
    cnt=content.length;
    return cnt;
}

function countchars(formname,editor_id,maxchars,displayID){
    if(isNaN(maxchars)){
        maxchars=eval(maxchars);
    }
    currCount=countchars_TinyMCE(editor_id);
    remainCount=maxchars-currCount+1;
    tmpvar=editor_id+'_count';
    eval(tmpvar + '=currCount');
    displayObj=document.getElementById(displayID);
    displayObj.innerHTML=eval(remainCount-1);
    if(remainCount<=0){
        thisBuffer=eval(editor_id+'_undobuffer');
        if(thisBuffer.length > 0){
            tinyMCE_timer2=setTimeout("tinyMCE.setContent(thisBuffer)",250);
        };
        displayObj.innerHTML="0";
    } else {
        eval(editor_id+'_undobuffer=getHTML_TinyMCE(editor_id)');
    }
}

