from .models import LessonInfo, Time, Community

def get_validated_data(data):
    res = []
    for i in data:
        lesson_dict = i._mapping
        lesson = LessonInfo.model_validate(lesson_dict)
        time = Time.model_validate({'start':lesson_dict['start'], 'end': lesson_dict['end']})
        group = Community.model_validate({
            'id':lesson_dict['group_id'], 
            'department_id':lesson_dict['group_department_id'], 
            'year':lesson_dict['group_year'],
            'value':lesson_dict['group_value'],
            })
        teacher = Community.model_validate({
            'id':lesson_dict['teacher_id'], 
            'department_id':lesson_dict['teacher_department_id'], 
            'year':lesson_dict['teacher_year'],
            'value':lesson_dict['teacher_value'],
            })
        lesson.group = group
        lesson.teacher = teacher
        lesson.time = time
        res.append(lesson)
    return res