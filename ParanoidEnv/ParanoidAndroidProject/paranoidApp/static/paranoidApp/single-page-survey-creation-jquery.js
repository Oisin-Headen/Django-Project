var QUESTION_LENGTH = 100;

var question = [
    '<div class="question">',
        '<div>',
            '<label>Question Text <span class="required-marker">*</span></label>',
            '<textarea class="question-text"></textarea>',
            '<p class="survey-error"></p>',
        '</div>',
        '<div>',
            '<label>Question Name <span class="required-marker">*</span></label>',
            '<input class="question-name" type="text">',
            '<p class="survey-error"></p>',
        '</div>',
        '<div>',
            '<label>Optional Question</label>',
            '<input class="question-optional" type="checkbox">',
        '</div>',
        '<div>',
            '<label>Question Type</label>',
            '<select class="question-type">',
                '<option value="text">Text</option>',
                '<option value="dropdown">Dropdown</option>',
                '<option value="boolean">Yes or No</option>',
                '<option value="radio">Radio Buttons</option>',
                '<option value="number_rating">Numerical Range</option>',
                '<option value="numerical">Number</option>',
                '<option value="email">Email</option>',
            '</select>',
        '</div>',
        '<div class="question-type-specific"></div>',
        '<p class="remove">Remove Question</p>',
    '</div>'
].join('\n');


var number_rating_extra = [
    '<div class="number-rating-extra">',
        '<div>',
            '<label>Minimum Number <span class="required-marker">*</span></label>',
            '<input type="number" class="minimum" value="0" required>',
            '<p class="survey-error"></p>',
        '</div>',
        '<div>',
            '<label>Maximum Number <span class="required-marker">*</span></label>',
            '<input type="number" class="maximum" value="10" required>',
            '<p class="survey-error"></p>',
        '</div>',
    '</div>'
].join('\n');

var numerical_extra = [
    '<div class="numerical-extra">',
        '<div>',
            '<label>Minimum Number</label>',
            '<input type="number" class="minimum">',
        '</div>',
        '<div>',
            '<label>Maximum Number</label>',
            '<input type="number" class="maximum">',
        '</div>',
        '<p class="survey-error"></p>',
    '</div>'
].join('\n');

var multiple_choice_extra_option = [
    '<div class="option">',
        '<input type="text" class="option-text"><span class="required-marker">*</span>',
        '<p class="survey-error"></p>',
        '<p class="remove-option">Remove Option</p>',
    '</div>'
].join('\n');


var multiple_choice_extra_start = [
    '<div class="multiple-choice-extra">',
        '<label>Options:</label>',
        '<div class="options"></div>',
        '<p class="survey-error"></p>',
        '<p class="add-option">Add an Option</p>',
    '</div>'
].join('\n');

var boolean_extra = [
    '<label>Reveal on:</label>',
    '<select class="boolean-on">',
        '<option value="true">Yes</option>',
        '<option value="false">No</option>',
    '</select>',
    '<div class="boolean-subquestions"></div>',
    '<p class="add-subquestion">Add a Subquestion</p>'
].join('\n');

function RemoveOption($question_type_area)
{
    $question_type_area.find('.remove-option').click(function(){
        $(this).parents('.option').remove();
    });
}

$(document).ready(function () {
    $('#add-question').click(function () {
        $('#questions').append(question);
        $('.remove').click(function () {
            $(this).parent('.question').remove();
        });
        $('.question-type').change(function(){
            var $question_type_specific = $(this).parents('.question').find('.question-type-specific');
            $question_type_specific.empty();
            var type = $(this).val();
            if(type == 'number_rating'){
                $question_type_specific.append(number_rating_extra);
            }
            if(type == 'numerical'){
                $question_type_specific.append(numerical_extra);
            }
            else if(type == 'radio' || type == 'dropdown'){
                $question_type_specific.append(multiple_choice_extra_start);
                $question_type_specific.find('.options').append(multiple_choice_extra_option);
                $question_type_specific.find('.add-option').click(function(){
                    $(this).siblings('.options').append(multiple_choice_extra_option);
                    RemoveOption($question_type_specific);
                });
                RemoveOption($question_type_specific);
            }
            else if(type == 'boolean'){
                $question_type_specific.append(boolean_extra);
                $question_type_specific.find('.add-subquestion').click(function(){
                    $(this).siblings('.boolean-subquestions').append(question);
                    $(this).siblings('.boolean-subquestions').find('.question').each(function(){
                        $(this).addClass('subquestion');
                        $(this).removeClass('question');
                    });
                    $(this).siblings('.boolean-subquestions').find('.remove').click(function () {
                        $(this).parent('.subquestion').remove();
                    });
                    $('.question-type').change(function(){
                        var $boolean_question_type_specific = $(this).parent('div').siblings('.question-type-specific');
                        $boolean_question_type_specific.empty();
                        var type = $(this).val();
                        if(type == 'number_rating'){
                            $boolean_question_type_specific.append(number_rating_extra);
                        }
                        if(type == 'numerical'){
                            $boolean_question_type_specific.append(numerical_extra);
                        }
                        else if(type == 'radio' || type == 'dropdown'){
                            $boolean_question_type_specific.append(multiple_choice_extra_start);
                            $boolean_question_type_specific.find('.options').append(multiple_choice_extra_option);
                            $boolean_question_type_specific.find('.add-option').click(function(){
                                $(this).siblings('.options').append(multiple_choice_extra_option);
                                RemoveOption($boolean_question_type_specific);
                            });
                            RemoveOption($boolean_question_type_specific);
                        }
                    });
                });
            }
        });
    });




    

    $('#submit').click(function () {
        $('.survey-error').empty()
        error = false;
        survey_json = {}
        survey_json['name'] = $('#survey-name').val();
        if(survey_json['name'].length > 200 || survey_json['name'].length <= 0)
        {
            $('#survey-name').siblings(".survey-error").html("Name must be between 1 and 200 characters.");
            error = true;
        }
        survey_json['desc'] = $('#survey-desc').val();
        if(survey_json['desc'].length > 500 || survey_json['desc'].length <= 0)
        {
            $('#survey-desc').siblings(".survey-error").html("Description must be between 1 and 500 characters.");
            error = true;
        }

        survey_json['questions'] = [];
        $('#questions .question').each(function () {
            question_column_name = $(this).find('.question-name').val();
            question_text = $(this).find('.question-text').val();
            question_type = $(this).find('.question-type').val();

            if(question_column_name.length > QUESTION_LENGTH || question_column_name.length <= 0)
            {
                $(this).find('.question-name').siblings(".survey-error").html("Question name must be between 1 and "+QUESTION_LENGTH+" characters");
                error = true;
            }
            if(question_text.length > QUESTION_LENGTH || question_text.length <= 0)
            {
                $(this).find('.question-text').siblings(".survey-error").html("Question must be between 1 and "+QUESTION_LENGTH+" characters");
                error = true;
            }

            question_data = {
                'column-name': question_column_name,
                'text': question_text,
                'type': question_type
            }
            if ($(this).find('.question-optional').is(':checked'))
            {
                question_data['optional'] = 'optional';
            }

            if(question_type == 'number_rating')
            {
                question_data['min'] = $(this).find('.minimum').val();
                question_data['max'] = $(this).find('.maximum').val();

                if(question_data['min'] > question_data['max'])
                {
                    $(this).find('.number-rating-extra .survey-error').html("Min cannot be greater than max");
                    error = true;
                }
                if(question_data['min'] == '')
                {
                    $(this).find(".minimum").siblings(".survey-error").html("Min is required")
                    error = true;
                }
                if(question_data['max'] == '')
                {
                    $(this).find(".maximum").siblings(".survey-error").html("Max is required")
                    error = true;
                }
            }
            if(question_type == 'numerical')
            {
                min = $(this).find('.minimum').val();
                max = $(this).find('.maximum').val();
                if(min != '')
                {
                    question_data['min'] = min;
                }
                if(max != '')
                {
                    question_data['max'] = max;
                }
                if(max != '' && min != '')
                {
                    if(min > max)
                    {
                        $(this).find('.numerical-extra .survey-error').html("Min cannot be greater than max");
                        error = true;
                    }
                }
            }
            else if(question_type == 'radio' || question_type == 'dropdown'){
                var options = [];
                $(this).find('.option-text').each(function(){
                    option = $(this).val()
                    if(option.length == 0)
                    {
                        $(this).siblings(".survey-error").html("Option cannot be left empty");
                        error = true;
                    }
                    if (options.includes(option))
                    {
                        $(this).siblings(".survey-error").html("This option is already listed");
                        error = true;
                    }
                    options.push(option);
                });
                if(options.length == 0)
                {
                    $(this).find(".multiple-choice-extra").children(".survey-error").html("At least one option must be listed");
                    error = true;
                }
                question_data['choices'] = options;
            }




            else if (question_type == 'boolean')
            {  
                var subquestions = [];
                $(this).find('.subquestion').each(function(){
                    subquestion_column_name = $(this).find('.question-name').val();
                    subquestion_text = $(this).find('.question-text').val();
                    subquestion_type = $(this).find('.question-type').val();

                    if(subquestion_column_name.length > QUESTION_LENGTH || subquestion_column_name.length <= 0)
                    {
                        $(this).find('.question-name').siblings(".survey-error").html("Question name must be between 1 and "+QUESTION_LENGTH+" characters");
                        error = true;
                    }
                    if(subquestion_text.length > QUESTION_LENGTH || subquestion_text.length <= 0)
                    {
                        $(this).find('.question-text').siblings(".survey-error").html("Question must be between 1 and "+QUESTION_LENGTH+" characters");
                        error = true;
                    }

                    subquestion_data = {
                        'column-name': subquestion_column_name,
                        'text': subquestion_text,
                        'type': subquestion_type
                    }
                    if ($(this).find('.question-optional').is(':checked'))
                    {
                        subquestion_data['optional'] = 'optional';
                    }

                    if(subquestion_type == 'number_rating'){
                        subquestion_data['min'] = $(this).find('.minimum').val();
                        subquestion_data['max'] = $(this).find('.maximum').val();
                        if(subquestion_data['min'] > subquestion_data['max'])
                        {
                            $(this).find('.number-rating-extra .survey-error').html("Min cannot be greater than max");
                            error = true;
                        }
                        if(subquestion_data['min'] == '')
                        {
                            $(this).find(".minimum").siblings(".survey-error").html("Min is required")
                            error = true;
                        }
                        if(subquestion_data['max'] == '')
                        {
                            $(this).find(".maximum").siblings(".survey-error").html("Max is required")
                            error = true;
                        }
                    }
                    else if(subquestion_type == 'numerical'){
                        min = $(this).find('.minimum').val();
                        max = $(this).find('.maximum').val();
                        if(min != '')
                        {
                            subquestion_data['min'] = min;
                        }
                        if(max != '')
                        {
                            subquestion_data['max'] = max;
                        }
                        if(max != '' && min != '')
                        {
                            if(min > max)
                            {
                                $(this).find('.numerical-extra .survey-error').html("Min cannot be greater than max");
                                error = true;
                            }
                        }
                    }
                    else if(subquestion_type == 'radio' || subquestion_type == 'dropdown')
                    {
                        var options = [];
                        $(this).find('.option-text').each(function(){
                            option = $(this).val()
                            if(option.length == 0)
                            {
                                $(this).siblings(".survey-error").html("Option cannot be left empty");
                                error = true;
                            }
                            if (options.includes(option))
                            {
                                $(this).siblings(".survey-error").html("This option is already listed");
                                error = true;
                            }
                            options.push(option);
                        });
                        if(options.length == 0)
                        {
                            $(this).find(".multiple-choice-extra").children(".survey-error").html("At least one option must be listed");
                            error = true;
                        }
                        subquestion_data['choices'] = options;
                    }
                    subquestions.push(subquestion_data);
                });
                if(subquestions.length != 0)
                {
                    question_data['subquestions'] = subquestions;
                    question_data['on'] = $(this).find('.boolean-on').val();
                }
            }

            survey_json['questions'].push(question_data);
        });
        if(!error)
        {
            var survey_string = JSON.stringify(survey_json);
            $('#hidden-input').val(survey_string);
            $('#hidden-form').submit();
        }
    });
});