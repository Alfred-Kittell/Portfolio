using System;
using System.Windows;
using System.Windows.Media;

namespace AccountControl.Windows
{
    /// <summary>
    /// Interaction logic for AuthWindow.xaml
    /// </summary>
    public partial class AuthWindow : Window
    {
        public string login = "admin";
        public string password = "test";

        // #################################################################################

        /// <summary>
        /// Initializes a new instance of the class <see cref="AuthWindow"/>.
        /// Authorization and login window
        /// </summary>
        public AuthWindow()
        {
            InitializeComponent();
        }

        // #################################################################################

        /// <summary>
        /// Button - authorization
        /// </summary>
        private void AuthClick(object sender, RoutedEventArgs e)
        {
            if (loginBox.Text == login && passBox.Text == password)
            {
                MainWindow main = new MainWindow();
                main.Show();
                Close();
            }
            else
            {
                loginButt.BorderBrush = new SolidColorBrush(Colors.Red);
            }
        }
    }
}
