from flask import Flask, render_template, flash, redirect, url_for, session, request, \
    logging, send_file, send_from_directory, make_response, Response
from wtforms import Form, StringField, TextAreaField, PasswordField, SelectField, SelectMultipleField, validators
from flask_mysqldb import MySQL
from data_resource import create_csv
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'cs533'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init MYSQL
mysql = MySQL(app)


def getFeatures(type=''):
    # Create cursor
    cur = mysql.connection.cursor()
    # Get features
    if type == '':
        result = cur.execute("SELECT * FROM features")
    else:
        result = cur.execute("SELECT * FROM features where type='{}'".format(type))
    features = cur.fetchall()

    return result, features
    # Close connection
    cur.close()


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/features')
def features():
    result, features = getFeatures()
    if result > 0:
        return render_template('features.html', features=features)
    else:
        msg = 'No Features Found'
        return render_template('features.html', msg=msg)


@app.route('/correlations', methods=['GET', 'POST'])
def correlations():
    corform = DataRequestFormCor(request.form)
    if request.method == 'POST':
        app.logger.info('Correlations for submitted:{}'.format(corform.correlation.data))
        name = "{}.png".format(corform.correlation.data)

        return render_template('correlations.html', form=corform, filename=name)
    return render_template('correlations.html', form=corform)


class DataRequestFormCor(Form):
    correlation = SelectField('Correlations', choices=[
        ('income', 'Income vs Time'),
        ('children', 'Income vs No of Children'),
        ('house_price', 'Housing Prices vs Population')
    ])

@app.route('/user_generated/<filename>')
def send_image(filename):
    return send_from_directory("user_generated", filename)


@app.route('/return_file/<string:filename>')
def return_file(filename):
    return send_file("user_generated/{}".format(filename), attachment_filename=filename, as_attachment=True)


@app.route('/housing_data', methods=['GET', 'POST'])
def housingData():
    # result, features = getFeatures()
    form = DataRequestForm(request.form)
    if request.method == 'POST':
        app.logger.info('this has been submitted:{}'.format(form.feature.data))
        filename, name = create_csv('housing', form.feature.data)
        posts = [
            {
                'filename': name
            }
        ]
        return render_template('housing_data.html', form=form, posts=posts)
    return render_template('housing_data.html', form=form)


class DataRequestForm(Form):
    data = [
        ('RT', 'Record Type'),
        ('SERIALNO', 'Housing unit/GQ person serial number'),
        ('DIVISION', 'Division code based on 2010 Census definitions'),
        ('PUMA', 'Public use microdata area code (PUMA) based on 2010 Census definition'),
        ('REGION', 'Region code based on 2010 Census definitions'),
        ('ST', 'State Code based on 2010 Census definitions'),
        ('ADJHSG', 'Adjustment factor for housing dollar amounts (6 implied decimal places)'),
        ('ADJINC', 'Adjustment factor for income and earnings dollar amounts (6 implied decimal places)'),
        ('WGTP', 'Housing Unit Weight'),
        ('NP', 'Number of persons associated with this housing record'),
        ('TYPE', 'Type of unit'),
        ('ACR', 'Lot size'),
        ('AGS', 'Sales of Agriculture Products (Yearly sales)'),
        ('BATH', 'Bathtub or shower'),
        ('BDSP', 'Number of bedrooms'),
        ('BLD', 'Units in structure'),
        ('BUS', 'Business or medical office on property'),
        ('CONP', 'Condo fee (monthly amount)'),
        ('ELEP', 'Electricity (monthly cost)'),
        ('FS', 'Yearly food stamp/Supplemental Nutrition Assistance Program recipiency'),
        ('FULP', 'Fuel cost(yearly cost for fuels other than gas and electricity)'),
        ('GASP', 'Gas (monthly cost)'),
        ('HFL', 'House heating fuel'),
        ('INSP', 'Fire/hazard/flood insurance (yearly amount)'),
        ('MHP', 'Mobile home costs (yearly amount)'),
        ('MRGI', 'First mortgage payment includes fire/hazard/flood insurance'),
        ('MRGP', 'First mortgage payment (monthly amount)'),
        ('MRGT', 'First mortgage payment includes real estate taxes'),
        ('MRGX', 'First mortgage status'),
        ('REFR', 'Refrigerator'),
        ('RMSP', 'Number of Rooms'),
        ('RNTM', 'Meals included in rent'),
        ('RNTP', 'Monthly rent'),
        ('RWAT', 'Hot and cold running water'),
        ('RWATPR', 'Running water'),
        ('SINK', 'Sink with a faucet'),
        ('SMP', 'Total payment on all second and junior mortgages and home equity loans (monthly amount)'),
        ('STOV', 'Stove or range'),
        ('TEL', 'Telephone service'),
        ('TEN', 'Tenure'),
        ('TOIL', 'Flush toilet'),
        ('VACS', 'Vacancy status'),
        ('VALP', 'Property value'),
        ('VEH', 'Vehicles (1 ton or less) available'),
        ('WATP', 'Water (yearly cost)'),
        ('YBL', 'When structure first built'),
        ('FES', 'Family type and employment status'),
        ('FINCP', 'Family income (past 12 months)'),
        ('FPARC', 'Family presence and age of related children'),
        ('GRNTP', 'Gross rent (monthly amount)'),
        ('GRPIP', 'Gross rent as a percentage of household income past 12 months'),
        ('HHL', 'Household language'),
        ('HHT', 'Household/family type'),
        ('HINCP', 'Household income (past 12 months)'),
        ('HUGCL', 'Household with grandparent living with grandchildren'),
        ('HUPAC', 'HH presence and age of children'),
        ('HUPAOC', 'HH presence and age of own children'),
        ('HUPARC', 'HH presence and age of related children'),
        ('KIT', 'Complete kitchen facilities'),
        ('LNGI', 'Limited English speaking household'),
        ('MULTG', 'Multigenerational Household'),
        ('MV', 'When moved into this house or apartment'),
        ('NOC', 'Number of own children in household (unweighted)'),
        ('NPF', 'Number of persons in family (unweighted)'),
        ('NPP', 'Grandparent headed household with no parent present'),
        ('NR', 'Presence of nonrelative in household'),
        ('NRC', 'Number of related children in household (unweighted)'),
        ('OCPIP', 'Selected monthly owner costs as a percentage of household income during the past 12 months'),
        ('PARTNER', 'Unmarried partner household'),
        ('PLM', 'Complete plumbing facilities'),
        ('PSF', 'Presence of subfamilies in Household'),
        ('R18', 'Presence of persons under 18 years in household (unweighted)'),
        ('R60', 'Presence of persons 60 years and over in household (unweighted)'),
        ('R65', 'Presence of persons 65 years and over in household (unweighted)'),
        ('RESMODE', 'Response mode'),
        ('SMOCP', 'Selected monthly owner costs'),
        ('SMX', 'Second or junior mortgage or home equity loan status'),
        ('SRNT', 'Specified rental unit'),
        ('SVAL', 'Specified owner unit'),
        ('TAXP', 'Property taxes (yearly amount)'),
        ('WIF', 'Workers in family during the past 12 months'),
        ('WKEXREL', 'Work experience of householder and spouse'),
        ('WORKSTAT', 'Work status of householder or spouse in family households'),
        ('FACRP', 'Lot size allocation flag'),
        ('FAGSP', 'Sales of Agricultural Products allocation flag'),
        ('FBATHP', 'Bathtub or shower allocation flag'),
        ('FBDSP', 'Number of bedrooms allocation flag'),
        ('FBLDP', 'Units in structure allocation flag'),
        ('FBUSP', 'Business or medical office on property allocation flag'),
        ('FCONP', 'Condominium fee allocation flag'),
        ('FELEP', 'Electricity (monthly cost) allocation flag'),
        ('FFINCP', 'Family income (past 12 months) allocation flag'),
        ('FFSP', 'Yearly food stamp/Supplemental Nutrition Assistance Program recipiency allocation flag'),
        ('FFULP', 'Fuel cost (yearly cost for fuels other than gas and electricity) allocation flag'),
        ('FGASP', 'Gas (monthly cost) allocation flag'),
        ('FGRNTP', 'Gross rent (monthly amount) allocation flag'),
        ('FHFLP', 'House heating fuel allocation flag'),
        ('FHINCP', 'Household income (past 12 months) allocation flag'),
        ('FINSP', 'Fire, hazard, flood insurance (yearly amount) allocation flag'),
        ('FKITP', 'Complete kitchen facilities allocation flag'),
        ('FMHP', 'Mobile home costs (yearly amount) allocation flag'),
        ('FMRGIP', 'First mortgage payment includes fire, hazard, flood insurance allocation flag'),
        ('FMRGP', 'First mortgage payment (monthly amount) allocation flag'),
        ('FMRGTP', 'First mortgage payment includes real estate taxes allocation flag'),
        ('FMRGXP', 'First mortgage status allocation flag'),
        ('FMVP', 'When moved into this house or apartment allocation flag'),
        ('FPLMP', 'Complete plumbing facilities allocation flag'),
        ('FREFRP', 'Refrigerator allocation flag'),
        ('FRMSP', 'Number of rooms allocation flag'),
        ('FRNTMP', 'Meals included in rent allocation flag'),
        ('FRNTP', 'Monthly rent allocation flag'),
        ('FRWATP', 'Hot and cold running water allocation flag'),
        ('FRWATPRP', 'Running water allocation flag'),
        ('FSINKP', 'Sink with a faucet allocation flag'),
        ('FSMOCP', 'Selected monthly owner cost allocation flag'),
        ('FSMP', 'Total payment on second and junior mortgages and home equity loans (monthly amount) allocation flag'),
        ('FSMXHP', 'Home equity loan status allocation flag'),
        ('FSMXSP', 'Second mortgage status allocation flag'),
        ('FSTOVP', 'Stove or range allocation flag'),
        ('FTAXP', 'Property taxes (yearly amount) allocation flag'),
        ('FTELP', 'Telephone service allocation flag'),
        ('FTENP', 'Tenure allocation flag'),
        ('FTOILP', 'Flush toilet allocation flag'),
        ('FVACSP', 'Vacancy status allocation flag'),
        ('FVALP', 'Property value allocation flag'),
        ('FVEHP', 'Vehicles available allocation flag'),
        ('FWATP', 'Water (yearly cost) allocation flag'),
        ('FYBLP', 'When structure first built allocation flag'),
        ('WGTP1', 'Housing Unit Weight replicate 1'),
        ('WGTP2', 'Housing Unit Weight replicate 2'),
        ('WGTP3', 'Housing Unit Weight replicate 3'),
        ('WGTP4', 'Housing Unit Weight replicate 4'),
        ('WGTP5', 'Housing Unit Weight replicate 5'),
        ('WGTP6', 'Housing Unit Weight replicate 6'),
        ('WGTP7', 'Housing Unit Weight replicate 7'),
        ('WGTP8', 'Housing Unit Weight replicate 8'),
        ('WGTP9', 'Housing Unit Weight replicate 9'),
        ('WGTP10', 'Housing Unit Weight replicate 10'),
        ('WGTP11', 'Housing Unit Weight replicate 11'),
        ('WGTP12', 'Housing Unit Weight replicate 12'),
        ('WGTP13', 'Housing Unit Weight replicate 13'),
        ('WGTP14', 'Housing Unit Weight replicate 14'),
        ('WGTP15', 'Housing Unit Weight replicate 15'),
        ('WGTP16', 'Housing Unit Weight replicate 16'),
        ('WGTP17', 'Housing Unit Weight replicate 17'),
        ('WGTP18', 'Housing Unit Weight replicate 18'),
        ('WGTP19', 'Housing Unit Weight replicate 19'),
        ('WGTP20', 'Housing Unit Weight replicate 20'),
        ('WGTP21', 'Housing Unit Weight replicate 21'),
        ('WGTP22', 'Housing Unit Weight replicate 22'),
        ('WGTP23', 'Housing Unit Weight replicate 23'),
        ('WGTP24', 'Housing Unit Weight replicate 24'),
        ('WGTP25', 'Housing Unit Weight replicate 25'),
        ('WGTP26', 'Housing Unit Weight replicate 26'),
        ('WGTP27', 'Housing Unit Weight replicate 27'),
        ('WGTP28', 'Housing Unit Weight replicate 28'),
        ('WGTP29', 'Housing Unit Weight replicate 29'),
        ('WGTP30', 'Housing Unit Weight replicate 30'),
        ('WGTP31', 'Housing Unit Weight replicate 31'),
        ('WGTP32', 'Housing Unit Weight replicate 32'),
        ('WGTP33', 'Housing Unit Weight replicate 33'),
        ('WGTP34', 'Housing Unit Weight replicate 34'),
        ('WGTP35', 'Housing Unit Weight replicate 35'),
        ('WGTP36', 'Housing Unit Weight replicate 36'),
        ('WGTP37', 'Housing Unit Weight replicate 37'),
        ('WGTP38', 'Housing Unit Weight replicate 38'),
        ('WGTP39', 'Housing Unit Weight replicate 39'),
        ('WGTP40', 'Housing Unit Weight replicate 40'),
        ('WGTP41', 'Housing Unit Weight replicate 41'),
        ('WGTP42', 'Housing Unit Weight replicate 42'),
        ('WGTP43', 'Housing Unit Weight replicate 43'),
        ('WGTP44', 'Housing Unit Weight replicate 44'),
        ('WGTP45', 'Housing Unit Weight replicate 45'),
        ('WGTP46', 'Housing Unit Weight replicate 46'),
        ('WGTP47', 'Housing Unit Weight replicate 47'),
        ('WGTP48', 'Housing Unit Weight replicate 48'),
        ('WGTP49', 'Housing Unit Weight replicate 49'),
        ('WGTP50', 'Housing Unit Weight replicate 50'),
        ('WGTP51', 'Housing Unit Weight replicate 51'),
        ('WGTP52', 'Housing Unit Weight replicate 52'),
        ('WGTP53', 'Housing Unit Weight replicate 53'),
        ('WGTP54', 'Housing Unit Weight replicate 54'),
        ('WGTP55', 'Housing Unit Weight replicate 55'),
        ('WGTP56', 'Housing Unit Weight replicate 56'),
        ('WGTP57', 'Housing Unit Weight replicate 57'),
        ('WGTP58', 'Housing Unit Weight replicate 58'),
        ('WGTP59', 'Housing Unit Weight replicate 59'),
        ('WGTP60', 'Housing Unit Weight replicate 60'),
        ('WGTP61', 'Housing Unit Weight replicate 61'),
        ('WGTP62', 'Housing Unit Weight replicate 62'),
        ('WGTP63', 'Housing Unit Weight replicate 63'),
        ('WGTP64', 'Housing Unit Weight replicate 64'),
        ('WGTP65', 'Housing Unit Weight replicate 65'),
        ('WGTP66', 'Housing Unit Weight replicate 66'),
        ('WGTP67', 'Housing Unit Weight replicate 67'),
        ('WGTP68', 'Housing Unit Weight replicate 68'),
        ('WGTP69', 'Housing Unit Weight replicate 69'),
        ('WGTP70', 'Housing Unit Weight replicate 70'),
        ('WGTP71', 'Housing Unit Weight replicate 71'),
        ('WGTP72', 'Housing Unit Weight replicate 72'),
        ('WGTP73', 'Housing Unit Weight replicate 73'),
        ('WGTP74', 'Housing Unit Weight replicate 74'),
        ('WGTP75', 'Housing Unit Weight replicate 75'),
        ('WGTP76', 'Housing Unit Weight replicate 76'),
        ('WGTP77', 'Housing Unit Weight replicate 77'),
        ('WGTP78', 'Housing Unit Weight replicate 78'),
        ('WGTP79', 'Housing Unit Weight replicate 79'),
        ('WGTP80', 'Housing Unit Weight replicate 80')
    ]
    feature = SelectMultipleField(
        'Available Features',
        choices=data
    )


@app.route('/population_data', methods=['GET', 'POST'])
def populationData():
    form = DataRequestFormPop(request.form)
    if request.method == 'POST':
        app.logger.info('this has been submitted', form.feature.data)
        filename, name = create_csv('population', form.feature.data)
        posts = [
            {
                'filename': name
            }
        ]
        return render_template('population_data.html', form=form, posts=posts)
    return render_template('population_data.html', form=form)


class DataRequestFormPop(Form):
    data = [
        ('RT', 'Record Type'),
        ('SERIALNO', 'Housing unit/GQ person serial number'),
        ('SPORDER', 'Person number'),
        ('PUMA', 'Public use microdata area code (PUMA) based on 2010 Census definition'),
        ('ST', 'State Code based on 2010 Census definitions'),
        ('ADJINC', 'Adjustment factor for income and earnings dollar amounts (6 implied decimal places)'),
        ('PWGTP', 'Person weight'),
        ('AGEP', 'Age'),
        ('CIT', 'Citizenship status'),
        ('CITWP', 'Year of naturalization write-in'),
        ('COW', 'Class of worker'),
        ('DDRS', 'Self-care difficulty'),
        ('DEAR', 'Hearing difficulty'),
        ('DEYE', 'Vision difficulty'),
        ('DOUT', 'Independent living difficulty'),
        ('DPHY', 'Ambulatory difficulty'),
        ('DRAT', 'Veteran service connected disability rating (percentage)'),
        ('DRATX', 'Veteran service connected disability rating (checkbox)'),
        ('DREM', 'Cognitive difficulty'),
        ('ENG', 'Ability to speak English'),
        ('FER', 'Gave birth to child within the past 12 months'),
        ('GCL', 'Grandparents living with grandchildren'),
        ('GCM', 'Length of time responsible for grandchildren'),
        ('GCR', 'Grandparents responsible for grandchildren'),
        ('HINS1', 'Insurance through a current or former employer or union'),
        ('HINS2', 'Insurance purchased directly from an insurance company'),
        ('HINS3', 'Medicare, for people 65 and older, or people with certain disabilities'),
        ('HINS4',
         'Medicaid, Medical Assistance, or any kind of government-assistance plan for those with low incomes or a disability'),
        ('HINS5', 'TRICARE or other military health care'),
        ('HINS6', 'VA (including those who have ever used or enrolled for VA health care)'),
        ('HINS7', 'Indian Health Service'),
        ('INTP', 'Interest, dividends, and net rental income past 12 months (signed)'),
        ('JWMNP', 'Travel time to work'),
        ('JWRIP', 'Vehicle occupancy'),
        ('JWTR', 'Means of transportation to work'),
        ('LANX', 'Language other than English spoken at home'),
        ('MAR', 'Marital status'),
        ('MARHD', 'Divorced in the past 12 months'),
        ('MARHM', 'Married in the past 12 months'),
        ('MARHT', 'Number of times married'),
        ('MARHW', 'Widowed in the past 12 months'),
        ('MARHYP', 'Year last married'),
        ('MIG', 'Mobility status (lived here 1 year ago)'),
        ('MIL', 'Military service'),
        ('MLPA', 'Served September 2001 or later'),
        ('MLPB', 'Served August 1990 - August 2001 (including Persian Gulf War)'),
        ('MLPCD', 'Served May 1975 - July 1990'),
        ('MLPE', 'Served Vietnam era (August 1964 - April 1975)'),
        ('MLPFG', 'Served February 1955 - July 1964'),
        ('MLPH', 'Served Korean War (July 1950 - January 1955)'),
        ('MLPI', 'Served January 1947 - June 1950'),
        ('MLPJ', 'Served World War II (December 1941 - December 1946)'),
        ('MLPK', 'Served November 1941 or earlier'),
        ('NWAB', 'Temporary absence from work (Unedited-See "Employment Status Recode" (ESR))'),
        ('NWAV', 'Available for work (Unedited-See "Employment Status Recode" (ESR))'),
        ('NWLA', 'On layoff from work (UNEDITED-See "Employment Status Recode" (ESR))'),
        ('NWLK', 'Looking for work (Unedited-See "Employment Status Recode" (ESR))'),
        ('NWRE', 'Informed of recall (Unedited-See "Employment Status Recode" (ESR))'),
        ('OIP', 'All other income past 12 months'),
        ('PAP', 'Public assistance income past 12 months'),
        ('RELP', 'Relationship'),
        ('RETP', 'Retirement income past 12 months'),
        ('SCH', 'School enrollment'),
        ('SCHG', 'Grade level attending'),
        ('SCHL', 'Educational attainment'),
        ('SEMP', 'Self-employment income past 12 months (signed)'),
        ('SEX', 'Sex'),
        ('SSIP', 'Supplementary Security Income past 12 months'),
        ('SSP', 'Social Security income past 12 months'),
        ('WAGP', 'Wages or salary income past 12 months'),
        ('WKHP', 'Usual hours worked per week past 12 months'),
        ('WKL', 'When last worked'),
        ('WKW', 'Weeks worked during past 12 months'),
        ('WRK', 'Worked last week'),
        ('YOEP', 'Year of entry'),
        ('ANC', 'Ancestry recode'),
        ('DECADE', 'Decade of entry'),
        ('DIS', 'Disability recode'),
        ('DRIVESP', 'Number of vehicles calculated from JWRI'),
        ('ESP', 'Employment status of parents'),
        ('ESR', 'Employment status recode'),
        ('HICOV', 'Health insurance coverage recode'),
        ('HISP', 'Recoded detailed Hispanic origin'),
        ('INDP', 'Industry recode based on 2012 IND codes'),
        ('JWAP', 'Time of arrival at work - hour and minute'),
        ('JWDP', 'Time of departure for work - hour and minute'),
        ('LANP', 'Language spoken at home'),
        ('MIGPUMA', 'Migration PUMA based on 2010 Census definition'),
        ('MIGSP', 'Migration recode - State or foreign country code'),
        ('MSP', 'Married, spouse present/spouse absent'),
        ('NAICSP', 'NAICS Industry code based on 2012 NAICS codes'),
        ('NATIVITY', 'Nativity'),
        ('NOP', 'Nativity of parent'),
        ('OC', 'Own child'),
        ('OCCP', 'Occupation recode based on 2010 OCC codes'),
        ('PAOC', 'Presence and age of own children'),
        ('PERNP', 'Total persons earnings'),
        ('PINCP', 'Total persons income (signed)'),
        ('POBP', 'Place of birth (Recode)'),
        ('POVPIP', 'Income-to-poverty ratio recode'),
        ('POWPUMA', 'Place of work PUMA based on 2010 Census'),
        ('POWSP', 'Place of work - State or foreign country recode'),
        ('PRIVCOV', 'Private health insurance coverage recode'),
        ('PUBCOV', 'Public health coverage recode'),
        ('QTRBIR', 'Quarter of birth'),
        ('RACAIAN',
         'American Indian and Alaska Native recode (American Indian and Alaska Native alone or in combination with one or more other races)'),
        ('RACASN', 'Asian recode (Asian alone or in combination with one or more other races)'),
        ('RACBLK', 'Black or African American recode (Black alone or in combination with one or more other races)'),
        ('RACNH', 'Native Hawaiian recode (Native Hawaiian alone or in combination with one or more other races)'),
        ('RACNUM', 'Number of major race groups represented'),
        ('RACPI',
         'Other Pacific Islander recode (Other Pacific Islander alone or in combination with one or more other races)'),
        ('RACSOR', 'Some other race recode (Some other race alone or in combination with one or more other races)'),
        ('RACWHT', 'White recode (White alone or in combination with one or more other races)'),
        ('RC', 'Related child'),
        ('SCIENGP', 'Field of degree science and engineering flag - NSF definition'),
        ('SCIENGRLP', 'Field of degree science and engineering related flag - NSF definition'),
        ('SFN', 'Subfamily number'),
        ('SFR', 'Subfamily relationship'),
        ('SOCP', 'SOC Occupation recode based on 2010 SOC codes'),
        ('VPS', 'Veteran period of service'),
        ('WAOB', 'World area of birth'),
        ('FAGEP', 'Age allocation flag'),
        ('FANCP', 'Ancestry allocation flag'),
        ('FCITP', 'Citizenship allocation flag'),
        ('FCITWP', 'Year of naturalization write-in allocation flag'),
        ('FCOWP', 'Class of worker allocation flag'),
        ('FDDRSP', 'Self-care difficulty allocation flag'),
        ('FDEARP', 'Hearing difficulty allocation flag'),
        ('FDEYEP', 'Vision difficulty allocation flag'),
        ('FDISP', 'Disability recode allocation flag'),
        ('FDOUTP', 'Independent living difficulty allocation flag'),
        ('FDPHYP', 'Ambulatory difficulty allocation flag'),
        ('FDRATP', 'Disability rating percentage allocation flag'),
        ('FDRATXP', 'Disability rating checkbox allocation flag'),
        ('FDREMP', 'Cognitive difficulty allocation flag'),
        ('FENGP', 'Ability to speak English allocation flag'),
        ('FESRP', 'Employment status recode allocation flag'),
        ('FFERP', 'Gave birth to child within the past 12 months allocation flag'),
        ('FFODP', 'Field of Degree allocation flag'),
        ('FGCLP', 'Grandparents living with grandchildren allocation flag'),
        ('FGCMP', 'Length of time responsible for grandchildren allocation flag'),
        ('FGCRP', 'Grandparents responsible for grandchildren allocation flag'),
        ('FHISP', 'Detailed Hispanic origin allocation flag'),
        ('FINDP', 'Industry allocation flag'),
        ('FINTP', 'Interest, dividend, and net rental income allocation flag'),
        ('FJWDP', 'Time of departure to work allocation flag'),
        ('FJWMNP', 'Travel time to work allocation flag'),
        ('FJWRIP', 'Vehicle occupancy allocation flag'),
        ('FJWTRP', 'Means of transportation to work allocation flag'),
        ('FLANP', 'Language spoken at home allocation flag'),
        ('FLANXP', 'Language other than English allocation flag'),
        ('FMARP', 'Marital status allocation flag'),
        ('FMARHDP', 'Divorced in the past 12 months allocation flag'),
        ('FMARHMP', 'Married in the past 12 months allocation flag'),
        ('FMARHTP', 'Times married allocation flag'),
        ('FMARHWP', 'Widowed in the past 12 months allocation flag'),
        ('FMARHYP', 'Year last married allocation flag'),
        ('FMIGP', 'Mobility status allocation flag'),
        ('FMIGSP', 'Migration state allocation flag'),
        ('FMILPP', 'Military periods of service allocation flag'),
        ('FMILSP', 'Military service allocation flag'),
        ('FOCCP', 'Occupation allocation flag'),
        ('FOIP', 'All other income allocation flag'),
        ('FPAP', 'Public assistance income allocation flag'),
        ('FPERNP', 'Total persons earnings allocation flag'),
        ('FPINCP', 'Total persons income (signed) allocation flag'),
        ('FPOBP', 'Place of birth allocation flag'),
        ('FPOWSP', 'Place of work state allocation flag'),
        ('FPRIVCOVP', 'Private health insurance coverage recode allocation flag'),
        ('FPUBCOVP', 'Public health coverage recode allocation flag'),
        ('FRACP', 'Detailed race allocation flag'),
        ('FRELP', 'Relationship allocation flag'),
        ('FRETP', 'Retirement income allocation flag'),
        ('FSCHGP', 'Grade attending allocation flag'),
        ('FSCHLP', 'Highest education allocation flag'),
        ('FSCHP', 'School enrollment allocation flag'),
        ('FSEMP', 'Self-employment income allocation flag'),
        ('FSEXP', 'Sex allocation flag'),
        ('FSSIP', 'Supplementary Security Income allocation flag'),
        ('FSSP', 'Social Security income allocation flag'),
        ('FWAGP', 'Wages and salary income allocation flag'),
        ('FWKHP', 'Usual hours worked per week past 12 months allocation flag'),
        ('FWKLP', 'Last worked allocation flag'),
        ('FWKWP', 'Weeks worked past 12 months allocation flag'),
        ('FWRKP', 'Worked last week allocation flag'),
        ('FYOEP', 'Year of entry allocation flag'),
        ('PWGTP1', 'Person Weight replicate 1'),
        ('PWGTP2', 'Person Weight replicate 2'),
        ('PWGTP3', 'Person Weight replicate 3'),
        ('PWGTP4', 'Person Weight replicate 4'),
        ('PWGTP5', 'Person Weight replicate 5'),
        ('PWGTP6', 'Person Weight replicate 6'),
        ('PWGTP7', 'Person Weight replicate 7'),
        ('PWGTP8', 'Person Weight replicate 8'),
        ('PWGTP9', 'Person Weight replicate 9'),
        ('PWGTP10', 'Person Weight replicate 10'),
        ('PWGTP11', 'Person Weight replicate 11'),
        ('PWGTP12', 'Person Weight replicate 12'),
        ('PWGTP13', 'Person Weight replicate 13'),
        ('PWGTP14', 'Person Weight replicate 14'),
        ('PWGTP15', 'Person Weight replicate 15'),
        ('PWGTP16', 'Person Weight replicate 16'),
        ('PWGTP17', 'Person Weight replicate 17'),
        ('PWGTP18', 'Person Weight replicate 18'),
        ('PWGTP19', 'Person Weight replicate 19'),
        ('PWGTP20', 'Person Weight replicate 20'),
        ('PWGTP21', 'Person Weight replicate 21'),
        ('PWGTP22', 'Person Weight replicate 22'),
        ('PWGTP23', 'Person Weight replicate 23'),
        ('PWGTP24', 'Person Weight replicate 24'),
        ('PWGTP25', 'Person Weight replicate 25'),
        ('PWGTP26', 'Person Weight replicate 26'),
        ('PWGTP27', 'Person Weight replicate 27'),
        ('PWGTP28', 'Person Weight replicate 28'),
        ('PWGTP29', 'Person Weight replicate 29'),
        ('PWGTP30', 'Person Weight replicate 30'),
        ('PWGTP31', 'Person Weight replicate 31'),
        ('PWGTP32', 'Person Weight replicate 32'),
        ('PWGTP33', 'Person Weight replicate 33'),
        ('PWGTP34', 'Person Weight replicate 34'),
        ('PWGTP35', 'Person Weight replicate 35'),
        ('PWGTP36', 'Person Weight replicate 36'),
        ('PWGTP37', 'Person Weight replicate 37'),
        ('PWGTP38', 'Person Weight replicate 38'),
        ('PWGTP39', 'Person Weight replicate 39'),
        ('PWGTP40', 'Person Weight replicate 40'),
        ('PWGTP41', 'Person Weight replicate 41'),
        ('PWGTP42', 'Person Weight replicate 42'),
        ('PWGTP43', 'Person Weight replicate 43'),
        ('PWGTP44', 'Person Weight replicate 44'),
        ('PWGTP45', 'Person Weight replicate 45'),
        ('PWGTP46', 'Person Weight replicate 46'),
        ('PWGTP47', 'Person Weight replicate 47'),
        ('PWGTP48', 'Person Weight replicate 48'),
        ('PWGTP49', 'Person Weight replicate 49'),
        ('PWGTP50', 'Person Weight replicate 50'),
        ('PWGTP51', 'Person Weight replicate 51'),
        ('PWGTP52', 'Person Weight replicate 52'),
        ('PWGTP53', 'Person Weight replicate 53'),
        ('PWGTP54', 'Person Weight replicate 54'),
        ('PWGTP55', 'Person Weight replicate 55'),
        ('PWGTP56', 'Person Weight replicate 56'),
        ('PWGTP57', 'Person Weight replicate 57'),
        ('PWGTP58', 'Person Weight replicate 58'),
        ('PWGTP59', 'Person Weight replicate 59'),
        ('PWGTP60', 'Person Weight replicate 60'),
        ('PWGTP61', 'Person Weight replicate 61'),
        ('PWGTP62', 'Person Weight replicate 62'),
        ('PWGTP63', 'Person Weight replicate 63'),
        ('PWGTP64', 'Person Weight replicate 64'),
        ('PWGTP65', 'Person Weight replicate 65'),
        ('PWGTP66', 'Person Weight replicate 66'),
        ('PWGTP67', 'Person Weight replicate 67'),
        ('PWGTP68', 'Person Weight replicate 68'),
        ('PWGTP69', 'Person Weight replicate 69'),
        ('PWGTP70', 'Person Weight replicate 70'),
        ('PWGTP71', 'Person Weight replicate 71'),
        ('PWGTP72', 'Person Weight replicate 72'),
        ('PWGTP73', 'Person Weight replicate 73'),
        ('PWGTP74', 'Person Weight replicate 74'),
        ('PWGTP75', 'Person Weight replicate 75'),
        ('PWGTP76', 'Person Weight replicate 76'),
        ('PWGTP77', 'Person Weight replicate 77'),
        ('PWGTP78', 'Person Weight replicate 78'),
        ('PWGTP79', 'Person Weight replicate 79'),
        ('PWGTP80', 'Person Weight replicate 80')

    ]

    feature = SelectMultipleField(
        'Available features',
        choices=data
    )


if __name__ == '__main__':
    app.run(debug=True)
