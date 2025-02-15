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