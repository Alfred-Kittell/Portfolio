using System;
using System.IO;
using System.Collections.Generic;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Input;

using AccountControl.Classes;
using TinyJson;

namespace AccountControl.Windows
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        private Accounts accounts;
        private string dataPath = "data.json";

        // #################################################################################

        /// <summary>
        /// Initializes a new instance of the class <see cref="MainWindow"/>.
        /// Main control window
        /// </summary>
        public MainWindow()
        {
            InitializeComponent();

            accounts = (Accounts)Resources["accounts"];

            AccountsLoad();
        }

        // #################################################################################

        #region Top menu bar

        /// <summary>
        /// Button - create an account.
        /// For senders with the "open" tag, opening the created account
        /// </summary>
        private void Create_Click(object sender, RoutedEventArgs e)
        {
            string tag = (sender as Button).Tag as string;

            Account account = AccountCreate("New accounts", "New");
            accounts.Add(account);
            if (tag == "open")
            {
                AccountOpen(account);
            }
        }

        /// <summary>
        /// Button - loading accounts
        /// </summary>
        private void Load_Click(object sender, RoutedEventArgs e)
        {
            AccountsLoad();
        }

        /// <summary>
        /// Button - saving accounts
        /// </summary>
        private void Save_Click(object sender, RoutedEventArgs e)
        {
            AccountsSave();
        }

        #endregion Top menu bar

        // #################################################################################

        #region Data panel

        /// <summary>
        /// Event - header generation
        /// </summary>
        private void DataGrid_AutoGeneratingColumn(object sender, DataGridAutoGeneratingColumnEventArgs e)
        {
            switch (e.Column.Header.ToString())
            {
                case "Name":
                    e.Column.Header = "Name";
                    break;
                default:
                    e.Column.Visibility = Visibility.Hidden;
                    break;
            }
        }

        /// <summary>
        /// Event - double click on a row
        /// </summary>
        private void Row_DoubleClick(object sender, MouseButtonEventArgs e)
        {
            DataGridRow row = sender as DataGridRow;
            Account item = row.Item as Account;

            AccountOpen(item);
        }

        #endregion Data panel

        // #################################################################################

        #region Data Panel Context Menu

        /// <summary>
        /// Context button - creating an account with a main tag.
        /// For senders with the "open" tag, opening the created account
        /// </summary>
        private void FirstTagCreate_Click(object sender, RoutedEventArgs e)
        {
            CollectionViewGroup group = (sender as MenuItem).DataContext as CollectionViewGroup;
            string tag = (sender as MenuItem).Tag as string;
            string firstTag = group.Name as string;

            Account account = AccountCreate(firstTag, "New");
            accounts.Add(account);
            if (tag == "open")
            {
                AccountOpen(account);
            }
        }

        /// <summary>
        /// Context button - creating an account with a main and side tag.
        /// For senders with the "open" tag, opening the created account
        /// </summary>
        private void SecondTagGreate_Click(object sender, RoutedEventArgs e)
        {
            CollectionViewGroup group = (sender as MenuItem).DataContext as CollectionViewGroup;
            string tag = (sender as MenuItem).Tag as string;

            CollectionViewGroup parentgroup = group.GetType()
                .GetProperty("Parent", System.Reflection.BindingFlags.GetProperty | System.Reflection.BindingFlags.Instance | System.Reflection.BindingFlags.NonPublic)
                .GetValue(group, null) as CollectionViewGroup;

            string firstTag = parentgroup.Name as string;
            string secondTag = group.Name as string;

            Account account = AccountCreate(firstTag, secondTag);
            accounts.Add(account);
            if (tag == "open")
            {
                AccountOpen(account);
            }
        }

        /// <summary>
        /// Context button - account duplication
        /// </summary>
        private void DubAccount_Click(object sender, RoutedEventArgs e)
        {
            Account account = (sender as MenuItem).DataContext as Account;
            accounts.Add(account.Clone());
        }

        /// <summary>
        /// Context button - account deletion
        /// </summary>
        private void DelAccount_Click(object sender, RoutedEventArgs e)
        {
            Account account = (sender as MenuItem).DataContext as Account;
            accounts.Remove(account);
        }

        #endregion Data Panel Context Menu

        // #################################################################################

        #region Operations with accounts

        /// <summary>
        /// Opening an account card
        /// </summary>
        /// <param name="account">Account details</param>
        private void AccountOpen(Account account)
        {
            AccountWindow main = new AccountWindow(this, account);
            main.Show();
        }

        /// <summary>
        /// Account update. For an external call
        /// </summary>
        /// <param name="account">Account details</param>
        public void AccountUpdate(Account account)
        {
            int id = accounts.IndexOf(account);
            if (id < 0)
            {
                accounts.Add(account);
            }
            else
            {
                accounts[id] = account;
            }
        }

        /// <summary>
        /// Create an account
        /// </summary>
        /// <param name="mainTag">Filling in the main tag</param>
        /// <param name="sideTag">Filling in the side tag</param>
        /// <returns>Created account</returns>
        private Account AccountCreate(string mainTag, string sideTag)
        {
            Account account = new Account
            {
                MainTag = mainTag,
                SideTag = sideTag,
                Name = "New account"
            };

            account.data.Add(new AccountData());

            return account;
        }

        /// <summary>
        /// Loading accounts from a file
        /// </summary>
        private void AccountsLoad()
        {
            if (!File.Exists(dataPath))
            {
                return;
            }

            string fileJson = File.ReadAllText(dataPath);

            List<Account> values = fileJson.FromJson<List<Account>>();
            accounts.Clear();
            values.Sort();

            foreach (var item in values)
            {
                accounts.Add(item);
            }
        }

        /// <summary>
        /// Saving accounts to a file
        /// </summary>
        private void AccountsSave()
        {
            string json = accounts.ToJson(true);
            File.WriteAllText(dataPath, json);
        }

        #endregion Operations with accounts

        // #################################################################################

    }
}
