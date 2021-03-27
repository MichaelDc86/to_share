"""Module for fuel calculations"""
from decimal import Decimal
from enum import Enum
from typing import Tuple, List


class PlanetGravity(Enum):
    """Class to store gravity constants"""
    earth: Decimal = Decimal('9.807')
    moon: Decimal = Decimal('1.620')
    mars: Decimal = Decimal('3.711')


class SpaceProgram:
    """
    Space Program class
    Example:
        Program Apollo 11
        apollo_11 = SpaceProgram(route=[('earth', 'moon'), ('moon', 'earth')], ship_weight=28801)
        route -> launch from Earth, land on Moon, then back(launch from Moon and land on Earth),
        ship_weight -> weight of equipment
    """
    launch_constant: int = 33
    land_constant: int = 42
    launch_gravity_constant: Decimal = Decimal('0.042')
    land_gravity_constant: Decimal = Decimal('0.033')
    route: List[Tuple[str, str]]
    ship_weight: int

    def __init__(self, route: List[Tuple[str, str]], ship_weight: int) -> None:
        """
        Constructor method
        Args:
            route: List[Tuple[str]] - journey route
            ship_weight: int - weight of equipment
        """
        self.route = route
        self.ship_weight = ship_weight
        self.gravity_info = PlanetGravity

    def calculate_fuel(self) -> int:
        """
        Method to calculate sufficient fuel for the program
        Returns:
            int - sufficient fuel for the program
        """
        gravity_dict = {
            'earth': self.gravity_info.earth.value,
            'moon': self.gravity_info.moon.value,
            'mars': self.gravity_info.mars.value,
        }
        route = []
        for item in self.route:
            launch = gravity_dict.get(item[0])
            land = gravity_dict.get(item[1])
            if all((launch, land)):
                route.append((launch, land))
            else:
                return 0
        return self._amount_calculate(mass=self.ship_weight, route=route)

    def _amount_calculate(
            self, mass: int, route: List[Tuple[Decimal, Decimal]]) -> int:
        """
        Method to calculate the fuel amount for journey from one planet to another and back.
        Args:
            mass: int - mass of the spaceship
            route: Tuple[Decimal, Decimal] - gravity characteristics for trip

        Returns:
            int - sufficient fuel for travel
        """
        travel_routes = []
        for item in route:
            travel_routes.append((item[0], self.launch_gravity_constant, self.launch_constant))
            travel_routes.append((item[1], self.land_gravity_constant, self.land_constant))

        tmp_mass = mass
        # reverse travel_routes because with init mass ship will finish trip and max mass will be at start
        for gravity, gravity_constant, direction_constant in travel_routes[::-1]:
            tmp_fuel_mass = self._count_fuel_per_mass(
                mass=tmp_mass,
                gravity=gravity,
                gravity_constant=gravity_constant,
                direction_constant=direction_constant)
            tmp_mass += tmp_fuel_mass

        return tmp_mass - mass

    @staticmethod
    def _count_fuel_per_mass(
            mass: int, gravity: Decimal, gravity_constant: Decimal, direction_constant: int) -> int:
        """
        Calculate fuel using simple formula
        Args:
            direction_constant: Decimal - constant
            gravity_constant: Decimal - constant
            gravity: Decimal - constant
            mass: int - mass of the spaceship

        Returns:
            Decimal - fuel weight
        """
        fuel_mass = 0
        tmp_mass = mass
        while True:
            tmp_mass = int(tmp_mass * gravity * gravity_constant - direction_constant)  # int because round down
            if tmp_mass <= 0:
                break
            fuel_mass += tmp_mass

        return fuel_mass


def print_examples() -> None:
    """
    Prints examples given in the task
    """
    apollo_11 = SpaceProgram(route=[('earth', 'moon'), ('moon', 'earth')], ship_weight=28801)
    mars = SpaceProgram(route=[('earth', 'mars'), ('mars', 'earth')], ship_weight=14606)
    passenger = SpaceProgram(route=[('earth', 'moon'), ('moon', 'mars'), ('mars', 'earth')], ship_weight=75432)
    answer_apollo_11 = apollo_11.calculate_fuel()
    answer_mars = mars.calculate_fuel()
    answer_passenger = passenger.calculate_fuel()
    print(f'Apollo_11 Space journey will take {answer_apollo_11} kg of fuel! --> 51898')
    print(f'Mars Space journey will take {answer_mars} kg of fuel! --> 33388')
    print(f'Passenger Space journey will take {answer_passenger} kg of fuel! --> 212161')


def app() -> None:
    """
    Interacts with user, builds the SpaceProgram and calculates sufficient fuel for travel
    """
    input_dict = {
        '1': 'earth',
        '2': 'moon',
        '3': 'mars',
    }
    print('*********************')
    print('Specify your space journey!')
    while True:
        ship_weight = input('Print your equipment/spaceship weight in kg: ')
        try:
            ship_weight = int(ship_weight)
            break
        except ValueError:
            print(f'Value {ship_weight} is not an integer. Please input integer value of your ship weight!')
    route = []
    while True:
        while True:
            print('Choose start planet:\n1 - Earth\n2 - Moon\n3 - Mars')
            launch = input('Print the number from the list above:  ')
            launch = input_dict.get(launch)
            if launch:
                break
            print('Please choose from listed planets!(digits 1, 2 or 3)')
        while True:
            print('Choose destination planet:\n1 - Earth\n2 - Moon\n3 - Mars')
            land = input('Print the number from the list above:  ')
            land = input_dict.get(land)
            if land:
                break
            print('Please choose from listed planets!(digits 1, 2 or 3)')
        route.append((launch, land))
        stop = input('Do you want to add new trip to your route? Print Y - yes, N - no: ')
        if stop.lower() != 'y':
            break
    user_program = SpaceProgram(route=route, ship_weight=ship_weight)
    answer_user_program = user_program.calculate_fuel()
    print(f'Your Space journey will take {answer_user_program} kg of fuel!')


if __name__ == '__main__':
    print_examples()
    app()
