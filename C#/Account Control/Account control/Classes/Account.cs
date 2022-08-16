using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.ComponentModel;

namespace AccountControl.Classes
{
    /// <summary>
    /// Main class for storing account data
    /// </summary>
    public class Account : INotifyPropertyChanged, IComparable
    {
        /// <summary>
        /// Main group tag
        /// </summary>
        public string MainTag
        {
            get => _mainTag;
            set
            {
                if (value != _mainTag)
                {
                    _mainTag = value;
                    NotifyPropertyChanged("MainTag");
                }
            }

        }
        private string _mainTag;

        /// <summary>
        /// Side group tag
        /// </summary>
        public string SideTag
        {
            get => _sideTag;
            set
            {
                if (value != _sideTag)
                {
                    _sideTag = value;
                    NotifyPropertyChanged("SideTag");
                }
            }
        }
        private string _sideTag;

        /// <summary>
        /// Account name
        /// </summary>
        public string Name
        {
            get => _name;
            set
            {
                if (value != _name)
                {
                    _name = value;
                    NotifyPropertyChanged("Name");
                }
            }
        }
        private string _name;

        /// <summary>
        /// Input variants
        /// </summary>
        public List<AccountData> data = new List<AccountData>();

        // #################################################################################

        public event PropertyChangedEventHandler PropertyChanged;

        public void NotifyPropertyChanged(string propertyName)
        {
            if (PropertyChanged != null)
            {
                PropertyChanged(this, new PropertyChangedEventArgs(propertyName));
            }
        }

        public int CompareTo(object obj)
        {
            Account o = obj as Account;

            int first = _mainTag.CompareTo(o._mainTag);
            if (first == 0)
            {
                int second = _sideTag.CompareTo(o._sideTag);
                if (second == 0) return _name.CompareTo(o._name);
                else return second;
            }
            else return first;
        }

        /// <summary>
        /// Clone an account
        /// </summary>
        /// <returns>Full copy of the account</returns>
        public Account Clone()
        {
            Account clone = new Account
            {
                MainTag = _mainTag,
                SideTag = _sideTag,
                Name = _name,
            };

            foreach (var item in data)
            {
                clone.data.Add(new AccountData()
                {
                    Mail = item.Mail,
                    Login = item.Login,
                    Password = item.Password,
                    Additional = item.Additional,
                });
            }

            return clone;
        }
    }

    /// <summary>
    /// Dynamic collection of accounts
    /// </summary>
    public class Accounts : ObservableCollection<Account> { }

    /// <summary>
    /// Account Variant Data
    /// </summary>
    public class AccountData
    {
        /// <summary>
        /// Mail variant
        /// </summary>
        public string Mail { get; set; } = "";
        /// <summary>
        /// Login variant
        /// </summary>
        public string Login { get; set; } = "";
        /// <summary>
        /// Password variant
        /// </summary>
        public string Password { get; set; } = "";
        /// <summary>
        /// Additional Information variant
        /// </summary>
        public string Additional { get; set; } = "";
    }
}
