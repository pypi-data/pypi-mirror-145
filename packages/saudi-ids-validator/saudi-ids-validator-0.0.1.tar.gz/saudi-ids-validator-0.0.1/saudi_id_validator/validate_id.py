def _eastern_to_western_numbers(nums):
    western = "٠١٢٣٤٥٦٧٨٩"
    result = ""
    for num in nums:
        if num in western:
            result += str(western.index(num))
        else:
            result += num
    return result


def _evaluate_digit(current_digit):
    if current_digit < 5:
        return current_digit * 2
    num_str = str(current_digit * 2)
    return int(num_str[0]) + int(num_str[1])


def is_valid_saudi_id(saudi_id):
    string_id = _eastern_to_western_numbers(str(saudi_id)).strip()

    if len(string_id) != 10 or (not string_id.isdigit()) or (not string_id[0] in "12"):
        return False

    numbers_sum = 0
    for idx in range(0, len(string_id)):
        if idx % 2 == 0:
            numbers_sum += _evaluate_digit(int(string_id[idx]))
        else:
            numbers_sum += int(string_id[idx])

    return numbers_sum % 10 == 0
