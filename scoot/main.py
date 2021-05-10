import random
from colorama import Fore, Back, Style
from tqdm import tqdm
import time
import os
import json

class SteeringWheel():
	def __init__(self):
		self.SteeringWheelLevel = 100
		self.MaxSWLevel = 130
		self.MinSWLevel = 70
		self.Direction = "forward"

	def Requirements(self):
		self.id = "4.3 / 4.4"
		self.material = "metal"

	def SetSWLevel(self):
		self.SteeringWheelLevel = int(input("Set new height (70-130): "))
		if self.SteeringWheelLevel < 70:
			self.SteeringWheelLevel = 70
			print("Minimum height set (70)\n")
			return self.SteeringWheelLevel
		elif self.SteeringWheelLevel > 130:
			self.SteeringWheelLevel = 130
			print("Maximum height set (130)\n")
			return self.SteeringWheelLevel
		else:
			print("Height set ("+str(self.SteeringWheelLevel)+")\n")
			return self.SteeringWheelLevel
	def GetSWLevel(self):
		print("Current steering wheel height is: " + str(self.SteeringWheelLevel))
	
	def SetDirection(self, param, type):
		self.Direction = param
		if type != "bend":
			if param == "right":
				self.Direction = "right"
				return self.Direction
			elif param == "left":
				self.Direction = "left"
				return self.Direction
			elif param == "forward":
				self.Direction = "forward"
				return self.Direction
			return self.Direction
		else:
			return
	
	def GetDirection(self):
		return self.Direction

class Deck():
	def __init__(self):
		self.state = True

	def Requirements(self):
		self.id = "4.1"
		self.material = "metal"
		self.size = "23x52cm"

	def SetState(self):
		if self.state:
			print("Do you want to remove the deck? (1. Yes 2. No)")
			ans = int(input())
			if ans == 1:
				print("Deck is removed.")
				self.state = False
				return self.state
			elif ans == 2:
				return
		elif not self.state:
			print("Do you want to install the deck? (1. Yes 2. No)")
			ans = int(input())
			if ans == 1:
				print("Deck is installed.")
				self.state = True
				return self.state
			elif ans == 2:
				return
		else:
			return
	def GetState(self):
		if self.state:
			print("Deck is installed.")
		elif not self.state:
			print("Deck is removed.")
		else:
			return

class Step():
	def __init__(self):
		self.state = True

	def Requirements(self):
		self.id = "4.2"
		self.material = "metal"

	def SetState(self):
		if self.state:
			print("Step is up now.")
			self.state = False
			return self.state

		elif not self.state:
			print("Step is down now.")
			self.state = True
			return self.state
		else:
			return

	def GetState(self):
		if self.state:
			print("Step is down.")
		elif not self.state:
			print("Step is up.")
		else:
			return

class Customization():
	def __init__(self):
		self.step = Step()
		self.deck = Deck()
		self.sw = SteeringWheel()

	def SetStateStep(self):
		self.step.SetState()

	def GetStateStep(self):
		self.step.GetState()

class Engine():
	def __init__(self):
		self.IsOn = False
		self.EngineTurns = False

	def Requirements(self):
		self.id = "1.4"
		self.capacity = "350w"
		self.max_capacity = "600w"

	def SetState(self):
		if self.IsOn:
			self.IsOn = False
			return self.IsOn

		elif not self.IsOn:
			self.IsOn = True
			return self.IsOn
		else:
			return

	def GetState(self):
		if self.IsOn:
			print("Engine is working.")
		elif not self.IsOn:
			print("Engine is not working.")
		else:
			return

class Battery():
	def __init__(self):
		self.BatteryLevel = random.randrange(30,100)

	def Requirements(self):
		self.id = "1.2"
		self.capacity = "12400mAh"
		self.charging_time = "10h"

	def ChargeBattery(self):
		print(Fore.GREEN + 'Charging engine')
		for i in tqdm(range(100)):
			time.sleep(0.01)
		print(Style.RESET_ALL)
		self.BatteryLevel = 100
		print("Battery charged (100%)")
		return self.BatteryLevel

	def GetBatteryLevel(self):
		print("Current battery level is: "+str(self.BatteryLevel)+"%")
		return

class PowerSupply():
	def __init__(self):
		self.battery = Battery()
		self.engine = Engine()
		self.Power = False
		self.PowerConnection = False

	def SetPowerConnection(self):
		if self.PowerConnection:
			self.PowerConnection = False
			print("Stopped charging.")
			self.battery.GetBatteryLevel()
		elif not self.PowerConnection:
			self.PowerConnection = True
			print("Started charging.")
			self.battery.ChargeBattery()
			return
		else:
			return
	def GetPowerConnection(self):
		if self.PowerConnection:
			print("Scooter is charging.")
			return
		elif not self.PowerConnection:
			print("Scooter is not charging.")
			return
		else:
			return

	def PowerOn(self):
		if self.engine.IsOn:
			print(Fore.RED + 'Scooter is already turned on.')
			print(Style.RESET_ALL)
			return
		else:
			self.engine.SetState()
			print(Fore.GREEN + 'Turning on scooter')
			for i in tqdm(range(self.battery.BatteryLevel)):
				time.sleep(0.01)
			print(Style.RESET_ALL)
			self.Power = True
			return self.Power

	def PowerOff(self):
		if not self.engine.IsOn:
			print(Fore.RED + 'Scooter is not turned on.')
			print(Style.RESET_ALL)
			return
		else:
			self.engine.SetState()
			print(Fore.RED + 'Turning off scooter.')
			for i in tqdm(range(self.battery.BatteryLevel)):
				time.sleep(0.01)
			print(Style.RESET_ALL)
			self.Power = False
			return self.Power

class Throttle():
	def __init__(self):
		self.Kind = ""
		self.PressedState = False

	def Requirements(self):
		self.id = "5.1 / 5.2"
		self.material = "plastic"
		self.connection = "cabel"

	def SetState(self):
		if self.PressedState:
			self.PressedState = False
			return self.PressedState
		elif not self.PressedState:
			self.PressedState = True
			return self.PressedState
		else:
			return

	def GetState(self):
		if self.PressedState and self.Kind == "gas":
			print("Speeding up.")
		elif self.PressedState and self.Kind == "brake":
			print("Braking.")
		elif not self.PressedState and self.Kind == "gas":
			print("Stopped speeding up.")
		elif not self.PressedState and self.Kind == "brake":
			print("Stopped braking.")
		else:
			return

	def SetKind(self, param):
		self.Kind = param
		# if param == "gas":
		# 	self.Kind = "gas"
		# 	return self.Kind
		# elif param == "brake":
		# 	self.Kind = "brake"
		# 	return self.Kind
		# else:
		# 	return
		return self.Kind

	def GetKind(self):
		if self.Kind == "gas":
			print("You are speeding up.")
		elif self.Kind == "brake":
			print("You are braking.")
		return

class BackBreak():
	def __init__(self):
		self.PressedState = False

	def Requirements(self):
		self.id = "5.3"
		self.material = "metal"

	def SetState(self):
		if self.PressedState:
			print("Stop braking.")
			self.PressedState = False
			return self.PressedState
		elif not self.PressedState:
			print("Braking.")
			self.PressedState = True
			return self.PressedState
		else:
			return

	def GetState(self):
		if self.PressedState:
			print("Braking.")
		elif not self.PressedState:
			print("Not braking.")
		else:
			return

class SpeedAdjustment():
	def __init__(self):
		self.throttle = Throttle()
		self.backbreak = BackBreak()
		self.Speed = 0
		self.MaxSpeed = 40
		self.MinSpeed = 0

	def ChangeSpeed(self):
		print("1. Speed up 2. Brake")
		ans = int(input("Type here: "))
		if ans == 1:
			#додати швидкості
			self.throttle.SetKind("gas")
			if self.throttle.PressedState == False:
				self.throttle.SetState()
			self.Speed = self.Speed + 5
			if self.Speed >= self.MaxSpeed:
				self.Speed = self.MaxSpeed
			print("Current speed is: "+str(self.Speed)+" km/h")
			par = ""
			while par != "no":
				print("Go faster? (yes / no)")
				par = str(input("Type here: "))
				if par == "yes":
					self.Speed = self.Speed + 5
					if self.Speed >= self.MaxSpeed:
						self.Speed = self.MaxSpeed
					print("Current speed is: "+str(self.Speed)+" km/h")
				elif par == "no":
					self.throttle.SetState()
					break
				else:
					print("Error.")
			return self.Speed
		if ans == 2:
			#гальмувати
			print("Use 1.Throttle or 2.Back brake")
			var = int(input("Type here: "))
			if var == 1:
				#гальмувати за допомогою тросику
				self.throttle.SetKind("brake")
				if self.throttle.PressedState == False:
					self.throttle.SetState()
				self.Speed = self.Speed - 5
				print("Current speed is: "+str(self.Speed)+" km/h")
				if self.Speed <= self.MinSpeed:
					self.Speed = self.MinSpeed
				par = ""
				while par != "no":
					print("Go slower? (yes / no)")
					par = str(input("Type here: "))
					if par == "yes":
						self.Speed = self.Speed - 5
						if self.Speed <= self.MinSpeed:
							self.Speed = self.MinSpeed
						print("Current speed is: "+str(self.Speed)+" km/h")
					elif par == "no":
						self.throttle.SetState()
						break
					else:
						print("Error.")
			elif var == 2:
				#гальмувати за допомогою заднього гальма
				if self.backbreak.PressedState == False:
					self.backbreak.SetState()
				self.Speed = self.Speed - 5
				if self.Speed <= self.MinSpeed:
					self.Speed = self.MinSpeed
				print("Current speed is: "+str(self.Speed)+" km/h")
				par = ""
				while par != "no":
					print("Go slower? (yes / no)")
					par = str(input("Type here: "))
					if par == "yes":
						self.Speed = self.Speed - 5
						if self.Speed <= self.MinSpeed:
							self.Speed = self.MinSpeed
						print("Current speed is: "+str(self.Speed)+" km/h")
					elif par == "no":
						self.throttle.SetState()
						break
					else:
						print("Error.")

	def GetSpeed(self):
		print("Current speed is: "+str(self.Speed)+" km/h")

class RearWheel():
	def __init__(self):
		self.State = False

	def Requirements(self):
		self.id = "3.2"
		self.diametr = '10"'
		self.material = "polyuretan"

	def SetState(self):
		if self.State:
			#print("Rear wheel is not in movement.")
			self.State = False
			return self.State
		elif not self.State:
			#print("Rear wheel is in movement.")
			self.State = True
			return self.State
		else:
			return

	def GetState(self):
		if self.State:
			print("Rear wheel is in movement.")
		elif not self.State:
			print("Rear wheel is not in movement.")
		return

class FrontWheel():
	def __init__(self):
		self.State = False
		self.Direction = "forward"

	def Requirements():
		self.id = "3.2"
		self.diametr = '10"'
		self.material = "polyuretan"

	def SetDirection(self, param, type):
		self.Direction = param
		if type == "bend":
			if param == "right":
				print("You've bent right.")
			elif param == "left":
				print("You've bent left.")
			elif param == "forward":
				print("You are moving forward.")
			return self.Direction
		else:
			if param == "right":
				print("You've turned right.")
			elif param == "left":
				print("You've turned left.")
			elif param == "forward":
				print("You are moving forward.")
			return self.Direction

	def GetDirection(self):
		print("Last chosen direction: " + str(self.Direction))

	def SetState(self):
		if self.State:
			#print("Front wheel is not in movement.")
			self.State = False
			return self.State
		elif not self.State:
			#print("Front wheel is in movement.")
			self.State = True
			return self.State
		else:
			return
	
	def GetState(self):
		if self.State:
			print("Front wheel is in movement.")
		elif not self.State:
			print("Front wheel is not in movement.")
		return

class MovementSystem():
	def __init__(self):
		self.IsMoving = False
		self.rearwheel = RearWheel()
		self.frontwheel = FrontWheel()

	def SetMovement(self):
		if self.IsMoving:
			if self.rearwheel.State == True and self.frontwheel.State == True:
				print("Stopped moving.")
				self.rearwheel.SetState()
				self.frontwheel.SetState()
				self.IsMoving = False
			return self.IsMoving
		elif not self.IsMoving:
			if self.rearwheel.State == False and self.frontwheel.State == False:
				print("Started moving.")
				self.rearwheel.SetState()
				self.frontwheel.SetState()
				self.IsMoving = True
			return self.IsMoving
		else:
			return

	def GetMovement(self):
		if self.IsMoving:
			print("Is moving.")
		elif not self.IsMoving:
			print("Not moving.")
		else:
			return

class Direction():
	def __init__(self):
		self.Direction = "forward"
		self.frontwheel = FrontWheel()
		self.sw = SteeringWheel()

	def SetDirection(self, type):
		ans = 100
		param = type
		while ans != 0:
			print("How do you want to move next?")
			print("1.Turn right 2.Turn left 3.Move forward 0.Don't turn")
			ans = int(input("Type here: "))
			if ans == 1:
				self.Direction = "right"
				self.frontwheel.SetDirection(self.Direction, param)
				self.sw.Direction = "right"
				return self.Direction, self.sw.Direction
			elif ans == 2:
				self.Direction = "left"
				self.frontwheel.SetDirection(self.Direction, param)
				self.sw.Direction = "left"
				return self.Direction, self.sw.Direction
			elif ans == 3:
				self.Direction = "forward"
				self.frontwheel.SetDirection(self.Direction, param)
				self.sw.Direction = "forward"
				return self.Direction, self.sw.Direction
			elif ans == 0:
				return	
		while ans != 0:
			print("How do you want to move next?")
			print("1.Turn right 2.Turn left 3.Move forward 0.Don't turn")
			ans = int(input("Type here: "))
			if ans == 1:
				self.Direction = "right"
				self.frontwheel.SetDirection(self.Direction)
				self.sw.Direction = "right"
				return self.Direction, self.sw.Direction
			elif ans == 2:
				self.Direction = "left"
				self.frontwheel.SetDirection(self.Direction)
				self.sw.Direction = "left"
				return self.Direction, self.sw.Direction
			elif ans == 3:
				self.Direction = "forward"
				self.frontwheel.SetDirection(self.Direction)
				self.sw.Direction = "forward"
				return self.Direction, self.sw.Direction
			elif ans == 0:
				return

	def GetDirection(self):
		if self.Direction == "right":
			print("Last chosen direction: " + str(self.Direction))
		elif self.Direction == "left":
			print("Last chosen direction: " + str(self.Direction))
		elif self.Direction == "forward":
			print("Last chosen direction: " + str(self.Direction))
		return

class Display():
	def __init__(self):
		self.Display = False

	def Requirementrs(self):
		self.id = "2.1"
		self.ci_id = "2.2"
		self.type = 'LED'
		self.density = "300ppi"
		self.ci_type = "lightdiod"

	def DisplayOn(self):
		print(Fore.GREEN + 'Display downloaded.')
		for i in tqdm(range(100)):
			time.sleep(0.01)
		print(Style.RESET_ALL)
		self.Display = True
		return self.Display

	def DisplayOff(self):
		print(Fore.RED + 'Display turned off.')
		print(Style.RESET_ALL)
		self.Display = False
		return self.Display

	def GetState(self):
		if self.Display:
			print(Fore.GREEN + 'Display downloaded.')
		elif not self.Display:
			print(Fore.RED + 'Display turned off.')

class InfoSystem():
	def __init__(self):
		self.IsOn = False
		self.ChargeIndicator = False
		self.display = Display()
		self.battery = Battery()
		self.speedadjustment = SpeedAdjustment()
		self.powersupply = PowerSupply()
	
	def InfoShow(self):
		if self.IsOn:
			self.display.DisplayOff()
			self.IsOn = False
			return self.IsOn
		elif not self.IsOn:
			self.display.DisplayOn()
			self.IsOn = True
			return self.IsOn
		else:
			return

	def ciOn(self):
		if self.powersupply.PowerConnection:
			self.ChargeIndicator = True
			return self.ChargeIndicator
		else:
			return

	def ciOff(self):
		if not self.powersupply.PowerConnection:
			self.ChargeIndicator = True
			return self.ChargeIndicator
		else:
			return

class ElectricScooter():
	def __init__(self):
		self.powersupply = PowerSupply()
		self.speedadjustment = SpeedAdjustment()
		self.customization = Customization()
		self.direction = Direction()
		self.movementsystem = MovementSystem()
		self.infosystem = InfoSystem()

class Person():
	def __init__(self):
		self.name = "User"
		self.electricscooter = ElectricScooter()

	def ScooterTurnOn(self):
		if self.electricscooter.customization.deck.state == False:
			self.electricscooter.customization.deck.GetState()
			return
		else:
			self.electricscooter.powersupply.PowerOn()
	
	def ScooterTurnOff(self):
		self.electricscooter.powersupply.PowerOff()
		self.electricscooter.speedadjustment.Speed = 0
		return self.electricscooter.speedadjustment.Speed

	
	def ChangeDirection(self):
		self.electricscooter.direction.GetDirection()
		if self.electricscooter.movementsystem.IsMoving == True:
			self.electricscooter.direction.SetDirection("type")
		else:
			self.electricscooter.movementsystem.GetMovement()

	def StartMoving(self):
		if (self.electricscooter.powersupply.Power == True 
		and self.electricscooter.customization.step.state == False 
		and self.electricscooter.customization.deck.state == True
		and self.electricscooter.powersupply.PowerConnection == False
		and self.electricscooter.movementsystem.IsMoving == False):
			self.electricscooter.movementsystem.SetMovement()
			self.electricscooter.speedadjustment.Speed = 5
			return self.electricscooter.speedadjustment.Speed

		elif self.electricscooter.customization.deck.state == False:
			self.electricscooter.customization.deck.GetState()
			return
		elif self.electricscooter.powersupply.Power == False:
			print("Engine is turned off.")
			return
		elif self.electricscooter.customization.step.state == True:
			self.electricscooter.customization.GetStateStep()
			return
		elif self.electricscooter.powersupply.PowerConnection == True:
			self.electricscooter.powersupply.GetPowerConnection()
			return
		elif self.electricscooter.movementsystem.IsMoving == True:
			self.electricscooter.movementsystem.GetMovement()
			return
		else:
			return

	def StopMoving(self):
		if self.electricscooter.movementsystem.IsMoving == True:
			self.electricscooter.movementsystem.SetMovement()
			self.electricscooter.speedadjustment.Speed = 0
			return self.electricscooter.speedadjustment.Speed
		else:
			return

	def ChangeSpeed(self):
		if (self.electricscooter.powersupply.Power == True
		and self.electricscooter.movementsystem.IsMoving == True):
			self.electricscooter.speedadjustment.ChangeSpeed()
			return
		elif self.electricscooter.powersupply.Power == False:
			print("Engine is turned off.")
			return
		elif self.electricscooter.movementsystem.IsMoving == False:
			self.electricscooter.movementsystem.GetMovement()
			return
		else:
			return

	def ShowScooterState(self):
		if (self.electricscooter.powersupply.Power == True
		and self.electricscooter.infosystem.IsOn == False):
			self.electricscooter.infosystem.InfoShow()
			print("Battery level: " + str(self.electricscooter.powersupply.battery.BatteryLevel) + "%")
			if self.electricscooter.powersupply.PowerConnection:
				self.electricscooter.infosystem.ciOn()
				self.electricscooter.powersupply.GetPowerConnection()
			elif not self.electricscooter.powersupply.PowerConnection:
				self.electricscooter.infosystem.ciOff()
				self.electricscooter.powersupply.GetPowerConnection()
			print("Current speed: " + str(self.electricscooter.speedadjustment.Speed) + " km/h")
			#print("State: " + self.electricscooter.movementsystem.GetMovement())
			self.electricscooter.movementsystem.GetMovement()	
			return

		if (self.electricscooter.powersupply.Power == True
		and self.electricscooter.infosystem.IsOn == True):
			print("Do you want to turn off the display? (y/n)")
			ans = str(input("Type here: "))
			if ans == "y":
				self.electricscooter.infosystem.InfoShow()
			else:
				print("Battery level: " + str(self.electricscooter.powersupply.battery.BatteryLevel) + "%")
				if self.electricscooter.powersupply.PowerConnection:
					self.electricscooter.infosystem.ciOn()
					self.electricscooter.powersupply.GetPowerConnection()
				elif not self.electricscooter.powersupply.PowerConnection:
					self.electricscooter.infosystem.ciOff()
					self.electricscooter.powersupply.GetPowerConnection()
				print("Current speed: " + str(self.electricscooter.speedadjustment.Speed) + " km/h")
				self.electricscooter.movementsystem.GetMovement()
				return

		elif (self.electricscooter.powersupply.Power == False
		and self.electricscooter.infosystem.IsOn == True):
			self.electricscooter.infosystem.IsOn == False
			return self.electricscooter.infosystemIsOn

		elif (self.electricscooter.powersupply.Power == False):
			print("Engine is turned off.")
			return
		
		else:
			return

	def AdjustSWLevel(self):
		self.electricscooter.customization.sw.GetSWLevel()
		print("Do you want to change it? (y/n)")
		ans = str(input("Type here: "))
		if ans == "y":
			self.electricscooter.customization.sw.SetSWLevel()
			return
		elif ans == "n":
			return
		else:
			return

	def AdjustStep(self):
		self.electricscooter.customization.GetStateStep()
		print("Do you want to change it? (y/n)")
		ans = str(input("Type here: "))
		if ans == "y":
			self.electricscooter.customization.SetStateStep()
			return
		elif ans == "n":
			return
		else:
			return

	def ChargeScooterBattery(self):
		if (self.electricscooter.movementsystem.IsMoving == False
		and self.electricscooter.powersupply.PowerConnection == False):
			self.electricscooter.powersupply.battery.GetBatteryLevel()
			print("Do you want to charge? (y/n)")
			ans = str(input("Type here: "))
			if ans == "y":
				self.electricscooter.powersupply.SetPowerConnection()
				return
			elif ans == "n":
				return
			else:
				return
		elif self.electricscooter.movementsystem.IsMoving == True:
			self.electricscooter.movementsystem.GetMovement()
			return

		elif (self.electricscooter.movementsystem.IsMoving == False
		and self.electricscooter.powersupply.PowerConnection == True):
			self.electricscooter.powersupply.battery.GetBatteryLevel()
			print("Do you want to stop charging? (y/n)")
			ans = str(input("Type here: "))
			if ans == "y":
				self.electricscooter.powersupply.SetPowerConnection()
				return
			elif ans == "n":
				return
			else:
				return
		else:
			return

	def PushScooter(self):
		if (self.electricscooter.customization.step.state == False 
		and self.electricscooter.customization.deck.state == True
		and self.electricscooter.powersupply.PowerConnection == False
		and self.electricscooter.customization.deck.state == True):
			self.electricscooter.speedadjustment.Speed = random.randrange(2,7)
			if self.electricscooter.movementsystem.IsMoving == False:
				self.electricscooter.movementsystem.SetMovement()
			print("You are pushing with speed: "+str(self.electricscooter.speedadjustment.Speed) + "km/h")
			return self.electricscooter.speedadjustment.Speed, self.electricscooter.movementsystem.IsMoving
		elif (self.electricscooter.movementsystem.IsMoving == True
			and self.electricscooter.speedadjustment.Speed >= 10):
			self.electricscooter.movementsystem.GetMovement()
			return
		elif self.electricscooter.customization.deck.state == False:
			self.electricscooter.customization.deck.GetState()
			return
		elif self.electricscooter.customization.step.state == True:
			self.electricscooter.customization.GetStateStep()
			return
		elif self.electricscooter.powersupply.PowerConnection == True:
			self.electricscooter.powersupply.GetPowerConnection()
			return
		elif self.electricscooter.customization.deck.state == False:
			self.electricscooter.customization.deck.GetState()
			return
		else:
			return

	def Deviate(self):
		self.electricscooter.direction.GetDirection()
		if self.electricscooter.movementsystem.IsMoving == True:
			self.electricscooter.direction.SetDirection("bend")
		else:
			self.electricscooter.movementsystem.GetMovement()

def main():
	electricscooter = ElectricScooter()
	person = Person()

	print("""
            ==,
             _| 
            (_|=<
 ___         _|
',-.\       /,|.
: o :=======: o :
 `-'         `-'
""")
	print("Write 'h' for help.")
	while True:
		ans = str(input("Type here: "))
		if ans == 'h' or ans == 'help':
			print(
"""
0. Customize
1. Engine control (turn on/off)
2. Movement control (start/stop moving)(electric or pushing)
3. Speed control (faster/slower)
4. Direction control (turn left right forward)
4.1 Deviate
5. Charging control
6. Information control
7. Dismantle
""")

		if ans == "0":
			if (person.electricscooter.movementsystem.IsMoving == False
			and person.electricscooter.customization.deck.state == True):
				person.AdjustSWLevel()
				print("")
				person.AdjustStep()
				print("")
			elif person.electricscooter.customization.deck.state == False:
				person.electricscooter.customization.deck.GetState()
				print("")
				return
			else:
				print("You can't do it in movement!\n")

		elif ans == "1":
			if person.electricscooter.powersupply.Power:
				person.ScooterTurnOff()
			else:
				person.ScooterTurnOn()

		elif ans == "2":
			if not person.electricscooter.movementsystem.IsMoving:
				print("Do you want to move with battery charge or push? (1/2)")
				param = int(input("Type here: "))
				if param == 1:
					person.StartMoving()
					print("")
				elif param == 2:
					person.PushScooter()
					print("")
				else:
					return
			elif person.electricscooter.movementsystem.IsMoving:
				person.StopMoving()
				print("")

		elif ans == "3":
			person.ChangeSpeed()
			print("")

		elif ans == "4.1":
			person.Deviate()
			print("")

		elif ans == "4":
			person.ChangeDirection()
			print("")
		
		elif ans == "5":
			person.ChargeScooterBattery()
			print("")

		elif ans == "6":
			person.ShowScooterState()
			print("")

		elif ans == "7":
			person.electricscooter.customization.deck.SetState()
			print("")


if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		print('\n\nThanks. Good luck!')

