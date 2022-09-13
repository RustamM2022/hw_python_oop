from typing import Dict, Tuple
from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (f"Тип тренировки: {self.training_type}; "
                f"Длительность: {self.duration:.3f} ч.; "
                f"Дистанция: {self.distance:.3f} км; "
                f"Ср. скорость: {self.speed:.3f} км/ч; "
                f"Потрачено ккал: {self.calories:.3f}.")


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        self.action: str = action
        self.duration: str = duration
        self.weight: str = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        get_distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return get_distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        get_mean_speed: float = self.get_distance() / self.duration
        return get_mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
              "Определите get_spent_calories в %s."
              % (self.__class__.__name__))

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Получить количество потраченных калорий за тренировку"""
        coeff_calorie_1: int = 18
        coeff_calorie_2: int = 20
        MIN_H: int = 60
        get_spent_calories: float = ((coeff_calorie_1 * self.get_mean_speed()
                                     - coeff_calorie_2)
                                     * self.weight / self.M_IN_KM
                                     * MIN_H * self.duration)
        return get_spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height: str = height

    def get_spent_calories(self) -> float:
        """Получить количество потраченных калорий за тренировку"""
        coeff_calorie_1: float = 0.035
        coeff_calorie_2: float = 0.029
        MIN_H: int = 60

        get_spent_calories: float = ((coeff_calorie_1 * self.weight
                                     + (self.get_mean_speed()
                                        ** 2 // self.height)
                                     * coeff_calorie_2 * self.weight)
                                     * MIN_H * self.duration)
        return get_spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool: str = length_pool
        self.count_pool: str = count_pool

    """Получить среднюю скорость движения."""
    def get_mean_speed(self) -> float:
        get_mean_speed: float = (self.length_pool * self.count_pool
                                 / self.M_IN_KM / self.duration)
        return get_mean_speed

    """Получить количество потраченных калорий за тренировку"""
    def get_spent_calories(self) -> float:
        coeff_calorie_1: float = 1.1
        coeff_calorie_2: float = 2
        get_spent_calories: float = ((self.get_mean_speed() + coeff_calorie_1)
                                     * coeff_calorie_2 * self.weight)
        return get_spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    t_training: Dict[str, Tuple[float, ...]] = {"SWM": Swimming,
                                                "RUN": Running,
                                                "WLK": SportsWalking}
    type_training = t_training.get(workout_type, None)
    if type_training is None:
        raise ValueError(f"Неизвестная тренировка {workout_type}.")
    else:
        return t_training[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    try:
        for workout_type, data in packages:
            training = read_package(workout_type, data)
            main(training)
    except ValueError:
        print(f"Неизвестная тренировка {workout_type}.")
