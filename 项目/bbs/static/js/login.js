$('#btn').click(function () {
    let user = $('#id_user').val();
    let pwd = $('#id_pwd').val();
    let v_code = $('#v_code').val();
    let csrf_token = $('[name=csrfmiddlewaretoken]').val();
    $.ajax({
        url: '/login/',
        type: 'post',
        data: {
            'user': user,
            'pwd': pwd,
            'v_code': v_code,
            'csrfmiddlewaretoken': csrf_token,
        },
        success: function (res) {
            if (res.code === 0) {
                console.log('没问题');
                $('#msg').text('');
                location.href = '/index/'
            } else {
                console.log('有问题');
                $('#msg').text(res.msg).css('color', 'red')

            }
        }
    })
});
$('#v_code_img').click(function () {
        this.src += '?'
});

