function ask_post(){
    var id = document.getElementsByName('mail_id')[0].value;
    var service = document.getElementsByName('mail_service')[0].value;
    var rcpt_to = encodeURI(id + '@' + service); 
    var cate = encodeURI(document.getElementsByName('cate')[0].value);
    var mail_from = encodeURI(document.getElementsByName('email')[0].value);
    var user_name = encodeURI(document.getElementsByName('user_name')[0].value);
    var budget = encodeURI(document.getElementsByName('budget')[0].value);
    var body = encodeURI(document.getElementsByName('body')[0].value);
    if (MailCheck(mail_from) == false) {
        alert('連絡先メールアドレスが不正です');
        return;
    }
    var post_data = {'rcpt_to': rcpt_to, 'cate': cate, 'mail_from': mail_from, 'user_name': user_name, 'budget': budget, 'body': body};

    // ajax
    $.ajax({
        url: 'https://nanaomi3.shop/ask/post',
        type: 'POST',
        cache: false,
        data: post_data
    }).done(function(data, textStatus, jqXHR){ 
        alert('メールを送信しました');
        window.location.href = 'https://nanaomi3.shop';
        return;
    }).fail(function(jqXHR, textStatus, errorThrown){
        alert('メール送信に失敗しました');
        return;
    });
}


function MailCheck(mail) {
    var mail_regex1 = new RegExp( '(?:[-!#-\'*+/-9=?A-Z^-~]+\.?(?:\.[-!#-\'*+/-9=?A-Z^-~]+)*|"(?:[!#-\[\]-~]|\\\\[\x09 -~])*")@[-!#-\'*+/-9=?A-Z^-~]+(?:\.[-!#-\'*+/-9=?A-Z^-~]+)*' );
    var mail_regex2 = new RegExp( '^[^\@]+\@[^\@]+$' );
    if( mail.match( mail_regex1 ) && mail.match( mail_regex2 ) ) {
        // 全角チェック
        if( mail.match( /[^a-zA-Z0-9\!\"\#\$\%\&\'\(\)\=\~\|\-\^\\\@\[\;\:\]\,\.\/\\\<\>\?\_\`\{\+\*\} ]/ ) ) { return false; }
        // 末尾TLDチェック（〜.co,jpなどの末尾ミスチェック用）
        if( !mail.match( /\.[a-z]+$/ ) ) { return false; }
        return true;
    } else {
        return false;
    }
}
