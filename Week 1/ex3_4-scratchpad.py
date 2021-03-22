def calc_wind_chill(temp, windSpeed):
    # check error conditions first
    # calc is only valid if temperature is less than 10 degrees
    if (temp > 10):
        print("ERROR: Ensure that temperature is less than or equal to 10 Celsius")
        exit()
    # cal is only valid if wind speed is above 4.8
    if (windSpeed < 4.8):
        print("ERROR: Ensure that wind speed greater than 4.8 km/h")
        exit()
    
    # formula for windchill 
    v = windSpeed**0.16

    chillFactor = 13.12 + 0.6215 * temp - 11.37 * v + 0.3965 * temp * v
    return chillFactor

def convertToKMH(mphSpeed):
    return mphSpeed * 1.609

# test values
temperature = 5
windSpeed = convertToKMH(20) 

# call the fuction to calculate wind chill
wind_chill = calc_wind_chill(temperature, windSpeed)

# print a string out
print("The wind chill factor is ", wind_chill, " Celsius")

# print a pretty string out
print("The wind chill factor is ", round(wind_chill, 2), " Celsius")