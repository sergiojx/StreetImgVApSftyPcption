import requests
import urllib, os
import json
import math
import datetime
import time
import re


# Determine if a point is inside a given polygon or not
# Polygon is a list of (x,y) pairs. This function
# returns True or False.  The algorithm is called
# the "Ray Casting Method".

def point_in_poly(x,y,poly):

    n = len(poly)
    inside = False

    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x,p1y = p2x,p2y

    return inside


# un delta de [0.000180] equivale aprox. a 20m
DELTA = 0.000180
DELTA2 = 0.000360

# zone search template javaScript absolute file system path
# This holds search coordinates

cityZone = 'suba'


imgsJsPath = '/vagrant/ggStreetView/map/localidades/%s/imgs/set_%s.js' % (cityZone, cityZone)
imgsJsDirPath = '/vagrant/ggStreetView/map/localidades/%s/imgs' % cityZone



# Zone polygone
polygon = [
              (-74.042454,4.830661),
              (-74.04279,4.831048),
              (-74.043122,4.831538),
              (-74.043548,4.832066),
              (-74.044146,4.833001),
              (-74.044296,4.833024),
              (-74.044323,4.833028),
              (-74.044473,4.832782),
              (-74.044664,4.83244),
              (-74.044895,4.831866),
              (-74.0451,4.831292),
              (-74.045264,4.830936),
              (-74.045536,4.830526),
              (-74.045986,4.830294),
              (-74.046354,4.830116),
              (-74.046586,4.830108),
              (-74.047563,4.830571),
              (-74.047786,4.831036),
              (-74.048058,4.831893),
              (-74.048259,4.832387),
              (-74.048546,4.832969),
              (-74.04876,4.833411),
              (-74.048912,4.833733),
              (-74.049084,4.834268),
              (-74.049324,4.834761),
              (-74.04967,4.835033),
              (-74.049963,4.835167),
              (-74.050112,4.834944),
              (-74.050028,4.834536),
              (-74.049926,4.834079),
              (-74.049828,4.833731),
              (-74.049711,4.833221),
              (-74.049641,4.832772),
              (-74.049573,4.832415),
              (-74.049303,4.831606),
              (-74.049066,4.831189),
              (-74.049024,4.830889),
              (-74.049012,4.830642),
              (-74.04928,4.830462),
              (-74.049888,4.830452),
              (-74.050207,4.830552),
              (-74.050296,4.830528),
              (-74.050667,4.830885),
              (-74.050968,4.831278),
              (-74.051301,4.83164),
              (-74.051578,4.831972),
              (-74.051852,4.832363),
              (-74.052358,4.832702),
              (-74.052773,4.833058),
              (-74.053296,4.833085),
              (-74.053622,4.83275),
              (-74.053618,4.832284),
              (-74.053732,4.831772),
              (-74.053853,4.831358),
              (-74.054114,4.830892),
              (-74.054287,4.830563),
              (-74.054626,4.830179),
              (-74.054977,4.829866),
              (-74.055452,4.829575),
              (-74.055707,4.829194),
              (-74.056019,4.828854),
              (-74.056304,4.828796),
              (-74.056668,4.828875),
              (-74.057172,4.828987),
              (-74.057785,4.829057),
              (-74.058468,4.829007),
              (-74.059034,4.828946),
              (-74.059661,4.828791),
              (-74.060206,4.828625),
              (-74.060399,4.828277),
              (-74.060206,4.82793),
              (-74.06021,4.827642),
              (-74.060417,4.827525),
              (-74.060658,4.827438),
              (-74.060892,4.827708),
              (-74.06104,4.828115),
              (-74.061183,4.828522),
              (-74.061275,4.82883),
              (-74.061452,4.829111),
              (-74.061582,4.829547),
              (-74.061733,4.830094),
              (-74.061917,4.830651),
              (-74.062101,4.830991),
              (-74.062326,4.831397),
              (-74.062512,4.831739),
              (-74.062686,4.832175),
              (-74.062798,4.83264),
              (-74.062832,4.833538),
              (-74.06275,4.834062),
              (-74.062607,4.834666),
              (-74.062605,4.835205),
              (-74.062789,4.835506),
              (-74.062996,4.8356),
              (-74.063241,4.835419),
              (-74.063416,4.835163),
              (-74.063577,4.83478),
              (-74.063826,4.834274),
              (-74.064106,4.833948),
              (-74.064181,4.833647),
              (-74.064123,4.833324),
              (-74.064112,4.832907),
              (-74.064029,4.83257),
              (-74.063986,4.832346),
              (-74.063914,4.832051),
              (-74.063849,4.831699),
              (-74.063851,4.831208),
              (-74.063947,4.830758),
              (-74.064102,4.830438),
              (-74.064261,4.830298),
              (-74.064491,4.830214),
              (-74.064664,4.83043),
              (-74.064722,4.830771),
              (-74.064762,4.831057),
              (-74.064863,4.831343),
              (-74.064998,4.831866),
              (-74.065029,4.832212),
              (-74.064971,4.832582),
              (-74.064877,4.832989),
              (-74.064756,4.833345),
              (-74.064726,4.833774),
              (-74.064779,4.834202),
              (-74.064862,4.834536),
              (-74.064961,4.83487),
              (-74.065092,4.835197),
              (-74.065233,4.83539),
              (-74.065513,4.835472),
              (-74.065799,4.835463),
              (-74.066067,4.835371),
              (-74.066307,4.8351),
              (-74.066471,4.834773),
              (-74.066682,4.834381),
              (-74.066891,4.833998),
              (-74.067092,4.833554),
              (-74.067253,4.833135),
              (-74.067392,4.832655),
              (-74.067431,4.832207),
              (-74.067444,4.831691),
              (-74.067411,4.831302),
              (-74.067382,4.83091),
              (-74.067366,4.830477),
              (-74.067337,4.830062),
              (-74.067245,4.829765),
              (-74.067145,4.82933),
              (-74.067064,4.828964),
              (-74.067019,4.828605),
              (-74.066975,4.828341),
              (-74.066968,4.828064),
              (-74.067082,4.827974),
              (-74.067292,4.828006),
              (-74.067508,4.828144),
              (-74.067685,4.828263),
              (-74.067996,4.828432),
              (-74.068264,4.828524),
              (-74.068475,4.828588),
              (-74.068692,4.828632),
              (-74.068903,4.828632),
              (-74.069083,4.828621),
              (-74.069245,4.828585),
              (-74.069327,4.828598),
              (-74.069597,4.828545),
              (-74.069868,4.828485),
              (-74.070089,4.828407),
              (-74.070274,4.828348),
              (-74.070431,4.828354),
              (-74.070571,4.828345),
              (-74.070742,4.828399),
              (-74.070767,4.828564),
              (-74.070844,4.828939),
              (-74.070886,4.829282),
              (-74.070871,4.829443),
              (-74.070834,4.829817),
              (-74.070891,4.830225),
              (-74.070872,4.83044),
              (-74.070853,4.830871),
              (-74.070848,4.831225),
              (-74.070918,4.831644),
              (-74.070965,4.832037),
              (-74.071034,4.832326),
              (-74.071205,4.832714),
              (-74.071281,4.833052),
              (-74.071345,4.833267),
              (-74.071451,4.83353),
              (-74.071535,4.833756),
              (-74.071624,4.833957),
              (-74.071715,4.83416),
              (-74.071894,4.834456),
              (-74.072074,4.834675),
              (-74.072199,4.834866),
              (-74.072634,4.835362),
              (-74.07283,4.835555),
              (-74.073054,4.835745),
              (-74.073192,4.835856),
              (-74.073284,4.835922),
              (-74.073388,4.835996),
              (-74.073608,4.836157),
              (-74.073995,4.836392),
              (-74.074374,4.836599),
              (-74.074541,4.836671),
              (-74.074752,4.83671),
              (-74.074949,4.836724),
              (-74.075196,4.836747),
              (-74.075415,4.836761),
              (-74.075624,4.836779),
              (-74.075816,4.836777),
              (-74.076001,4.836778),
              (-74.076201,4.836753),
              (-74.07638,4.83673),
              (-74.076523,4.836713),
              (-74.076633,4.836694),
              (-74.0768,4.836685),
              (-74.077053,4.836612),
              (-74.077233,4.836555),
              (-74.077408,4.836475),
              (-74.07752,4.836435),
              (-74.077898,4.836304),
              (-74.078738,4.835975),
              (-74.0796,4.835681),
              (-74.080468,4.835335),
              (-74.081376,4.834795),
              (-74.082141,4.834409),
              (-74.08294,4.834006),
              (-74.083802,4.833373),
              (-74.08475,4.83293),
              (-74.085721,4.832601),
              (-74.086554,4.832186),
              (-74.086714,4.831836),
              (-74.086502,4.831544),
              (-74.085872,4.83119),
              (-74.085156,4.830418),
              (-74.08432,4.829691),
              (-74.083753,4.828976),
              (-74.083042,4.828117),
              (-74.082537,4.827287),
              (-74.080968,4.825576),
              (-74.080178,4.824981),
              (-74.079867,4.823864),
              (-74.079391,4.822994),
              (-74.079178,4.822272),
              (-74.079126,4.822042),
              (-74.078952,4.821114),
              (-74.079373,4.820339),
              (-74.079881,4.819811),
              (-74.080685,4.818811),
              (-74.080998,4.818369),
              (-74.081356,4.817474),
              (-74.08164,4.816682),
              (-74.082023,4.816377),
              (-74.082533,4.816887),
              (-74.082723,4.817505),
              (-74.082781,4.817981),
              (-74.082519,4.818481),
              (-74.082217,4.818894),
              (-74.08231,4.819536),
              (-74.082608,4.820149),
              (-74.082872,4.820687),
              (-74.083194,4.821529),
              (-74.083424,4.822142),
              (-74.083983,4.821763),
              (-74.084999,4.821136),
              (-74.085428,4.82106),
              (-74.086051,4.821156),
              (-74.086565,4.821029),
              (-74.086638,4.820209),
              (-74.086653,4.819211),
              (-74.086714,4.818437),
              (-74.086787,4.81768),
              (-74.086974,4.817124),
              (-74.087042,4.816785),
              (-74.08712,4.816017),
              (-74.086925,4.815495),
              (-74.086049,4.815056),
              (-74.085083,4.814886),
              (-74.084242,4.814693),
              (-74.083167,4.814334),
              (-74.082909,4.813641),
              (-74.083537,4.813399),
              (-74.084228,4.813288),
              (-74.084948,4.812983),
              (-74.084683,4.812118),
              (-74.084059,4.811752),
              (-74.083121,4.811255),
              (-74.08244,4.810878),
              (-74.081696,4.810622),
              (-74.080758,4.810263),
              (-74.080043,4.809989),
              (-74.07975,4.809376),
              (-74.079949,4.80851),
              (-74.08053,4.807861),
              (-74.081255,4.807401),
              (-74.081906,4.807233),
              (-74.082625,4.80675),
              (-74.083356,4.806284),
              (-74.084195,4.805669),
              (-74.084903,4.805398),
              (-74.085457,4.805092),
              (-74.086193,4.804609),
              (-74.086604,4.804305),
              (-74.087123,4.803982),
              (-74.087723,4.803683),
              (-74.088476,4.803309),
              (-74.088773,4.802901),
              (-74.088269,4.802724),
              (-74.087583,4.802502),
              (-74.087096,4.802062),
              (-74.087101,4.801701),
              (-74.088375,4.8014),
              (-74.088998,4.801387),
              (-74.088877,4.801009),
              (-74.088429,4.799737),
              (-74.088319,4.799106),
              (-74.088381,4.798888),
              (-74.088597,4.798171),
              (-74.089276,4.797596),
              (-74.090059,4.797836),
              (-74.090796,4.797645),
              (-74.091515,4.797179),
              (-74.091571,4.796686),
              (-74.091056,4.796423),
              (-74.090427,4.796235),
              (-74.089701,4.796174),
              (-74.088913,4.796416),
              (-74.087256,4.79681),
              (-74.087175,4.796213),
              (-74.08754,4.795628),
              (-74.088076,4.795266),
              (-74.089383,4.79415),
              (-74.089907,4.793484),
              (-74.090575,4.793059),
              (-74.091288,4.792575),
              (-74.092053,4.791972),
              (-74.092852,4.791374),
              (-74.093502,4.790891),
              (-74.093873,4.790798),
              (-74.094017,4.791067),
              (-74.094333,4.791697),
              (-74.094631,4.792471),
              (-74.095332,4.793897),
              (-74.095643,4.794911),
              (-74.095884,4.795621),
              (-74.095909,4.796619),
              (-74.095893,4.797255),
              (-74.095879,4.798763),
              (-74.096069,4.799239),
              (-74.096817,4.799048),
              (-74.097937,4.798604),
              (-74.09872,4.798711),
              (-74.099778,4.798904),
              (-74.10071,4.799114),
              (-74.101309,4.798626),
              (-74.101667,4.797937),
              (-74.101923,4.797174),
              (-74.10203,4.79644),
              (-74.102388,4.795688),
              (-74.102759,4.795245),
              (-74.103495,4.794883),
              (-74.103861,4.795008),
              (-74.103685,4.795513),
              (-74.103486,4.795766),
              (-74.103138,4.796099),
              (-74.102796,4.796627),
              (-74.10278,4.797154),
              (-74.103175,4.797417),
              (-74.103867,4.797479),
              (-74.104661,4.7973),
              (-74.105248,4.796874),
              (-74.105664,4.796242),
              (-74.106051,4.795554),
              (-74.10629,4.795094),
              (-74.106489,4.794389),
              (-74.106887,4.793643),
              (-74.10728,4.792764),
              (-74.107616,4.792047),
              (-74.107882,4.790997),
              (-74.108,4.790063),
              (-74.108049,4.788847),
              (-74.108511,4.788571),
              (-74.109196,4.788357),
              (-74.110995,4.787505),
              (-74.111623,4.787205),
              (-74.112122,4.788196),
              (-74.112163,4.788649),
              (-74.112388,4.789434),
              (-74.111605,4.78963),
              (-74.111102,4.789454),
              (-74.110548,4.789524),
              (-74.110051,4.789829),
              (-74.110041,4.790339),
              (-74.110425,4.790648),
              (-74.111041,4.790526),
              (-74.11231,4.790604),
              (-74.11295,4.790229),
              (-74.113422,4.789196),
              (-74.113626,4.788646),
              (-74.113877,4.788232),
              (-74.114127,4.787561),
              (-74.114354,4.78689),
              (-74.11417,4.78654),
              (-74.11373,4.786329),
              (-74.113146,4.786003),
              (-74.112672,4.785959),
              (-74.112323,4.785638),
              (-74.112099,4.785341),
              (-74.112251,4.784475),
              (-74.112652,4.784491),
              (-74.11304,4.784616),
              (-74.113476,4.785028),
              (-74.113819,4.785228),
              (-74.114334,4.785605),
              (-74.114752,4.785639),
              (-74.114957,4.785357),
              (-74.114853,4.784847),
              (-74.114766,4.78428),
              (-74.114644,4.783615),
              (-74.114534,4.782996),
              (-74.114408,4.782624),
              (-74.114367,4.782245),
              (-74.114744,4.781998),
              (-74.115246,4.781831),
              (-74.115812,4.781743),
              (-74.116314,4.781519),
              (-74.116988,4.781179),
              (-74.117198,4.780697),
              (-74.117135,4.78029),
              (-74.116546,4.780423),
              (-74.115935,4.780614),
              (-74.115198,4.780868),
              (-74.114713,4.780926),
              (-74.11438,4.780594),
              (-74.114345,4.780061),
              (-74.114658,4.77947),
              (-74.115063,4.779056),
              (-74.115668,4.778722),
              (-74.116353,4.778446),
              (-74.116884,4.778192),
              (-74.117209,4.77779),
              (-74.117186,4.777503),
              (-74.116831,4.777435),
              (-74.11582,4.777696),
              (-74.115347,4.77815),
              (-74.114662,4.778593),
              (-74.113913,4.778697),
              (-74.113884,4.778118),
              (-74.114168,4.777516),
              (-74.114378,4.776982),
              (-74.114543,4.776288),
              (-74.114775,4.77525),
              (-74.114938,4.774309),
              (-74.115097,4.773718),
              (-74.115565,4.773322),
              (-74.116147,4.77285),
              (-74.116523,4.772437),
              (-74.116608,4.772041),
              (-74.116111,4.771979),
              (-74.115682,4.772072),
              (-74.115351,4.772267),
              (-74.114877,4.772308),
              (-74.114345,4.771983),
              (-74.114452,4.771403),
              (-74.11469,4.770566),
              (-74.115825,4.769296),
              (-74.116755,4.768841),
              (-74.117737,4.768031),
              (-74.118147,4.767531),
              (-74.1183,4.76678),
              (-74.117676,4.766466),
              (-74.117145,4.76669),
              (-74.116427,4.767506),
              (-74.115702,4.767989),
              (-74.115454,4.767222),
              (-74.115413,4.766379),
              (-74.115804,4.765197),
              (-74.116123,4.764382),
              (-74.116292,4.763573),
              (-74.116744,4.762061),
              (-74.116826,4.761786),
              (-74.116846,4.761785),
              (-74.1177,4.761615),
              (-74.11862,4.761613),
              (-74.120128,4.761151),
              (-74.120863,4.760461),
              (-74.121239,4.759819),
              (-74.121186,4.759199),
              (-74.120933,4.758455),
              (-74.12076,4.757784),
              (-74.120678,4.756919),
              (-74.120556,4.755967),
              (-74.120378,4.755188),
              (-74.120244,4.754403),
              (-74.12041,4.754196),
              (-74.121421,4.754102),
              (-74.12241,4.754083),
              (-74.123181,4.754058),
              (-74.124295,4.75401),
              (-74.125238,4.753973),
              (-74.12542,4.753462),
              (-74.124818,4.752736),
              (-74.124206,4.752181),
              (-74.123758,4.751201),
              (-74.123241,4.749912),
              (-74.122947,4.748835),
              (-74.122504,4.747753),
              (-74.12268,4.747265),
              (-74.122932,4.747339),
              (-74.123384,4.747418),
              (-74.123465,4.748117),
              (-74.123977,4.749601),
              (-74.124281,4.750036),
              (-74.125196,4.750482),
              (-74.126054,4.750743),
              (-74.127254,4.750638),
              (-74.127544,4.749834),
              (-74.127577,4.749312),
              (-74.12712,4.749313),
              (-74.126143,4.749493),
              (-74.125857,4.749265),
              (-74.125662,4.749018),
              (-74.125449,4.748308),
              (-74.125379,4.747546),
              (-74.125572,4.747064),
              (-74.126405,4.746678),
              (-74.126873,4.746304),
              (-74.12741,4.746154),
              (-74.12829,4.746215),
              (-74.129085,4.746345),
              (-74.130067,4.745918),
              (-74.130334,4.745413),
              (-74.130521,4.744645),
              (-74.130554,4.744054),
              (-74.130729,4.743113),
              (-74.131054,4.742505),
              (-74.131321,4.741822),
              (-74.131862,4.741093),
              (-74.131986,4.740284),
              (-74.131676,4.739746),
              (-74.131007,4.739438),
              (-74.130515,4.739181),
              (-74.129652,4.738993),
              (-74.129542,4.738495),
              (-74.129438,4.73783),
              (-74.129226,4.737469),
              (-74.128802,4.73735),
              (-74.128288,4.737357),
              (-74.127621,4.737319),
              (-74.12738,4.737305),
              (-74.127417,4.738846),
              (-74.127281,4.739069),
              (-74.127164,4.739306),
              (-74.126776,4.739665),
              (-74.126536,4.739835),
              (-74.12613,4.740018),
              (-74.125775,4.740098),
              (-74.125446,4.740119),
              (-74.125049,4.740058),
              (-74.124528,4.73998),
              (-74.122955,4.739744),
              (-74.122163,4.739596),
              (-74.12157,4.739584),
              (-74.12113,4.73953),
              (-74.12069,4.739437),
              (-74.120573,4.739309),
              (-74.120573,4.738789),
              (-74.120597,4.738545),
              (-74.1206,4.737986),
              (-74.120599,4.737878),
              (-74.120503,4.737701),
              (-74.120291,4.737562),
              (-74.120124,4.737386),
              (-74.120007,4.737254),
              (-74.119787,4.736999),
              (-74.11965,4.736823),
              (-74.119315,4.736576),
              (-74.119005,4.736412),
              (-74.118645,4.736299),
              (-74.118412,4.736328),
              (-74.117815,4.736247),
              (-74.117216,4.736111),
              (-74.116935,4.736015),
              (-74.116711,4.73585),
              (-74.116524,4.735685),
              (-74.11636,4.735483),
              (-74.116158,4.735167),
              (-74.116014,4.735018),
              (-74.115835,4.734936),
              (-74.115489,4.734849),
              (-74.114995,4.734769),
              (-74.114603,4.734695),
              (-74.114471,4.734482),
              (-74.114341,4.734141),
              (-74.114289,4.733955),
              (-74.114224,4.73381),
              (-74.114176,4.733642),
              (-74.114133,4.733477),
              (-74.114116,4.733227),
              (-74.114123,4.732993),
              (-74.114125,4.732899),
              (-74.114125,4.732721),
              (-74.114114,4.732501),
              (-74.114131,4.732258),
              (-74.114089,4.732134),
              (-74.114026,4.732051),
              (-74.113945,4.73197),
              (-74.113804,4.73194),
              (-74.113667,4.731908),
              (-74.113558,4.731889),
              (-74.113313,4.731798),
              (-74.113034,4.731551),
              (-74.112875,4.73125),
              (-74.112587,4.730926),
              (-74.112355,4.730656),
              (-74.111958,4.730259),
              (-74.111528,4.729885),
              (-74.11131,4.729711),
              (-74.111063,4.729604),
              (-74.110891,4.729571),
              (-74.110593,4.729541),
              (-74.110355,4.729514),
              (-74.109986,4.729338),
              (-74.109737,4.72911),
              (-74.109529,4.728773),
              (-74.109372,4.728485),
              (-74.109229,4.728201),
              (-74.10909,4.727913),
              (-74.108901,4.72761),
              (-74.108685,4.727427),
              (-74.108346,4.727182),
              (-74.108109,4.726981),
              (-74.107724,4.726716),
              (-74.107418,4.726613),
              (-74.10727,4.726391),
              (-74.107098,4.726267),
              (-74.106935,4.726137),
              (-74.106788,4.725978),
              (-74.106603,4.725874),
              (-74.106363,4.725877),
              (-74.106205,4.725969),
              (-74.106019,4.726033),
              (-74.105891,4.726093),
              (-74.105546,4.7261),
              (-74.105387,4.72606),
              (-74.105102,4.726052),
              (-74.104858,4.726096),
              (-74.104227,4.725933),
              (-74.104092,4.725824),
              (-74.103979,4.725588),
              (-74.10402,4.725463),
              (-74.104003,4.725092),
              (-74.104079,4.724545),
              (-74.104043,4.724262),
              (-74.104067,4.724014),
              (-74.103982,4.723755),
              (-74.103858,4.723608),
              (-74.103688,4.723477),
              (-74.103436,4.72331),
              (-74.103143,4.723204),
              (-74.102856,4.722983),
              (-74.102686,4.722732),
              (-74.102505,4.722475),
              (-74.102349,4.722263),
              (-74.102143,4.722098),
              (-74.101904,4.721965),
              (-74.101481,4.721901),
              (-74.101157,4.721811),
              (-74.100784,4.721675),
              (-74.100564,4.721556),
              (-74.100467,4.721395),
              (-74.100427,4.721142),
              (-74.100393,4.720805),
              (-74.100448,4.720488),
              (-74.100478,4.720306),
              (-74.100428,4.720062),
              (-74.100374,4.719775),
              (-74.100366,4.719518),
              (-74.100417,4.719219),
              (-74.100368,4.718952),
              (-74.100297,4.718722),
              (-74.100215,4.718545),
              (-74.100138,4.718341),
              (-74.099995,4.718183),
              (-74.099843,4.717998),
              (-74.099576,4.717782),
              (-74.099377,4.717699),
              (-74.09925,4.717608),
              (-74.099077,4.717536),
              (-74.098858,4.71746),
              (-74.098561,4.717567),
              (-74.098299,4.717664),
              (-74.098122,4.71765),
              (-74.097975,4.71758),
              (-74.097767,4.717479),
              (-74.097594,4.717381),
              (-74.09734,4.717394),
              (-74.097272,4.717413),
              (-74.097029,4.717451),
              (-74.096887,4.717463),
              (-74.096684,4.71738),
              (-74.096545,4.717257),
              (-74.096404,4.71707),
              (-74.096248,4.716947),
              (-74.096012,4.716688),
              (-74.095791,4.716409),
              (-74.095725,4.71631),
              (-74.09557,4.716097),
              (-74.095353,4.715994),
              (-74.095243,4.715832),
              (-74.095086,4.715436),
              (-74.095058,4.715194),
              (-74.09499,4.714893),
              (-74.094785,4.714489),
              (-74.094595,4.714246),
              (-74.094455,4.714026),
              (-74.094246,4.71387),
              (-74.094009,4.713765),
              (-74.093832,4.713602),
              (-74.093708,4.713451),
              (-74.09351,4.713194),
              (-74.093442,4.712888),
              (-74.093505,4.712703),
              (-74.093552,4.71248),
              (-74.093587,4.712262),
              (-74.093608,4.711977),
              (-74.093533,4.711756),
              (-74.093457,4.711538),
              (-74.093351,4.711359),
              (-74.093064,4.711067),
              (-74.092782,4.710821),
              (-74.092519,4.710607),
              (-74.092255,4.710399),
              (-74.091998,4.710377),
              (-74.091744,4.710467),
              (-74.091513,4.710628),
              (-74.091222,4.71071),
              (-74.091038,4.710677),
              (-74.090873,4.710497),
              (-74.090774,4.710275),
              (-74.09072,4.710104),
              (-74.090578,4.709839),
              (-74.090465,4.709692),
              (-74.090438,4.709404),
              (-74.090478,4.709229),
              (-74.090548,4.70885),
              (-74.090529,4.708735),
              (-74.090489,4.708651),
              (-74.090374,4.708512),
              (-74.090255,4.708512),
              (-74.090118,4.708508),
              (-74.089959,4.708548),
              (-74.08982,4.708581),
              (-74.089724,4.708542),
              (-74.089678,4.708417),
              (-74.089713,4.708345),
              (-74.089675,4.708171),
              (-74.089657,4.707982),
              (-74.08963,4.707909),
              (-74.089546,4.707723),
              (-74.089548,4.70759),
              (-74.089623,4.70746),
              (-74.089737,4.707354),
              (-74.089824,4.707231),
              (-74.089737,4.707022),
              (-74.089638,4.706861),
              (-74.089206,4.706635),
              (-74.088898,4.706451),
              (-74.088609,4.706269),
              (-74.088373,4.706107),
              (-74.088164,4.705944),
              (-74.088065,4.705836),
              (-74.087989,4.705654),
              (-74.087972,4.705389),
              (-74.087893,4.705129),
              (-74.087893,4.70504),
              (-74.08787,4.70482),
              (-74.087878,4.70463),
              (-74.087851,4.704454),
              (-74.087976,4.704298),
              (-74.088108,4.70407),
              (-74.088098,4.703926),
              (-74.088127,4.703683),
              (-74.088114,4.70303),
              (-74.088174,4.702185),
              (-74.088252,4.701895),
              (-74.088314,4.701678),
              (-74.088364,4.701345),
              (-74.088421,4.701117),
              (-74.088485,4.70093),
              (-74.088372,4.70065),
              (-74.088298,4.700496),
              (-74.088277,4.700352),
              (-74.088328,4.700195),
              (-74.088478,4.699917),
              (-74.088539,4.699794),
              (-74.088508,4.699524),
              (-74.088461,4.699243),
              (-74.08846,4.698973),
              (-74.08843,4.698735),
              (-74.088369,4.69853),
              (-74.088129,4.698526),
              (-74.087945,4.698592),
              (-74.087755,4.69858),
              (-74.087694,4.698487),
              (-74.08747,4.698279),
              (-74.08732,4.698074),
              (-74.086933,4.697914),
              (-74.086591,4.697759),
              (-74.08637,4.697651),
              (-74.086217,4.697549),
              (-74.08589,4.697336),
              (-74.085745,4.697165),
              (-74.085566,4.696889),
              (-74.085464,4.696621),
              (-74.085379,4.696389),
              (-74.085371,4.69608),
              (-74.085201,4.695641),
              (-74.085201,4.695203),
              (-74.085145,4.695017),
              (-74.085003,4.694763),
              (-74.084819,4.694627),
              (-74.084672,4.694373),
              (-74.084245,4.694156),
              (-74.083659,4.693868),
              (-74.082918,4.693606),
              (-74.082428,4.693438),
              (-74.081851,4.693267),
              (-74.081634,4.693244),
              (-74.081375,4.693206),
              (-74.081088,4.693265),
              (-74.080948,4.693144),
              (-74.080811,4.692888),
              (-74.080687,4.692535),
              (-74.080562,4.692235),
              (-74.080384,4.691813),
              (-74.080309,4.691512),
              (-74.080295,4.691191),
              (-74.080335,4.690911),
              (-74.080343,4.690759),
              (-74.080275,4.690559),
              (-74.080163,4.690426),
              (-74.08004,4.690257),
              (-74.079817,4.690044),
              (-74.079607,4.689835),
              (-74.079454,4.689538),
              (-74.079388,4.689301),
              (-74.079284,4.688923),
              (-74.079197,4.68849),
              (-74.079102,4.688203),
              (-74.078983,4.687869),
              (-74.078837,4.687537),
              (-74.078674,4.687304),
              (-74.078518,4.687053),
              (-74.078419,4.686904),
              (-74.078335,4.686801),
              (-74.07827,4.68668),
              (-74.077328,4.68536),
              (-74.075784,4.686593),
              (-74.073928,4.688061),
              (-74.073262,4.688482),
              (-74.072749,4.688754),
              (-74.072332,4.688943),
              (-74.071707,4.68917),
              (-74.071155,4.689355),
              (-74.070436,4.689505),
              (-74.069798,4.689595),
              (-74.069087,4.689659),
              (-74.068163,4.68959),
              (-74.067394,4.689493),
              (-74.066617,4.689362),
              (-74.065454,4.689105),
              (-74.064723,4.688885),
              (-74.057254,4.686838),
              (-74.057247,4.686836),
              (-74.049693,4.731828),
              (-74.046835,4.74882),
              (-74.046729,4.751047),
              (-74.042136,4.777017),
              (-74.035082,4.820499),
              (-74.035022,4.822244),
              (-74.035046,4.822644),
              (-74.035006,4.82314),
              (-74.034884,4.823665),
              (-74.03478,4.824178),
              (-74.034497,4.825469),
              (-74.034885,4.825523),
              (-74.035013,4.825525),
              (-74.035619,4.825634),
              (-74.036244,4.825765),
              (-74.036841,4.825863),
              (-74.037475,4.825934),
              (-74.037969,4.82601),
              (-74.038345,4.826098),
              (-74.039733,4.826353),
              (-74.040261,4.826432),
              (-74.040704,4.826487),
              (-74.040781,4.826496),
              (-74.040829,4.826713),
              (-74.040875,4.826979),
              (-74.040987,4.827446),
              (-74.041044,4.827977),
              (-74.041168,4.828675),
              (-74.041153,4.828877),
              (-74.041476,4.829355),
              (-74.041883,4.829856),
              (-74.042196,4.830293),
              (-74.042423,4.830625),
              (-74.042454,4.830661)
        ]
4.822085,-74.066885
#                   latitud     longitud                 
# initialCordenate = (4.833245, -74.090645)
initialCordenate = (4.737125, -74.090645)
finalCordenate  =  (4.683169, -74.052515)
imageLatitud = initialCordenate[0]
imageLongitud = initialCordenate[1]
# crate associate image directory and image collection javaScript file
outFile = None
print("new directory: %s" %  imgsJsDirPath)
print("new js file: %s" %  imgsJsPath)
if not os.path.exists(imgsJsDirPath):
	os.makedirs(imgsJsDirPath)
	outFile = open(imgsJsPath, "w+")
	outFile.write("var set_%s =\n [" % (cityZone))
	outFile.close()

outF = open(imgsJsPath, "a")	
flag4comma = False


heading_lists = [0,45,90,135,180,-45,-90,-135]
headingIndex = 0
while imageLatitud >= finalCordenate[0]:
       while imageLongitud <= finalCordenate[1]:
              location = "%f,%f" % (imageLatitud, imageLongitud)
              heading = heading_lists[headingIndex ]
              urlmeta = "https://maps.googleapis.com/maps/api/streetview/metadata?size=600x300&location=%s&fov=100&heading=%i&pitch=0&key={CopyYourKeyHere}" % (location, heading)
              url = "https://maps.googleapis.com/maps/api/streetview?size=600x300&location=%s&fov=100&heading=%i&pitch=0&key={CopyYourKeyHere}" % (location, heading)
              print('location')
              print(location)
              try:
                     r = requests.get(urlmeta)
                     data = json.loads(r.text)
                     print('meta_data')
                     print(data)
                     if r.status_code == 200 and data["status"] == 'OK' and ('oogle' in data["copyright"]):
                            try:
                                   point_x = data['location']['lng']
                                   point_y = data['location']['lat']
                                   if point_in_poly(point_x,point_y,polygon) == True:
                                          dateTime = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
                                          imgName = "%s_%s_%i.jpg" %(data['location']['lat'],data['location']['lng'],heading)
                                          location = "%s,%s" % (data['location']['lat'],data['location']['lng'])
                                          url = "https://maps.googleapis.com/maps/api/streetview?size=600x300&location=%s&fov=100&heading=%i&pitch=0&key={CopyYourKeyHere}" % (location, heading)
                                          print(url)
                                          try:
                                                 urllib.urlretrieve(url, os.path.join(imgsJsDirPath,imgName))
                                                 if flag4comma:
                                                        outF.write(",\n")
                                                 outF.write("{\"name\":\"%s\", \"lat\":%s, \"log\":%s, \"sampletime\":\"%s\", \"heading\":%i}" %(imgName,data['location']['lat'],data['location']['lng'],data['date'],heading))
                                                 flag4comma = True
                                                 print('point is into polygon =)') 
                                                 time.sleep(3)
                                          except(HTTPError, ConnectionError, Timeout, RateLimitExceeded, timeout) as e:
                                                 print("urllib.urlretrieve fail =(: %s" % str(e))
                                                 print("longitud %f latitud %f heading %f" %(imageLongitud, imageLatitud, headingIndex))
                                   else:
                                          print('point is NOT into polygon =(')
                            except(HTTPError, ConnectionError, Timeout, RateLimitExceeded, timeout) as e:
                                   print("image access fail =(: %s" % str(e))
                                   print("longitud %f latitud %f heading %f" %(imageLongitud, imageLatitud, headingIndex))
                     imageLongitud = imageLongitud + DELTA2
                     headingIndex = (headingIndex + 1)%8
              except(HTTPError, ConnectionError, Timeout, RateLimitExceeded, timeout) as e:
                     print("metadata access fail =(: %s" % str(e))
                     print("longitud %f latitud %f heading %f" %(imageLongitud, imageLatitud, headingIndex))
        
       imageLatitud = imageLatitud - DELTA2
       imageLongitud = initialCordenate[1]


print("longitud %f latitud %f heading %f" %(imageLongitud, imageLatitud, headingIndex))      

outF.write("]\n")
outF.close()
	
	

