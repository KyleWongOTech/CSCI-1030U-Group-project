def get_user_pref() -> list[list[str]]:
    days = ["Monday ", "Tuesday ", "Wednesday ", "Thursday ", "Friday "]
    pref = []

    print ("Time of day prefrences")
    print( "1. Moring (8:00- 12:00)")
    print("2. Afternoon (12:00 - 16:00)")
    print("3. Evening (16:00 - 20:00)")
    print("4. No preference")


    for i in range(len(days)):
        while True:
            choose = input(f"Please choose from 1-4 for {days[i]}")

            if choose == "1":
                pref.append([days[i], "Morning"])
                break

            elif choose == "2":
                pref.append([days[i], "Afternoon"])
                break

            elif choose == "3":
                pref.append([days[i], "Evening"])
                break

            elif choose == "4":
                pref.append([days[i], "Any"])
                break

            else:
                print("Not a valid choice.")


    return pref
            
user_pref=get_user_pref()
print(user_pref)