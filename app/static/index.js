// function addQuotes()
// {
//        $.ajax({
//        type: "POST",
//        url: "/quotes/add",
//        // dataType: "json",
//        data: {
//          Author : $('#Author').val(),
//          BookTitle : $('#BookTitle').val(),
//          Quote: $('#Quote').val()
//        },
//        success: function(data,status)
//        {
//            alert(data);
//            $("#result").append(data);
//          },
//          complete: function(data,status) {
//             //optional, used for debugging purposes
//              // alert(status);
//          }
//  });
// }

function returnQuotesbyBook()
{
  $("#result").html("");

       $.ajax({
       type: "POST",
       url: "/quotes/getall",
       dataType: "json",
       data: $('form').serialize(),
       success: function(data,status)
       {
           // alert(data);
           $("#result").append(data);
         },
         complete: function(data,status) {
            //optional, used for debugging purposes
             // alert(status);
         }
 });
}

function addQuotes()
{
  // $("#result").html("");

       $.ajax({
       type: "POST",
       url: "/quotes/add",
       dataType: "json",
       data: $('form').serialize(),
       success: function(data,status)
       {
           // alert(data);
           $("#result").append(data);
         },
         complete: function(data,status) {
            //optional, used for debugging purposes
             // alert(status);
         }
 });
}
