# coding: utf-8
APP_ROBOT_SUCCESS = 'success'
APP_ROBOT_FAIL = 'fail'

APP_ROBOTS_PARSE_TRY_RESULT_TYPES = (
    (APP_ROBOT_SUCCESS, u'Успех'),
    (APP_ROBOT_FAIL, u'Неудача'),
)

#############################################################################################################

APP_ROBOTS_TRY_SITE_UNAVAILABLE = 'sitefail'
APP_ROBOTS_TRY_NO_SUCH_PAGE = 'pagefail'
APP_ROBOTS_TRY_PARSE_ERROR = 'parsefail'
APP_ROBOTS_TRY_SUCCESS = 'success'

APP_ROBOT_VALUE = ['ivi', 'nowru', 'tvigle', 'zoomby', 'tvzavr', 'mosfilm']

APP_ROBOTS_TRY_OUTCOME = (
    (APP_ROBOTS_TRY_SITE_UNAVAILABLE, u'Сайт недоступен'),
    (APP_ROBOTS_TRY_NO_SUCH_PAGE, u'Нет такой страницы'),
    (APP_ROBOTS_TRY_PARSE_ERROR, u'Ошибка при парсинге'),
    (APP_ROBOTS_TRY_SUCCESS, u'Данные успешно получены'),
)
