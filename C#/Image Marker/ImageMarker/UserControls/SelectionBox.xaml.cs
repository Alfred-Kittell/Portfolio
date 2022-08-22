using System;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using System.Windows.Shapes;

namespace ImageMarker.UserControls
{
    /// <summary>
    ///  Interaction logic for SelectionBox.xaml
    /// </summary>
    public partial class SelectionBox : UserControl
    {
        private bool isMoving = false;
        private bool isStretch = false;

        private Point startPos;
        private Point newPos;
        private EdgeTypes edgeType;
        private LayoutChange isChange;

        public Canvas canvas;

        /// <summary>
        /// Specifies the title
        /// </summary>
        public string Title
        {
            get => _title;
            set
            {
                _title = value;
                boxName.Content = value;
            }
        }
        private string _title;
        /// <summary>
        /// Specifies the toolTip
        /// </summary>
        public string SuperToolTip
        {
            get => _superToolTip;
            set
            {
                _superToolTip = value;
                ToolTip = value;
            }
        }
        private string _superToolTip;

        /// <summary>
        /// Specifies the height
        /// </summary>
        public double SuperHeight
        {
            get => _superHeight;
            set
            {
                _superHeight = value;
                Height = value;
            }
        }
        private double _superHeight;
        /// <summary>
        /// Specifies the width
        /// </summary>
        public double SuperWidth
        {
            get => _superWidth;
            set
            {
                _superWidth = value;
                Width = value;
            }
        }
        private double _superWidth;
        /// <summary>
        /// Specifies the distance from the top edge on the canvas
        /// </summary>
        public double SuperTop
        {
            get => _superTop;
            set
            {
                _superTop = value;
                Canvas.SetTop(this, value);
            }
        }
        private double _superTop;
        /// <summary>
        /// Specifies the distance from the left edge on the canvas
        /// </summary>
        public double SuperLeft
        {
            get => _superLeft;
            set
            {
                _superLeft = value;
                Canvas.SetLeft(this, value);
            }
        }
        private double _superLeft;

        // #################################################################################

        /// <summary>
        /// Initializes a new instance of the class <see cref="SelectionBox"/>
        /// </summary>
        /// <param name="canvas">Canvas to placing selectionBox</param>
        /// <param name="change">Layout change notify</param>
        public SelectionBox(Canvas canvas, LayoutChange change = null)
        {
            InitializeComponent();

            Title = "Label";
            SuperToolTip = "Label";

            SuperHeight = 60;
            SuperWidth = 40;
            SuperTop = 20;
            SuperLeft = 20;

            this.canvas = canvas;
            canvas.Children.Add(this);

            isChange = change;
        }

        // #################################################################################

        /// <summary>
        /// Button - save new position for selectionBox
        /// </summary>
        private void Save_Click(object sender, RoutedEventArgs e)
        {
            _superHeight = Height;
            _superWidth = Width;
            _superTop = Canvas.GetTop(this);
            _superLeft = Canvas.GetLeft(this);

            save.Visibility = Visibility.Hidden;
            cancel.Visibility = Visibility.Hidden;

            isChange?.Invoke(_superHeight, _superWidth, _superTop, _superLeft);
        }

        /// <summary>
        /// Button - cancel position change for selectionBox
        /// </summary>
        private void Cancel_Click(object sender, RoutedEventArgs e)
        {
            Height = _superHeight;
            Width = _superWidth;
            Canvas.SetTop(this, _superTop);
            Canvas.SetLeft(this, _superLeft);

            save.Visibility = Visibility.Hidden;
            cancel.Visibility = Visibility.Hidden;
        }

        // #################################################################################

        #region Movement

        /// <summary>
        /// Event - hold center with mouse
        /// </summary>
        private void CenterRect_MouseDown(object sender, MouseButtonEventArgs e)
        {
            isMoving = true;
            Cursor = Cursors.Hand;
            startPos = e.GetPosition(canvas);
            newPos = new Point(Canvas.GetLeft(this), Canvas.GetTop(this));
            Mouse.Capture((IInputElement)sender);
        }

        /// <summary>
        /// Event - move center with mouse
        /// </summary>
        private void CenterRect_MouseMove(object sender, MouseEventArgs e)
        {
            if (!isMoving)
            {
                return;
            }

            save.Visibility = Visibility.Visible;
            cancel.Visibility = Visibility.Visible;

            Point offset = new Point(startPos.X - newPos.X, startPos.Y - newPos.Y);
            double CanvasLeft = e.GetPosition(canvas).X - offset.X;
            double CanvasTop = e.GetPosition(canvas).Y - offset.Y;

            if (CanvasTop + Height <= canvas.ActualHeight && CanvasLeft + Width <= canvas.ActualWidth &&
                CanvasTop >= 0 && CanvasLeft >= 0)
            {
                SetValue(Canvas.TopProperty, CanvasTop);
                SetValue(Canvas.LeftProperty, CanvasLeft);
            }
        }

        /// <summary>
        /// Event - stop holding center with mouse
        /// </summary>
        private void CenterRect_MouseUp(object sender, MouseButtonEventArgs e)
        {
            isMoving = false;
            Cursor = Cursors.Arrow;
            Mouse.Capture(null);
        }

        #endregion Movement

        // #################################################################################

        #region Stretching

        /// <summary>
        /// Event - cursor change when hovering mouse over edge
        /// </summary>
        private void EdgeRect_MouseEnter(object sender, MouseEventArgs e)
        {
            Rectangle rect = sender as Rectangle;
            int tag = Convert.ToInt32(rect.Tag);

            switch ((EdgeTypes)tag)
            {
                case EdgeTypes.LeftUp:
                case EdgeTypes.RighDown:
                    Cursor = Cursors.SizeNWSE;
                    break;
                case EdgeTypes.RightUp:
                case EdgeTypes.LeftDown:
                    Cursor = Cursors.SizeNESW;
                    break;
                case EdgeTypes.Left:
                case EdgeTypes.Righ:
                    Cursor = Cursors.SizeWE;
                    break;
                case EdgeTypes.Up:
                case EdgeTypes.Down:
                    Cursor = Cursors.SizeNS;
                    break;
            }
        }

        /// <summary>
        /// Event - hold edge with mouse
        /// </summary>
        private void EdgeRect_MouseDown(object sender, MouseButtonEventArgs e)
        {
            Rectangle rect = sender as Rectangle;
            int tag = Convert.ToInt32(rect.Tag);

            isStretch = true;
            edgeType = (EdgeTypes)tag;
            Mouse.Capture((IInputElement)sender);
        }

        /// <summary>
        /// Event - move edge with mouse
        /// </summary>
        private void EdgeRect_MouseMove(object sender, MouseEventArgs e)
        {
            if (!isStretch)
            {
                return;
            }

            save.Visibility = Visibility.Visible;
            cancel.Visibility = Visibility.Visible;

            Point newPos = e.GetPosition(canvas);
            Point currPos = canvas.TranslatePoint(new Point(0, 0), this);

            // Top edge stretch
            if (edgeType == EdgeTypes.Up || edgeType == EdgeTypes.LeftUp || edgeType == EdgeTypes.RightUp)
            {
                double newHeight = ActualHeight + -currPos.Y - newPos.Y;
                if (newPos.Y >= 0 && newHeight >= MinHeight)
                {
                    Canvas.SetTop(this, newPos.Y);
                    Height = newHeight;
                }
            }
            // Left edge stretch
            if (edgeType == EdgeTypes.Left || edgeType == EdgeTypes.LeftUp || edgeType == EdgeTypes.LeftDown)
            {
                double newWidth = ActualWidth + -currPos.X - newPos.X;
                if (newPos.X >= 0 && newWidth >= MinWidth)
                {
                    Canvas.SetLeft(this, newPos.X);
                    Width = newWidth;
                }
            }
            // Right edge stretch
            if (edgeType == EdgeTypes.Righ || edgeType == EdgeTypes.RightUp || edgeType == EdgeTypes.RighDown)
            {
                double left = Canvas.GetLeft(this);
                double newWidth = newPos.X + currPos.X;
                if (newWidth >= 0 && newWidth + left <= canvas.ActualWidth)
                {
                    Width = newWidth;
                }
            }
            // Bottom edge stretch
            if (edgeType == EdgeTypes.Down || edgeType == EdgeTypes.LeftDown || edgeType == EdgeTypes.RighDown)
            {
                double top = Canvas.GetTop(this);
                double newHeight = newPos.Y + currPos.Y;
                if (newHeight >= 0 && newHeight + top <= canvas.ActualHeight)
                {
                    Height = newHeight;
                }
            }
        }

        /// <summary>
        /// Event - stop holding edge with mouse
        /// </summary>
        private void EdgeRect_MouseUp(object sender, MouseButtonEventArgs e)
        {
            isStretch = false;
            Mouse.Capture(null);
        }

        /// <summary>
        /// Event - resetting the cursor when the mouse leaves the edge
        /// </summary>
        private void EdgeRect_MouseLeave(object sender, MouseEventArgs e)
        {
            Cursor = Cursors.Arrow;
            isStretch = false;
        }

        #endregion Stretching
    }

    /// <summary>
    /// Event - layout change notify
    /// </summary>
    /// <param name="height">New height</param>
    /// <param name="width">New width</param>
    /// <param name="top">New distance from the top edge on the canvas</param>
    /// <param name="left">New distance from the left edge on the canvas</param>
    public delegate void LayoutChange(double height, double width, double top, double left);


    /// <summary>
    /// To delimit the use of a particular edge
    /// </summary>
    internal enum EdgeTypes
    {
        LeftUp = 1,
        Up = 2,
        RightUp = 3,
        Righ = 4,
        RighDown = 5,
        Down = 6,
        LeftDown = 7,
        Left = 8
    }
}
