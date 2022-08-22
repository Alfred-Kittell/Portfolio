using System;
using System.IO;
using System.Collections.Generic;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Collections.ObjectModel;

using ImageMarker.Classes;
using TinyJson;

namespace ImageMarker.Windows
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        private string imagesPath = "Images";
        private string dataPath = "data.json";

        public Zones zones;

        // #################################################################################

        /// <summary>
        /// Initializes a new instance of the class <see cref="MainWindow"/>.
        /// Main control window
        /// </summary>
        public MainWindow()
        {
            InitializeComponent();

            zones = (Zones)Resources["zones"];

            ImgUpdate_Click(null, null);

            //CreateZones();
        }

        // #################################################################################

        #region Operations with images

        /// <summary>
        /// Button - Refreshes the list of images
        /// </summary>
        private void ImgUpdate_Click(object sender, RoutedEventArgs e)
        {
            if (!Directory.Exists(imagesPath))
            {
                return;
            }

            imgList.Items.Clear();
            string[] fileEntries = Directory.GetFiles(imagesPath);
            foreach (string path in fileEntries)
            {
                string ext = Path.GetExtension(path);
                if (ext == ".png" || ext == ".jpg")
                {
                    imgList.Items.Add(path);
                }
            }
        }

        /// <summary>
        /// Event - Upload image and output to canvas
        /// </summary>
        private void SelectImg_MouseDoubleClick(object sender, MouseButtonEventArgs e)
        {
            string imgPath = imgList.SelectedItem.ToString();

            if (!File.Exists(imgPath))
            {
                return;
            }

            dataPath = imgPath.Replace(Path.GetExtension(imgPath), ".json");
            ZonesLoad_Click(sender, e);

            BitmapImage image = new BitmapImage(new Uri(imgPath, UriKind.Relative));
            imageBox.Background = new ImageBrush(image);
            imageBox.Height = image.Height + 200;
            imageBox.Width = image.Width + 200;
            ((TileBrush)imageBox.Background).Stretch = Stretch.None;
        }

        #endregion Operations with images

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
                case "IsVisible":
                    e.Column.Header = "";
                    break;
                default:
                    e.Column.Visibility = Visibility.Hidden;
                    break;
            }
        }

        /// <summary>
        /// Event - double click on a row.
        /// Opens or changes the visibility of a zone
        /// </summary>
        private void DataGridRow_DoubleClick(object sender, MouseButtonEventArgs e)
        {
            DataGridRow row = sender as DataGridRow;
            Zone zone = row.Item as Zone;

            if ((bool)openCheckBox.IsChecked)
            {
                zone.Open_Click(sender, e);
            }
            else
            {
                zone.IsVisible = !zone.IsVisible;
            }
        }

        #endregion Data panel

        // #################################################################################

        #region Data panel context menu

        /// <summary>
        /// Context button - creating a zone with a main and side tag.
        /// For senders with the "open" tag, opening the created zone
        /// </summary>
        private void GroupGreate_Click(object sender, RoutedEventArgs e)
        {
            CollectionViewGroup group = (sender as MenuItem).DataContext as CollectionViewGroup;
            string tag = (sender as MenuItem).Tag as string;

            CollectionViewGroup parentgroup = group.GetType()
                .GetProperty("Parent", System.Reflection.BindingFlags.GetProperty | System.Reflection.BindingFlags.Instance | System.Reflection.BindingFlags.NonPublic)
                .GetValue(group, null) as CollectionViewGroup;

            bool root = parentgroup.GetType().ToString() == "MS.Internal.Data.CollectionViewGroupRoot";
            
            string firstTag = root ? group.Name as string : parentgroup.Name as string;
            string secondTag = root ? "New" : group.Name as string;

            Zone zone = ZoneCreate(firstTag, secondTag);
            zones.Add(zone);
            if (tag == "open")
            {
                zone.Open_Click(sender, e);
            }
        }

        /// <summary>
        /// Context button - changing zone visibility for all nested objects
        /// For senders with the "show" tag, change visibility to visible
        /// </summary>
        private void GroupZoneVisibleChange_Click(object sender, RoutedEventArgs e)
        {
            CollectionViewGroup s = (sender as MenuItem).DataContext as CollectionViewGroup;
            ReadOnlyObservableCollection<object> items = s.Items;
            bool visible = ((sender as MenuItem).Tag as string) == "show";

            if (items[0].ToString() == "ImageMarker.Classes.Zone")
            {
                foreach (Zone zone in items)
                {
                    zone.IsVisible = visible;
                }
            }
            else
            {
                foreach (CollectionViewGroup item in items)
                {
                    foreach (Zone zone in item.Items)
                    {
                        zone.IsVisible = visible;
                    }
                }
            }
        }

        /// <summary>
        /// Context button - opening a zone card
        /// </summary>
        private void ZoneOpen_Click(object sender, RoutedEventArgs e)
        {
            Zone zone = (sender as MenuItem).DataContext as Zone;

            zone.Open_Click(sender, e);
        }

        /// <summary>
        /// Context button - changing zone visibility.
        /// For senders with the "show" tag, change visibility to visible
        /// </summary>
        private void ZoneVisibleChange_Click(object sender, RoutedEventArgs e)
        {
            Zone zone = (sender as MenuItem).DataContext as Zone;
            bool visible = ((sender as MenuItem).Tag as string) == "show";

            zone.IsVisible = visible;
        }

        /// <summary>
        /// Context button - zone duplication
        /// </summary>
        private void ZoneDub_Click(object sender, RoutedEventArgs e)
        {
            Zone zone = (sender as MenuItem).DataContext as Zone;

            Zone clone = zone.Clone();
            clone.CreateSelectionBox(imageBox);
            zones.Add(clone);
        }

        /// <summary>
        /// Context button - zone deletion
        /// </summary>
        private void ZoneDel_Click(object sender, RoutedEventArgs e)
        {
            Zone zone = (sender as MenuItem).DataContext as Zone;

            zone.DeleteSelectionBox();
            zones.Remove(zone);
        }

        #endregion Data panel context menu

        // #################################################################################

        #region Zones panel toolbar

        /// <summary>
        /// Button - create a zone.
        /// For senders with the "open" tag, opening the created zone
        /// </summary>
        private void ZoneCreate_Click(object sender, RoutedEventArgs e)
        {
            string tag = (sender as Button).Tag as string;

            Zone zone = ZoneCreate("New zones", "New");
            zones.Add(zone);
            if (tag == "open")
            {
                zone.Open_Click(sender, e);
            }
        }

        /// <summary>
        /// Button - loading zones from a file
        /// </summary>
        private void ZonesLoad_Click(object sender, RoutedEventArgs e)
        {
            zones.Clear();
            imageBox.Children.Clear();

            if (!File.Exists(dataPath))
            {
                return;
            }

            string fileJson = File.ReadAllText(dataPath);

            List<Zone> values = fileJson.FromJson<List<Zone>>();
            values.Sort();

            foreach (Zone item in values)
            {
                zones.Add(item);
                item.SetMainWindow(this);
                item.CreateSelectionBox(imageBox);
            }
        }

        /// <summary>
        /// Button - saving zones to a file
        /// </summary>
        private void ZonesSave_Click(object sender, RoutedEventArgs e)
        {
            string json = zones.ToJson(true);
            File.WriteAllText(dataPath, json);
        }

        #endregion Zones panel toolbar

        // #################################################################################

        #region Operations with zones

        /// <summary>
        /// Create a zone
        /// </summary>
        /// <param name="mainTag">Filling in the main tag</param>
        /// <param name="sideTag">Filling in the side tag</param>
        /// <returns>Created zone</returns>
        private Zone ZoneCreate(string mainTag, string sideTag)
        {
            Zone zone = new Zone
            {
                MainTag = mainTag,
                SideTag = sideTag,
                Name = "New zone"
            };

            zone.SetMainWindow(this);
            zone.CreateSelectionBox(imageBox);

            return zone;
        }

        /// <summary>
        /// Zone update. For an external call
        /// </summary>
        /// <param name="zone">Zone details</param>
        public void AccountUpdate(Zone zone)
        {
            int id = zones.IndexOf(zone);
            if (id < 0)
            {
                zones.Add(zone);
            }
            else
            {
                zones[id] = zone;
            }
        }

        #endregion Operations with zones

    }
}
