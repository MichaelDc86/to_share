"""Модуль обработки метрики"""
import os
import typing as t

import pandas as pd
import matplotlib.pyplot as plt


class DropOutliers:
    """Объект манипуляций с метриками"""
    window_mean: int
    window_std: int
    window_def: int
    n_std: int
    step_back: int
    df: pd.DataFrame

    def __init__(self):
        """Параметры скользящих средних подбирал руками"""
        self.window_mean = 100
        self.window_std = 100
        self.window_def = 100
        self.n_std = 2
        self.step_back = - 50
        self.df = self.get_df()

    def run(self, iter_count: int = 7):
        """
        Запускает очистку выбросов
        Args:
            iter_count: количество итераций очистки
        """
        res_col = 'y'
        plt.plot(self.df['x'], self.df[res_col])
        for i in range(iter_count):
            res_col = self.glide(i, res_col)
        plt.plot(self.df['x'], self.df[res_col])
        plt.show()

    def get_df(self):
        """Загружает df из файла"""
        assert os.path.exists(os.path.join(os.getcwd(), 'metrics.txt')), 'Укажите файл с данными'
        df = pd.read_json('metrics.txt')
        df.rename(columns={0: 'y', 1: 'x'}, inplace=True)
        return df

    def glide(self, num_filtration: int, data_col: str) -> str:
        """
        Сглаживает выбросы
        Args:
            data_col: колонка с исходными данными
            num_filtration: номер текущей итерациии сглаживания

        Returns: имя колонки со сглаженными данными

        """
        roll_mean = 'roll_mean' + str(num_filtration)
        roll_std = 'roll_std' + str(num_filtration)
        roll_fill = 'roll_fill' + str(num_filtration)
        roll_filtered = 'roll_filtered' + str(num_filtration)

        self.df[roll_mean] = self.df[data_col].rolling(self.window_mean).mean()
        self.df[roll_std] = self.df[data_col].rolling(self.window_std).std()
        self.df[roll_fill] = self.df[data_col].rolling(self.window_def).mean()

        self.df[roll_filtered] = self.roll_sort(
            self.df[data_col], self.df[roll_mean], self.df[roll_std], self.df[roll_fill])

        return roll_filtered

    def roll_sort(self, data: pd.Series, means: pd.Series, stds: pd.Series,
                  high_means: pd.Series) -> t.List:
        """
        Сглаживает по скользящим средним
        Args:
            data: исходные данные
            means: скользящие средние
            stds: скользящие отклонения
            high_means: скользящие редние с большим окном

        Returns: список сглаженных значений

        """
        res = []
        for i, val in enumerate(data):
            if val < means[i] - self.n_std * stds[i] or val > means[i] + self.n_std * stds[i]:
                if self.step_back < i < (len(high_means) - abs(self.step_back)):
                    res.append(high_means[i - self.step_back])
                else:
                    res.append(high_means[i])
            else:
                res.append(val)
        return res


if __name__ == '__main__':
    solution = DropOutliers()
    solution.run()
