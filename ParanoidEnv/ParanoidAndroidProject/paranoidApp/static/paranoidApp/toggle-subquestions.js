$(document).ready(function(){
    $(".subquestions").hide();
    $(".subquestions-mainquestion").change(function(){
        sectionclass = $(this).attr('data-subquestion-header');
        // $(".subquestions").slideToggle();
        // $("."+sectionclass).slideToggle();
        if ($(this).attr("data-on") == "True")
        {
            $("."+sectionclass).slideDown();
            $("."+sectionclass+" textarea," +
              "."+sectionclass+" select," +
              "."+sectionclass+" input").each(function(){
                optional = $(this).attr("data-optional");
                if(optional == "False")
                {
                    $(this).prop("required", true);
                }
            });
        }
        else
        {
            $("."+sectionclass).slideUp();
            $("."+sectionclass+" textarea," +
              "."+sectionclass+" select," +
              "."+sectionclass+" input").each(function(){
                $(this).prop("required", false);
            });
        }
    });
    $(".number-rating").each(function(){
        value = $(this).val();
        $(this).parent("section").find(".number-rating-display").html(value);
    });
    $(".number-rating").on("input",function(){
        value = $(this).val();
        $(this).parent("section").find(".number-rating-display").html(value);
    });
});