import sys

def main():
    while True:
        print("\n=================================")
        print("     JOB INTELLIGENCE SYSTEM     ")
        print("=================================")
        print("1. Search Jobs")
        print("2. View Recent Jobs")
        print("3. Search Jobs by Skill")
        print("4. Search Jobs by Company")
        print("5. View Job Statistics")
        print("6. Exit")
        
        choice = input("Enter choice: ")
        
        if choice == '1':
            print("Running job search pipeline... (To be implemented)")
        elif choice == '5':
            print("Running analytics report... (To be implemented)")
        elif choice == '6':
            print("Exiting...")
            sys.exit(0)
        else:
            print("Invalid choice, please try again.")

if __name__ == '__main__':
    main()
