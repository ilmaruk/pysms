import random
import typing
import uuid

from pysms.models import Team

# See https://github.com/Azgaar/Fantasy-Map-Generator/blob/master/modules/names-generator.js
NAMES = "Addundad,Ahagzad,Ahazil,Akil,Akzizad,Anumush,Araddush,Arar,Arbhur,Badushund,Baragzig,Baragzund,Barakinb,Barakzig,Barakzinb,Barakzir,Baramunz,Barazinb,Barazir,Bilgabar,Bilgatharb,Bilgathaz,Bilgila,Bilnaragz,Bilnulbar,Bilnulbun,Bizaddum,Bizaddush,Bizanarg,Bizaram,Bizinbiz,Biziram,Bunaram,Bundinar,Bundushol,Bundushund,Bundushur,Buzaram,Buzundab,Buzundush,Gabaragz,Gabaram,Gabilgab,Gabilgath,Gabizir,Gabunal,Gabunul,Gabuzan,Gatharam,Gatharbhur,Gathizdum,Gathuragz,Gathuraz,Gila,Giledzir,Gilukkhath,Gilukkhel,Gunala,Gunargath,Gunargil,Gundumunz,Gundusharb,Gundushizd,Kharbharbiln,Kharbhatharb,Kharbhela,Kharbilgab,Kharbuzadd,Khatharbar,Khathizdin,Khathundush,Khazanar,Khazinbund,Khaziragz,Khaziraz,Khizdabun,Khizdusharbh,Khizdushath,Khizdushel,Khizdushur,Kholedzar,Khundabiln,Khundabuz,Khundinarg,Khundushel,Khuragzig,Khuramunz,Kibarak,Kibilnal,Kibizar,Kibunarg,Kibundin,Kibuzan,Kinbadab,Kinbaragz,Kinbarakz,Kinbaram,Kinbizah,Kinbuzar,Nala,Naledzar,Naledzig,Naledzinb,Naragzah,Naragzar,Naragzig,Narakzah,Narakzar,Naramunz,Narazar,Nargabad,Nargabar,Nargatharb,Nargila,Nargundum,Nargundush,Nargunul,Narukthar,Narukthel,Nula,Nulbadush,Nulbaram,Nulbilnarg,Nulbunal,Nulbundab,Nulbundin,Nulbundum,Nulbuzah,Nuledzah,Nuledzig,Nulukkhaz,Nulukkhund,Nulukkhur,Sharakinb,Sharakzar,Sharamunz,Sharbarukth,Shatharbhizd,Shatharbiz,Shathazah,Shathizdush,Shathola,Shaziragz,Shizdinar,Shizdushund,Sholukkharb,Shundinulb,Shundushund,Shurakzund,Shuramunz,Tumunzadd,Tumunzan,Tumunzar,Tumunzinb,Tumunzir,Ukthad,Ulbirad,Ulbirar,Ulunzar,Ulur,Umunzad,Undalar,Undukkhil,Undun,Undur,Unduzur,Unzar,Unzathun,Usharar,Zaddinarg,Zaddushur,Zaharbad,Zaharbhizd,Zarakib,Zarakzar,Zaramunz,Zarukthel,Zinbarukth,Zirakinb,Zirakzir,Ziramunz,Ziruktharbh,Zirukthur,Zundumunz"
SHORT_LEN = 4

LOW_PROBABILITY = 1
MEDIUM_PROBABILITY = 2
HIGH_PROBABILITY = 3
VERY_HIGH_PROBABILITY = 5


def create_team() -> Team:
    name, short = random_name()
    return Team(id=uuid.uuid4(), name=name, short=short, colors=random_colors())


def random_name() -> typing.Tuple[str, str]:
    name = random.choice(NAMES.split(","))
    short = shorten_team_name(name)
    modifiers = ["FC {}", "{} FC", "{} Unuigita", "Urbo {}",
                 "Universitato {}", "Dinamo {}", "{} Fervojo",
                 "{}", "Atleta {}", "Internacia {}", "Laboristoj {}",
                 "{} Futbalo", "Futbalo {}"]
    weights = [HIGH_PROBABILITY, HIGH_PROBABILITY, MEDIUM_PROBABILITY, MEDIUM_PROBABILITY,
               LOW_PROBABILITY, MEDIUM_PROBABILITY, LOW_PROBABILITY, MEDIUM_PROBABILITY,
               MEDIUM_PROBABILITY, LOW_PROBABILITY, LOW_PROBABILITY, MEDIUM_PROBABILITY,
               MEDIUM_PROBABILITY]
    return random.choices(modifiers, weights=weights, k=1)[0].format(name), short


def shorten_team_name(name: str) -> str:
    vowels = "aeijouy"
    short = name[0].lower()
    for char in name[1:]:
        if char not in vowels:
            short += char
            if len(short) == SHORT_LEN:
                return short
    for char in name[1:]:
        if char in vowels:
            short += char
            if len(short) == SHORT_LEN:
                return short
    return short + "x" * (SHORT_LEN - len(short))


def random_colors() -> typing.List[str]:
    options = {
        ('black', 'blue'): 3,
        ('blue',): 4,
        ('blue', 'white'): 1,
        ('green', 'black'): 1,
        ('grey', 'red'): 1,
        ('lightblue',): 1,
        ('maroon',): 4,
        ('orange', 'green'): 1,
        ('pink', 'black'): 1,
        ('purple',): 1,
        ('red', 'black'): 1,
        ('red', 'darkblue'): 4,
        ('red', 'green'): 1,
        ('red', 'white'): 2,
        ('white', 'black'): 4,
        ('white', 'red'): 2,
        ('yellow', 'blue'): 4,
        ('yellow', 'red'): 3,
        ('white', 'lightblue'): 1,
        }
    cols = random.choices(population=list(options.keys()), weights=options.values(), k=1)[0]
    if len(cols) > 1 and random.choice([True, False]):
        # Flip colors
        cols = (cols[1], cols[0])
