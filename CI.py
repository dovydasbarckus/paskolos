from tkinter import *
from tkinter import messagebox
from tkinter.simpledialog import askstring
from send_email import SendEmail
from loan import Loan
import pandas as pd
import pickle
import logging

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler('logger.log')
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


class CommunicationInterface:
    def __init__(self):
        self.loans = []
        logger.info(f"Program has started")

    def show_Tkinter(self):

        my_screen = Tk()
        my_screen.title("Green Loans")
        my_screen.geometry("350x450")
        my_screen.iconbitmap(r'books.ico')

        variable1 = StringVar()
        variable2 = StringVar()
        variable3 = StringVar()

        my_screen.columnconfigure(0, weight=1)
        my_screen.columnconfigure(1, weight=3)
        my_screen.columnconfigure(2, weight=3)

        greeting = Label(my_screen, text="Green Loans for your Success", font=('Helvetica bold', 15), anchor="center")
        greeting.grid(row=1, columnspan=3, pady=10)

        amount = Label(my_screen, text="Enter your wanted loan amount € :")
        amount.grid(row=2, column=0, sticky=E, padx=10, pady=5)
        amount_field = Entry(my_screen, textvariable=variable1)
        amount_field.grid(row=2, column=1, pady=5, sticky=E)
        period = Label(my_screen, text="Time period in months :")
        period.grid(row=3, column=0, sticky=E, padx=10, pady=5)
        period_field = Entry(my_screen, textvariable=variable2)
        period_field.grid(row=3, column=1, pady=5, sticky=E)
        interest = Label(my_screen, text="Interest % :")
        interest.grid(row=4, column=0, sticky=E, padx=10, pady=5)
        interest_field = Entry(my_screen, textvariable=variable3)
        interest_field.grid(row=4, column=1, pady=5, sticky=E)

        button_submit = Button(my_screen, text="Submit",
                               command=lambda: self.adding(variable1, variable2, variable3))
        button_submit.grid(row=5,  columnspan=3, padx=30, pady=30, ipady=5, sticky=NS + EW)

        button_check = Button(my_screen, text="Check Loan and Save",
                               command=lambda: self.check())
        button_check.grid(row=6, columnspan=3, padx=30, ipady=5, sticky=NS + EW)

        meniu = Menu(my_screen)
        my_screen.config(menu=meniu)
        submeniu = Menu(meniu, tearoff=0)
        meniu.add_cascade(label="Meniu", menu=submeniu)
        submeniu.add_command(label="Show All Data", command=lambda: self.show_list())
        submeniu.add_command(label="Delete Data", command=lambda: self.delete())
        submeniu.add_command(label="Send Email", command=lambda: self.send())
        submeniu.add_separator()
        submeniu.add_command(label="Close", command=my_screen.destroy)
        my_screen.bind("<Escape>", lambda event: my_screen.destroy())
        my_screen.resizable(False, False)

        my_screen.mainloop()
        logger.info(f"Program has ended")

    def adding(self, variable1, variable2, variable3):
        try:
            n1 = float(variable1.get())
            n2 = float(variable2.get())
            n3 = float(variable3.get())
            self.loans.append(Loan(n1, n2, n3))
            variable1.set("")
            variable2.set("")
            variable3.set("")

        except ValueError:
            messagebox.showinfo("Opps Error", f"Field or fields having not a number\n"
                                             f"Check fields with wrong values")
            logger.exception("Entered invalid Value")

    def check(self):
        results = self.loans[-1]
        amount = results.amount
        period = results.period
        interest = results.interest
        total_interests = results.total_interests
        columns = results.columns
        new_row = results.new_row
        messagebox.showinfo("Loan Information", f"Loan: {amount} €\n"
                                                      f"Months: {round(period)}\n"
                                                      f"Percentages: {interest} %\n"
                                                      f"Total Interests: {round(sum(total_interests), 2)} €\n"
                                                      f"Total Sum To Pay: {amount + round(sum(total_interests), 2)} €\t\t\t")

        self.my_table(columns, new_row, results)

    def my_table(self, columns, new_row, results):
        data1 = pd.DataFrame(columns)
        data2 = pd.DataFrame(new_row)
        data = pd.concat([data1, data2], axis=0)
        print(data)
        answer = str(askstring(f"Saving File to CSV",
                               "Do you want to save file? Yes or No?: \t\t\t").lower())
        if answer == "yes":
            answer2 = str(askstring(f"File Name",
                                    "Write your file name: \t\t\t").lower())
            my_csv = f"Loan.{answer2}.csv"
            data.to_csv(f"{my_csv}", index=False, encoding="UTF-8")
            self.add_to_db(results)


    def release_db(self):
        try:
            with open(f"data.pkl", 'rb') as file:
                self.loans = pickle.load(file)
        except FileNotFoundError:
            with open(f"data.pkl.", 'wb') as file:
                all_data = self.loans
                pickle.dump(all_data, file)

    def add_to_db(self, results):
        with open(f"data.pkl", 'rb') as file:
            info = pickle.load(file)
            with open(f"data.pkl", 'wb') as file:
                info.append(results)
                pickle.dump(info, file)
                logger.info(f"Added new item to DataBase")

    def show_list(self):

        try:
            if len(self.loans) != 0:
                answer = int(askstring(f"There is/are {len(self.loans)}",
                                       "Write number, what Loans data you want! \t\t\t"))
                my_loan = self.loans[answer - 1]
                messagebox.showinfo("Loan Information", f"Loan: {my_loan.amount} €\n"
                                                        f"Months: {my_loan.period}\n"
                                                        f"Percentages: {my_loan.interest} %\n"
                                                        f"Total Interests: {round(sum(my_loan.total_interests), 2)} €\n"

                                                        f"Total Sum To Pay: {my_loan.amount + round(sum(my_loan.total_interests), 2)} €\t\t\t")
                self.my_table(my_loan.columns, my_loan.new_row, my_loan)

            else:
                messagebox.showinfo("Oops Error", "No current saved data!")
        except:
            messagebox.showinfo("Oops Error", "Canceled or Given value doesn't exist, try again!")
            logger.exception("Entered invalid Value")

    def delete(self):
        try:
            answer = int(askstring(f"There is/are {len(self.loans)}",
                                   "Write number, what Loans you want delete? \t\t\t"))
            del self.loans[answer - 1]
            with open(f"data.pkl", 'wb') as file:
                pickle.dump(self.loans, file)
        except:
            messagebox.showinfo("Oops Error", "Canceled or Given value doesn't exist, try again!")
            logger.exception("Entered invalid Value")

    def send(self):
        try:
            answer = int(askstring(f"There is/are {len(self.loans)}",
                                   "What Loan you want to send? \t\t\t"))
            loan = self.loans[answer - 1]
            write_email = str(askstring(f"Sender Email Address",
                                   "Write your email: \t\t\t").lower())
            write_to_email = str(askstring(f"Receiver Email Address",
                                   "Write receiver email: \t\t\t").lower())
            write_password = str(askstring(f"Your Email Password",
                                   "Write your password: \t\t\t").lower())

            SendEmail(loan, write_email, write_password, write_to_email)
            logger.info(f"Sended Loan information via Email")
        except:
            messagebox.showinfo("Oops Error", "Canceled or Given values do not match or invalid values, try again!")
            logger.exception("Entered invalid Value")





