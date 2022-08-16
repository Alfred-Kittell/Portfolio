using System;
using System.Windows;
using System.Windows.Controls;
using AccountControl.Classes;

namespace AccountControl.Windows
{
    /// <summary>
    /// Interaction logic for AccountWindow.xaml
    /// </summary>
    public partial class AccountWindow : Window
    {
        private readonly MainWindow main;
        private readonly Account account;
        private int selectData = 0;

        // #################################################################################

        /// <summary>
        /// Initializes a new instance of the class <see cref="AccountWindow"/>.
        /// Account card
        /// </summary>
        /// <param name="main">Link to main menu</param>
        /// <param name="account">Account details</param>
        public AccountWindow(MainWindow main, Account account)
        {
            InitializeComponent();

            this.main = main;
            this.account = account;

            firstTagBox.Text = account.MainTag;
            secondTagBox.Text = account.SideTag;
            nameBox.Text = account.Name;

            if (account.data.Count == 0)
            {
                Create_Click(null, null);
            }
            else
            {
                DisplayInfo();
            }
        }

        // #################################################################################

        #region Operations with fields

        /// <summary>
        /// Account data output
        /// </summary>
        private void DisplayInfo()
        {
            mailBox.Text = account.data[selectData].Mail;
            loginBox.Text = account.data[selectData].Login;
            passwordBox.Text = account.data[selectData].Password;
            additionalBox.Text = account.data[selectData].Additional;

            countBox.Content = selectData + 1 + "/" + account.data.Count;
        }

        /// <summary>
        /// Event - text change 
        /// </summary>
        private void Text_Changed(object sender, TextChangedEventArgs e)
        {
            if (account.data.Count < 1)
            {
                return;
            }

            TextBox s = sender as TextBox;

            switch (s.Name)
            {
                case "firstTagBox":
                    account.MainTag = s.Text;
                    break;
                case "secondTagBox":
                    account.SideTag = s.Text;
                    break;
                case "nameBox":
                    account.Name = s.Text;
                    break;
                case "mailBox":
                    account.data[selectData].Mail = s.Text;
                    break;
                case "loginBox":
                    account.data[selectData].Login = s.Text;
                    break;
                case "passwordBox":
                    account.data[selectData].Password = s.Text;
                    break;
                case "additionalBox":
                    account.data[selectData].Additional = s.Text;
                    break;
            }
        }

        /// <summary>
        /// Button - copy field to clipboard
        /// </summary>
        private void Copy_Click(object sender, RoutedEventArgs e)
        {
            Button s = sender as Button;

            switch (s.Name)
            {
                case "mailCopy":
                    Clipboard.SetText(mailBox.Text);
                    break;
                case "loginCopy":
                    Clipboard.SetText(loginBox.Text);
                    break;
                case "passwordCopy":
                    Clipboard.SetText(passwordBox.Text);
                    break;
            }
        }

        #endregion Operations with fields

        // #################################################################################

        #region Toolbar

        /// <summary>
        /// Button - shift variant to the left
        /// </summary>
        private void Left_Click(object sender, RoutedEventArgs e)
        {
            if (account.data.Count < 1)
            {
                return;
            }

            selectData = (selectData - 1) < 0 ? account.data.Count - 1 : selectData - 1;

            DisplayInfo();
        }

        /// <summary>
        /// Button - shift variant to the right
        /// </summary>
        private void Right_Click(object sender, RoutedEventArgs e)
        {
            if (account.data.Count < 1)
            {
                return;
            }

            selectData = (selectData + 1) > account.data.Count - 1 ? 0 : selectData + 1;

            DisplayInfo();
        }

        /// <summary>
        /// Button - new variant
        /// </summary>
        private void Create_Click(object sender, RoutedEventArgs e)
        {
            account.data.Add(new AccountData());
            selectData = account.data.Count - 1;

            DisplayInfo();
        }

        /// <summary>
        /// Button - delete variant
        /// </summary>
        private void Delete_Click(object sender, RoutedEventArgs e)
        {
            if (account.data.Count < 2)
            {
                return;
            }

            account.data.RemoveAt(selectData);
            if (selectData >= account.data.Count)
            {
                selectData = Math.Max(account.data.Count - 1, 0);
            }

            DisplayInfo();
        }

        /// <summary>
        /// Button - saving changes
        /// </summary>
        private void Save_Click(object sender, RoutedEventArgs e)
        {
            main.AccountUpdate(account);
            Close();
        }

        #endregion Toolbar

    }
}
