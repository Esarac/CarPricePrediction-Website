from django.http import HttpResponse
from django.template import Template, Context
from django.shortcuts import render

import pickle
import pandas as pd
import os

from sklearn.model_selection import train_test_split
from sklearn import metrics

MARCAS = ['Jeep', 'Volkswagen', 'Mercedes-Benz', 'Toyota', 'Land Rover',
       'Nissan', 'Renault', 'Dodge', 'BMW', 'Suzuki', 'Daihatsu', 'Honda',
       'Mitsubishi', 'Fiat', 'Mazda', 'Chevrolet', 'Hyundai', 'Volvo',
       'Ford', 'Subaru', 'Daewoo', 'Peugeot', 'Skoda', 'Kia', 'Citroen',
       'Audi', 'Lexus', 'Seat', 'Porsche', 'Cadillac', 'Ssangyong',
       'Chrysler', 'Hummer', 'Hafei', 'Chery', 'Zotye', 'Mini', 'Alpina',
       'Lifan', 'Geely', 'Changan', 'DFM/DFSK', 'BYD', 'MG', 'JMC',
       'Changhe', 'Mahindra', 'Brilliance', 'JBC', 'Jaguar', 'Foton',
       'Baic', 'DS', 'RAM']
MODELO = ['WILLYS', 'ESCARABAJO', '250', 'LAND CRUISER', '1970', 'PATROL',
       'R12', 'DART', 'R4', 'R 12', 'SERIE 5', '230', 'SERIE 3', 'LJ',
       'CROWN', 'F20', 'DATSUN', 'ACCORD', 'CLASE E', 'MONTERO',
       'FJ CRUISER', '200', '280 SE', 'SJ', 'R18', 'CLASE G', '147',
       '626', '323', 'CELEBRITY', 'ROCKY', 'CHEVETTE', 'R9', 'WRANGLER',
       'TROOPER', 'MONZA', 'B2000', 'BURBUJA', 'GOLF', 'CLASE S',
       '4RUNNER', 'SWIFT', 'SAMURAI', 'SPRINT', '21', 'GALANT', 'BLAZER',
       'UNO', 'SONATA', 'AD WAGON', '850', 'INTEGRA', 'CIVIC', 'BRONCO',
       '940', 'LEGACY', 'EXCEL', 'SUNNY', 'SENTRA', 'GRAND CHEROKEE',
       'CHEROKEE', 'RACER', 'VITARA', 'FEROZA', 'SILVERADO', 'CAMRY',
       '1994', 'CARAVAN', '460', 'CAVALIER', 'CLASE C', 'ELANTRA',
       'QUEST', '405', 'FORMAN', '306', 'LUV', 'SPORTAGE', '205',
       'ALLEGRO', 'HILUX', 'LANCER', 'GRAND BLAZER', 'XANTIA', 'FAVORIT',
       'FESTIVA', 'AX', 'FELICIA', 'PREMIO', 'CIELO', 'RAV4', 'COROLLA',
       'VENTO', '325I', 'ESTEEM', 'TERCEL', 'DISCOVERY', 'CORSA',
       'TEMPRA', 'I3', 'ALMERA', 'RANGE ROVER', 'TICO', 'Z3', 'F-350',
       'PATHFINDER', 'ESPERO', 'ZX', 'ACCENT', 'R19', '1996', 'TWINGO',
       '307', 'EXPLORER', 'URVAN', 'A4', 'LX', 'S40', 'SAXO', 'RODEO',
       'STARLET', 'PALIO', 'CHARADE', '106', 'FIESTA', 'IMPREZA', 'CLIO',
       'XSARA', 'GRAND SPORTAGE', 'NATIVA', 'FORESTER', 'CHEYENNE',
       'OUTBACK', 'VIVIO', 'GOL', 'PRIDE', 'NUBIRA', 'LEGEND', 'CR-V',
       'MAXIMA', '1998', 'PARATI', 'PRIMERA', 'LANOS', 'ML', 'IBIZA',
       'SIENA', 'A6', 'PRADO', '121', 'JIMNY', 'SIRION', 'PASSAT',
       'LAGUNA', 'LASER', 'POLO', 'SUPER CARRY', 'GRAND VITARA', 'X5',
       'YARIS', 'NEON', '406', 'JETTA', 'MEGANE', 'ALTO', 'CLASE A',
       'FREELANDER', 'A3', 'SYMBOL', 'KORANDO', 'FABIA', 'SEQUOIA',
       'ASTRA', 'PREGIO', 'SANTA FE', 'ZAFIRA', 'X-TRAIL', 'C5',
       'TRAILBLAZER', 'TERIOS', 'GRACE', 'OCTAVIA', 'OUTLANDER', '206',
       'B2600', 'EPICA', 'RANGER', 'MURANO', 'LEON', 'CAYENNE',
       'TERRACAN', '6', 'CARNIVAL', 'C3', 'OPTRA', 'ATOS', 'X3',
       'MEGANE 2', 'C4', 'FRONTIER', 'ESCALADE', 'DEMIO', 'S60', 'D22',
       'PILOT', 'PICANTO', 'NAVARA', 'SERIE 1', 'XSARA PICASSO',
       'ECOSPORT', '3', 'CHEVY', 'FIT', 'ODYSSEY', 'SPARK', '407', 'BORA',
       'SORENTO', 'LUV D-MAX', 'H3', 'ESCAPE', 'TOUAREG', 'CLASE R',
       'CARENS', 'AVEO', 'NEW BEETLE', 'TUCSON', 'KYRON', 'VIVANT',
       'GETZ', 'RIO', 'MINYI', 'STAREX', 'LOGAN', 'TIIDA', 'CX-7', 'CX-9',
       'XC90', '5', 'FUSION', 'SAHARA', 'COMPASS', 'RANGE ROVER SPORT',
       'EXPEDITION', 'D-MAX', 'FOCUS', 'REXTON', 'CERATO', 'L300',
       'B2200', 'AVEO EMOTION', 'IDEA', 'WRX', 'CLASE B', '2008', 'EDGE',
       'QASHQAI', 'CLASE GLK', '2', 'FORTUNER', 'SANDERO', '308', '207',
       'JOURNEY', 'GENESIS', 'KOLEOS', 'Q7', 'S80', 'XC60', 'QQ',
       'MOHAVE', 'I30', 'CAPTIVA', 'TRIBECA', 'TIGUAN', 'C30', '2009',
       'HHR', 'ACTYON', 'NOMADA', 'COOPER', '2010', 'TUCSON IX-35',
       'SERIE 7', 'RCZ', 'CERATO FORTE', 'Q5', 'X1', 'BT-50', 'SOUL',
       'GX', 'Z4', 'STEPWAY', 'MITO', 'VERACRUZ', 'TAHOE', 'A5', '500',
       '320', 'SCALA', 'NEW SPORTAGE', 'CADENZA', 'CROSSFOX', 'SPARK GT',
       'COUNTRYMAN', 'SIENNA', 'CRUZE', 'ASX', 'V60', 'Q3', 'OPTIMA',
       'A1', 'MK', 'ECLIPSE', 'X6', '2011', 'YETI', 'N200', 'VOYAGE',
       'STAR VAN', 'KANGOO', 'PALIO ADVENTURE', 'TRAVERSE', 'DUNA',
       'F-150', 'I10', '2012', 'VERSA', 'NUEVO JETTA', 'DURANGO', 'D-22',
       'EVOQUE', 'STAVIC', 'HAVAL', 'CERATO KOUP', 'DS3', 'YOYA', '508',
       'FLUENCE', 'NEW SPORTAGE LX', 'RAM', 'OTING', 'MARCH', 'F0',
       'STRADA', '107', 'I35', 'DUSTER', 'H1', 'AZERA', 'SONIC', 'SX4',
       'SAIL', 'TRANSPORTER', 'ECOSPORT 2', 'KIZASHI', 'TRACKER', 'VAN',
       'N300', '2013', 'COBALT', 'JX', 'CX-5', 'MÉGANE III', '350',
       'FREEDOM', 'SCORPIO', 'GIULIETTA', 'XCROSS', 'ALTIMA', 'V5',
       'ORLANDO', 'YOYO', 'REFINE', 'B-CROSS', 'L200 SPORTERO',
       'CERATO PRO', 'AMAROK', 'A200', 'RODIUS', '208', 'V40',
       'CLASE CLA', '2014', 'QUORIS', 'JUNYI', 'COOPER S', 'TIGGO',
       'VITO', 'NOTE', 'S6', 'CELERIO', 'C-ELYSÉE', '116I', 'A7', 'XV',
       '301', 'V27', 'JUKE', 'ZONORA', 'FULWIN', 'MINIVAN',
       'DISCOVERY SPORT', 'RANGE ROVER EVOQUE', 'XF', 'X4', 'SERIE 4',
       '2015', 'A 200', 'BERLINGO', 'ERTIGA', 'GRAND I10', 'TRAFIC',
       'KICKS', 'DS4', 'I25', 'CLASE GLA', 'EON', 'GRAND TIGGO',
       'S-CROSS', 'CIAZ', 'FOISON', 'Q', 'MINI VAN', 'ONIX', 'TIVOLI',
       '2016', 'CLASE GLE', 'XE', 'GRAND CARNIVAL SEDONA', 'BEETLE',
       'EULOVE', 'CLASE GLC', 'C4 CACTUS', 'MIRAGE', 'MZ40', 'HR-V',
       'SERIE 2', 'CS 35', 'APV', 'ALASKAN', 'CAPTUR', 'CRETA', 'CLUBMAN',
       'VELOSTER', 'RENEGADE', 'SPORTERO', 'GT', 'GLORY', 'BALENO', 'I20',
       'S3', 'MIATA', '3008', 'Q2', 'EQUINOX', 'WINGLE 5', '5008', 'S2',
       'WR-V', 'MAZDA 3', 'M 4', '2018', 'XC40', 'CLASE GL', 'X2', '318I',
       'BEAT', 'RUSH', 'TONIC', 'IONIQ', 'TIGER 7', 'C3 AIRCROSS', '2019',
       'VIRTUS', 'ZS', 'ARGO', 'CX-3', 'NIRO', 'DS7', 'FOX', 'CS 15',
       'KUV100', 'S2 URBAN', 'X25', 'Q35', 'DUSTER OROCH', 'KWID', '1000',
       'CS15', 'T-CROSS', 'CROSS UP', 'SOLUTO', 'ARONA', '2020', 'MOBI',
       'S-PRESSO', '2021', 'Q3 SPORTBACK', 'NIVUS', 'MAZDA 2', 'CX-30',
       'JOY', 'TWIZY', 'C37', 'ATECA', 'M3', 'CELICA', 'I', 'TIBURON',
       'ESCORT', '80', 'M5', 'SUPRA']
CARROCERIA = ['Camioneta', 'Hatchback', 'Sedan']
COMBUSTIBLE = ['Gasolina', 'Diesel', 'Gasolina y Gas', 'Híbrido', 'Eléctrico',
       'Gas']
COLOR = ['Rojo', 'Amarillo', 'Azul', 'Verde', 'Blanco', 'Negro',
       'No Disponible', 'Gris', 'Dorado', 'Beige', 'Cafe', 'Naranja',
       'Plateado', 'Violeta', 'Lila', 'Rosa', 'Celeste', 'Champaña',
       'Nacar', 'Ocre', 'Tan']
MAE = 4866175.178500091

#Vistas
def index(request):
    return render(request, 'index.html')

def form(request):
    return render(request, 'form.html', {"marcas":MARCAS, "modelos":MODELO, "carrocerias":CARROCERIA, "combustibles":COMBUSTIBLE, "colores":COLOR})

def result(request):
    marca = request.GET['marca']
    modelo = request.GET['modelo']
    anio = int(request.GET['anio'])
    carroceria = request.GET['carroceria']
    combustible = request.GET['combustible']
    color = request.GET['color']

    path = os.path.join(os.path.dirname(__file__), "resources/car.pickle.dat")
    model = pickle.load(open(path, "rb"))

    cols_when_model_builds = model.get_booster().feature_names

    car = {'Marca_'+marca:1, 'Modelo_'+modelo:1,'Anio':anio, 'Tipo de carroceria_'+carroceria:1, 'Tipo de combustible_'+combustible:1, 'Color_'+color:1}
    car_df = pd.DataFrame(columns=cols_when_model_builds)
    car_df = car_df.append(car, ignore_index = True)
    car_df = car_df.fillna(0)

    val_pred = model.predict(car_df)
    
    price_min = "${:,.2f}".format(val_pred[0]-MAE)
    price_max = "${:,.2f}".format(val_pred[0]+MAE)

    return render(request, 'result.html', {"price_max":price_max, "price_min":price_min})