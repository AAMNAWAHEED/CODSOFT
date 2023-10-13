from flask import Flask,render_template,redirect,request
app = Flask(__name__,template_folder='template')
import re
def checkoperator(opr):
     if opr == '+' or opr =='-'or opr == '*' or opr=="/" or opr == "%" or opr=='(' or opr==')':
          return -1
     else:
          return 1

def createExpression(input):
     exp = ""
     expression =[]
     for i in input:
            if checkoperator(i) == 1:
               exp+=i
            else:
                 if exp!="":
                    expression.append(exp)
                 expression.append(i)
                 exp= ""
     if exp!="":
          expression.append(exp)
     return expression
                        
               
def precedence(opr):
    if opr=='+' or opr =='-':
          pre =1
    elif opr =='*' or opr =='/' or opr == '%':
         pre=2
    elif opr =='(':
         pre = 3
    elif opr == ')':
         pre =4
    return pre

def associtivity(opr):
    if opr == '+' or opr =='-'or opr == '*' or opr=="/" or opr == "%": 
          asso = 1
    return asso

def calculate(val1,val2,opr):
    if opr == '+':
        return val2 + val1
    elif opr == '-':
         return val2 - val1
    elif opr =='*':
        return val2*val1
    elif opr =='/':
         return val2/val1
    elif opr =='%':
         return val2%val1

@app.route('/')
def calculator():
    return render_template("calculator.html",result = 0)

@app.route('/submit', methods = ['Get','Post'])
def submit():
        res=""
        input = request.form['expression']
        print(input)
        #validate expression through regex
        import re
        a=0
       # pattern = r"^\d+(?:[+\-*/%]\d+)*(?:(?:\((?:(?:(?:(?:\d+(?:[+\-*/%]\d+)*))|(?:\((?1)\)))\)))(?:[+\-*/%]\d+)*|(?1))*$"
        #pattern = r"^\d+(?:[+\-*/%]\d+|[(]\d+(?:[+\-*/%]\d+)*[)])*$"
        #match = re.findall(pattern,input)
        if input!=None:
            #create list of input
            expression = createExpression(input)
            print(expression)
            #now solve it using expression tree
            #convert to postfix expression
            stack =[]
            postfix_exp =[]
            for i in expression:
                #check int or operator
                if checkoperator(i) == 1:
                        postfix_exp.append(i)
                else:
                      #goes to stack
                        if len(stack) == 0:
                           stack.append(i)
                        else:
                             #check precedence
                             #id open bracket pust it
                                if i == '(':
                                    stack.append(i)
                                elif i ==')':
                                    while stack[-1] != '(':
                                          postfix_exp.append(stack[-1])
                                          stack.pop()
                                    stack.pop()
                             #1-greater precedence
                                elif (precedence(i) > precedence(stack[-1])):
                                    stack.append(i)
                                elif precedence(i) < precedence(stack[-1]):
                                    if stack[-1] == '(':
                                        stack.append(i)
                                    else:
                                        while len(stack)!=0 and precedence(i) < precedence(stack[-1]) and stack[-1]!='(': 
                                            postfix_exp.append(stack.pop())
                                            #postfix_exp+=stack.pop()
                                        if len(stack)!=0 and precedence(i) == precedence(stack[-1]):
                                        #check associtivy
                                        #if l->R assco
                                            if associtivity(i) == 1:
                                                print("left to right asso",stack)
                                                postfix_exp.append(stack.pop())
                                                print("left to right asso after popp",stack)
                                                #postfix_exp+=stack.pop()
                                                #stack.append(i)
                                        stack.append(i)
                                elif precedence(i) == precedence(stack[-1]):
                                     #check associtivy
                                     #if l->R assco
                                     if associtivity(i) == 1:
                                           print("left to right asso",stack)
                                           postfix_exp.append(stack.pop())
                                           print("left to right asso after popp",stack)
                                          #postfix_exp+=stack.pop()
                                           stack.append(i)
            if len(postfix_exp)==0:
                 res = "ERROR"
            while len(stack)!=0:
                if stack[-1] == '(':
                    stack.pop()
                    res= "ERROR"
                else:
                    postfix_exp.append(stack.pop())
                    #postfix_exp+=stack.pop()
            print(postfix_exp)
            print(stack)
            #solve the expression. 99/
            if res!='ERROR' and len(postfix_exp)!=0:
                for val in postfix_exp:
                    #print(stack)
                    if checkoperator(val) == 1:
                        stack.append(val)
                    else:
                        if len(stack) == 0:
                            res="error"
                            break
                        val1 = int(stack.pop())
                        if len(stack) == 0:
                            res="error"
                            break
                        val2 = int(stack.pop())
                        stack.append(calculate(val1,val2,val))
                        #print(stack)
                if len(stack)!=0:
                     res = stack.pop()
                else:
                     res= "ERROR"
            print(res)
            return render_template('calculator.html',result= res)
        else:
            return render_template('calculator.html',result= "ERROR")
if __name__ =='__main__':
    app.run(debug=True)