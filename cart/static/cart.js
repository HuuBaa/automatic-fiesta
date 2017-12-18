$(document).ready(function() {
    var session=$('#session').val();
    setTimeout(requestInventory,100);

    $('#addCart').click(function (event) {
        $.ajax({
            url:'http://localhost:8000/cart/',
            type:'post',
            data:{
                session:session,
                action:'add'
            },
            beforeSend:function (xhr) {
                $(event.target).attr('disabled','disabled');
            },
            success:function (data,status,xhr) {
                $("#add-cart").hide();
                $('#remove-from-cart').show();
                $(event.target).removeAttr('disabled')
            }
        })
    });

    $('#removeCart').click(function (event) {
        $.ajax({
            url:'http://localhost:8000/cart/',
            type:'post',
            data:{
                session:session,
                action:'remove'
            },
            beforeSend:function (xhr) {
                $(event.target).attr('disabled','disabled');
            },
            success:function (data,status,xhr) {
                $('#remove-from-cart').hide();
                $('#add-cart').show();
                $(event.target).removeAttr('disabled');
            }

        })
    });


    function requestInventory(){
       $.getJSON('http://localhost:8000/cart/status/',{session:session},function(data,status,xhr) {
            $('#count').html(data['inventoryCount']);
           setTimeout(requestInventory,0);
       })
    }
});