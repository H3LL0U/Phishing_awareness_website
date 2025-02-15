from collections import defaultdict

def dict_to_javascript_format(_dict:dict):
    parsed_str = ""
    for value in _dict:
        parsed_str += '{"date": "' + value + '", value: ' + str(_dict[value]) + '}, \n'
    return parsed_str


def get_hourly_date_from_documents(docs:list[dict],db_parameter:str):
    users_by_time = dict()
    for user in docs:
        try:
            date = user[db_parameter][:-5] + "00:00"
            if not date in users_by_time:
                users_by_time[date] = 1
            else:
                users_by_time[date] +=1
        


        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except:
            continue
    return users_by_time

def structure_date_data(_list: list[dict]) -> dict:
    
    '''
    takes a list of dictionaries containing the redirect type as the key and the date as teh value and restuctures them 
    as follows:

    Input:
        _list (list of dict): A list of dictionaries where each dictionary contains a redirect type as the key 
                            and a timestamp as the value.
                            Example:
                            [
                                {"redirect_type_1": "2025-02-15 19:12:22"},
                                {"redirect_type_1": "2025-02-15 19:14:01"},
                                {"redirect_type_2": "2025-02-15 19:12:22"}
                            ]

    Output:
    dict: A dictionary where each key is a redirect type and each value is a dictionary where the keys are the 
          dates (with the time set to "00:00") and the values are the counts of occurrences of that date for that 
          specific redirect type.
          Example output:
          {
              "redirect_type_1": {"2025-02-15 19:00:00": 2},
              "redirect_type_2": {"2025-02-15 19:00:00": 1}
          }
    '''


    formatted_data = defaultdict(lambda: defaultdict(int))

    
    for entry in _list:
        for key, value in entry.items():
            try:
                
                date_str = value[:-5] + "00:00"  

                
                formatted_data[key][date_str] += 1

            except KeyboardInterrupt:
                raise KeyboardInterrupt
            except Exception as e:
                continue  

    
    return {key: dict(value) for key, value in formatted_data.items()}