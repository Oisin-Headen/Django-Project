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
            "<label>Optional Question</label>",
            "<input class=\"question-optional\" type=\"checkbox\">",
        "</div>",
        "<div>",
            "<label>Question Type</label>",
            "<select class=\"question-type\">",
                "<option value=\"text\">Text</option>",
                "<option value=\"dropdown\">Dropdown</option>",
                "<option value=\"boolean\">Yes or No</option>",
                "<option value=\"radio\">Radio Buttons</option>",
                "<option value=\"number_rating\">Numerical Range</option>",
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
    "<div class=\"option\">",
        "<input type=\"text\" class=\"option-text\">",
        "<p class=\"remove-option\">Remove Option</p>",
    "</div>"
].join("\n");


multiple_choice_extra_start = [
    "<label>Options:</label>",
    "<div class=\"options\"></div>",
    "<p class=\"add-option\">Add an Option</p>"
].join("\n");

boolean_extra = [
    "<label>Reveal on:</label>",
    "<select class=\"boolean-on\">",
        "<option value=\"true\">Yes</option>",
        "<option value=\"false\">No</option>",
    "</select>",
    "<div class=\"boolean-subquestions\"></div>",
    "<p class=\"add-subquestion\">Add a Subquestion</p>"
].join("\n");

function RemoveOption($question_type_area)
{
    $question_type_area.find(".remove-option").click(function(){
        $(this).parents(".option").remove();
    });
}

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
            else if(type == "radio" || type == "dropdown"){
                $question_type_specific.append(multiple_choice_extra_start);
                $question_type_specific.find(".options").append(multiple_choice_extra_option);
                $question_type_specific.find(".add-option").click(function(){
                    $(this).siblings(".options").append(multiple_choice_extra_option);
                    RemoveOption($question_type_specific);
                });
                RemoveOption($question_type_specific);
            }
            else if(type == "boolean"){
                $question_type_specific.append(boolean_extra);
                $question_type_specific.find(".add-subquestion").click(function(){
                    $(this).siblings(".boolean-subquestions").append(question);
                    $(this).siblings(".boolean-subquestions").find(".question").each(function(){
                        $(this).addClass("subquestion");
                        $(this).removeClass("question");
                    });
                    $(".remove").click(function () {
                        $(this).parent(".question").remove();
                    });
                    $(".question-type").change(function(){
                        var $boolean_question_type_specific = $(this).parent("div").siblings(".question-type-specific");
                        $boolean_question_type_specific.empty();
                        var type = $(this).val();
                        if(type == "number_rating"){
                            $boolean_question_type_specific.append(number_rating_extra);
                        }
                        else if(type == "radio" || type == "dropdown"){
                            $boolean_question_type_specific.append(multiple_choice_extra_start);
                            $boolean_question_type_specific.find(".options").append(multiple_choice_extra_option);
                            $boolean_question_type_specific.find(".add-option").click(function(){
                                $(this).siblings(".options").append(multiple_choice_extra_option);
                                RemoveOption($boolean_question_type_specific);
                            });
                            RemoveOption($boolean_question_type_specific);
                        }
                    });
                });
            }
        });
    });

    

    $("#submit").click(function () {
        survey_json['name'] = $("#survey-name").val();
        survey_json['desc'] = $("#survey-desc").val();
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
            if ($(this).find(".question-optional").is(":checked"))
            {
                question_data['optional'] = "optional";
            }

            if(question_type == "number_rating"){
                question_data['min'] = $(this).find(".minimum").val();
                question_data['max'] = $(this).find(".maximum").val();
            }
            else if(question_type == "radio" || question_type == "dropdown"){
                var options = [];
                $(this).find(".option-text").each(function(){
                    options.push($(this).val());
                });
                question_data['choices'] = options;
            }
            else if (question_type == "boolean")
            {  
                var subquestions = [];
                $(this).find(".subquestion").each(function(){
                    subquestion_column_name = $(this).find(".question-name").val();
                    subquestion_text = $(this).find(".question-text").val();
                    subquestion_type = $(this).find(".question-type").val();
                    subquestion_data = {
                        "column-name": subquestion_column_name,
                        "text": subquestion_text,
                        "type": subquestion_type
                    }
                    if ($(this).find(".question-optional").is(":checked"))
                    {
                        subquestion_data['optional'] = "optional";
                    }

                    if(subquestion_type == "number_rating"){
                        subquestion_data['min'] = $(this).find(".minimum").val();
                        subquestion_data['max'] = $(this).find(".maximum").val();
                    }
                    else if(subquestion_type == "radio" || subquestion_type == "dropdown"){
                        var options = [];
                        $(this).find(".option-text").each(function(){
                            options.push($(this).val());
                        });
                        subquestion_data['choices'] = options;
                    }
                    subquestions.push(subquestion_data);
                });
                if(subquestions.length != 0)
                {
                    question_data['subquestions'] = subquestions;
                    question_data['on'] = $(this).find(".boolean-on").val();
                }
            }

            survey_json['questions'].push(question_data);
        });
        var survey_string = JSON.stringify(survey_json);
        // console.log(survey_json);
        $("#hidden-input").val(survey_string);
        $("#hidden-form").submit();
    });
});