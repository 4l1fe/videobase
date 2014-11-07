# coding: utf-8

###############################################################################
APP_CONTENTS_LOC_TYPE = (
    ('ivi','ivi'),
    ('zoomby','zoomby'),
    ('megogo','megogo'),
    ('tvigle','tvigle'),
    ('playfamily','playfamily'),
    ('amediateka','amediateka'),
    ('molodejj','molodejj'),
    ('nowru','nowru'),
    ('streamru','streamru'),
    ('tvzavr','tvzavr'),
    ('viaplay','viaplay'),
    ('zabavaru','zabavaru'),
    ('tvzorru','tvzorru'),
    ('playgoogle','playgoogle'),
    ('itunes','itunes'),
    ('ayyo','ayyo'),
    ('mosfilm','mosfilm'),
    ('olltv','olltv'),
    ('0','0'),
)


###############################################################################
APP_CONTENTS_PRICE_TYPE_FREE = 0
APP_CONTENTS_PRICE_TYPE_SUBSCRIPTION = 1
APP_CONTENTS_PRICE_TYPE_PAY = 2

APP_CONTENTS_PRICE_TYPE = (
    (APP_CONTENTS_PRICE_TYPE_FREE, 'Бесплатно'),
    (APP_CONTENTS_PRICE_TYPE_SUBSCRIPTION, 'По подписке'),
    (APP_CONTENTS_PRICE_TYPE_PAY, 'Платно')
)

###############################################################################
APP_CONTENTS_COMMENT_STATUS = ()

##############################################################################
APP_LOCATION_TYPE_ADDITIONAL_MATERIAL_FILM = 'FILM'
APP_LOCATION_TYPE_ADDITIONAL_MATERIAL_SEASON = 'SEASON'
APP_LOCATION_TYPE_ADDITIONAL_MATERIAL_EPISODE = 'EPISODE'

APP_LOCATION_TYPE_ADDITIONAL_MATERIAL = (
    (APP_LOCATION_TYPE_ADDITIONAL_MATERIAL_FILM, u'Фильм'),
    (APP_LOCATION_TYPE_ADDITIONAL_MATERIAL_SEASON, u'Сезон'),
    (APP_LOCATION_TYPE_ADDITIONAL_MATERIAL_EPISODE, u'Серия')
)
