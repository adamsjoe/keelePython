def eval_loop():
    
    result = None # variable to handle the result
    while True:  # while true means this always runs
        userInput = input("please enter your expression or 'done' to quit: ")  # provide instruction
        if userInput.lower() == "done": # convert the input to lowercase and check if it is "done"
            break # if so, break out the loop
        result = eval(userInput) # do the evaluation and store result
        print(result) # print the result
    
eval_loop() # initiate program


