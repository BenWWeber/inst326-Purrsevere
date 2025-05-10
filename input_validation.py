def input_validation(input_type, data_type=str, allowed_values=None):
    while True:
        response = input(input_type)
        try:
            input_value = response.lower() if data_type is str else response
            converted_value = input_value if data_type is str else data_type(input_value)
        
        except ValueError:
            print(f"Please enter a valid {data_type.__name__}")
            continue
        
        if allowed_values is not None and converted_value not in allowed_values:
            print(f"Input Invalid! Try again!")
            continue
        return converted_value         
