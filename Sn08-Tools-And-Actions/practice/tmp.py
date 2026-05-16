def say_hello(name):
    '''A function that says hello to parameter `name` as string.'''
    print(f'Hello, {name}!')

function_obj = say_hello

print(function_obj.__name__)
print(function_obj.__doc__)
print('\n' * 10)
say_hello("Eng. Mohamed")
function_obj("Eng. Mohamed")