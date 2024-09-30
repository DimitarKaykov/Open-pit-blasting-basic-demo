# Rockmass properties / Свойства на скалния масив
rm_density = 2.75         # Rockmass density (Плътност на скалата от масива), t/m³
rm_rock_factor = 8.19     # Rock factor (Коефициент, отчитащ якостните свойства на скалата и състоянието на масива)
rm_swell_factor = 1.4     # Swell factor (Коефициент на разбухване)

# Blast panel geometric features / Геометрични характеристики на взривяваното поле
bp_height = 15            # Bench height (Височина на стъпалото), m
bp_width = 30             # Blast panel width (Широчина на взривяваното поле), m
bp_length = 100           # Blast panel length (Дължина на взривяваното поле), m
bp_slope_angle = 65       # Bench slope angle (Ъгъл на откоса на стъпалото), m

# Explosive properties / Свойства на взривното вещество
expl_density = 1.1       # Explosive density (Плътност на взривното вещество), g/dm³ (t/m³)
expl_rws = 116            # Relative weight strength (Относителна тегловна енергия)
expl_price = 1.51         # Explosive price (Цена на взривното вещество), EUR/kg

# Energy sources for mining operation / Източници на енергия използвана в минния обект
energy_diesel_price = 1.6  # Diesel price (Цена на гориво - дизел), EUR/l

# Blast panel drillhole features / Параметри на взривните сондажи
bp_dh_diameter = 200      # Drillhole diameter (Диаметър на взривните сондажи), mm
bp_dh_dev = 0.1         # Drillhole location deviation (Отклонение на устието на сондажите от проектното), m

# Drilling equipment specs / Параметри на сондата
drill_h_rate = 25                                   # Drilling rate (Скорост на пробиване), m/h
drill_h_fuel = 62.31                                # Drilling fuel consumption per hour, (Разход на гориво при 1 h сондиране) l/h
drill_h_costs = drill_h_fuel * energy_diesel_price  # Drilling costs (Разходи за пробиване), EUR/h

# Excavator equipment specs / Параметри на багера
loader_bucket_vol = 27.5                                # Bucket volume (Геометричен обем на кофата на багера), m³
loader_s_cycle = 30                                     # Excavator cycle time (Цикъл на работа на багера), s
loader_h_fuel = 225.39                                  # Excavator fuel consumption per hour
loader_h_costs = loader_h_fuel * energy_diesel_price    # Excavator costs (Разходи за работа на багера), EUR/h

# Truck equipment specs / Параметри на автосамосвала
truck_cap_vol = 130                                    # Truck capacity volume (Вместимост на коша на автосамосвала), m³
truck_cap_t = 320                                      # Truck payload capacity (Товароносимост на автосамосвала), t
truck_min_haul = 15                                    # Truck haul time (Време на курса на автосамосвала), min
truck_h_fuel = 311.74                                  # Truck fuel consumption per hour
truck_h_costs = truck_h_fuel * energy_diesel_price     # Truck haul costs (Разходи за транспорт), EUR/h

