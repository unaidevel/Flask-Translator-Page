# def factorial_number(x):
#     if x == 1 or x == 0:
#         return 1
#     elif x == 2:
#         return 2
#     else:
#         return x * factorial_number(x - 1)

# x = 5

# print(factorial_number(x))




# def reverse_string(x):
#     my_list = []
#     for i in x:
#         my_list.insert(0, i)
#     new_string = ''.join(my_list)
#     return new_string

# x = "This is a string"

# print(reverse_string(x))






# import time
# print("Hola ahora pasan")
# time.sleep(2)
# print("2 segundos")


# def suma_asincrona():
#     x = input("Introduce el primer número")
#     y = input("Introduce el segundo número")
#     z = int(input("Introduce el tiempo de espera"))
#     try:
#         total_sum = x + y
#         time.sleep(z)
#         return f"La suma total entre {x} y {y} es {total_sum}."
#     except Exception as e:
#         return f"Se ha producido el siguiente error:{e}"



# print(suma_asincrona())


import numpy as np



def conjuntos(arr1, arr2, the_boolean):    
    arr1 = list(arr1)
    arr2 = list(arr2)
    result = []
    if the_boolean:
        for i in arr1:
            if i in arr2 and i not in result:
                result.append(i)
    else:
        for z in arr2:
            if z not in arr1 and z not in result:
                result.append(z)
        for z in arr1:
            if z not in arr1 and z not in result:
                result.append(z)
    
    return np.array(result)


arr1 = np.array([0, 4, 6, 8, 10, -4, -2])    
arr2 = np.array([1, 2, 4, 7, -14, -2, 0])
print(conjuntos(arr1, arr2, True))



# for x in range(0,101):
#     print(x)






# def lista():
#     the_boolean = True
#     list_1 = [0, 1, 2, 3, 4, 5]
#     list_2 = [1, 4, 6, 8, 10]
#     new_list = []
#     aux_list = list_1 + list_2
#     for x in aux_list:
#         if x not in new_list:
#             new_list.append(x)    
#             return new_list
# print(lista())
