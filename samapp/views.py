from decimal import Decimal, InvalidOperation
import re

from django.contrib import messages
from django.db.models import Q
from django.utils.dateparse import parse_date
from django.shortcuts import get_object_or_404, redirect, render

from .models import Booking, Car, ContactMessage


STATIC_CARS = [
	{
		'number': 1, 'image': 'images/car01.jpeg', 'title': '2021 Toyota Hilux Diesel Z Black Rally Edition',
		'body_type': 'Pickup', 'price': Decimal('6100000'), 'price_label': 'KSh 6.1M',
		'description': 'A Japan-version 4WD Hilux with 42,680 km, Rally styling, reverse camera, lane assist, cruise control, and original Toyota alloy rims.',
		'search_text': 'Toyota Hilux diesel new shape 2021 Japan version 4WD Z Black Rally Edition fog lamps LED xenon push start steering controls DVD reverse camera lane assist traction control auto stopper eco mode power mode cruise control 42680 km good tyres original Toyota alloy rims',
	},
	{
		'number': 2, 'image': 'images/car 02.jpeg', 'title': '2022 Toyota Land Cruiser Prado Petrol',
		'body_type': 'SUV', 'price': Decimal('7000000'), 'price_label': 'KSh 7M',
		'description': 'A low-mileage 7-seater Prado with only 26,000 km, sunroof, black leather, heated and cooled electric seats, parking sensors, and 4WD confidence.',
		'search_text': 'Toyota Land Cruiser Prado petrol 2022 sunroof very low mileage 26000 kms fog lamps LED xenon parking sensors steering controls DVD reverse camera cruise control traction control lane assist black leather seats electric power seats heated seats cooling seats 7 seater roof rails spoiler good tyres original alloy rims',
	},
	{
		'number': 3, 'image': 'images/car 3.jpeg', 'title': '2019 Volkswagen Golf',
		'body_type': 'Hatchback', 'price': Decimal('2400000'), 'price_label': 'KSh 2.4M',
		'description': 'A fully loaded, unregistered 1.4L Golf with 100,000 km, LED xenon lights, roof rails, reverse camera, drive modes, and multi-function steering.',
		'search_text': 'Volkswagen Golf 2019 1400cc mileage 100k LED xenon fog light roof rail original alloy wheels rear view camera eyesight drive mode auto stopper black color multi steering control fully loaded not registered',
	},
	{
		'number': 4, 'image': 'images/car 4.jpeg', 'title': '2019 Subaru Forester SK9 X-Break',
		'body_type': 'SUV', 'price': Decimal('3750000'), 'price_label': 'KSh 3.75M',
		'description': 'An unregistered army-green Forester with symmetrical AWD, EyeSight safety, X-Modes, blind-spot monitoring, heated seats, and 102,000 km.',
		'search_text': 'Subaru Forester SK9 X Break 2019 army green 2500cc engine eyesight technology xenon DRL foglights symmetrical AWD powered seats memory heated seats steering responsive headlights blind spot monitoring multiple camera view X mode snow dirt mud electric parking brakes AVH steering warmer rear vehicle monitoring cruise control lane departure anti collision dual zone AC rear heated seats semi leather interior mileage 102000 not registered',
	},
	{
		'number': 5, 'image': 'images/car 05.jpeg', 'title': '2019 Mazda CX-8 XDL Premium Exclusive',
		'body_type': 'SUV', 'price': Decimal('3850000'), 'price_label': 'KSh 3.85M',
		'description': 'A premium 2.2L turbo-diesel CX-8 with 53,000 km, six cream leather seats, sunroof, HUD, ventilated seats, 360 camera, and Bose audio.',
		'search_text': 'Mazda CX-8 XDL Premium Exclusive 2019 grey 2200cc turbocharged diesel 6 speed automatic digital cluster 6 cream leather seats 53k kms heads up display HUD DRL sunroof driver memory seat front rear ventilated seats warmers blind spot monitoring lane departure 360 camera cruise control paddle shifts Bose sound system multimedia DVD Bluetooth parking sensors reverse camera steering warmer alloy wheels push start xenon traction control dual climate cash trade ins bank finance',
	},
	{
		'number': 6, 'image': 'images/car 06.jpeg', 'title': '2019 Range Rover Vogue Autobiography SDV8',
		'body_type': 'SUV', 'price': Decimal('14800000'), 'price_label': 'KSh 14.8M',
		'description': 'A 4.4L V8 turbo-diesel luxury SUV with 75,000 km, panoramic sunroof, massage seats, four-zone climate, HUD, and 360 camera.',
		'search_text': 'Range Rover Vogue Autobiography SDV8 2019 4.4L V8 turbocharged diesel 340 BHP 740NM 8 speed automatic panoramic sunroof height control 75k mileage soft close doors paddle shifts steering controls parking sensors lane assist blind spot automatic handbrake 4 zone climate heated cooled seats massage seats HUD 360 camera adaptive cruise memory seats powered boot Meridian sound DVD tyre pressure monitor touchscreen radar guided cruise',
	},
	{
		'number': 7, 'image': 'images/car 07.jpeg', 'title': '2020 Mercedes-Benz GLS400d AMG-Line 4MATIC',
		'body_type': 'SUV', 'price': Decimal('15000000'), 'price_label': 'KSh 15M',
		'description': 'A black AMG-Line GLS with 25,000 km, 3.0L twin-turbo diesel power, panoramic sunroof, soft-close doors, Burmester audio, and 4MATIC drive.',
		'search_text': 'Mercedes Benz GLS400D AMG LINE 4MATIC black 2020 9 speed automatic 3000cc twin turbo diesel 330 bhp 700nm 25k kms 360 camera parking aid panoramic sunroof softclose doors auto stop start dual zone air conditioning powered seats navigation ambient display Burmester sound DVD Bluetooth keyless entry ABS hill descent electric parking brake AMG wheels memory seats adaptive suspension blind spot lane departure autonomous braking',
	},
	{
		'number': 8, 'image': 'images/car 08.jpeg', 'title': 'Toyota Land Cruiser 300 Series ZX / VXR',
		'body_type': 'SUV', 'price': Decimal('21000000'), 'price_label': 'KSh 17M - 21M',
		'description': 'A high-spec LC300 with twin-turbo V6 power, 10-speed automatic transmission, full-time 4WD, 7-seat leather interior, and Toyota Safety Sense.',
		'search_text': 'Toyota Land Cruiser 300 Series LC300 ZX VXR 3.5L V6 twin turbo petrol 409 hp 3.3L V6 diesel 304 hp 10 speed automatic full time 4WD 20 inch alloy wheels 7 seater leather interior multi terrain select adaptive variable suspension Toyota Safety Sense imported 2022 2023 brand new high spec 2024 2025',
	},
	{
		'number': 9, 'image': 'images/car 09.jpeg', 'title': '2019 Honda Vezel RS Hybrid',
		'body_type': 'SUV', 'price': Decimal('2700000'), 'price_label': 'KSh 2.7M',
		'description': 'A sporty black RS Hybrid with excellent fuel economy, 1.5L automatic power, push start, paddle shifters, reverse camera, and climate control.',
		'search_text': 'Honda Vezel RS Hybrid 2019 black RS sport trim hybrid petrol 1500cc automatic fuel economy sporty exterior RS alloy wheels LED headlights DRL keyless entry push start multifunction steering paddle shifters reverse camera infotainment Bluetooth climate control comfortable interior folding rear seats electric mirrors sporty RS interior',
	},
	{
		'number': 10, 'image': 'images/car 10.jpeg', 'title': '2023 Toyota Land Cruiser 300 Series ZX',
		'body_type': 'SUV', 'price': Decimal('17800000'), 'price_label': 'KSh 17.8M',
		'description': 'A white ZX LC300 with 30,000 km, 409 BHP twin-turbo V6, 7 seats, cooled leather, JBL sound, 360 camera, and advanced 4WD systems.',
		'search_text': 'Toyota Land Cruiser 300 Series ZX 2023 white 3.5 litre V6 twin turbo petrol 409 BHP 650nm 10 speed automatic 30k kms heated steering beige leather power seats memory seats rear entertainment electric sunroof 7 seater heated cooled seats Apple CarPlay JBL sound multi terrain select adaptive suspension 4WD downhill assist crawl control adaptive cruise traction lane keeping pre collision parking sensors 360 view camera LED headlights cash bank finance trade ins',
	},
	{
		'number': 11, 'image': 'images/car 11.jpeg', 'title': '2019 Toyota Prado J150 TX-L',
		'body_type': 'SUV', 'price': Decimal('6000000'), 'price_label': 'KSh 6M',
		'description': 'A black 4WD Prado with 70,000 km, sunroof, beige leather, cooled and warmed electric seats, blind-spot monitoring, and parking assist.',
		'search_text': 'Toyota Prado J150 TX L 2019 black 2700cc petrol 6 speed automatic 70k kms 4WD sunroof beige leather seats electric seats cooled warmed seats multimedia Bluetooth DVD surround sound dual zone climate reverse camera blind spot anti collision lane departure parking assist sensors steering controls cruise control ABS traction control',
	},
	{
		'number': 12, 'image': 'images/car 12.jpeg', 'title': '2020 Mercedes-Benz GLE 400d 4MATIC',
		'body_type': 'SUV', 'price': Decimal('13700000'), 'price_label': 'KSh 13.7M',
		'description': 'A refined GLE 400d with 4MATIC all-wheel drive, sunroof, bounce mode, and approximately 53,000 km.',
		'search_text': 'Mercedes Benz GLE 400d 2020 bouncing mode 4MATIC sunroof 53xxx kms luxury SUV diesel',
	},
	{
		'number': 13, 'image': 'images/car 13.jpeg', 'title': '2020 BMW X3 xDrive20d M Sport',
		'body_type': 'SUV', 'price': None, 'price_label': 'Price on request',
		'description': 'A fresh-import BMW X3 with xDrive AWD, 53,000 km, M Sport styling, Cognac leather, navigation, Apple CarPlay, and parking sensors.',
		'search_text': 'BMW X3 xDrive20d M Sport fresh import 2020 2.0L TwinPower Turbo diesel B47D20 8 speed Steptronic automatic 53000KM AWD pearl white black Vernasca Cognac leather M Sport body kit LED headlights fog lights leather steering paddle shifters touchscreen iDrive navigation Apple CarPlay ambient lighting dual zone climate rear camera parking sensors electric seats memory power tailgate cruise control lane departure forward collision hill descent 19 inch M alloy wheels',
	},
	{
		'number': 14, 'image': 'images/car 14.jpeg', 'title': '2021 Land Rover Defender X-Dynamic D250',
		'body_type': 'SUV', 'price': Decimal('16000000'), 'price_label': 'KSh 16M',
		'description': 'A rugged yet refined Defender with 3.0L D250 turbo-diesel power, 249 HP, 570 Nm, automatic transmission, and intelligent AWD.',
		'search_text': 'Land Rover Defender X Dynamic D250 2021 3.0L inline 6 turbo diesel 249 HP 570 Nm automatic intelligent all wheel drive AWD luxury SUV rugged premium off road cash price',
	},
]


STATIC_IMPORT_CARS = [
	{
		'number': 1, 'image': 'imports/import 1.jpeg', 'title': '2022 Mercedes-Benz Maybach GLS600',
		'price_label': 'GBP 112,990',
		'description': 'A first-class Maybach GLS600h with a 4.0L V8 mild-hybrid engine, 4MATIC all-wheel drive, and G-Tronic automatic transmission.',
		'search_text': 'Mercedes Benz Maybach GLS 2022 GLS600h V8 MHEV first class G Tronic 4MATIC Euro 6 luxury SUV automatic petrol imported car',
	},
	{
		'number': 2, 'image': 'imports/import 2.jpeg', 'title': '2023 BMW M3 Competition M xDrive',
		'price_label': 'USD 69,878 to Mombasa port',
		'description': 'A right-hand-drive BMW M3 Competition with xDrive 4WD, 3.0L petrol power, automatic transmission, and only 9,031 km. Inspection and shipping are included; taxes and duties are separate.',
		'search_text': 'BMW M3 Competition M xDrive 2023 9031KM 3000cc petrol automatic RHD 4WD DCB3739 shipping inspection Mombasa port import',
	},
	{
		'number': 3, 'image': 'imports/import 3.jpeg', 'title': '2022 BMW M3 Competition',
		'price_label': 'KSh 19M total landing cost',
		'description': 'A performance-focused 3.0L BiTurbo BMW M3 Competition with Steptronic automatic transmission and Euro 6 efficiency.',
		'search_text': 'BMW M3 2022 3.0 BiTurbo Competition Steptronic Euro 6 automatic petrol performance car total landing cost',
	},
	{
		'number': 4, 'image': 'imports/import 4.jpeg', 'title': '2021 Audi RS7 4.0 V8 TFSI',
		'price_label': 'KSh 21.965M total landing cost',
		'description': 'A German-spec RS7 with 7,000 miles, 591 HP, 800 Nm, panoramic sunroof, Quattro sports differential, Matrix LED lights, 360 camera, Bose audio, and four-zone climate.',
		'search_text': 'Audi RS7 2021 4.0 V8 TFSI panoramic sunroof 7000 miles twin turbo petrol 8 speed automatic 800NM 591HP sports exhaust parking assist Bose virtual cockpit cruise climate Matrix LED heated seats navigation RS brakes rear camera Quattro AWD import Germany 45 days shipping',
	},
	{
		'number': 5, 'image': 'imports/import 5.jpeg', 'title': 'Lexus LX 500d Luxury SUV',
		'price_label': 'KSh 17M total',
		'description': 'A commanding LX 500d powered by a 3.3L twin-turbo V6 diesel with 304 HP, 700 Nm, 10-speed automatic transmission, and serious off-road capability.',
		'search_text': 'Lexus LX 500d 3.3L twin turbo V6 diesel 304 horsepower 700Nm 10 speed automatic luxury SUV Land Cruiser platform off road terrain management premium interior reliability import',
	},
	{
		'number': 6, 'image': 'imports/import 6.jpeg', 'title': '2019 Nissan GT-R R35 Track Edition by Litchfield',
		'price_label': 'Price on request',
		'description': 'A rare Pearl Black GT-R Track Edition upgraded by Litchfield to 976 BHP with forged engine internals, BorgWarner turbos, Akrapovic titanium exhaust, Dodson transmission, Quaife differential, and carbon-fibre aero.',
		'search_text': 'Nissan GT R R35 Track Edition 2019 Litchfield 976bhp 3.8 litre twin turbo V6 562bhp 0 62 2.7 seconds Bilstein suspension forged engine BorgWarner turbo Capricorn pistons titanium Akrapovic exhaust Dodson transmission Quaife differential Pearl Black carbon fibre XPEL LM20 performance import',
	},
	{
		'number': 7, 'image': 'imports/import 7.jpeg', 'title': '2019 Nissan GT-R R35 Nismo Performance',
		'price_label': 'KSh 22M',
		'description': 'A Fire Red Metallic GT-R with 31,000 km, 565 HP 3.8L twin-turbo V6, 4WD, Nappa leather and suede, Nismo handling pack, carbon-titanium exhaust, ceramic brakes, and 360 camera.',
		'search_text': 'Nissan GT R 2019 3800cc V6 automatic 4WD Euro 6 31000 Kms 565 hp Fire Red Metallic Nappa black leather suede Nissan infotainment telemetry navigation TV 360 camera Apple CarPlay heated cooled massaging memory seats Nismo alloy rear wheel steer carbon titanium exhaust ceramic brakes Matrix LED Bose',
	},
	{
		'number': 8, 'image': 'imports/import 8.jpeg', 'title': '2022 BMW X6 M',
		'price_label': 'KSh 22M cash',
		'description': 'A high-performance luxury SUV coupe with a 4.4L twin-turbo V8, approximately 600 HP, 8-speed automatic transmission, xDrive AWD, premium leather, panoramic styling, and advanced driver assistance.',
		'search_text': 'BMW X6 M 2022 4.4 litre twin turbo V8 600hp 8 speed automatic xDrive all wheel drive leather Apple CarPlay Android Auto ambient lighting driver assistance quad exhaust M performance luxury SUV coupe cash',
	},
	{
		'number': 9, 'image': 'imports/import 9.jpeg', 'title': '2021 BMW X5 M Competition',
		'price_label': 'KSh 17M cash',
		'description': 'A 617 HP X5 M Competition combining supercar acceleration with SUV practicality, 4.4L twin-turbo V8 power, xDrive all-wheel drive, premium luxury, and sporty M detailing.',
		'search_text': 'BMW X5 M Competition 2021 4.4 litre twin turbo V8 617 horsepower 8 speed automatic xDrive AWD 0 100 under 4 seconds luxury SUV premium materials infotainment M detailing cash import',
	},
	{
		'number': 10, 'image': 'imports/import 10.jpeg', 'title': 'Audi RS Q8 Performance SUV',
		'price_label': 'KSh 21M',
		'description': 'Audi performance and luxury in one package: 4.0L twin-turbo V8, 591 HP, 800 Nm, Quattro AWD, panoramic sunroof, Valcona leather, 360 cameras, Bang & Olufsen audio, and adaptive cruise.',
		'search_text': 'Audi RS Q8 4.0 litre twin turbo V8 591 horsepower 800Nm 8 speed automatic Quattro all wheel drive powered leather seats memory heated seats panoramic sunroof Valcona leather virtual cockpit Bang Olufsen adaptive cruise traction control rear view 360 camera parking sensors LED electric tailgate sports styling',
	},
	{
		'number': 11, 'image': 'imports/import 11.jpeg', 'title': '2021 Mercedes-Benz S500 L AMG Line',
		'price_label': 'KSh 18M cash',
		'description': 'A long-wheelbase executive saloon with 3.0L turbocharged petrol mild-hybrid power, 4MATIC AWD, reclining heated and ventilated massage seats, Burmester 3D sound, air suspension, and rear-lounge comfort.',
		'search_text': 'Mercedes Benz S500 L AMG Line Premium Plus Executive 2021 3.0L inline 6 turbo petrol 48V mild hybrid EQ Boost 435hp 520Nm 9G Tronic 4MATIC long wheelbase rear legroom reclining heated ventilated massage seats rear entertainment Burmester 3D ambient lighting soft close doors air suspension driver assistance luxury saloon cash',
	},
	{
		'number': 12, 'image': 'imports/import 12.jpeg', 'title': '2019 Mercedes-AMG G63',
		'price_label': 'KSh 30M cash',
		'description': 'The iconic AMG G63 with a 4.0L V8 BiTurbo producing about 577 HP, explosive 0-100 km/h performance, AMG exhaust sound, and unmistakable military-inspired road presence.',
		'search_text': 'Mercedes AMG G63 2019 4.0L V8 BiTurbo 577hp 585PS 0 100 4.5 seconds AMG performance exhaust Sport Sport Plus boxy military inspired design luxury SUV raw loud performance cash',
	},
	{
		'number': 13, 'image': 'imports/import 13.jpeg', 'title': 'Bentley Continental GT Speed First Edition',
		'price_label': 'KSh 30M cash',
		'description': 'A grand tourer delivering 771 HP, handcrafted luxury, a powerful W12 engine, advanced all-wheel drive, premium cabin comfort, and Tourmaline Green road presence.',
		'search_text': 'Bentley Continental GT Speed First Edition 771HP W12 luxury grand tourer all wheel drive handcrafted interior Tourmaline Green comfort performance premium imported car cash',
	},
	{
		'number': 14, 'image': 'imports/import 14.jpeg', 'title': '2021 Ferrari 812 GTS',
		'price_label': 'GBP 399,995 / KSh 110M cash',
		'description': 'A Blu Elettrico 812 GTS with Nero and Rosso Corsa Alcantara interior, forged racing wheels, carbon-fibre driver zone, suspension lift, Apple CarPlay, and surround-view cameras.',
		'search_text': 'Ferrari 812 GTS 2021 Blu Elettrico Nero Rosso Corsa Alcantara 20 forged racing wheels matte black red calipers carbon fibre racing seats Apple CarPlay adaptive frontlight suspension lift surround view cameras V12 supercar cash',
	},
	{
		'number': 15, 'image': 'imports/import 15.jpeg', 'title': '2024 Lamborghini Urus Performante',
		'price_label': 'GBP 259,995 / KSh 95M cash',
		'description': 'A Verde Turbine Urus Performante with carbon-fibre exterior, Akrapovic exhaust, panoramic roof, ventilated massage seats, full ADAS, HUD, Bang & Olufsen sound, and top-view camera.',
		'search_text': 'Lamborghini Urus Performante 2024 Verde Turbine Nero Ade leather Alcantara 23 wheels carbon fibre Akrapovic exhaust panoramic roof ventilated massage seats ADAS heated steering Bang Olufsen HUD intelligent park assist soft close top view camera SUV cash',
	},
	{
		'number': 16, 'image': 'imports/import 16.jpeg', 'title': '2025 Porsche Panamera Hybrid',
		'price_label': 'KSh 28M cash',
		'description': 'A Jet Black Metallic Panamera Hybrid with black leather, 21-inch alloy wheels, sports exhaust, black styling package, and Bose sound system.',
		'search_text': 'Porsche Panamera Hybrid 2025 Jet Black Metallic black leather 21 inch alloy wheels sports exhaust black styling package Bose sound system Panamera 4E hybrid luxury cash sold',
	},
	{
		'number': 17, 'image': 'imports/import 17.jpeg', 'title': '2022 BMW 420d M Sport Convertible',
		'price_label': 'KSh 8M landing cost',
		'description': 'A stylish 2022 BMW 420d M Sport Convertible import, prepared for a refined open-air drive with premium M Sport character.',
		'search_text': 'BMW 420d M Sport Convertible 2022 diesel cabriolet open top M Sport import landing cost 8M luxury car',
	},
	{
		'number': 18, 'image': 'imports/import 18.jpeg', 'title': '2026 Rolls-Royce Cullinan Series II',
		'price_label': 'KSh 125M',
		'description': 'A brand-new 2026 Cullinan Series II, offering unmistakable Rolls-Royce presence, effortless performance, first-class comfort, and exceptional luxury SUV craftsmanship.',
		'search_text': 'Rolls Royce Cullinan Series II 2026 brand new luxury SUV premium comfort effortless performance Mombasa imported car 125M',
	},
	{
		'number': 19, 'image': 'imports/import 19.jpeg', 'title': '2025 BMW i7 xDrive60 M Sport Pro',
		'price_label': 'KSh 28M cash',
		'description': 'A Frozen Pure Grey electric executive saloon with Tartufo Merino leather, 21-inch Style 908M alloy wheels, xDrive60 electric performance, and M Sport Pro specification.',
		'search_text': 'BMW i7 xDrive60 M Sport Pro 2025 electric luxury saloon Frozen Pure Grey Tartufo Merino leather 21 inch Style 908M alloy wheels M Sport Pro EV cash sold',
	},
]


def _search_static_cars(cars, query):
	if not query:
		return cars
	query_words = set(re.findall(r'[a-z0-9]+', query.lower()))
	results = []
	for car in cars:
		search_words = set(re.findall(r'[a-z0-9]+', f"{car['title']} {car['description']} {car['search_text']}".lower()))
		score = len(query_words & search_words)
		if score:
			results.append((score, car))
	return [car for _, car in sorted(results, key=lambda result: result[0], reverse=True)]


CAR_BRANDS = ('Toyota', 'Nissan', 'Mazda', 'Mercedes-Benz', 'Subaru', 'Honda', 'Volkswagen')


def _static_car_brand(car):
	title = car['title'].lower()
	for brand in CAR_BRANDS:
		if brand.lower() in title or (brand == 'Mercedes-Benz' and 'mercedes' in title):
			return brand
	return 'Other'


def home(request):
	featured_cars = Car.objects.filter(
		availability=Car.Availability.AVAILABLE,
		featured=True,
	)[:6]
	return render(request, 'home.html', {'featured_cars': featured_cars})


def cars(request):
	inventory = Car.objects.filter(
		is_import=False,
		availability__in=(Car.Availability.AVAILABLE, Car.Availability.SOLD),
	)
	has_database_cars = inventory.exists()
	query = request.GET.get('q', '').strip()
	brand = request.GET.get('brand', '').strip()
	max_price = request.GET.get('max_price', '').strip()

	if query:
		inventory = inventory.filter(
			Q(make__icontains=query)
			| Q(model__icontains=query)
			| Q(description__icontains=query)
		)
	if brand:
		if brand == 'Other':
			inventory = inventory.exclude(make__in=CAR_BRANDS)
		else:
			inventory = inventory.filter(make__icontains=brand.replace('-Benz', ''))
	if max_price:
		try:
			inventory = inventory.filter(price__lte=Decimal(max_price))
		except (InvalidOperation, TypeError, ValueError):
			pass

	static_inventory = _search_static_cars(STATIC_CARS, query)
	if brand:
		static_inventory = [car for car in static_inventory if _static_car_brand(car) == brand]
	if max_price:
		try:
			static_inventory = [car for car in static_inventory if car['price'] is None or car['price'] <= Decimal(max_price)]
		except (InvalidOperation, TypeError, ValueError):
			pass

	return render(request, 'cars.html', {
		'cars': inventory,
		'has_database_cars': has_database_cars,
		'static_cars': static_inventory,
		'inventory': inventory,
		'search_query': query,
		'selected_brand': brand,
		'max_price': max_price,
		'car_brands': CAR_BRANDS,
	})


def car_detail(request, pk):
	car = get_object_or_404(Car, pk=pk)
	return render(request, 'cars.html', {'car': car, 'cars': [car], 'inventory': [car]})


def about_us(request):
	return render(request, 'about_us.html')


def contact_us(request):
	if request.method == 'POST':
		required = ('name', 'email', 'message')
		if all(request.POST.get(field, '').strip() for field in required):
			ContactMessage.objects.create(
				name=request.POST['name'].strip(),
				email=request.POST['email'].strip(),
				phone=request.POST.get('phone', '').strip(),
				subject=request.POST.get('subject', '').strip(),
				message=request.POST['message'].strip(),
			)
			messages.success(request, 'Your message has been sent.')
			return redirect('samapp:contact')
		messages.error(request, 'Please provide your name, email, and message.')
	return render(request, 'contact_us.html')


def book_car(request, pk):
	car = get_object_or_404(Car, pk=pk, availability=Car.Availability.AVAILABLE)
	if request.method == 'POST':
		required = ('name', 'email')
		if all(request.POST.get(field, '').strip() for field in required):
			Booking.objects.create(
				car=car,
				name=request.POST['name'].strip(),
				email=request.POST['email'].strip(),
				phone=request.POST.get('phone', '').strip(),
				preferred_date=parse_date(request.POST.get('preferred_date', '')),
				notes=request.POST.get('notes', '').strip(),
			)
			messages.success(request, 'Your booking request has been received.')
			return redirect('samapp:cars')
		messages.error(request, 'Please provide your name and email.')
	return render(request, 'cars.html', {'car': car, 'booking_car': car})


def payment_options(request):
	return render(request, 'payment_options.html')


def imports_only(request):
	import_cars = Car.objects.filter(
		is_import=True,
		availability__in=(Car.Availability.AVAILABLE, Car.Availability.SOLD),
	)
	return render(request, 'importsonly.html', {
		'import_cars': import_cars,
		'static_import_cars': STATIC_IMPORT_CARS,
	})
