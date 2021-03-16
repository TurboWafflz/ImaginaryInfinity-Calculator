import ast
import astor
import re
import types
import decimal
# import colorama

class RewriteCall(ast.NodeTransformer):
	# Visit all Call objects in AST
	def visit_Call(self, node):
		# Get number of child Call objects nested in current node
		nestedFunctions = sum(1 for _ in ast.walk(node) if isinstance(_, ast.Call)) - 1

		# No more children, evaluate
		if nestedFunctions == 0:
			# print(colorama.Fore.YELLOW + astor.to_source(node) + colorama.Fore.RESET)
			# print(colorama.Fore.BLUE + str(eval(astor.to_source(node))) + colorama.Fore.RESET)
			# try:
			# 	print(colorama.Fore.GREEN + ast.dump(ast.parse(str(eval(astor.to_source(node)))), indent=4) + colorama.Fore.RESET)
			# except Exception as e:
			# 	print(e)
			# 	import time
			# 	time.sleep(1)
			evaluated = astor.to_source(node)
			# Surround every float with `decimal.Decimal('<value>')` to fix floating point arithmetic errors
			evaluatedDecimal = re.sub(r'(\d*\.\d+)(?!j)([^j0-9]|$)|(\d+\.\d*)(?!j)([^j0-9]|$)', "decimal.Decimal(\"" + r"\1" + "\")", evaluated)
			try:
				evaluatedDecimal = eval(evaluatedDecimal)
				if isinstance(evaluatedDecimal, str):
					evaluatedDecimal = "\"" + str(evaluatedDecimal) + "\""
				evaluatedDecimal = ast.parse(str(evaluatedDecimal))

				# Modify AST node to evaluated expression
				return ast.fix_missing_locations(evaluatedDecimal)
			except Exception:
				evaluated = eval(evaluated)
				if isinstance(evaluated, str):
					evaluated = "\"" + evaluated + "\""
				evaluated = ast.parse(str(evaluated))

				# Modify AST node to evaluated expression
				return ast.fix_missing_locations(evaluated)
		else:
			# print(astor.to_source(node))
			# Children remaining, keep current node the same and visit children
			self.generic_visit(node)
			return node

class Expression(object):
	def __init__(self, expr, newGlobals, newLocals):
		self.expr = expr
		self.tree = ast.parse(self.expr)
		self.modified = False
		# Make locals and globals of module that makes the expression object globals in this file
		for definition in newGlobals:
			globals()[definition] = newGlobals[definition]
		for definition in newLocals:
			globals()[definition] = newLocals[definition]
		# print(globals())

	def evaluateFunctions(self):
		# Number of Call objects in tree
		callsRemaining = sum(1 for _ in ast.walk(self.tree) if isinstance(_, ast.Call))

		# While calls remain in tree, evaluate lowest level of tree
		while callsRemaining != 0:
			self.modified = True
			# print(ast.dump(self.tree, indent=4))
			self.tree = RewriteCall().visit(self.tree)
			callsRemaining = sum(1 for _ in ast.walk(self.tree) if isinstance(_, ast.Call))

		# Convert tree back to python code
		if self.modified == True:
			self.expr = "(" + astor.to_source(self.tree) + ")"
		return self

	def floatToDecimal(self):
		self.expr = re.sub(r'(\d*\.\d+)(?!j)([^j0-9]|$)|(\d+\.\d*)(?!j)([^j0-9]|$)', "decimal.Decimal(\"" + str(r"\1") + "\")", self.expr)
		return self