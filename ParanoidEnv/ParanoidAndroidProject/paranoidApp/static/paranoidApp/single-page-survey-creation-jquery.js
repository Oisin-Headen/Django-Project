var survey_json = {};
var question = [
    "<div class=\"question\">",
        "<div>",
            "<label>Question Text</label>",
            "<textarea class=\"question-text\"></textarea>",
        "</div>",
        "<div>",
            "<label>Question Name</label>",
            "<input class=\"question-name\" type=\"text\">",
        "</div>",
        "<div>",
            "<label>Question type</label>",
            "<select class=\"question-type\">",
                "<option value=\"text\">Text</option>",
                "<option value=\"single_answer_multiple_choice\">Dropdown</option>",
                "<option value=\"boolean\">Yes or No</option>",
                "<option value=\"scale\">Radio Buttons</option>",
                "<option value=\"number_rating\">Numerical</option>",
                "<option value=\"email\">Email</option>",
            "</select>",
        "</div>",
        "<div class=\"question-type-specific\"></div>",
        "<p class=\"remove\">Remove Question</p>",
    "</div>"
].join("\n");


number_rating_extra = [
    "<div>",
        "<label>Minimum Number</label>",
        "<input type=\"number\" class=\"minimum\" value=\"0\">",
    "</div>",
    "<div>",
        "<label>Maximum Number</label>",
        "<input type=\"number\" class=\"maximum\" value=\"10\">",
    "</div>"
].join("\n");

multiple_choice_extra_option = [
    "<div>",
        "<input type=\"text\">",
        "<p class=\"remove-option\">Remove Option</p>",
    "</div>"
].join("\n");


multiple_choice_extra_start = [
    "<div class=\"options\">",
        "<label>Options:</label>",
    "</div>",
    "<p class=\"add-option\">Add an Option</p>"
].join("\n");


$(document).ready(function () {
    $("#add-question").click(function () {
        $("#questions").append(question);
        $(".remove").click(function () {
            $(this).parent(".question").remove();
        });
        $(".question-type").change(function(){
            var $question_type_specific = $(this).parents(".question").find(".question-type-specific");
            $question_type_specific.empty();
            var type = $(this).val();
            if(type == "number_rating"){
                $question_type_specific.append(number_rating_extra);
            }
            else if(type == "scale" || type == "single_answer_multiple_choice"){
                $question_type_specific.append(multiple_choice_extra_start);
                $question_type_specific.find(".options").append(multiple_choice_extra_option);
            }
            
        });
    });

    

    $("#submit").click(function () {
        survey_json['survey-name'] = $("#survey-name").val();
        survey_json['survey-desc'] = $("#survey-desc").val();
        survey_json['questions'] = [];
        $("#questions .question").each(function () {
            question_column_name = $(this).find(".question-name").val();
            question_text = $(this).find(".question-text").val();
            question_type = $(this).find(".question-type").val();
            question_data = {
                "column-name": question_column_name,
                "text": question_text,
                "type": question_type
            }

            if(question_type == "number_rating"){
                question_data['min'] = $(this).find(".minimum").val();
                question_data['max'] = $(this).find(".maximum").val();
            }

            survey_json['questions'].push(question_data);
        });
        console.log(survey_json);
    });
});