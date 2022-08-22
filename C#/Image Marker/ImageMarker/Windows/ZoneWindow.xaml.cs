using System;
using System.Collections.Generic;
using System.Windows;
using System.Windows.Controls;

using ImageMarker.Classes;

namespace ImageMarker.Windows
{
    /// <summary>
    /// Interaction logic for ZoneWindow.xaml
    /// </summary>
    public partial class ZoneWindow : Window
    {
        private MainWindow mainWindow;
        private Zone zone;
        private Zone clone;

        // #################################################################################

        /// <summary>
        /// Initializes a new instance of the class <see cref="ZoneWindow"/>.
        /// Zone card
        /// </summary>
        public ZoneWindow(MainWindow mainWindow, Zone zone)
        {
            InitializeComponent();

            this.mainWindow = mainWindow;
            this.zone = zone;
            this.clone = zone.Clone();

            mainTagBox.Text = zone.MainTag;
            sideTagBox.Text = zone.SideTag;
            nameBox.Text = zone.Name;
            visibleBox.IsChecked = zone.IsVisible;
        }

        // #################################################################################

        /// <summary>
        /// Event - text change 
        /// </summary>
        private void Text_Changed(object sender, TextChangedEventArgs e)
        {
            TextBox s = sender as TextBox;

            switch (s.Name)
            {
                case "mainTagBox":
                    clone.MainTag = s.Text;
                    break;
                case "sideTagBox":
                    clone.SideTag = s.Text;
                    break;
                case "nameBox":
                    clone.Name = s.Text;
                    break;
                case "additionalBox":
                    clone.Description = s.Text;
                    break;
            }
        }

        /// <summary>
        /// Button - saving changes
        /// </summary>
        private void Cancel_Click(object sender, RoutedEventArgs e)
        {
            clone.MainTag = zone.MainTag;
            clone.SideTag = zone.SideTag;
            clone.Name = zone.Name;
            clone.Description = zone.Description;
            clone.IsVisible = zone.IsVisible;

            mainTagBox.Text = zone.MainTag;
            sideTagBox.Text = zone.SideTag;
            nameBox.Text = zone.Name;
            additionalBox.Text = zone.Description;
            visibleBox.IsChecked = zone.IsVisible;
        }

        /// <summary>
        /// Button - saving changes
        /// </summary>
        private void Save_Click(object sender, RoutedEventArgs e)
        {
            zone.MainTag = clone.MainTag;
            zone.SideTag = clone.SideTag;
            zone.Name = clone.Name;
            zone.Description = clone.Description;
            zone.IsVisible = clone.IsVisible;
            zone.RenameSelectionBox(clone.Name);

            mainWindow.AccountUpdate(zone);
            Close();
        }
    }
}
