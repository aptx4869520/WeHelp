# Task 1

def func1(name):
    positions = {
        "悟空": (0, 0),
        "特南克斯": (1, -2),
        "辛巴": (-3, 3),
        "丁滿": (-1, 4),
        "貝吉塔": (-4, -1),
        "弗利沙": (4, -1)
    }

    sides = {
        "悟空": "left",
        "特南克斯": "left",
        "辛巴": "left",
        "丁滿": "right",
        "貝吉塔": "left",
        "弗利沙": "right"
    }

    x1, y1 = positions[name]

    min_distance = None
    closest = []

    max_distance = None
    farthest = []

    for other_name in positions:
        if other_name != name:
            x2, y2 = positions[other_name]

            distance = abs(x1 - x2) + abs(y1 - y2)

            if sides[name] != sides[other_name]:
                distance = distance + 2

            if min_distance == None or distance < min_distance:
                min_distance = distance
                closest = [other_name]
            elif distance == min_distance:
                closest.append(other_name)

            if max_distance == None or distance > max_distance:
                max_distance = distance
                farthest = [other_name]
            elif distance == max_distance:
                farthest.append(other_name)

    if len(farthest) > 1 or len(closest) > 1:
        separator = ";"
    else:
     separator = "，"
    print("最遠" + "、".join(farthest) + separator + "最近" + "、".join(closest))

func1("辛巴")
func1("悟空")
func1("弗利沙")
func1("特南克斯")


# Task 2

bookings = {
    "S1": [],
    "S2": [],
    "S3": []
}


def parse_criteria(criteria):
    if ">=" in criteria:
        field, value = criteria.split(">=")
        operator = ">="
    elif "<=" in criteria:
        field, value = criteria.split("<=")
        operator = "<="
    else:
        field, value = criteria.split("=")
        operator = "="

    if field != "name":
        value = float(value)

    return field, operator, value


def match_criteria(service, field, operator, value):
    if operator == "=":
        return service[field] == value

    if operator == ">=":
        return service[field] >= value

    if operator == "<=":
        return service[field] <= value


def is_available(service_name, start, end):
    for old_start, old_end in bookings[service_name]:
        if start < old_end and end > old_start:
            return False

    return True


def func2(ss, start, end, criteria):
    field, operator, value = parse_criteria(criteria)

    best_service = None

    for service in ss:
        service_name = service["name"]

        if match_criteria(service, field, operator, value) and is_available(service_name, start, end):

            if operator == "=":
                best_service = service

            elif operator == ">=":
                if best_service == None or service[field] < best_service[field]:
                    best_service = service

            elif operator == "<=":
                if best_service == None or service[field] > best_service[field]:
                    best_service = service

    if best_service == None:
        print("Sorry")
    else:
        print(best_service["name"])
        bookings[best_service["name"]].append((start, end))


services = [
    {"name": "S1", "r": 4.5, "c": 1000},
    {"name": "S2", "r": 3, "c": 1200},
    {"name": "S3", "r": 3.8, "c": 800}
]

func2(services, 15, 17, "c>=800")   # S3
func2(services, 11, 13, "r<=4")     # S3
func2(services, 10, 12, "name=S3")  # Sorry
func2(services, 15, 18, "r>=4.5")   # S1
func2(services, 16, 18, "r>=4")     # Sorry
func2(services, 13, 17, "name=S1")  # Sorry
func2(services, 8, 9, "c<=1500")    # S2


# Task 3

def func3(index):
    number = 25
    steps = [-2, -3, 1, 2]

    for i in range(index):
        number = number + steps[i % 4]

    print(number)    

func3(1) #4*0+1
func3(5) #4*1+1
func3(10) #4*2+2
func3(30) #4*7+2


# Task 4

def func4(sp, stat, n):
    best_index = None
    best_diff = None

    for i in range(len(sp)):
        if stat[i] == "0":
            diff = abs(sp[i] - n)

            if best_diff is None or diff < best_diff:
                best_diff = diff
                best_index = i

    print(best_index)

func4([3, 1, 5, 4, 3, 2], "101000", 2)
func4([1, 0, 5, 1, 3], "10100", 4)
func4([4, 6, 5, 8], "1000", 4)