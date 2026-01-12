import argparse
import sys
from typing import List, Union


def read_numbers(file_path: str) -> List[float]:
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
        # Разбиваем содержимое на числа, игнорируя пустые строки
        numbers = []
        for item in content.split():
            try:
                # Пробуем преобразовать в float (работает и с целыми, и с дробными)
                num = float(item)
                numbers.append(num)
            except ValueError:
                raise ValueError(f"Некорректное значение в файле: '{item}'")
        
        if not numbers:
            raise ValueError("Файл не содержит чисел")
            
        return numbers
        
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл не найден: {file_path}")
    except PermissionError:
        raise PermissionError(f"Нет доступа к файлу: {file_path}")


def calculate(data: List[float], operation: str) -> Union[float, int]:
    if not data:
        raise ValueError("Список чисел пуст")
    
    operation = operation.lower()
    
    if operation == 'sum':
        return sum(data)
    
    elif operation == 'avg':
        return sum(data) / len(data)
    
    elif operation == 'min':
        return min(data)
    
    elif operation == 'max':
        return max(data)
    
    else:
        raise ValueError(f"Неподдерживаемая операция: {operation}")


def format_result(result: Union[float, int]) -> str:
    # Если результат целый, выводим без десятичной части
    if isinstance(result, int) or result.is_integer():
        return str(int(result))
    else:
        # Округляем до 2 знаков после запятой
        return f"{result:.2f}"


def main():
    """Основная функция программы."""
    # Создаем парсер аргументов командной строки
    parser = argparse.ArgumentParser(
        description='TaskCalc - калькулятор для обработки чисел из файла',
        epilog='Пример использования: python taskcalc.py numbers.txt sum',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Добавляем аргументы
    parser.add_argument(
        'file',
        type=str,
        help='Путь к файлу с числами (формат: числа через пробел или с новой строки)'
    )
    
    parser.add_argument(
        'operation',
        type=str,
        choices=['sum', 'avg', 'min', 'max'],
        help='Операция: sum (сумма), avg (среднее), min (минимум), max (максимум)'
    )
    
    # Дополнительные опциональные аргументы
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Подробный вывод (показывает считанные числа)'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='TaskCalc 1.0.0'
    )
    
    # Парсим аргументы
    args = parser.parse_args()
    
    try:
        # Читаем числа из файла
        numbers = read_numbers(args.file)
        
        if args.verbose:
            print(f"Считано {len(numbers)} чисел: {numbers}")
            print(f"Выполняется операция: {args.operation}")
        
        # Выполняем операцию
        result = calculate(numbers, args.operation)
        
        # Форматируем и выводим результат
        formatted_result = format_result(result)
        
        # Определяем русское название операции для вывода
        operation_names = {
            'sum': 'Сумма',
            'avg': 'Среднее значение',
            'min': 'Минимальное значение',
            'max': 'Максимальное значение'
        }
        
        op_name = operation_names.get(args.operation, args.operation)
        print(f"{op_name}: {formatted_result}")
        
    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()