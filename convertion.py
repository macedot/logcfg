# Python program to convert infix expression to postfix
# This code is contributed by Nikhil Kumar Singh(nickzuck_007)
# Class to convert the expression
class Conversion:

	# Constructor to initialize the class variables
	def __init__(self, capacity):
		self.top = -1
		self.capacity = capacity
		# This array is used a stack
		self.array = []
		# Precedence setting
		self.output = []
		self.precedence = {'+':1, '-':1, '*':2, '/':2, '^':3}

	# check if the stack is empty
	def isEmpty(self):
		return True if self.top == -1 else False

	# Return the value of the top of the stack
	def peek(self):
		return self.array[-1]

	# Pop the element from the stack
	def pop(self):
		if not self.isEmpty():
			self.top -= 1
			return self.array.pop()
		else:
			return "$"

	# Push the element to the stack
	def push(self, op):
		self.top += 1
		self.array.append(op)

	# Check is the given character is operand
	def isOperand(self, ch):
		return True if ch not in "()+-*/^" else False

	# Check if the precedence of operator is strictly
	# less than top of stack or not
	def notGreater(self, i):
		try:
			a = self.precedence[i]
			b = self.precedence[self.peek()]
			return True if a <= b else False
		except KeyError:
			return False

	# The main function that converts given infix expression
	# to postfix expression
	def infixToPostfix(self, exp):
		operand = ''
		# Iterate over the expression for conversion
		for i in exp:
			if self.isOperand(i):
				operand += i
			else:
				if len(operand) > 0:
					self.output.append(operand)
					operand = ''
				if i == '(':
					self.push(i)

				# If the scanned character is an ')',
				# pop and output from the stack until and '(' is found
				elif i == ')':
					while( (not self.isEmpty()) and self.peek() != '('):
						a = self.pop()
						self.output.append(a)
					if (not self.isEmpty() and self.peek() != '('):
						return None
					else:
						self.pop()

				# An operator is encountered
				else:
					while(not self.isEmpty() and self.notGreater(i)):
						self.output.append(self.pop())
					self.push(i)
		if len(operand) > 0:
			self.output.append(operand)
			operand = ''

		# pop all the operator from the stack
		while not self.isEmpty():
			self.output.append(self.pop())

		return ",".join(self.output)

if __name__ == "__main__":
    # Driver program to test above function
    exp = "1.23+bc*(cc^.5-ee)^(ff+0.123*.123)-i+[ABC:123]"
    obj = Conversion(len(exp))
    print(obj.infixToPostfix(exp))
