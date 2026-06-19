// Task 1

function func1(name) {
    const positions = {
        "悟空": [0, 0],
        "特南克斯": [1, -2],
        "辛巴": [-3, 3],
        "丁滿": [-1, 4],
        "貝吉塔": [-4, -1],
        "弗利沙": [4, -1]
    };

    const sides = {
        "悟空": "left",
        "特南克斯": "left",
        "辛巴": "left",
        "丁滿": "right",
        "貝吉塔": "left",
        "弗利沙": "right"
    };

    const [x1, y1] = positions[name];

    let minDistance = null;
    let closest = [];

    let maxDistance = null;
    let farthest = [];

    for (let otherName in positions) {
        if (otherName !== name) {
            const [x2, y2] = positions[otherName];

            let distance = Math.abs(x1 - x2) + Math.abs(y1 - y2);

            if (sides[name] !== sides[otherName]) {
                distance = distance + 2;
            }

            if (minDistance === null || distance < minDistance) {
                minDistance = distance;
                closest = [otherName];
            } else if (distance === minDistance) {
                closest.push(otherName);
            }

            if (maxDistance === null || distance > maxDistance) {
                maxDistance = distance;
                farthest = [otherName];
            } else if (distance === maxDistance) {
                farthest.push(otherName);
            }
        }
    }

    let separator;

    if (farthest.length > 1 || closest.length > 1) {
        separator = "；";
    } else {
        separator = "，";
    }

    console.log("最遠" + farthest.join("、") + separator + "最近" + closest.join("、"));
}

func1("辛巴");
func1("悟空");
func1("弗利沙");
func1("特南克斯");


// Task 2

const bookings = {
    "S1": [],
    "S2": [],
    "S3": []
};

function parseCriteria(criteria) {
    let field;
    let value;
    let operator;

    if (criteria.includes(">=")) {
        [field, value] = criteria.split(">=");
        operator = ">=";
    } else if (criteria.includes("<=")) {
        [field, value] = criteria.split("<=");
        operator = "<=";
    } else {
        [field, value] = criteria.split("=");
        operator = "=";
    }

    if (field !== "name") {
        value = Number(value);
    }

    return [field, operator, value];
}

function matchCriteria(service, field, operator, value) {
    if (operator === "=") {
        return service[field] === value;
    }

    if (operator === ">=") {
        return service[field] >= value;
    }

    if (operator === "<=") {
        return service[field] <= value;
    }
}

function isAvailable(serviceName, start, end) {
    for (let booking of bookings[serviceName]) {
        const oldStart = booking[0];
        const oldEnd = booking[1];

        if (start < oldEnd && end > oldStart) {
            return false;
        }
    }

    return true;
}

function func2(ss, start, end, criteria) {
    const [field, operator, value] = parseCriteria(criteria);

    let bestService = null;

    for (let service of ss) {
        const serviceName = service["name"];

        if (matchCriteria(service, field, operator, value) && isAvailable(serviceName, start, end)) {
            if (operator === "=") {
                bestService = service;
            } else if (operator === ">=") {
                if (bestService === null || service[field] < bestService[field]) {
                    bestService = service;
                }
            } else if (operator === "<=") {
                if (bestService === null || service[field] > bestService[field]) {
                    bestService = service;
                }
            }
        }
    }

    if (bestService === null) {
        console.log("Sorry");
    } else {
        console.log(bestService["name"]);
        bookings[bestService["name"]].push([start, end]);
    }
}

const services = [
    {"name": "S1", "r": 4.5, "c": 1000},
    {"name": "S2", "r": 3, "c": 1200},
    {"name": "S3", "r": 3.8, "c": 800}
];

func2(services, 15, 17, "c>=800");   // S3
func2(services, 11, 13, "r<=4");     // S3
func2(services, 10, 12, "name=S3");  // Sorry
func2(services, 15, 18, "r>=4.5");   // S1
func2(services, 16, 18, "r>=4");     // Sorry
func2(services, 13, 17, "name=S1");  // Sorry
func2(services, 8, 9, "c<=1500");    // S2


// Task 3

function func3(index) {
    let number = 25;
    const steps = [-2, -3, 1, 2];

    for (let i = 0; i < index; i++) {
        number = number + steps[i % 4];
    }

    console.log(number);
}

func3(1); // print 23
func3(5); // print 21
func3(10); // print 16
func3(30); // print 6


// Task 4

function func4(sp, stat, n) {
    let bestIndex = null;
    let bestDiff = null;

    for (let i = 0; i < sp.length; i++) {
        if (stat[i] === "0") {
            const diff = Math.abs(sp[i] - n);

            if (bestDiff === null || diff < bestDiff) {
                bestDiff = diff;
                bestIndex = i;
            }
        }
    }

    console.log(bestIndex);
}

func4([3, 1, 5, 4, 3, 2], "101000", 2); // 5
func4([1, 0, 5, 1, 3], "10100", 4);     // 4
func4([4, 6, 5, 8], "1000", 4);         // 2