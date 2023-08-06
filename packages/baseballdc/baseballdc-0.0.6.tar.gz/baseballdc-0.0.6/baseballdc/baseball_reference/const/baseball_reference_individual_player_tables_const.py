BASEBALL_REFERENCE_INDIVIDUAL_PLAYER_URL_PREFIX = 'https://www.baseball-reference.com/players'

BASEBALL_REFERENCE_PLAYER_TABLE_CONFIGS = [
    {
        'table': 'Standard Batting',
        'table_identifier': 'batting_standard',
        'url_prefix': BASEBALL_REFERENCE_INDIVIDUAL_PLAYER_URL_PREFIX,
        'first_name_required': True,
        'last_name_required': True,
        'url_postfix': '',
        'shtml_postfix_required': True,
        'remove_rows_on': []     
    },
    {
        'table': 'Player Value—Batting',
        'table_identifier': 'batting_value',
        'url_prefix': BASEBALL_REFERENCE_INDIVIDUAL_PLAYER_URL_PREFIX,
        'first_name_required': True,
        'last_name_required': True,
        'url_postfix': '',
        'shtml_postfix_required': True,
        'remove_rows_on': []     
    },
    {
        'table': 'Advanced Batting',
        'table_identifier': 'batting_advanced',
        'url_prefix': BASEBALL_REFERENCE_INDIVIDUAL_PLAYER_URL_PREFIX,
        'first_name_required': True,
        'last_name_required': True,
        'url_postfix': '',
        'shtml_postfix_required': True,
        'remove_rows_on': []     
    },
    {
        'table': 'Standard Fielding',
        'table_identifier': 'standard_fielding',
        'url_prefix': BASEBALL_REFERENCE_INDIVIDUAL_PLAYER_URL_PREFIX,
        'first_name_required': True,
        'last_name_required': True,
        'url_postfix': '',
        'shtml_postfix_required': True,
        'remove_rows_on': []     
    },
    {
        'table': 'Appearances',
        'table_identifier': 'appearances',
        'url_prefix': BASEBALL_REFERENCE_INDIVIDUAL_PLAYER_URL_PREFIX,
        'first_name_required': True,
        'last_name_required': True,
        'url_postfix': '',
        'shtml_postfix_required': True,
        'remove_rows_on': []     
    }
]

BASEBALL_REFERENCE_INDIVIDUAL_PLAYER_TABLE_CONFIGS = [
    *BASEBALL_REFERENCE_PLAYER_TABLE_CONFIGS
]