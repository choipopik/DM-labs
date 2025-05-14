from math import comb

# Размеры сетки
horizontal_steps = 19  # R - шаги вправо
vertical_steps = 16    # U - шаги вверх

# =============================
# Задача 1: Все кратчайшие пути  // Порядок этих шагов может быть любым, поэтому число таких путей равно числу перестановок строки из 35 символов
# =============================
total_paths = comb(horizontal_steps + vertical_steps, horizontal_steps) #Можно было бы использовать comb(35, 19) — 
                                                                        #это то же самое, просто считали бы, где будут шаги "вправо" (R) .
print(f"Общее количество кратчайших путей: {total_paths}")

# =============================
# Задача 2: Пути без двух U подряд
# =============================

def count_restricted_paths(h_steps, v_steps):
    # dp_r[i][j]: пути с i R и j U, заканчивающиеся на R
    # dp_u[i][j]: пути с i R и j U, заканчивающиеся на U
    dp_r = [[0] * (v_steps + 1) for _ in range(h_steps + 1)]
    dp_u = [[0] * (v_steps + 1) for _ in range(h_steps + 1)]

    # Начальное состояние: пустой путь
    dp_r[0][0] = 1  # начинаем условно с R

    for i in range(h_steps + 1):
        for j in range(v_steps + 1):
            if i == 0 and j == 0:
                continue
            # Добавляем шаг R (можно всегда, если есть остаток R)
            if i > 0:
                dp_r[i][j] = dp_r[i-1][j] + dp_u[i-1][j]
            # Добавляем шаг U (только если предыдущий был R)
            if j > 0:
                dp_u[i][j] = dp_r[i][j-1]

    return dp_r[h_steps][v_steps] + dp_u[h_steps][v_steps]


# Вычисляем ответ для второй задачи
restricted_paths = count_restricted_paths(horizontal_steps, vertical_steps)
print(f"Количество путей без двух U подряд: {restricted_paths}")