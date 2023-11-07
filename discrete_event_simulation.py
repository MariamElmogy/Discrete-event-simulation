'''
    Name: Mariam Mohamed ElMogy
    Reg#: 19101076
'''
import random
customer_number = []
inter_arrival = []
service = []
random_numbers = []
uniform_random_numbers = []
time_arrival = []
prob_time_arrival = []
cdf_time_arrival = []
generate_arrival = []
time_service = []
prob_time_service = []
cdf_time_service = []
arrival = []
begin_service = []
idle = []
end_service = []
system = []
wait = []
queue_copy = []
queue_length = []


def readTheFile(ask):
    if ask == 1:
        for i in range(0, 100):
            customer_number.append(i)
            random_numbers.append(str(random.randint(1, 10000)))
        # file = open('random.txt', "r")
        # for line in file:
        #     data = line.split()
        #     customer_number.append(data[0])
        #     random_numbers.append(data[1])

        # file.close()
        get_uniform_random()
        get_time_arrival()
        get_cdf_time_arrival()
        generate_time_arrival()
        print_time_arrival()

        get_time_service()
        get_cdf_time_service()
        generate_time_service()
        print_time_service()

    elif ask == 2:
        file = open('table.txt', "r")
        for line in file:
            data = line.split()
            customer_number.append(data[0])
            inter_arrival.append(data[1])
            service.append(data[2])

        file.close()


def get_uniform_random():
    global power_max
    for i in range(len(random_numbers)):
        digits = len(str(abs(int(random_numbers[i]))))
        max_digit = max(str(digits))
        if random_numbers[i].startswith("0"):
            uniform_random_numbers.append(int(random_numbers[i]) / (power_max*1))

        elif max_digit == 1:
            power_max = max_digit
            uniform_random_numbers.append(int(random_numbers[i]) / power_max)

        else:
            power_max = pow(10, int(max_digit))
            uniform_random_numbers.append(int(random_numbers[i]) / power_max)


def get_time_arrival():
    file = open('time_arrival.txt', "r")
    for line in file:
        data = line.split()
        time_arrival.append(data[0])
        prob_time_arrival.append(data[1])
    file.close()


def get_cdf_time_arrival():
    cdf_time_arrival.append(float(prob_time_arrival[0]))
    for i in range(1, len(time_arrival)):
        cdf_time_arrival.append(float(prob_time_arrival[i]) + float(cdf_time_arrival[i-1]))


def generate_time_arrival():
    for i in range(0, len(customer_number)):
        for j in range(0, len(time_arrival)):
            if float(uniform_random_numbers[i]) <= float(cdf_time_arrival[j]):
                inter_arrival.append(time_arrival[j])
                break


def print_time_arrival():
    print('#\tRandom Number\tUniform Random\tGenerate inter-arr')
    for i in range(0, len(random_numbers)):
        print(customer_number[i], "\t|", random_numbers[i], "\t\t|\t", uniform_random_numbers[i], "\t|\t\t", inter_arrival[i])
    print('-----------------------------------------------------')


def get_time_service():
    file = open('service_time.txt', "r")
    for line in file:
        data = line.split()
        time_service.append(data[0])
        prob_time_service.append(data[1])
    file.close()


def get_cdf_time_service():
    cdf_time_service.append(float(prob_time_service[0]))
    for i in range(1, len(time_service)):
        cdf_time_service.append(float(prob_time_service[i]) + float(cdf_time_service[i-1]))


def generate_time_service():
    for i in range(0, len(customer_number)):
        for j in range(0, len(time_service)):
            if float(uniform_random_numbers[i]) <= float(cdf_time_service[j]):
                service.append(time_service[j])
                break


def print_time_service():
    print('#\tRandom Number\tUniform Random\tGenerate inter-arr')
    for i in range(0, len(random_numbers)):
        print(customer_number[i], "\t|", random_numbers[i], "\t\t|\t", uniform_random_numbers[i], "\t|\t\t", service[i])
    print('-----------------------------------------------------')


def get_arrival():
    arrival.append(inter_arrival[0])
    for i in range(0, len(customer_number)-1):
        arrival.append(int(inter_arrival[i+1]) + int(arrival[i]))


def get_data():
    for i in range(0, len(customer_number)):
        if i == 0:
            begin_service.append(arrival[i])
            idle.append(begin_service[i])

        elif i >= 1:
            begin_service.append(max(int(arrival[i]), int(end_service[i-1])))
            idle.append(int(begin_service[i]) - int(end_service[i - 1]))

        end_service.append(int(begin_service[i]) + int(service[i]))


def get_system():
    for i in range(0, len(customer_number)):
        system.append(int(end_service[i]) - int(arrival[i]))


def get_wait():
    for i in range(0, len(customer_number)):
        wait.append(int(begin_service[i]) - int(arrival[i]))


def get_queueLength(ask):
    for i in range(0, len(customer_number)):

        if int(wait[i]) == 0:
            queue_length.append(int(wait[i]))
            queue_copy.append(int(wait[i]))

        elif (int(arrival[i]) < int(end_service[i - 1])) and (int(begin_service[i - 1]) < int(arrival[i])):
            count = queue_copy[len(queue_copy) - 1] + 1
            queue_copy.append(count)
            queue_length.append(count)
            if (i + 1) > len(customer_number) - 1:
                break
            else:
                if begin_service[i] > arrival[i + 1]:
                    pass
                else:
                    queue_copy.pop()

        elif int(arrival[i]) == int(begin_service[i - 1]):
            count = queue_copy[len(queue_copy) - 1] + 1
            queue_copy.append(count)
            queue_length.append(count)

        elif int(begin_service[i - 1]) > int(arrival[i]):
            count = queue_copy[len(queue_copy) - 1] + 1
            queue_copy.append(count)
            queue_length.append(count)
            if (i + 1) > len(customer_number) - 1:
                break
            else:
                if begin_service[i] > arrival[i + 1]:
                    pass
                if (int(arrival[i + 1]) < int(begin_service[i - 1])) and \
                    (int(arrival[i - 1]) < int(arrival[i + 1])):
                    pass
                elif (int(arrival[i]) < int(begin_service[i - 1])) and \
                        (int(arrival[i - 1]) < int(arrival[i])):
                    if ask == 1:
                        for j in range(len(queue_copy)-1):
                            queue_copy.pop()
                    elif ask == 2:
                        queue_copy.pop()
                else:
                    queue_copy.pop()
#

def get_equations():
    sum_inter_arrival = 0
    sum_service = 0
    sum_wait = 0
    sum_waiting_customers = 0
    sum_system = 0
    sum_idle = 0
    sum_queue_length = 0
    for i in range(0, len(customer_number)):
        sum_wait += wait[i]
        sum_idle += int(idle[i])
        sum_service += int(service[i])
        sum_inter_arrival += int(inter_arrival[i])
        sum_queue_length += int(queue_length[i])
        sum_system += int(system[i])
        if wait[i] != 0:
            sum_waiting_customers += 1
        else:
            pass
    # 1- Average waiting time in queue.
    print(sum_wait)
    print('Average waiting time in queue = ', (sum_wait / len(customer_number)))

    # 2- Probability of waiting.
    print('Probability of waiting = ', (sum_waiting_customers / len(customer_number)))

    # 3- Probability of the server being idle.
    print('Probability of the server being idle = ', (sum_idle / end_service[len(customer_number)-1]))

    # 4- Average service time.
    print('Average service time = ', (sum_service / len(customer_number)))

    # 5- Average Interarrival time(time between arrivals).
    print('Average Interarrival time(time between arrivals) = ', (sum_inter_arrival/ (len(customer_number)-1)))

    # 6- Average time a customer spends in the queue(waiting time in queue).
    print('Average time a customer spends in the queue = ', (sum_wait / end_service[len(customer_number)-1]))

    # 7- Average time a customer spends in the system.
    print('Average time a customer spends in the system = ', (sum_system / len(customer_number)))

    # 8- Average queue length.
    print('Average queue length = ', (sum_queue_length / len(customer_number)))

    # 9- Server utilization.
    print('Server utilization = ', (1 - sum_idle / end_service[len(customer_number)-1]))


def printData():
    print('#\tinter_arr\tarrival\tservice\tbegin_serv\twait\tend_serv\tsystem\tidle\tqueue_length')
    for i in range(len(customer_number)):
        print(customer_number[i], '\t|', inter_arrival[i], "\t\t|", arrival[i], "\t|", service[i], "\t|", begin_service[i]
              , "\t\t|", wait[i], "\t|", end_service[i], "\t\t|", system[i], "\t|", idle[i], "\t|", queue_length[i])


def main():
    ask = int(input('Choose: \n1- Random Generated Number \n2- Simulation Table\n'))
    readTheFile(ask)
    get_arrival()
    get_data()
    get_wait()
    get_system()
    get_queueLength(ask)
    printData()
    get_equations()

main()