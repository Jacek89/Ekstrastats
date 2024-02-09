import random
from ..templatetags.custom_filters import ordinal


def summary_post(round_num: int, num_games: int, goals: int, gpm: float, score_stats: dict, own_goals):
    title = f"Summary of the {ordinal(round_num)} round of Ekstraklasa."
    subtitle_phrase = "all nine matches" if num_games == 9 else f"{num_games} of nine matches"
    subtitle_choice = [f"The {ordinal(round_num)} round of the Ekstraklasa has concluded with {subtitle_phrase} "
                       f"delivering a spectacle of football that left fans on the edge of their seats. "
                       f"From nail-biting encounters to goal fests, this round had it all.",
                       f"The {ordinal(round_num)} round of Ekstraklasa has wrapped up, treating fans to an "
                       f"exhilarating display of football across {subtitle_phrase}. From intense nail-biters to "
                       f"goal-filled extravaganzas, this round showcased a diverse range of thrilling moments that had "
                       f"spectators eagerly anticipating every play.",
                       f"The curtains have fallen on the {ordinal(round_num)} round of Ekstraklasa, leaving "
                       f"football enthusiasts captivated by the drama unfolding across {subtitle_phrase}. This round "
                       f"offered a rich tapestry of excitement, featuring gripping encounters and goal-filled "
                       f"spectacles that had fans at the edge of their seats."]
    subtitle = random.choice(subtitle_choice)

    body_choice = [f"In summary, the latest round of the Ekstraklasa treated fans to an array of captivating matches, "
                   f"producing a total of {goals} goals. From high-scoring encounters to tightly contested draws, "
                   f"the league continues to showcase the competitive spirit of Polish football. As teams look ahead"
                   f" to the next fixtures, the race for the top spot intensifies, promising more excitement for fans"
                   f" in the upcoming matches.",
                   f"Summing up the most recent Ekstraklasa fixtures, fans were treated to a series of enthralling "
                   f"matches that collectively saw the net bulge {goals} times. Whether through high-scoring showdowns "
                   f"or closely fought draws, the league remains a testament to the fierce competition in Polish "
                   f"football. As teams set their sights on the upcoming fixtures, the battle for the top position "
                   f"escalates, ensuring heightened anticipation and excitement for fans in the matches ahead.",
                   f"In a nutshell, the latest round of Ekstraklasa unfolded with a variety of captivating matches, "
                   f"boasting a total of {goals} goals. Ranging from goal-rich clashes to tightly contested draws, "
                   f"the league continues to embody the competitive essence of Polish football. Looking forward to the"
                   f" upcoming fixtures, the quest for the top spot gains momentum, promising fans more exhilarating "
                   f"moments in the matches to come."]

    if gpm >= 3.5:
        body_gpm = f"In a football extravaganza, the Ekstraklasa delivered an astonishing average of {gpm} goals " \
                    f"per match in the round. This goal-scoring spectacle made the round truly exceptional," \
                    f" showcasing a richness and flair rarely witnessed in football matches. The sheer abundance of" \
                    f" goals added an extraordinary vibrancy, turning each match into a captivating display of skil" \
                    f"l and excitement. Such a prolific goal-per-match ratio is a rarity, underlining the uniqueness" \
                    f" of this particular Ekstraklasa round. The experience of watching these matches was nothing " \
                    f"short of fantastic, as the relentless scoring contributed to a thrilling and memorable viewing " \
                    f"spectacle for football enthusiasts."
    elif gpm >= 3:
        body_gpm = f"An average of {gpm} goals per match illuminated the pitch, " \
                    f"offering a notable increase from the usual standards. The intriguing nature of this round is " \
                    f"evident, given the elevated goal-scoring activity. The matches must have been particularly " \
                    f"captivating, showcasing an above-average level of excitement and offensive action. The hope " \
                    f"among fans is that this uptick in goal-scoring isn't a one-time occurrence but rather a trend " \
                    f"that will continue to grace future rounds, adding sustained excitement to the league."
    elif gpm >= 2.4:
        body_gpm = f"An average of {gpm} goals per match colored the competitions." \
                    f" Despite the goal count aligning roughly with the typical standards, the matches unfolded in an" \
                    f" intriguing fashion, weaving captivating storylines. However, there is a sense of regret that" \
                    f" this round wasn't embellished with a higher number of goals, as a greater goal tally would have"\
                    f" truly elevated the spectacle. Nonetheless, the round managed to offer fans an engaging" \
                    f" narrative, even if the goal count didn't reach the heights of what could have been a truly" \
                    f" spectacular showcase."
    else:
        body_gpm = f"An average of {gpm} goals per match marked a notably" \
                    f" low-scoring affair. While the goal tally was modest, a silver lining emerged in the form of" \
                    f" a few exceptionally beautiful goals that are bound to be etched in our memories for a long " \
                    f"time. Despite the scarcity of goals in this round, the uniqueness and quality of those scored" \
                    f" added a touch of brilliance to the matches. We hope that this minimal goal count is a one-time" \
                    f" occurrence, and we eagerly anticipate the upcoming Ekstraklasa round to compensate with a more" \
                    f" plentiful display of goals, restoring the high-scoring excitement we've come to expect."

    body_scores = ""
    if score_stats['draw'] >= 6:
        body_scores = "<br><br>Prevalent theme was the abundance of drawn matches, " \
                       "creating an atmosphere of parity and closely contested encounters. The league witnessed a " \
                       "considerable number of teams sharing the spoils, resulting in a series of matches that " \
                       "reflected a balanced competition. This prevalence of draws adds an intriguing layer to the " \
                       "narrative of the round, highlighting the competitiveness and the ability of teams to evenly " \
                       "match each other on the field. The frequency of ties serves as a testament to the closely " \
                       "matched skill levels and unpredictability that characterize the Ekstraklasa, keeping fans " \
                       "on the edge of their seats as teams strive for supremacy."
    elif score_stats['home'] >= 6:
        body_scores = "<br><br>Notable trend emerged as a significant number of teams " \
                       "secured victories on their home turf. This pattern sheds light on the pivotal role that home" \
                       " support and playing in familiar stadiums play in the dynamics of the league. The prevalence" \
                       " of home wins underscores the impact of enthusiastic fanbases and the comfort that comes with" \
                       " playing on one's own ground. It emphasizes the psychological advantage that comes with the" \
                       " familiar surroundings, showcasing the importance of a strong home presence in influencing" \
                       " match outcomes. The league's landscape, shaped by these home victories, highlights " \
                       "the symbiotic relationship between teams and their passionate supporters."
    elif score_stats['away'] / score_stats['home'] >= 2:
        body_scores = "<br><br>Noteworthy trend emerged with a considerable number of teams securing victories in away"\
                       " matches. The conventional advantage of playing on one's home turf seemed to have diminished," \
                       " as clubs demonstrated remarkable determination in triumphing over their opponents on their " \
                       "own grounds. This shift challenges the traditional notion that home matches guarantee an " \
                       "upper hand and emphasizes the need for clubs to showcase immense grit and resilience when " \
                       "facing rivals in their home stadiums. The prevalence of away victories adds an element of " \
                       "unpredictability to the league, highlighting the competitive spirit and adaptability required" \
                       " for success in diverse footballing environments."

    body_own_goals = ""
    if len(own_goals) >= 3:

        body_own_goals = "<br><br>In an unexpected turn of events during the matches, a rare occurrence unfolded" \
                         f" with {len(own_goals)} own goals, credited to" \
                         f"{''.join(' %s from %s,' % (og.full_name, og.team.name) for og in own_goals)} The impact of" \
                         " these unintentional contributions must have weighed heavily on their respective teams." \
                         " The added challenge of scoring against one's own team not only alters the dynamics of the" \
                         " match but also presents a unique mental hurdle for the players and their teams. Such " \
                         "instances highlight the unpredictable nature of the sport, where even the most skilled " \
                         "players can find themselves inadvertently influencing the outcome in unexpected ways, " \
                         "adding an element of complexity to the beautiful game."
    elif len(own_goals) == 2:
        body_own_goals = "<br><br>In a surprising turn of events during matches, two own goals were registered, with "\
                          f"{own_goals[0].full_name} from {own_goals[0].team.name} and {own_goals[1].full_name} " \
                          f"from {own_goals[1].team.name} finding themselves on the score sheet for the opposing " \
                          "teams. The occurrence of own goals inevitably sparks curiosity about their potential " \
                          "impact on the final standings of the league table. Such unexpected events can indeed " \
                          "influence the overall outcome, as they contribute not only to the immediate match results" \
                          " but also to the goal differentials crucial in determining the final rankings. The " \
                          "unintended goals may introduce an element of unpredictability, leaving fans and pundits " \
                          "alike speculating on the potential repercussions for the teams involved in the broader " \
                          "context of the league standings."
    elif len(own_goals) == 1:
        body_own_goals = "<br><br>In a twist of fate during recent matches, a unique occurrence unfolded as an own " \
                         f"goal was recorded, with {own_goals[0].full_name} from {own_goals[0].team.name}" \
                          " inadvertently becoming the scorer. The question arises as to whether this " \
                          "unexpected own goal will have a lasting impact on the final standings of the " \
                          "league table. Beyond the immediate match result, own goals can play a role in " \
                          "determining goal differentials, which in turn influence a team's overall position in" \
                          " the standings. Additionally, the mental resilience of the player involved, in this " \
                          f"case, {own_goals[0].full_name}, becomes a point of interest. Overcoming the " \
                          "psychological impact of scoring an own goal requires considerable mental strength, " \
                          "and how players navigate and bounce back from such situations can significantly " \
                          "affect their performance in subsequent matches."

    footer = "<br><br>Text generated automatically<br><br>"

    body = random.choice(body_choice) + "<br><br>" + body_gpm + body_scores + body_own_goals + footer

    return {'title': title,
            'subtitle': subtitle,
            'body': body}

def flag(country:str):
    dict = {
         'Afghanistan': 'AF',
         'Albania': 'AL',
         'Algeria': 'DZ',
         'American Samoa': 'AS',
         'Andorra': 'AD',
         'Angola': 'AO',
         'Anguilla': 'AI',
         'Antarctica': 'AQ',
         'Antigua and Barbuda': 'AG',
         'Argentina': 'AR',
         'Armenia': 'AM',
         'Aruba': 'AW',
         'Australia': 'AU',
         'Austria': 'AT',
         'Azerbaijan': 'AZ',
         'Bahamas': 'BS',
         'Bahrain': 'BH',
         'Bangladesh': 'BD',
         'Barbados': 'BB',
         'Belarus': 'BY',
         'Belgium': 'BE',
         'Belize': 'BZ',
         'Benin': 'BJ',
         'Bermuda': 'BM',
         'Bhutan': 'BT',
         'Bolivia, Plurinational State of': 'BO',
         'Bonaire, Sint Eustatius and Saba': 'BQ',
         'Bosnia and Herzegovina': 'BA',
         'Botswana': 'BW',
         'Bouvet Island': 'BV',
         'Brazil': 'BR',
         'British Indian Ocean Territory': 'IO',
         'Brunei Darussalam': 'BN',
         'Bulgaria': 'BG',
         'Burkina Faso': 'BF',
         'Burundi': 'BI',
         'Cambodia': 'KH',
         'Cameroon': 'CM',
         'Canada': 'CA',
         'Cape Verde': 'CV',
         'Cayman Islands': 'KY',
         'Central African Republic': 'CF',
         'Chad': 'TD',
         'Chile': 'CL',
         'China': 'CN',
         'Christmas Island': 'CX',
         'Cocos (Keeling) Islands': 'CC',
         'Colombia': 'CO',
         'Comoros': 'KM',
         'Congo': 'CG',
         'Congo DR': 'CD',
         'Cook Islands': 'CK',
         'Costa Rica': 'CR',
         'Croatia': 'HR',
         'Cuba': 'CU',
         'Curaçao': 'CW',
         'Cyprus': 'CY',
         'Czech Republic': 'CZ',
         'Czechia': 'CZ',
         "Côte d'Ivoire": 'CI',
         'Denmark': 'DK',
         'Djibouti': 'DJ',
         'Dominica': 'DM',
         'Dominican Republic': 'DO',
         'Ecuador': 'EC',
         'Egypt': 'EG',
         'El Salvador': 'SV',
         'Equatorial Guinea': 'GQ',
         'Eritrea': 'ER',
         'Estonia': 'EE',
         'Ethiopia': 'ET',
         'Falkland Islands (Malvinas)': 'FK',
         'Faroe Islands': 'FO',
         'Fiji': 'FJ',
         'Finland': 'FI',
         'France': 'FR',
         'French Guiana': 'GF',
         'French Polynesia': 'PF',
         'French Southern Territories': 'TF',
         'Gabon': 'GA',
         'Gambia': 'GM',
         'Georgia': 'GE',
         'Germany': 'DE',
         'Ghana': 'GH',
         'Gibraltar': 'GI',
         'Greece': 'GR',
         'Greenland': 'GL',
         'Grenada': 'GD',
         'Guadeloupe': 'GP',
         'Guam': 'GU',
         'Guatemala': 'GT',
         'Guernsey': 'GG',
         'Guinea': 'GN',
         'Guinea-Bissau': 'GW',
         'Guyana': 'GY',
         'Haiti': 'HT',
         'Heard Island and McDonald Islands': 'HM',
         'Holy See (Vatican City State)': 'VA',
         'Honduras': 'HN',
         'Hong Kong': 'HK',
         'Hungary': 'HU',
         'Iceland': 'IS',
         'India': 'IN',
         'Indonesia': 'ID',
         'Iran': 'IR',
         'Iraq': 'IQ',
         'Ireland': 'IE',
         'Isle of Man': 'IM',
         'Israel': 'IL',
         'Italy': 'IT',
         'Jamaica': 'JM',
         'Japan': 'JP',
         'Jersey': 'JE',
         'Jordan': 'JO',
         'Kazakhstan': 'KZ',
         'Kenya': 'KE',
         'Kiribati': 'KI',
         'Kosovo': 'XK',
         "Korea, Democratic People's Republic of": 'KP',
         'Korea, Republic of': 'KR',
         'Kuwait': 'KW',
         'Kyrgyzstan': 'KG',
         "Lao People's Democratic Republic": 'LA',
         'Latvia': 'LV',
         'Lebanon': 'LB',
         'Lesotho': 'LS',
         'Liberia': 'LR',
         'Libya': 'LY',
         'Liechtenstein': 'LI',
         'Lithuania': 'LT',
         'Luxembourg': 'LU',
         'Macao': 'MO',
         'North Macedonia': 'MK',
         'Madagascar': 'MG',
         'Malawi': 'MW',
         'Malaysia': 'MY',
         'Maldives': 'MV',
         'Mali': 'ML',
         'Malta': 'MT',
         'Marshall Islands': 'MH',
         'Martinique': 'MQ',
         'Mauritania': 'MR',
         'Mauritius': 'MU',
         'Mayotte': 'YT',
         'Mexico': 'MX',
         'Micronesia, Federated States of': 'FM',
         'Moldova': 'MD',
         'Monaco': 'MC',
         'Mongolia': 'MN',
         'Montenegro': 'ME',
         'Montserrat': 'MS',
         'Morocco': 'MA',
         'Mozambique': 'MZ',
         'Myanmar': 'MM',
         'Namibia': 'NA',
         'Nauru': 'NR',
         'Nepal': 'NP',
         'Netherlands': 'NL',
         'New Caledonia': 'NC',
         'New Zealand': 'NZ',
         'Nicaragua': 'NI',
         'Niger': 'NE',
         'Nigeria': 'NG',
         'Niue': 'NU',
         'Norfolk Island': 'NF',
         'Northern Mariana Islands': 'MP',
         'Norway': 'NO',
         'Oman': 'OM',
         'Pakistan': 'PK',
         'Palau': 'PW',
         'Palestine, State of': 'PS',
         'Panama': 'PA',
         'Papua New Guinea': 'PG',
         'Paraguay': 'PY',
         'Peru': 'PE',
         'Philippines': 'PH',
         'Pitcairn': 'PN',
         'Poland': 'PL',
         'Portugal': 'PT',
         'Puerto Rico': 'PR',
         'Qatar': 'QA',
         'Romania': 'RO',
         'Russia': 'RU',
         'Rwanda': 'RW',
         'Réunion': 'RE',
         'Saint Barthélemy': 'BL',
         'Saint Helena, Ascension and Tristan da Cunha': 'SH',
         'Saint Kitts and Nevis': 'KN',
         'Saint Lucia': 'LC',
         'Saint Martin (French part)': 'MF',
         'Saint Pierre and Miquelon': 'PM',
         'Saint Vincent and the Grenadines': 'VC',
         'Samoa': 'WS',
         'San Marino': 'SM',
         'Sao Tome and Principe': 'ST',
         'Saudi Arabia': 'SA',
         'Senegal': 'SN',
         'Serbia': 'RS',
         'Seychelles': 'SC',
         'Sierra Leone': 'SL',
         'Singapore': 'SG',
         'Sint Maarten (Dutch part)': 'SX',
         'Slovakia': 'SK',
         'Slovenia': 'SI',
         'Solomon Islands': 'SB',
         'Somalia': 'SO',
         'South Africa': 'ZA',
         'South Georgia and the South Sandwich Islands': 'GS',
         'South Sudan': 'SS',
         'Spain': 'ES',
         'Sri Lanka': 'LK',
         'Sudan': 'SD',
         'Suriname': 'SR',
         'Svalbard and Jan Mayen': 'SJ',
         'Swaziland': 'SZ',
         'Sweden': 'SE',
         'Switzerland': 'CH',
         'Syrian Arab Republic': 'SY',
         'Taiwan, Province of China': 'TW',
         'Tajikistan': 'TJ',
         'Tanzania, United Republic of': 'TZ',
         'Thailand': 'TH',
         'Timor-Leste': 'TL',
         'Togo': 'TG',
         'Tokelau': 'TK',
         'Tonga': 'TO',
         'Trinidad and Tobago': 'TT',
         'Tunisia': 'TN',
         'Turkey': 'TR',
         'Türkiye': 'TR',
         'Turkmenistan': 'TM',
         'Turks and Caicos Islands': 'TC',
         'Tuvalu': 'TV',
         'Uganda': 'UG',
         'Ukraine': 'UA',
         'United Arab Emirates': 'AE',
         'United Kingdom': 'GB',
         'United States': 'US',
         'United States Minor Outlying Islands': 'UM',
         'Uruguay': 'UY',
         'Uzbekistan': 'UZ',
         'Vanuatu': 'VU',
         'Venezuela, Bolivarian Republic of': 'VE',
         'Viet Nam': 'VN',
         'Virgin Islands, British': 'VG',
         'Virgin Islands, U.S.': 'VI',
         'Wallis and Futuna': 'WF',
         'Western Sahara': 'EH',
         'Yemen': 'YE',
         'Zambia': 'ZM',
         'Zimbabwe': 'ZW',
         'Åland Islands': 'AX',
         'England': 'gb-eng',
         'Wales': 'gb-wls',
         'Scotland': 'gb-sct',
         'Northern Ireland': 'gb-nir'}
    try:
        return dict[country].lower()
    except KeyError:
        return 'unknown'
