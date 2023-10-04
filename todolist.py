from flask import Flask,render_template,request,url_for,redirect
app=Flask(__name__,template_folder='template')
global tasklist
tasklist = []
#[{'task':value, 'status':complete}]
def all_completed():
    return all(task['status'] == 'complete' for task in tasklist)

@app.route('/')
def main():
    global tasklist
    return render_template('todo.html',tasklist = tasklist,all_completed = all_completed())
@app.route('/add',methods=['Get','Post'])
def addTask():
    global tasklist
    if request.method == 'POST':
        task = request.form['new-task']
        tasklist.append({'index':len(tasklist),'task':task,'status':'not complete'})
    return redirect('/')

@app.route('/editTask', methods = ['Get','Post'])
def edit():
    global tasklist
    if request.method =='POST':
        new_task=request.form['new-task']
        index = int(request.form['index'])#HTML form input values are sent as text, and Flask does not automatically cast them to specific data types like integers or floats.
        tasklist[index]['task'] = new_task
        #tasklist = list(map(lambda x: x.replace(old_task, new_task), tasklist))
        return redirect('/')
    return redirect('/')
@app.route('/edit',methods=['Get','Post'])
def editTask():
    if request.method == 'POST':
        index = int(request.form['index'])
        old_task = request.form['task']
        if tasklist[index]['status'] == 'complete':
            return "you can not edit completed task"
        return render_template('editTask.html',index=index,old_task=old_task)
    return redirect('/')

@app.route('/delete',methods=['Get','Post'])
def deleteTask():
    global tasklist
    if request.method == 'POST':
        index = int(request.form['index'])
        del tasklist[index]
        for dic in tasklist:
            if dic['index'] >  index:
                dic['index'] =  dic['index']-1 
        return redirect('/')
    return redirect('/')

@app.route('/check',methods=['Get','Post'])
def check():
    global tasklist
    if request.method == 'POST':
        index = int(request.form['index'])
        if tasklist[index]['status'] == 'complete':
            tasklist[index]['status'] = 'not complete'
        else:
            tasklist[index]['status'] = 'complete'
        return redirect('/')
    return redirect('/')
if __name__ == "__main__":
    app.run(debug=True)
