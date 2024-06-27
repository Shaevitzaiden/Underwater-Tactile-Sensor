EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
Wire Wire Line
	6100 2000 6350 2000
Wire Wire Line
	6100 1900 6100 2000
Wire Wire Line
	6100 1500 6350 1500
Wire Wire Line
	6100 1600 6100 1500
Wire Wire Line
	6100 2250 6350 2250
Wire Wire Line
	6100 2300 6100 2250
Wire Wire Line
	6100 2750 6350 2750
Wire Wire Line
	6100 2600 6100 2750
Wire Wire Line
	6100 2950 6350 2950
Wire Wire Line
	6100 3000 6100 2950
Wire Wire Line
	6100 3450 6350 3450
Wire Wire Line
	6100 3300 6100 3450
$Comp
L SamacSys_Parts:06034C104KAT2A C6
U 1 1 6198F41C
P 6350 3450
F 0 "C6" V 6578 3578 50  0000 L CNN
F 1 "06034C104KAT2A" H 6645 3578 20  0000 L CNN
F 2 "HighPressureSensorArray_Footprints:CAPC1608X90N" H 6700 3500 50  0001 L CNN
F 3 "https://componentsearchengine.com/Datasheets/1/06031A100FAT2A.pdf" H 6700 3400 50  0001 L CNN
F 4 "Multilayer Ceramic Capacitors MLCC - SMD/SMT 4V .1uF X7R 0603 10%" H 6700 3300 50  0001 L CNN "Description"
F 5 "0.9" H 6700 3200 50  0001 L CNN "Height"
F 6 "581-06034C104KAT2A" H 6700 3100 50  0001 L CNN "Mouser Part Number"
F 7 "https://www.mouser.co.uk/ProductDetail/AVX/06034C104KAT2A?qs=EbDiPP9peV90W1IAXf%252BZmA%3D%3D" H 6700 3000 50  0001 L CNN "Mouser Price/Stock"
F 8 "AVX" H 6700 2900 50  0001 L CNN "Manufacturer_Name"
F 9 "06034C104KAT2A" H 6700 2800 50  0001 L CNN "Manufacturer_Part_Number"
	1    6350 3450
	0    -1   -1   0   
$EndComp
$Comp
L SamacSys_Parts:06034C104KAT2A C5
U 1 1 6198E66A
P 6350 2750
F 0 "C5" V 6578 2878 50  0000 L CNN
F 1 "06034C104KAT2A" H 6645 2878 20  0000 L CNN
F 2 "HighPressureSensorArray_Footprints:CAPC1608X90N" H 6700 2800 50  0001 L CNN
F 3 "https://componentsearchengine.com/Datasheets/1/06031A100FAT2A.pdf" H 6700 2700 50  0001 L CNN
F 4 "Multilayer Ceramic Capacitors MLCC - SMD/SMT 4V .1uF X7R 0603 10%" H 6700 2600 50  0001 L CNN "Description"
F 5 "0.9" H 6700 2500 50  0001 L CNN "Height"
F 6 "581-06034C104KAT2A" H 6700 2400 50  0001 L CNN "Mouser Part Number"
F 7 "https://www.mouser.co.uk/ProductDetail/AVX/06034C104KAT2A?qs=EbDiPP9peV90W1IAXf%252BZmA%3D%3D" H 6700 2300 50  0001 L CNN "Mouser Price/Stock"
F 8 "AVX" H 6700 2200 50  0001 L CNN "Manufacturer_Name"
F 9 "06034C104KAT2A" H 6700 2100 50  0001 L CNN "Manufacturer_Part_Number"
	1    6350 2750
	0    -1   -1   0   
$EndComp
$Comp
L SamacSys_Parts:06034C104KAT2A C4
U 1 1 6198C536
P 6350 2000
F 0 "C4" V 6578 2128 50  0000 L CNN
F 1 "06034C104KAT2A" H 6645 2128 20  0000 L CNN
F 2 "HighPressureSensorArray_Footprints:CAPC1608X90N" H 6700 2050 50  0001 L CNN
F 3 "https://componentsearchengine.com/Datasheets/1/06031A100FAT2A.pdf" H 6700 1950 50  0001 L CNN
F 4 "Multilayer Ceramic Capacitors MLCC - SMD/SMT 4V .1uF X7R 0603 10%" H 6700 1850 50  0001 L CNN "Description"
F 5 "0.9" H 6700 1750 50  0001 L CNN "Height"
F 6 "581-06034C104KAT2A" H 6700 1650 50  0001 L CNN "Mouser Part Number"
F 7 "https://www.mouser.co.uk/ProductDetail/AVX/06034C104KAT2A?qs=EbDiPP9peV90W1IAXf%252BZmA%3D%3D" H 6700 1550 50  0001 L CNN "Mouser Price/Stock"
F 8 "AVX" H 6700 1450 50  0001 L CNN "Manufacturer_Name"
F 9 "06034C104KAT2A" H 6700 1350 50  0001 L CNN "Manufacturer_Part_Number"
	1    6350 2000
	0    -1   -1   0   
$EndComp
$Comp
L Sensors_Pressure_Underwater:MS5837 U7
U 1 1 6196C9CA
P 5700 2900
F 0 "U7" H 5775 3025 50  0000 C CNN
F 1 "MS5837" H 5775 2934 50  0000 C CNN
F 2 "HighPressureSensorArray_Footprints:MS5837-30B" H 5750 2900 50  0001 C CNN
F 3 "" H 5750 2900 50  0001 C CNN
	1    5700 2900
	1    0    0    -1  
$EndComp
$Comp
L Sensors_Pressure_Underwater:MS5837 U6
U 1 1 6196C4FA
P 5700 2200
F 0 "U6" H 5775 2325 50  0000 C CNN
F 1 "MS5837" H 5775 2234 50  0000 C CNN
F 2 "HighPressureSensorArray_Footprints:MS5837-30B" H 5750 2200 50  0001 C CNN
F 3 "" H 5750 2200 50  0001 C CNN
	1    5700 2200
	1    0    0    -1  
$EndComp
$Comp
L Sensors_Pressure_Underwater:MS5837 U5
U 1 1 6196B9D1
P 5700 1500
F 0 "U5" H 5775 1625 50  0000 C CNN
F 1 "MS5837" H 5775 1534 50  0000 C CNN
F 2 "HighPressureSensorArray_Footprints:MS5837-30B" H 5750 1500 50  0001 C CNN
F 3 "" H 5750 1500 50  0001 C CNN
	1    5700 1500
	1    0    0    -1  
$EndComp
Wire Wire Line
	5450 3300 5450 3350
Wire Wire Line
	5400 3000 5400 3100
Wire Wire Line
	5450 3000 5400 3000
Wire Wire Line
	5350 2600 5350 2650
Wire Wire Line
	5450 2600 5350 2600
Wire Wire Line
	5300 2300 5300 2400
Wire Wire Line
	5450 2300 5300 2300
Wire Wire Line
	5250 1900 5250 1950
Wire Wire Line
	5450 1900 5250 1900
Wire Wire Line
	5450 1600 5200 1600
Wire Wire Line
	3250 3600 4400 3600
Wire Wire Line
	3250 3350 3250 3400
Wire Wire Line
	3600 3350 3250 3350
Wire Wire Line
	3200 3650 4300 3650
Wire Wire Line
	3200 3050 3200 3150
Wire Wire Line
	3600 3050 3200 3050
Wire Wire Line
	4600 3700 4600 3900
Wire Wire Line
	3150 3700 4600 3700
Wire Wire Line
	3150 2650 3150 2700
Wire Wire Line
	3600 2650 3150 2650
Wire Wire Line
	4500 3750 4500 3900
Wire Wire Line
	3100 3750 4500 3750
Wire Wire Line
	3100 2350 3100 2450
Wire Wire Line
	3600 2350 3100 2350
Wire Wire Line
	3050 1950 3050 2050
Wire Wire Line
	3000 1650 3000 1800
$Comp
L Sensors_Pressure_Underwater:MS5837 U3
U 1 1 619683A4
P 3850 2950
F 0 "U3" H 3925 3075 50  0000 C CNN
F 1 "MS5837" H 3925 2984 50  0000 C CNN
F 2 "HighPressureSensorArray_Footprints:MS5837-30B" H 3900 2950 50  0001 C CNN
F 3 "" H 3900 2950 50  0001 C CNN
	1    3850 2950
	1    0    0    -1  
$EndComp
$Comp
L SamacSys_Parts:06034C104KAT2A C3
U 1 1 6198AA09
P 4500 3500
F 0 "C3" V 4728 3628 50  0000 L CNN
F 1 "06034C104KAT2A" H 4795 3628 20  0000 L CNN
F 2 "HighPressureSensorArray_Footprints:CAPC1608X90N" H 4850 3550 50  0001 L CNN
F 3 "https://componentsearchengine.com/Datasheets/1/06031A100FAT2A.pdf" H 4850 3450 50  0001 L CNN
F 4 "Multilayer Ceramic Capacitors MLCC - SMD/SMT 4V .1uF X7R 0603 10%" H 4850 3350 50  0001 L CNN "Description"
F 5 "0.9" H 4850 3250 50  0001 L CNN "Height"
F 6 "581-06034C104KAT2A" H 4850 3150 50  0001 L CNN "Mouser Part Number"
F 7 "https://www.mouser.co.uk/ProductDetail/AVX/06034C104KAT2A?qs=EbDiPP9peV90W1IAXf%252BZmA%3D%3D" H 4850 3050 50  0001 L CNN "Mouser Price/Stock"
F 8 "AVX" H 4850 2950 50  0001 L CNN "Manufacturer_Name"
F 9 "06034C104KAT2A" H 4850 2850 50  0001 L CNN "Manufacturer_Part_Number"
	1    4500 3500
	0    -1   -1   0   
$EndComp
Wire Wire Line
	4250 3350 4250 3500
Wire Wire Line
	4250 3500 4500 3500
Wire Wire Line
	4250 3050 4250 3000
Wire Wire Line
	4250 3000 4500 3000
$Comp
L Interface_Expansion:PCA9548ADB U4
U 1 1 61980A16
P 4800 4300
F 0 "U4" H 4800 5381 50  0000 C CNN
F 1 "PCA9548ADB" H 4800 5290 50  0000 C CNN
F 2 "Package_SO:SSOP-24_5.3x8.2mm_P0.65mm" H 4800 3300 50  0001 C CNN
F 3 "http://www.ti.com/lit/ds/symlink/pca9548a.pdf" H 4850 4550 50  0001 C CNN
	1    4800 4300
	0    -1   -1   0   
$EndComp
Wire Wire Line
	5300 4700 5300 5450
Wire Wire Line
	5200 4700 5200 5350
Wire Wire Line
	5100 4700 5100 5250
$Comp
L Connector_Generic:Conn_01x08 J1
U 1 1 61992DA7
P 4850 5750
F 0 "J1" V 4814 5262 50  0000 R CNN
F 1 "Conn_01x08" V 4723 5262 50  0000 R CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x08_P2.54mm_Horizontal" H 4850 5750 50  0001 C CNN
F 3 "~" H 4850 5750 50  0001 C CNN
	1    4850 5750
	0    1    1    0   
$EndComp
$Comp
L Sensors_Pressure_Underwater:MS5837 U2
U 1 1 6196A989
P 3850 2250
F 0 "U2" H 3925 2375 50  0000 C CNN
F 1 "MS5837" H 3925 2284 50  0000 C CNN
F 2 "HighPressureSensorArray_Footprints:MS5837-30B" H 3900 2250 50  0001 C CNN
F 3 "" H 3900 2250 50  0001 C CNN
	1    3850 2250
	1    0    0    -1  
$EndComp
$Comp
L SamacSys_Parts:06034C104KAT2A C2
U 1 1 619832FB
P 4500 2700
F 0 "C2" V 4728 2828 50  0000 L CNN
F 1 "06034C104KAT2A" H 4795 2828 20  0000 L CNN
F 2 "HighPressureSensorArray_Footprints:CAPC1608X90N" H 4850 2750 50  0001 L CNN
F 3 "https://componentsearchengine.com/Datasheets/1/06031A100FAT2A.pdf" H 4850 2650 50  0001 L CNN
F 4 "Multilayer Ceramic Capacitors MLCC - SMD/SMT 4V .1uF X7R 0603 10%" H 4850 2550 50  0001 L CNN "Description"
F 5 "0.9" H 4850 2450 50  0001 L CNN "Height"
F 6 "581-06034C104KAT2A" H 4850 2350 50  0001 L CNN "Mouser Part Number"
F 7 "https://www.mouser.co.uk/ProductDetail/AVX/06034C104KAT2A?qs=EbDiPP9peV90W1IAXf%252BZmA%3D%3D" H 4850 2250 50  0001 L CNN "Mouser Price/Stock"
F 8 "AVX" H 4850 2150 50  0001 L CNN "Manufacturer_Name"
F 9 "06034C104KAT2A" H 4850 2050 50  0001 L CNN "Manufacturer_Part_Number"
	1    4500 2700
	0    -1   -1   0   
$EndComp
Wire Wire Line
	4250 2350 4250 2200
Wire Wire Line
	4250 2200 4500 2200
Wire Wire Line
	4250 2650 4250 2700
Wire Wire Line
	4250 2700 4500 2700
Wire Wire Line
	6700 1200 6700 1500
Wire Wire Line
	6700 1500 6350 1500
Connection ~ 6350 1500
Wire Wire Line
	4700 1200 4700 1550
Wire Wire Line
	4700 1550 4500 1550
Wire Wire Line
	4700 1550 4700 1700
Wire Wire Line
	4700 2200 4500 2200
Connection ~ 4700 1550
Connection ~ 4500 2200
Wire Wire Line
	4700 2200 4700 2400
Wire Wire Line
	4700 3000 4500 3000
Connection ~ 4700 2200
Connection ~ 4500 3000
Wire Wire Line
	6700 1500 6700 2250
Wire Wire Line
	6700 2250 6350 2250
Connection ~ 6700 1500
Connection ~ 6350 2250
Wire Wire Line
	6700 2250 6700 2950
Connection ~ 6700 2250
Connection ~ 6350 2950
Wire Wire Line
	6600 4300 6600 3450
Wire Wire Line
	6600 3450 6350 3450
Connection ~ 5800 4300
Connection ~ 6350 3450
Wire Wire Line
	6600 2750 6350 2750
Connection ~ 6600 3450
Connection ~ 6350 2750
Wire Wire Line
	6600 2750 6600 2000
Wire Wire Line
	6600 2000 6350 2000
Connection ~ 6600 2750
Connection ~ 6350 2000
Wire Wire Line
	6600 2000 6600 1400
Connection ~ 6600 2000
Connection ~ 4500 2700
Connection ~ 4500 3500
Wire Wire Line
	2600 1200 4700 1200
$Comp
L Device:R R1
U 1 1 61BA7CA2
P 2750 1800
F 0 "R1" V 2543 1800 50  0000 C CNN
F 1 "R" V 2634 1800 50  0000 C CNN
F 2 "SamacSys_Parts:CAPC1608X90N" V 2680 1800 50  0001 C CNN
F 3 "~" H 2750 1800 50  0001 C CNN
	1    2750 1800
	0    1    1    0   
$EndComp
Connection ~ 2600 1800
Wire Wire Line
	2600 1800 2600 1200
$Comp
L Device:R R2
U 1 1 61BADD2E
P 2750 2050
F 0 "R2" V 2543 2050 50  0000 C CNN
F 1 "R" V 2634 2050 50  0000 C CNN
F 2 "SamacSys_Parts:CAPC1608X90N" V 2680 2050 50  0001 C CNN
F 3 "~" H 2750 2050 50  0001 C CNN
	1    2750 2050
	0    1    1    0   
$EndComp
Connection ~ 2600 2050
Wire Wire Line
	2600 2050 2600 1800
Wire Wire Line
	2900 1800 3000 1800
Connection ~ 3000 1800
Wire Wire Line
	2900 2050 3050 2050
Connection ~ 3050 2050
Wire Wire Line
	3050 2050 3050 3800
$Comp
L Device:R R3
U 1 1 61BBADA9
P 2750 2450
F 0 "R3" V 2543 2450 50  0000 C CNN
F 1 "R" V 2634 2450 50  0000 C CNN
F 2 "SamacSys_Parts:CAPC1608X90N" V 2680 2450 50  0001 C CNN
F 3 "~" H 2750 2450 50  0001 C CNN
	1    2750 2450
	0    1    1    0   
$EndComp
Connection ~ 2600 2450
Wire Wire Line
	2600 2450 2600 2050
Wire Wire Line
	2600 4300 2600 3400
$Comp
L Device:R R4
U 1 1 61BBC7DF
P 2750 2700
F 0 "R4" V 2543 2700 50  0000 C CNN
F 1 "R" V 2634 2700 50  0000 C CNN
F 2 "SamacSys_Parts:CAPC1608X90N" V 2680 2700 50  0001 C CNN
F 3 "~" H 2750 2700 50  0001 C CNN
	1    2750 2700
	0    1    1    0   
$EndComp
Connection ~ 2600 2700
Wire Wire Line
	2600 2700 2600 2450
$Comp
L Device:R R6
U 1 1 61BBD55B
P 2750 3400
F 0 "R6" V 2543 3400 50  0000 C CNN
F 1 "R" V 2634 3400 50  0000 C CNN
F 2 "SamacSys_Parts:CAPC1608X90N" V 2680 3400 50  0001 C CNN
F 3 "~" H 2750 3400 50  0001 C CNN
	1    2750 3400
	0    1    1    0   
$EndComp
Connection ~ 2600 3400
Wire Wire Line
	2600 2700 2600 3150
$Comp
L Device:R R5
U 1 1 61BBDAEA
P 2750 3150
F 0 "R5" V 2543 3150 50  0000 C CNN
F 1 "R" V 2634 3150 50  0000 C CNN
F 2 "SamacSys_Parts:CAPC1608X90N" V 2680 3150 50  0001 C CNN
F 3 "~" H 2750 3150 50  0001 C CNN
	1    2750 3150
	0    1    1    0   
$EndComp
Connection ~ 2600 3150
Wire Wire Line
	2600 3150 2600 3400
Wire Wire Line
	2900 2450 3100 2450
Connection ~ 3100 2450
Wire Wire Line
	3100 2450 3100 3750
Wire Wire Line
	2900 2700 3150 2700
Connection ~ 3150 2700
Wire Wire Line
	3150 2700 3150 3700
Wire Wire Line
	2900 3150 3200 3150
Connection ~ 3200 3150
Wire Wire Line
	3200 3150 3200 3650
Wire Wire Line
	2900 3400 3250 3400
Connection ~ 3250 3400
Wire Wire Line
	3250 3400 3250 3600
Connection ~ 4750 2700
Wire Wire Line
	4750 2700 4500 2700
Wire Wire Line
	4750 1400 4750 2050
Wire Wire Line
	4500 2050 4750 2050
Connection ~ 4750 2050
Wire Wire Line
	4750 2050 4750 2700
Wire Wire Line
	4750 2700 4750 3500
Wire Wire Line
	4750 3500 4500 3500
$Comp
L Device:R R7
U 1 1 61C2CCF4
P 5000 1700
F 0 "R7" V 4793 1700 50  0000 C CNN
F 1 "R" V 4884 1700 50  0000 C CNN
F 2 "SamacSys_Parts:CAPC1608X90N" V 4930 1700 50  0001 C CNN
F 3 "~" H 5000 1700 50  0001 C CNN
	1    5000 1700
	0    1    1    0   
$EndComp
$Comp
L Device:R R8
U 1 1 61C2E086
P 5000 1950
F 0 "R8" V 4793 1950 50  0000 C CNN
F 1 "R" V 4884 1950 50  0000 C CNN
F 2 "SamacSys_Parts:CAPC1608X90N" V 4930 1950 50  0001 C CNN
F 3 "~" H 5000 1950 50  0001 C CNN
	1    5000 1950
	0    1    1    0   
$EndComp
$Comp
L Device:R R9
U 1 1 61C30DA8
P 5000 2400
F 0 "R9" V 4793 2400 50  0000 C CNN
F 1 "R" V 4884 2400 50  0000 C CNN
F 2 "SamacSys_Parts:CAPC1608X90N" V 4930 2400 50  0001 C CNN
F 3 "~" H 5000 2400 50  0001 C CNN
	1    5000 2400
	0    1    1    0   
$EndComp
$Comp
L Device:R R10
U 1 1 61C30DAE
P 5000 2650
F 0 "R10" V 4793 2650 50  0000 C CNN
F 1 "R" V 4884 2650 50  0000 C CNN
F 2 "SamacSys_Parts:CAPC1608X90N" V 4930 2650 50  0001 C CNN
F 3 "~" H 5000 2650 50  0001 C CNN
	1    5000 2650
	0    1    1    0   
$EndComp
$Comp
L Device:R R11
U 1 1 61C37EF4
P 5000 3100
F 0 "R11" V 4793 3100 50  0000 C CNN
F 1 "R" V 4884 3100 50  0000 C CNN
F 2 "SamacSys_Parts:CAPC1608X90N" V 4930 3100 50  0001 C CNN
F 3 "~" H 5000 3100 50  0001 C CNN
	1    5000 3100
	0    1    1    0   
$EndComp
$Comp
L Device:R R12
U 1 1 61C37EFA
P 5000 3350
F 0 "R12" V 4793 3350 50  0000 C CNN
F 1 "R" V 4884 3350 50  0000 C CNN
F 2 "SamacSys_Parts:CAPC1608X90N" V 4930 3350 50  0001 C CNN
F 3 "~" H 5000 3350 50  0001 C CNN
	1    5000 3350
	0    1    1    0   
$EndComp
Wire Wire Line
	5150 1700 5200 1700
Wire Wire Line
	5150 1950 5250 1950
Wire Wire Line
	5150 2400 5300 2400
Wire Wire Line
	5150 2650 5350 2650
Wire Wire Line
	5150 3100 5400 3100
Wire Wire Line
	5150 3350 5450 3350
Wire Wire Line
	4750 1400 6600 1400
Wire Wire Line
	4700 1200 6700 1200
Connection ~ 4700 1200
Wire Wire Line
	4850 1700 4700 1700
Connection ~ 4700 1700
Wire Wire Line
	4700 1700 4700 1950
Wire Wire Line
	4850 1950 4700 1950
Connection ~ 4700 1950
Wire Wire Line
	4700 1950 4700 2200
Wire Wire Line
	4850 2400 4700 2400
Connection ~ 4700 2400
Wire Wire Line
	4850 2650 4700 2650
Wire Wire Line
	4700 2400 4700 2650
Connection ~ 4700 2650
Wire Wire Line
	4700 2650 4700 3000
Wire Wire Line
	4850 3100 4700 3100
Wire Wire Line
	4700 3100 4700 3000
Connection ~ 4700 3000
Wire Wire Line
	4850 3350 4700 3350
Wire Wire Line
	4700 3350 4700 3100
Connection ~ 4700 3100
Wire Wire Line
	5300 2400 5300 3700
Wire Wire Line
	5300 3700 5100 3700
Connection ~ 5300 2400
Wire Wire Line
	5350 2650 5350 3750
Wire Wire Line
	5200 3750 5200 3900
Connection ~ 5350 2650
Wire Wire Line
	5400 3100 5400 3800
Connection ~ 5400 3100
Wire Wire Line
	5800 4300 6600 4300
Wire Wire Line
	4200 4700 4200 5450
Wire Wire Line
	4450 5250 4450 5550
Wire Wire Line
	4600 4700 4600 5300
Wire Wire Line
	4450 5250 5100 5250
Wire Wire Line
	4100 4700 4100 5500
Wire Wire Line
	4100 5500 4550 5500
Wire Wire Line
	4550 5500 4550 5550
Wire Wire Line
	4200 5450 4650 5450
Wire Wire Line
	4650 5450 4650 5550
Wire Wire Line
	5150 5300 5150 5550
Wire Wire Line
	4600 5300 5150 5300
Wire Wire Line
	5800 5550 5200 5550
Wire Wire Line
	5200 5550 5200 5500
Wire Wire Line
	5200 5500 4850 5500
Wire Wire Line
	4850 5500 4850 5550
Wire Wire Line
	4950 5450 4950 5550
Wire Wire Line
	4950 5450 5300 5450
Wire Wire Line
	4950 5350 4950 5400
Wire Wire Line
	4950 5400 5050 5400
Wire Wire Line
	5050 5400 5050 5550
Connection ~ 4500 2050
Connection ~ 4500 1550
Wire Wire Line
	4250 2050 4500 2050
Wire Wire Line
	4250 1950 4250 2050
Wire Wire Line
	4250 1550 4500 1550
Wire Wire Line
	4250 1650 4250 1550
$Comp
L SamacSys_Parts:06034C104KAT2A C1
U 1 1 6198B603
P 4500 2050
F 0 "C1" V 4728 2178 50  0000 L CNN
F 1 "06034C104KAT2A" H 4795 2178 20  0000 L CNN
F 2 "HighPressureSensorArray_Footprints:CAPC1608X90N" H 4850 2100 50  0001 L CNN
F 3 "https://componentsearchengine.com/Datasheets/1/06031A100FAT2A.pdf" H 4850 2000 50  0001 L CNN
F 4 "Multilayer Ceramic Capacitors MLCC - SMD/SMT 4V .1uF X7R 0603 10%" H 4850 1900 50  0001 L CNN "Description"
F 5 "0.9" H 4850 1800 50  0001 L CNN "Height"
F 6 "581-06034C104KAT2A" H 4850 1700 50  0001 L CNN "Mouser Part Number"
F 7 "https://www.mouser.co.uk/ProductDetail/AVX/06034C104KAT2A?qs=EbDiPP9peV90W1IAXf%252BZmA%3D%3D" H 4850 1600 50  0001 L CNN "Mouser Price/Stock"
F 8 "AVX" H 4850 1500 50  0001 L CNN "Manufacturer_Name"
F 9 "06034C104KAT2A" H 4850 1400 50  0001 L CNN "Manufacturer_Part_Number"
	1    4500 2050
	0    -1   -1   0   
$EndComp
$Comp
L Sensors_Pressure_Underwater:MS5837 U1
U 1 1 6196B0CE
P 3850 1550
F 0 "U1" H 3925 1675 50  0000 C CNN
F 1 "MS5837" H 3925 1584 50  0000 C CNN
F 2 "HighPressureSensorArray_Footprints:MS5837-30B" H 3900 1550 50  0001 C CNN
F 3 "" H 3900 1550 50  0001 C CNN
	1    3850 1550
	1    0    0    -1  
$EndComp
Wire Wire Line
	3600 1650 3000 1650
Wire Wire Line
	3050 1950 3600 1950
Wire Wire Line
	6600 3450 6600 2750
Wire Wire Line
	6700 2950 6350 2950
Wire Wire Line
	4300 3650 4300 3900
Wire Wire Line
	3000 3900 3450 3900
Wire Wire Line
	3450 3900 3450 3550
Wire Wire Line
	3450 3550 4700 3550
Wire Wire Line
	4700 3550 4700 3900
Wire Wire Line
	3000 1800 3000 3900
Wire Wire Line
	4400 3600 4400 3900
Wire Wire Line
	3050 3800 4800 3800
Wire Wire Line
	4800 3800 4800 3900
Connection ~ 5450 3350
Wire Wire Line
	5450 3350 5450 3850
Wire Wire Line
	5200 3750 5350 3750
Wire Wire Line
	5450 3850 5000 3850
Wire Wire Line
	5000 3850 5000 3900
Wire Wire Line
	5400 3800 4900 3800
Wire Wire Line
	4900 3800 4900 3900
Wire Wire Line
	5100 3700 5100 3900
Wire Wire Line
	5200 3670 5240 3670
Wire Wire Line
	5240 3670 5240 3730
Wire Wire Line
	5240 3730 5300 3730
Wire Wire Line
	5300 3730 5300 3900
Wire Wire Line
	5200 1600 5200 1700
Connection ~ 5200 1700
Wire Wire Line
	5200 1700 5200 3670
Wire Wire Line
	5400 3900 5400 3830
Wire Wire Line
	5400 3830 5430 3830
Wire Wire Line
	5430 3830 5430 3570
Wire Wire Line
	5430 3570 5250 3570
Wire Wire Line
	5250 3570 5250 1950
Connection ~ 5250 1950
$Comp
L Device:C C7
U 1 1 61ADC204
P 5650 4960
F 0 "C7" V 5902 4960 50  0000 C CNN
F 1 "C" V 5811 4960 50  0000 C CNN
F 2 "SamacSys_Parts:CAPC1608X90N" H 5688 4810 50  0001 C CNN
F 3 "~" H 5650 4960 50  0001 C CNN
	1    5650 4960
	0    -1   -1   0   
$EndComp
Wire Wire Line
	5800 4300 5800 4960
Wire Wire Line
	2600 4300 3870 4300
$Comp
L Device:C C8
U 1 1 61B060DB
P 5650 5230
F 0 "C8" V 5902 5230 50  0000 C CNN
F 1 "C" V 5811 5230 50  0000 C CNN
F 2 "SamacSys_Parts:CAPC1005X55N" H 5688 5080 50  0001 C CNN
F 3 "~" H 5650 5230 50  0001 C CNN
	1    5650 5230
	0    -1   -1   0   
$EndComp
Connection ~ 5800 4960
Wire Wire Line
	5800 4960 5800 5230
Connection ~ 5800 5230
Wire Wire Line
	5800 5230 5800 5550
Wire Wire Line
	5200 5350 4950 5350
Wire Wire Line
	4750 5280 5500 5280
Wire Wire Line
	5500 5280 5500 5230
Wire Wire Line
	4750 5280 4750 5550
Wire Wire Line
	5500 5230 5500 4960
Connection ~ 5500 5230
Wire Wire Line
	5500 4960 3870 4960
Wire Wire Line
	3870 4960 3870 4300
Connection ~ 5500 4960
Connection ~ 3870 4300
Wire Wire Line
	3870 4300 3900 4300
$EndSCHEMATC
