using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Media;

using ImageMarker.Windows;
using ImageMarker.UserControls;

namespace ImageMarker.Classes
{
    /// <summary>
    /// Main class for storing zone data
    /// </summary>
    public class Zone : INotifyPropertyChanged, IComparable
    {
        private MainWindow mainWindow;
        private ZoneWindow zoneWindow;
        private SelectionBox selectionBox;

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
        /// Zone name
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
        /// Additional Information
        /// </summary>
        public string Description
        {
            get => _description;
            set
            {
                if (value != _description)
                {
                    _description = value;
                    NotifyPropertyChanged("Description");
                }
            }
        }
        private string _description;

        /// <summary>
        /// Zone display
        /// </summary>
        public bool IsVisible
        {
            get => _visible;
            set
            {
                if (value != _visible)
                {
                    _visible = value;
                    if (selectionBox != null)
                    {
                        selectionBox.Visibility = value ? Visibility.Visible : Visibility.Hidden;
                    }
                    NotifyPropertyChanged("IsVisible");
                }
            }
        }
        private bool _visible = true;

        /// <summary>
        /// Height for the selectionBox
        /// </summary>
        public double Height { get; set; } = 200;
        /// <summary>
        /// Width for the selectionBox
        /// </summary>
        public double Width { get; set; } = 200;
        /// <summary>
        /// Distance from the top edge on the canvas for the selectionBox
        /// </summary>
        public double Top { get; set; } = 20;
        /// <summary>
        /// Distance from the top edge on the canvas for the selectionBox
        /// </summary>        
        public double Left { get; set; } = 20;

        // #################################################################################

        /// <summary>
        /// Set value to mainWindow
        /// </summary>
        /// <param name="main">link to main window</param>
        public void SetMainWindow(MainWindow mainWindow)
        {
            this.mainWindow = mainWindow;
        }

        // #################################################################################

        #region Operations with selectionBox

        /// <summary>
        /// Create and placing the selectionBox on the canvas
        /// </summary>
        /// <param name="canvas">Canvas to placing selectionBox</param>
        public void CreateSelectionBox(Canvas canvas)
        {
            selectionBox = new SelectionBox(canvas, SelectionBox_LayoutChange)
            {
                Visibility = IsVisible ? Visibility.Visible : Visibility.Hidden,
                Title = Name,
                SuperToolTip = string.Format("Main tag - {0}\nSide tag - {1}\nName - {2}\n\nDescription:\n{3}", MainTag, SideTag, Name, Description),
                SuperHeight = Height,
                SuperWidth = Width,
                SuperTop = Top,
                SuperLeft = Left
            };

            // Create contexMenu for selectionBox 
            selectionBox.ContextMenu = new ContextMenu();
            MenuItem open = new MenuItem()
            {
                Header = "Open",
                FontFamily = new FontFamily("Verdana")
            };
            open.Click += Open_Click;
            selectionBox.ContextMenu.Items.Add(open);
            selectionBox.ContextMenu.Items.Add(new Separator());
            MenuItem hide = new MenuItem()
            {
                Header = "Hide",
                FontFamily = new FontFamily("Verdana")
            };
            hide.Click += Hide_Click;
            selectionBox.ContextMenu.Items.Add(hide);
            selectionBox.ContextMenu.Items.Add(new Separator());
            MenuItem dub = new MenuItem()
            {
                Header = "Dublicate",
                FontFamily = new FontFamily("Verdana")
            };
            dub.Click += Dub_Click;
            selectionBox.ContextMenu.Items.Add(dub);
            MenuItem del = new MenuItem()
            {
                Header = "Delete",
                FontFamily = new FontFamily("Verdana")
            };
            del.Click += Del_Click;
            selectionBox.ContextMenu.Items.Add(del);
        }

        /// <summary>
        /// Removing and removing the selectionBox from the canvas
        /// </summary>
        public void DeleteSelectionBox()
        {
            if (selectionBox != null)
            {
                selectionBox.canvas.Children.Remove(selectionBox);
            }
        }

        /// <summary>
        /// Rename title for selectionBox
        /// </summary>
        public void RenameSelectionBox(string newTitle)
        {
            selectionBox.Title = newTitle;
        }

        /// <summary>
        /// Event - react to layout change notification
        /// </summary>
        /// <param name="height">New height</param>
        /// <param name="width">New width</param>
        /// <param name="top">New distance from the top edge on the canvas</param>
        /// <param name="left">New distance from the left edge on the canvas</param>
        private void SelectionBox_LayoutChange(double height, double width, double top, double left)
        {
            Height = height;
            Width = width;
            Top = top;
            Left = left;
        }

        #endregion Operations with selectionBox

        // #################################################################################

        #region Contex buttons for selectionBox

        /// <summary>
        /// Contex button - opening a zone card
        /// </summary>
        public void Open_Click(object sender, RoutedEventArgs e)
        {
            zoneWindow = new ZoneWindow(mainWindow, this);
            zoneWindow.Show();
        }

        /// <summary>
        /// Contex button - changing zone visibility
        /// </summary>
        private void Hide_Click(object sender, RoutedEventArgs e)
        {
            IsVisible = false;
        }

        /// <summary>
        /// Contex button - zone duplication
        /// </summary>
        private void Dub_Click(object sender, RoutedEventArgs e)
        {
            Zone clone = Clone();
            clone.CreateSelectionBox(mainWindow.imageBox);
            mainWindow.zones.Add(clone);
        }

        /// <summary>
        /// Contex button - zone deletion
        /// </summary>
        private void Del_Click(object sender, RoutedEventArgs e)
        {
            DeleteSelectionBox();
            mainWindow.zones.Remove(this);
        }

        #endregion Contex buttons for selectionBox

        // #################################################################################

        public event PropertyChangedEventHandler PropertyChanged;

        public void NotifyPropertyChanged(string propertyName)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }

        public int CompareTo(object obj)
        {
            Zone o = obj as Zone;

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
        /// Clone a zone
        /// </summary>
        /// <returns>Full copy of the zone</returns>
        public Zone Clone()
        {
            Zone clone = new Zone
            {
                MainTag = MainTag,
                SideTag = SideTag,
                Name = Name,
                IsVisible = IsVisible,
                Left = Left,
                Top = Top,
                Width = Width,
                Height = Height,
            };

            clone.SetMainWindow(mainWindow);

            return clone;
        }
    }


    /// <summary>
    /// Dynamic collection of Zones
    /// </summary>
    public class Zones : ObservableCollection<Zone> { }
}
