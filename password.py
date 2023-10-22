from flask import Flask,render_template,request
import string,random
app = Flask(__name__,template_folder='template')
@app.route('/')
def main():
    return render_template("password_generator.html",password= "")
@app.route("/submit",methods=['Get','Post'])
def submit():
    mixed_list =[]
    password = []
    if request.method == 'POST':
        lower_case = list(string.ascii_lowercase)
        upper_case = list(string.ascii_uppercase)
        numbers =list(string.digits)
        characters = list(string.punctuation)
        length = int(request.form['length'])
        upper = request.form.get('uppercase')
        if upper!=None:
            mixed_list.extend(upper_case)
            password.append(random.choice(upper_case))
        lower = request.form.get('lowercase')
        if lower!=None:
            mixed_list.extend(lower_case)
            password.append(random.choice(lower_case))
        num = request.form.get('numbers')
        if num!=None:
            mixed_list.extend(numbers)
            password.append(random.choice(numbers))
        symbols = request.form.get('symbols')
        if symbols!=None:
            mixed_list.extend(symbols)
            password.append(random.choice(characters))
        #to determine password length at this time
        l = len(password)
        if l > length:
            return render_template("password_generator.html",password= "you specified greater length")    
        elif l < length:
            password.extend(random.choices(mixed_list,k=length-l))
        random.shuffle(password)
        strong_pass=''.join(password)
        print(strong_pass)

        return render_template("password_generator.html",password= strong_pass)
    return "hello"


        
if __name__ == '__main__':
    app.run(debug=True)