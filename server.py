import os,sys
from flask import Flask, request, jsonify
# current_file_name = os.path.basename(__file__)
# #print("file name: ",current_file_name)
import unusedimport,longfunctions,badexception,bad_context_management,dead_code, cyclomatic_complexity, hardcoded_values, deep_nesting, too_many_params, multiple_files_duplicate_code
app = Flask(__name__)
folder_insights_store = {}
file_contents = {}

@app.route('/process', methods=['POST'])
def process_file_and_folder():
    data = request.get_json()
    file_content = data.get('fileContent', "")
    folder_content = data.get('folderContent', {})
    current_file = data.get('current_fileName')
    current_file = current_file.split("\\")[-1]

    # Process the active file content
    highlights = process_file_content(file_content,folder_content,current_file)

    # Process the folder content recursively
    folder_insights = analyze_folder_contents(folder_content,current_file)
    # folder_insights = []
    #print("folder insightsss: ", folder_insights)
    # Return the processed results
    return jsonify({
        "highlights": highlights,
        "folderInsights": folder_insights
    })

def process_file_content(file_content,folder_content,current_file):
    """
    Analyzes the file content for keywords and generates line-based suggestions.
    """
    highlights = []

    #print(file_content)
    unused_vars, unused_imports = unusedimport.find_unused_variables_and_imports(file_content)
    #print("Unused variables:", unused_vars)
    #print("Unused imports:", unused_imports)

    for imports in unused_imports.keys():
            ##print(imports,unused_imports.get(imports))
            highlights.append({
                "line": unused_imports.get(imports),
                "suggestion": imports + " library isnt used, do better!!",
                "tag": "unused"
            })
    
    for imports in unused_vars.keys():
            ##print(imports,unused_imports.get(imports))
            highlights.append({
                "line": unused_vars.get(imports),
                "suggestion": imports + " variable isnt used, do better!!",
                "tag": "unused"
            })

    max_length = 50
    long_functions = longfunctions.find_long_functions(file_content, max_length)
    for func_name, start_line, end_line, length in long_functions:
         highlights.append({
                "start_line": start_line,
                "end_line": end_line,
                "suggestion": func_name + " too long!!!",
                "tag": "long"
            })
    
    bad_handlers = badexception.find_bad_exception_handling(file_content)
    for lineno in bad_handlers:
        # #print(f"Bad exception: Bad exception handling found on line {lineno}")
        highlights.append({
                "line": lineno,
                "suggestion": "can do better exceptions hehe",
                "tag": "exception"
            })
        
    bad_context = bad_context_management.get_bad_context(file_content)
    for context in bad_context:
        highlights.append({
                    "line": context['line'],
                    "suggestion": "nah nah open file properly hehe",
                    "tag": "bad_context"
                })
    
    dead_context = dead_code.get_dead_code(file_content)
    for context in dead_context:
        highlights.append({
                    "line": context['line'],
                    "suggestion": "Do you really want this code here?",
                    "tag": "dead_context"
                })
        
    cyclomatic_complex = cyclomatic_complexity.get_cyclomatic_complexity(file_content)
    for complexity in cyclomatic_complex:
        if complexity['complexity'] > 5:
            highlights.append({
                        "line": complexity['line'],
                        "suggestion": "Nah Nah too complex for me",
                        "tag": "cyclomatic_complex"
                    })
        # #print(f"Function '{complexity['function']}' at line {complexity['line']}: Cyclomatic Complexity = {complexity['complexity']}")

    
    hardcoded = hardcoded_values.get_hardcoded(file_content)
    for value in hardcoded:
        highlights.append({
                        "line": value['line'],
                        "suggestion": "do you have an explanation for that value?",
                        "tag": "hardcoded"
                    })
    deep_nest = deep_nesting.get_deep_nesting(file_content)
    for nest in deep_nest:
        highlights.append({
                        "line": value['line'],
                        "suggestion": "too deep cant do?",
                        "tag": "deep_nesting"
                    })
    
    too_many = too_many_params.get_too_many_params(file_content)
    for line in too_many:
        highlights.append({
                        "line": line['line'],
                        "suggestion": "the params are confusing",
                        "tag": "too_many_params"
                    })
    # folder_insights = analyze_folder_contents(folder_content,current_file)
    analyze_folder_contents(folder_content,current_file)
    # print("current_file_name: ",current_file)
    # print("\n\nfolder_insights: ",folder_insights[current_file])
    # print("folder insights: ",folder_insights_store.keys())
    if current_file in folder_insights_store:
        for line in folder_insights_store[current_file]:
            highlights.append(line)
    print("\n\nhighlights: ",highlights)

    return highlights


    # # Split content by lines and look for keywords
    # lines = file_content.splitlines()
    # for index, line in enumerate(lines):
    #     if "TODO" in line:
    #         highlights.append({
    #             "line": index,
    #             "suggestion": "Complete this TODO item."
    #         })
    #     elif "FIXME" in line:
    #         highlights.append({
    #             "line": index,
    #             "suggestion": "Check and fix this issue."
    #         })

    # return highlights

def analyze_folder_contents(folder_content,current_file):
    """
    Analyzes the contents of the entire folder recursively for keywords.
    """

    # print(" in analyze_folder_contents")
    

    

    for filename, content in folder_content.items():
        
        # if filename == current_file:
        #     print("yessssss")
        if isinstance(content, dict):
            # print("in isinstanceeee")
            # Recurse into subdirectories
            analyze_folder_contents(content,current_file)
        else:
            # print("file name: ",filename)
            # print("not isinstanceeee")
            # Check for keywords in file content

            file_contents[filename] = content
            folder_insights_store[filename] = []
    
    duplicate_multiple = multiple_files_duplicate_code.get_duplicate_multiple(file_contents)

    for duplicate in duplicate_multiple:
        for value in duplicate['lines']:
            if value[0] == current_file:
                filename = value[0]
                # if not filename in folder_insights_store.keys():
                #     folder_insights_store[filename] = []
                # else:
                folder_insights_store[filename].append({
                    "start_line":value[1],
                    "end_line": value[2],
                    "suggestion": "repetitive code across files",
                    "tag": "multiple_duplicate"
                })

    # for filename, content in folder_content.items():
    #     insights = []
    #     # if "TODO" in content:
    #     #     insights.append("This file contains TODO items.")
    #     # if "FIXME" in content:
    #     #     insights.append("This file contains FIXME items.")
        
    #     for duplicate in duplicate_multiple:
    #         # print("duplicate: ",duplicate, file = sys.stderr)
    #         # print("duplicate: ",duplicate)
    #         for value in duplicate['lines']:
    #             print("value: ",value, current_file)
    #             if value[0] == current_file:
    #                 insights.append({
    #                         "start_line":value[1],
    #                         "end_line": value[2],
    #                         "suggestion": "repetitive code across files",
    #                         "tag": "multiple_duplicate"
    #                     })
    #                 if current_file == 'WordFrequency.py': print('look at me', len(insights))
    #     if current_file == 'WordFrequency.py':
    #         print("\n\ninsights: ",insights)
    #     folder_insights_store[filename] = insights if insights else ["No issues found."]
    #     # print("folder_insights: ",folder_insights_store.keys())

    #     # #print("folderrrr: ",folder_insights)
    #     # return folder_insights_store

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
