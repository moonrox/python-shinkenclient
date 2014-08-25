
def list_table(data, columns):
    results = []
    for row in data:
        _filtered_result = {key:value for (key, value) in row.items() if key in columns}
        result = []
        for column in columns:
            if not column in _filtered_result:
                result.append("")
            else:
                result.append(_filtered_result.get(column))
        results.append(result)
    return (columns, results)

def show_one_table(data, columns):
    for row in data:
        _filtered_result = {key:value for (key, value) in row.items() if key in columns}
        results=[]
        for column in columns:
            if not column in _filtered_result:
                results.append("")
            else:
                results.append(_filtered_result.get(column))
    return (columns, results)