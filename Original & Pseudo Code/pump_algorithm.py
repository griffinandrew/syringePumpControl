from time import sleep

rate = get.fromGUI				# Get pump rate from GUI
t_step = set.fromProgrammer		# Set t_step to arbitrary value (ideally <0.5)

# Constant volume pumped during an un-interrupted time step
pump_step = rate * t_step * (1/60)

# Init global command variables
com_cur = 0
com_prev = 0

# Init global pump position variables
pos_cur = 0
pos_prev = 0

# Init global inflation attribute
isInflating = False

# Activate GUI
isPlay = True

# Iterate through loop while GUI is active
while isPlay:

	sleep(t_step) # Iterate every t_step seconds

	com_cur = get.fromGUI # Get current command input from GUI

	if not isInflating:
		# Process from previous time step is finished

		pos_cur = com_prev # Current pump idling position

		Pump(com_cur - pos_cur)	# Actuate pump

		# Set current parameters to previous
		com_prev = com_cur
		pos_prev = pos_cur

	else:
		# Process is still occurring. Figure out the remainder necessary to pump.

		pos_cur = pos_prev + pump_step # Current pump actuating position

		Pump(com_cur - pos_cur)	# Actuate pump

		# Set current parameters to previous
		com_prev = com_cur
		pos_prev = pos_cur

	if com_cur - pos_cur <= pump_step:
		isInflating = False

	else:
		isInflating = True
